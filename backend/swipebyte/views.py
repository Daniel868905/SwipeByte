from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "pong"})


def home(request):
    return JsonResponse({"message": "SwipeByte API"})