import csv
import logging
from datetime import datetime
from itertools import groupby
from tempfile import TemporaryFile
from fuzzywuzzy import fuzz

from django import forms
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.csv_serializers import youth_field_names, youth_visit_field_names
from api.models import (Form, FormType, FormYouthVisit, PlacementType, Youth,
                        YouthVisit)
from api.serializers import (FormTypeSerializer, PlacementTypeSerializer,
                             serialize_form_youth_visit, serialize_youth,
                             serialize_youth_visit)

logger = logging.getLogger(__name__)

DATE_STRING_FORMAT = '%Y-%m-%d' # YYYY-MM-DD

class YouthList(APIView):
    '''View for the list youth endpoint

    GET /api/youth
        Param: activeOnly=True (if activeOnly param not specified, default value is False)
        Param: search=john (optional search param filters search results)
        Returns: Array of youth objects
    '''

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):

        json = {
            'youth': []
        }

        active_only = False
        if 'activeOnly' in request.query_params:
            active_only = request.query_params['activeOnly'].lower()
            active_only = active_only == 'true'

        youth_list = Youth.get_active_youth() if active_only else Youth.objects.all()

        searchQuery = False
        if 'search' in request.query_params:
            search = request.query_params['search']
            # insert code here to filter youth_list

        for youth in youth_list:

            serialized_youth = serialize_youth(youth)

            try:
                youth_visit = youth.latest_youth_visit()
            except YouthVisit.DoesNotExist:
                logger.warn(f'Youth with pk={youth.pk} doesn"t have any youth_visits')
                continue

            serialized_youth_visit = serialize_youth_visit(youth_visit)

            # merge both serialized objects, keep items from second object if conflicts
            obj = {**serialized_youth_visit, **serialized_youth}

            json['youth'].append(obj)

        return Response(json, status=status.HTTP_200_OK)

class YouthDetail(APIView):
    '''View for the youth detail endpoint


    GET /api/youth/ (pk is an int which represents a youth's primary key)
        Returns: Youth object for the youth with that PK
    '''

    renderer_classes = (JSONRenderer, )

    def get(self, request, youth_id, format=None):
        youth = get_object_or_404(Youth, pk=youth_id)
        json = serialize_youth(youth)

        youth_visits = []
        for youth_visit in YouthVisit.objects.filter(youth_id=youth).order_by('-visit_start_date'):
            serialized_youth_visit = serialize_youth_visit(youth_visit)

            forms = []
            for form_youth_visit in FormYouthVisit.objects.filter(youth_visit_id=youth_visit.id):
                serialized_form_youth_visit = serialize_form_youth_visit(form_youth_visit)
                forms.append(serialized_form_youth_visit)

            serialized_youth_visit['forms'] = forms

            youth_visits.append(serialized_youth_visit)
        json['youth_visits'] = youth_visits 


        return Response(json, status=status.HTTP_200_OK)


class ChangeFormStatus(APIView):
    '''Change the status of a form'''

    renderer_classes = (JSONRenderer, )

    def post(self, request, youth_visit_id):
        try:
            youth_visit = YouthVisit.objects.get(pk=youth_visit_id)
        except YouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Youth visit pk=%s does not exist' % youth_visit_id
            return response

        form_id = request.POST.get('form_id', None)

        if not form_id:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "form_id"'
            return response
            
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Form pk=%s does not exist' % form_id
            return response

        new_status = request.POST.get('status', None)
        if not new_status:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "status"'
            return response
        if new_status not in ['pending', 'in progress', 'done']:
            response = Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            response['error'] = 'POST param "status" should be a "pending", "in progress", or "done"'
            return response

        try:
            form_youth_visit = FormYouthVisit.objects.get(
                youth_visit_id=youth_visit.id,
                form_id=form.id)
        except FormYouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'FormYouthVisit with YouthVisit pk=%d and Form pk=%d does not exist' % (youth_visit.id, form.id)
            return response

        if new_status == 'pending':
            form_youth_visit.status = FormYouthVisit.PENDING
        elif new_status == 'in progress':
            form_youth_visit.status = FormYouthVisit.IN_PROGRESS
        elif new_status == 'done':
            form_youth_visit.status = FormYouthVisit.DONE
        else:
            raise Http404
        form_youth_visit.save()


        obj = {
            'youth_visit_id': youth_visit.id,
            'form_id': form.id,
            'new_status': form_youth_visit.status
        }

        return Response(obj, status=status.HTTP_202_ACCEPTED)

