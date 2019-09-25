from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import DevopsCapacitySerializer


@api_view(['POST'])
def calculate_devops_capacity(request):
    """
    Calculates number of DE required in addition to DM
    and defines the most efficient location for DM.
    ___
    Example: \n
        data = {
            "DM_capacity": 12,
            "DE_capacity": 5,
            "data_centers":
            [
                {"name": "Rome", "servers": 22},
                {"name": "Riga", "servers": 8}
            ]
        }
        headers = {
            "Content-Type": "application/json",
        }
    Return: \n
        HTTP 200 Ok
        {
            "DE": 5,
            "DM_data_center": "Rome"
        }
    """
    serializer = DevopsCapacitySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return JsonResponse(status=status.HTTP_200_OK, data=serializer.calculate_load())
