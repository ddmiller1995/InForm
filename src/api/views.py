from api.models import Youth
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

    activeOnly = False
    if 'activeOnly' in request.GET:
        activeOnly = request.GET['activeOnly'].lower()
        activeOnly = activeOnly == 'true'

    searchQuery = False
    if 'search' in request.GET:
        search = request.GET['search']

    youth_list = Youth.GetActiveYouth() if activeOnly else Youth.objects.all()

    # insert code here to filter youth_list by searchQuery if provided

    for youth in youth_list:
        obj = { # more fields need to be added to response
            'id': youth.pk,
            'name': youth.youth_name,
            'dob': youth.date_of_birth,
            'ethnicity': youth.ethnicity,
            'activeOnly': repr(activeOnly)
        }
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