from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from forms.models import Form
from forms.serializers import FormSerializer


@csrf_exempt
def form_list(request):
    """
    List all code forms, or create a new form.
    """
    if request.method == 'GET':
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FormSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def form_detail(request, pk):
    """
    Retrieve, update or delete a code form.
    """
    try:
        form = Form.objects.get(pk=pk)
    except Form.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FormSerializer(form)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FormSerializer(form, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        form.delete()
        return HttpResponse(status=204)