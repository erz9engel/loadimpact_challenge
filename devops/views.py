from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import DevopsCapacitySerializer


@api_view(['POST'])
def calculate_devops_capacity(request):
    serializer = DevopsCapacitySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return JsonResponse(status=status.HTTP_200_OK, data=serializer.calculate_load())
