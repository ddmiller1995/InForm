from api.models import Youth
from api.serializers import YouthSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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