class YouthChangePlacement(APIView):
    '''Change youth placement type

    Supported HTTP methods: POST
    
    Params:
        - youth_visit_id is parsed from the url and represents the pk
            of the youth_visit whose placement we are going to change
        - new_placement_type_id is a POST param that is required. It 
            is the pk of the placement_type that is going to be set on
            the youth_visit

            NOTE: You may need to first query the /api/placement-type endpoint
            to get all of the placement types and their PKs 

    Success:
        - If the request was succesfull, you will receive a
            HTTP_202_ACCEPTED response
    Failure:
        - If the request does not include a valid youth_visit_id,
            you will get a HTTP_404_NOT_FOUND response
        - If the request does not include a new_placement_type_id
            POST param, you will receive a HTTP_400_BAD_REQUEST response
        - If the request does not include a valid new_placement_type_id,
            you will receive a HTTP_404_NOT_FOUND response

        - All failure responses will have a "error" header with an
            error message
    '''

    renderer_classes = (JSONRenderer, )
    

    def post(self, request, youth_visit_id, format=None):
        # year/month/day YYYY-MM-DD
        try:
            youth_visit = YouthVisit.objects.get(pk=youth_visit_id)
        except YouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Youth visit pk=%s does not exist' % youth_visit_id
            return response

        new_placement_type_id = request.POST.get('new_placement_type_id', None)

        if not new_placement_type_id:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "new_placement_type_id"'
            return response
            
        try:
            new_placement_type = PlacementType.objects.get(pk=new_placement_type_id)
        except PlacementType.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Placement type pk=%s does not exist' % new_placement_type_id
            return response


        new_placement_start_date_string = request.POST.get('new_placement_start_date', None)

        if not new_placement_start_date_string:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "new_placement_start_date"'
            return response
            
        youth_visit.current_placement_type = new_placement_type
        youth_visit.current_placement_extension_days = 0
        
        youth_visit.current_placement_start_date = datetime.strptime(new_placement_start_date_string, DATE_STRING_FORMAT)
        youth_visit.save()

        obj = {
            'updated_youth_visit_id': youth_visit.id,
            'new_placement_type_id': new_placement_type.id,
            'new_placement_start_date': youth_visit.current_placement_start_date.strftime(DATE_STRING_FORMAT)
        }

        return Response(obj, status=status.HTTP_202_ACCEPTED)
        
class YouthMarkExited(APIView):
    '''
    Mark a Youth as exited

    Input:
        * Exit date
        * Where exited (string)
        * permanent housing (bool)
    '''
    renderer_classes = (JSONRenderer, )

    def post(self, request, youth_visit_id, format=None):
        try:
            youth_visit = YouthVisit.objects.get(pk=youth_visit_id)
        except YouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Youth visit pk=%s does not exist' % youth_visit_id
            return response

        exit_date_string = request.POST.get('exit_date_string', None)
        if not exit_date_string:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "exit_date_string"'
            return response

        where_exited = request.POST.get('where_exited', None)
        if not where_exited:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "where_exited"'
            return response 

        permanent_housing = request.POST.get('permanent_housing', None)
        if not permanent_housing:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "permanent_housing"'
            return response
        if permanent_housing == 'true':
            permanent_housing = True
        elif permanent_housing == 'false':
            permanent_housing = False
        elif permanent_housing == 'unknown':
            permanent_housing = None
        else:
            response = Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            response['error'] = 'POST param "permanent_housing" should be a true or false value'
            return response


        youth_visit.visit_exit_date = datetime.strptime(exit_date_string, DATE_STRING_FORMAT)
        youth_visit.exited_to = where_exited
        youth_visit.permanent_housing = permanent_housing
        youth_visit.save()

        obj = {}
        return Response(obj, status=status.HTTP_202_ACCEPTED)

