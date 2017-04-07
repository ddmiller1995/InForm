from api.models import Youth, YouthVisit
from api.serializers import YouthSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

def youth_list(request):
    '''View for the list youth endpoint

    GET /api/youth
        Param: activeOnly=True (if activeOnly param not specified, default value is False)
        Param: search=john (optional search param filters search results)
        Returns: Array of youth objects
    '''
    json = {
        'youth': []
    }

    active_only = False
    if 'activeOnly' in request.GET:
        active_only = request.GET['activeOnly'].lower()
        active_only = active_only == 'true'

    youth_list = Youth.GetActiveYouth() if active_only else Youth.objects.all()

    searchQuery = False
    if 'search' in request.GET:
        search = request.GET['search']
        # insert code here to filter youth_list

    for youth in youth_list:

        obj = { # Youth fields
            'id': youth.pk,
            'name': youth.youth_name,
            'dob': youth.date_of_birth,
            'ethnicity': youth.ethnicity,
        }

        youth_visit = None
        try:
            youth_visit = YouthVisit.objects.get(youth_id=youth)
            obj['placement_date'] = youth_visit.placement_date
            obj['city_of_origin'] = youth_visit.city_of_origin
            obj['guardian_name'] = youth_visit.guardian_name
            obj['placement_type'] = {
                'placement_type_name': youth_visit.placement_type.placement_type_name,
                'default_stay_length': youth_visit.placement_type.default_stay_length
            }
            obj['referred_by'] = youth_visit.referred_by
            obj['permanent_housing'] = youth_visit.permanent_housing
            obj['exited_to'] = youth_visit.exited_to
            obj['case_manager'] = {
                'first_name': youth_visit.case_manager.first_name,
                'last_name': youth_visit.case_manager.last_name,
                'username': youth_visit.case_manager.username,
            }
            obj['personal_counselor'] = {
                'first_name': youth_visit.personal_counselor.first_name,
                'last_name': youth_visit.personal_counselor.last_name,
                'username': youth_visit.personal_counselor.username,
            }
            obj['school'] = {
                'school_name': youth_visit.school.school_name,
                'school_district': youth_visit.school.school_district,
                'school_phone': youth_visit.school.school_phone,
            }

            obj['school_am_transport'] = youth_visit.school_am_transport
            obj['school_am_pickup_time'] = youth_visit.school_am_pickup_time
            obj['school_am_phone'] = youth_visit.school_am_phone
            obj['school_pm_transport'] = youth_visit.school_pm_transport
            obj['school_pm_dropoff_time'] = youth_visit.school_pm_dropoff_time
            obj['school_pm_phone'] = youth_visit.school_pm_phone

        except YouthVisit.DoesNotExist:
            pass # idk why this would happen, but it could


        json['youth'].append(obj)
    return JsonResponse(json)

def youth_detail(request, youth_id):
    '''View for the youth detail endpoint


    GET /api/youth/ (pk is an int which represents a youth's primary key)
        Returns: Youth object for the youth with that PK
    '''
    youth = get_object_or_404(Youth, pk=youth_id)
    obj = {# more fields need to be added to response
        'id': youth.pk,
        'name': youth.youth_name,
        'dob': youth.date_of_birth,
        'ethnicity': youth.ethnicity
    }
    return JsonResponse(obj)

def youth_detail_chart(request, youth_id):
    '''View for the list youth endpoint

    PUT /api/youth/PK/progress-chart
        (create or update operation for the progress chart.
        Once a user presses "save changes", the front end will persist changes with this PUT request)
        Returns: response code 201
    '''

    if request.method == 'PUT' or True: # or True for debugging with GET, replace with PUT only in prod
        youth = get_object_or_404(Youth, pk=youth_id)
        obj = {# more fields need to be added to response
            'id': youth.pk,
            'name': youth.youth_name,
            'dob': youth.date_of_birth,
            'ethnicity': youth.ethnicity,
            'stuff': True
        }
        return JsonResponse(obj)
    else:
        raise Http404



class YouthList(APIView):
    """
    List all youths, or create a new youth.
    """
    def get(self, request, format=None):
        youths = Youth.objects.all()
        serializer = YouthSerializer(youths, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = YouthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)