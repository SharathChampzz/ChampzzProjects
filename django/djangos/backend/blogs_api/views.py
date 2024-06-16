from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def blogs(request: Request) -> Response:
    return Response(data={'errorCode': 0, 'errorMessage': 'Successfull!'}, status=status.HTTP_200_OK)
