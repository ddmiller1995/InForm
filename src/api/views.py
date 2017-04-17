import logging

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import PlacementType, Youth, YouthVisit
from api.serializers import (PlacementTypeSerializer, serialize_youth,
                             serialize_youth_visit)

logger = logging.getLogger(__name__)

class YouthList(APIView):
    '''View for the list youth endpoint

    GET /api/youth
        Param: activeOnly=True (if activeOnly param not specified, default value is False)
        Param: search=john (optional search param filters search results)
        Returns: Array of youth objects
    '''

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
            obj = {**serialized_youth, **serialized_youth_visit}

            json['youth'].append(obj)

        return JsonResponse(json, safe=False)

class YouthDetail(APIView):
    '''View for the youth detail endpoint


    GET /api/youth/ (pk is an int which represents a youth's primary key)
        Returns: Youth object for the youth with that PK
    '''

    def get(self, request, youth_id, format=None):
        youth = get_object_or_404(Youth, pk=youth_id)
        json = serialize_youth(youth)

        youth_visits = []
        for youth_visit in YouthVisit.objects.filter(youth_id=youth).order_by('-current_placement_start_date'):
            serialized_youth_visit = serialize_youth_visit(youth_visit)
            youth_visits.append(serialized_youth_visit)

        json['youth_visits'] = youth_visits 

        
        return JsonResponse(json, safe=False)


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

    def post(self, request, youth_visit_id, format=None):

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

        youth_visit.current_placement_type = new_placement_type
        youth_visit.save()

        obj = {
            'updated_youth_visit_id': youth_visit.id,
            'new_placement_type_id': new_placement_type.id
        }
        return Response(obj, status=status.HTTP_202_ACCEPTED)
        
class PlacementTypeList(APIView):
    '''
    List all placement types

    Supported HTTP methods: GET
    
    GET /api/placement-type returns JSON response
    
    '''

    def get(self, request, format=None):
        placement_types = PlacementType.objects.all()
        serializer = PlacementTypeSerializer(placement_types, many=True)
        return Response(serializer.data)