class YouthAddExtension(APIView):
    '''
    Add an extension to a Youth Visit
    '''

    renderer_classes = (JSONRenderer, )

    def post(self, request, youth_visit_id, format=None):
        try:
            youth_visit = YouthVisit.objects.get(pk=youth_visit_id)
        except YouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Youth visit pk=%s does not exist' % youth_visit_id
            return response

        extension = request.POST.get('extension', None)
        if not extension:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "extension"'
            return response

        try:
            extension = int(extension)
        except ValueError:
            msg = 'Non int POST param passed to add extension endpoint'
            logger.warn(msg)
            response = Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            response['error'] = msg
            return response  

        youth_visit.current_placement_extension_days += int(extension)
        youth_visit.save()

        return Response({}, status=status.HTTP_202_ACCEPTED)

class YouthEditNote(APIView):
    '''Edit a Youth visit's note
    '''
    renderer_classes = (JSONRenderer, )

    def post(self, request, youth_visit_id, format=None):
        try:
            youth_visit = YouthVisit.objects.get(pk=youth_visit_id)
        except YouthVisit.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Youth visit pk=%s does not exist' % youth_visit_id
            return response

        note = request.POST.get('note', None)
        if not note:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response['error'] = 'Missing POST param "note"'
            return response

        youth_visit.notes = note
        youth_visit.save()

        return Response({
            'youth_visit_id': youth_visit_id,
            'note': note
        }, status=status.HTTP_202_ACCEPTED)


class PlacementTypeList(APIView):
    '''~
    List all placement types

    Supported HTTP methods: GET
    
    GET /api/placement-type returns JSON response
    
    '''

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        placement_types = PlacementType.objects.all()
        serializer = PlacementTypeSerializer(placement_types, many=True)
        return Response(serializer.data)

class DownloadImportTemplate(APIView):
    '''Download the import csv template'''

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inform-data-import-template.csv"'

        writer = csv.writer(response)

        column_names = youth_field_names + youth_visit_field_names
        writer.writerow(column_names)
        return response

class UploadFileForm(forms.Form):
    file = forms.FileField()



from pprint import pprint
class ImportYouthVisits(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request, format=None):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            lines = []
            for line in f.readlines():
                line = line.strip()
                line = line.split(b',')
                lines.append(line)

            line_count = len(lines)
            if line_count <= 1: # if it has only 1 line, that is the column names row
                raise Http404
            lines = lines[1:] # drop column names row


            keyfunc = lambda line: line[1]
            lines = sorted(lines, key=keyfunc)

            youth_map = {}

            for key, group in groupby(lines, keyfunc):
                youth_map[key] = list(group)

            MATCH_THRESHOLD_RATIO = 90

            # loop over grouped data to find and merge duplicated groups of data
            # using levenshtein distance (using fuzzywuzzy library)
            for key_a, value_a in youth_map.items():
                for key_b, value_b in youth_map.items():
                    if key_a == key_b: # skips case where keys are the same (no action needed)
                        continue
                    match_ratio = fuzz.token_set_ratio(str(key_a), str(key_b)) # compute similarity ratio
                    if match_ratio >= MATCH_THRESHOLD_RATIO: # if similarility ratio passes threshold, merge the two groupings
                        # determine which key is longer and which is shorter
                        # so we can always merge the shorter key's group
                        # into the larger key's group
                        if len(key_a) > len(key_b):
                            longest_key = key_a
                            shortest_key = key_b
                        else:
                            longest_key = key_b
                            shortest_key = key_a

                        # if the shortest key's group is empty, that means that it has already been merged.
                        # this scenario will happen once for each pair that passes the similarity threshold,
                        # because a gets compared to b, and then b gets compared to a
                        # on the first comparison, this operation goes down and the shorter key gets marked as
                        # deleted by emptying it's group
                        # on the second comparison, we should skip because the work has already been done
                        if not youth_map[shortest_key]:
                            continue

                        print('Merging %s with %s: %d' % (shortest_key, longest_key, match_ratio))
                        # add shortest key's group to the longest key's group
                        youth_map[longest_key] += youth_map[shortest_key]
                        # mark the shortest key as deleted without changing dict size during loop
                        youth_map[shortest_key] = []
                        print('Done!')

            keys_marked_for_deletion = []
            for key, youth_visits in youth_map.items():
                # record each key that was marked for deletion
                if len(youth_visits) == 0:
                    keys_marked_for_deletion.append(key)
                # correct youth name anomalies that happened
                # because of the previous fuzzy merge operation
                for youth_visit in youth_visits:
                    if youth_visit[1] != key:
                        youth_visit[1] = key

            # delete all keys from grouping map that were marked for deletion
            for key in keys_marked_for_deletion:
                del youth_map[key]
            pprint(youth_map)

            Youth.objects.all().delete()
            YouthVisit.objects.all().delete()

            for key, value in youth_map.items():
                for line in value:
                    try:
                        Youth.objects.get(youth_name=line[1])
                    except Youth.DoesNotExist:
                        Youth.objects.create(
                            youth_name=line[1],
                            date_of_birth=datetime.strptime(line[2].decode('ascii'), '%Y-%m-%d'),
                            ethnicity=line[3],
                            notes=line[4]
                        )

 
            
            return redirect('/admin/')


