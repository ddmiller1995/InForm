from api.models import Youth, YouthVisit
from api.serializers import serialize_youth, serialize_youth_visit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

import logging
logger = logging.getLogger(__name__)

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

    youth_list = Youth.get_active_youth() if active_only else Youth.objects.all()

    searchQuery = False
    if 'search' in request.GET:
        search = request.GET['search']
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

    return JsonResponse(json)


def youth_detail(request, youth_id):
    '''View for the youth detail endpoint


    GET /api/youth/ (pk is an int which represents a youth's primary key)
        Returns: Youth object for the youth with that PK
    '''
    youth = get_object_or_404(Youth, pk=youth_id)
    serialized_youth = serialize_youth(youth)

    try:
        youth_visit = youth.latest_youth_visit()
    except YouthVisit.DoesNotExist:
        logger.warn(f'Youth with pk={youth_id} has no youth_visit yet')
        raise Http404

    serialized_youth_visit = serialize_youth_visit(youth_visit)

    # merge both serialized objects, keep items from second object if conflicts
    json = {**serialized_youth, **serialized_youth_visit}
    
    return JsonResponse(json)

def youth_detail_chart(request, youth_id):
    '''View for the list youth endpoint

    PUT /api/youth/PK/progress-chart
        (create or update operation for the progress chart.
        Once a user presses "save changes", the front end will
        persist changes with this PUT request)
        Returns: response code 201
    '''

    # or True for debugging with GET, replace with PUT only in prod
    if request.method == 'PUT' or True:
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


