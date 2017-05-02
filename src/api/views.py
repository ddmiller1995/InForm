import logging
from datetime import datetime
import csv

from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from api.models import PlacementType, Youth, YouthVisit, FormYouthVisit
from api.serializers import (PlacementTypeSerializer, serialize_youth,
                             serialize_youth_visit, serialize_form_youth_visit, 
                             youth_field_names, youth_visit_field_names)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

    def get(self, request, youth_id, format=None):
        youth = get_object_or_404(Youth, pk=youth_id)
        json = serialize_youth(youth)

        youth_visits = []
        for youth_visit in YouthVisit.objects.filter(youth_id=youth).order_by('-current_placement_start_date'):
            serialized_youth_visit = serialize_youth_visit(youth_visit)
            youth_visits.append(serialized_youth_visit)

        json['youth_visits'] = youth_visits 

        return Response(json, status=status.HTTP_200_OK)

class YouthForms(APIView):

    def get(self, request, youth_id, format=None):
        youth = get_object_or_404(Youth, pk=youth_id)
        latest_youth_visit_id = youth.latest_youth_visit().pk
        json = []
        for form_youth_visit in FormYouthVisit.objects.filter(youth_visit_id=latest_youth_visit_id):
            serialized_form_youth_visit - serialize_form_youth_visit(form_youth_visit)
            json.append(serialized_form_youth_visit)

        return Response(json, status=status.HTTP_200_OK)


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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        placement_types = PlacementType.objects.all()
        serializer = PlacementTypeSerializer(placement_types, many=True)
        return Response(serializer.data)


class ExportYouthVisits(APIView):
    '''Export youth visit data as CSV
    
    Export flattened youth_visit objects, ordered by descending visit start date'''

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

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