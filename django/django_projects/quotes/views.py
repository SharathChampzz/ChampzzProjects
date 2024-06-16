from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Quotes
from .serializers import QuoteSerializer

from django.shortcuts import render

# FRONTEND VIEWS
def home(request):
    return render(request, 'quotes/home.html')

# BACKEND APIs
@api_view(['GET', 'POST'])
def quotes(request: Request) -> Response:
    if request.method == 'GET':
        quotes = Quotes.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def quote(request: Request, pk: int) -> Response:
    try:
        quote = Quotes.objects.get(pk=pk)
    except Quotes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)
    
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = QuoteSerializer(quote, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        try:
            quote.delete()
            return Response({'message': 'Quote deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'errorMessage': 'Failed to delete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
