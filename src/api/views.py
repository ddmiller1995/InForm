from django.http import HttpResponse, JsonResponse

def index(request):
    data = {
        'a': 1,
        'b': 13,
        'c': 24
    }

    return JsonResponse(data)