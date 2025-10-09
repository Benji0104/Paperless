from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def login(request):
    return Response ('API PARA LOGEASE EN EL DRIVE DE GOOGLE')