class FormTypeList(APIView):
    '''
    List all FormTypes

    Support HTTP methods: GET

    GET /api/form-type returns JSON Response
    '''

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        form_types = FormType.objects.all()
        serializer = FormTypeSerializer(form_types, many=True)
        return Response(serializer.data)



class ExportYouthVisits(APIView):
    '''Export youth visit data as CSV
    
    Export flattened youth_visit objects, ordered by descending visit start date'''

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inform-data-export.csv"'

        writer = csv.writer(response)

        column_names = youth_field_names + youth_visit_field_names
        writer.writerow(column_names)
        

        youth_visit_list = YouthVisit.objects.all().order_by('-visit_start_date')

        if youth_visit_list.count() == 0:
            logger.error("Tried to output to CSV but there is no data yet.")
            # Warn the user about what happened
            # Maybe redirect to an error page
            raise Http404 # placeholder

        for youth_visit in youth_visit_list:
            row = []

            # Youth table
            row.append(youth_visit.youth_id.id)
            row.append(youth_visit.youth_id.youth_name)
            row.append(youth_visit.youth_id.date_of_birth)
            row.append(youth_visit.youth_id.ethnicity)
            row.append(youth_visit.youth_id.notes)

            # YouthVisit table
            row.append(youth_visit.id)
            
            row.append(youth_visit.visit_start_date)
            # YouthVisit.PlacementType
            row.append(youth_visit.current_placement_type.id)
            row.append(youth_visit.current_placement_type.placement_type_name)
            row.append(youth_visit.current_placement_type.default_stay_length)
            row.append(youth_visit.current_placement_type.supervision_ratio)
            row.append(youth_visit.current_placement_start_date)
            row.append(youth_visit.current_placement_extension_days)
            row.append(youth_visit.city_of_origin)
            row.append(youth_visit.state_of_origin)
            row.append(youth_visit.guardian_name)
            row.append(youth_visit.referred_by)
            row.append(youth_visit.social_worker)
            row.append(youth_visit.visit_exit_date)
            row.append(youth_visit.permanent_housing)
            row.append(youth_visit.exited_to)

            # YouthVisit.User
            if (youth_visit.case_manager):
                row.append(youth_visit.case_manager.id)
                row.append(youth_visit.case_manager.get_full_name())
                row.append(youth_visit.case_manager.username)
            else:
                row.append('')
                row.append('')
                row.append('')   


            # YouthVisit.User
            if (youth_visit.personal_counselor):
                row.append(youth_visit.personal_counselor.id)
                row.append(youth_visit.personal_counselor.get_full_name())
                row.append(youth_visit.personal_counselor.username)
            else:
                row.append('')
                row.append('')
                row.append('')   

            # YouthVisit.School
            if (youth_visit.school):
                row.append(youth_visit.school.id)
                row.append(youth_visit.school.school_name)
                row.append(youth_visit.school.school_district)
                row.append(youth_visit.school.school_phone)
                row.append(youth_visit.school.notes)
            else:
                row.append('')
                row.append('')
                row.append('') 
                row.append('')
                row.append('')   

            row.append(youth_visit.school_am_transport)
            row.append(youth_visit.school_am_pickup_time)
            row.append(youth_visit.school_am_phone)
            row.append(youth_visit.school_pm_transport)
            row.append(youth_visit.school_pm_dropoff_time)
            row.append(youth_visit.school_pm_phone)
            row.append(youth_visit.school_date_requested)
            row.append(youth_visit.school_mkv_complete)
            row.append(youth_visit.notes)


            writer.writerow(row)

        return response

def api_docs(request):
    return render(request, 'api/docs.html')
