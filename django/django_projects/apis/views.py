from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def is_service_available(request):
    """
    Check if the service is available
    """
    return Response({'status': 'Webserver is up and running!'}, status=status.HTTP_200_OK)