from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET', 'POST'])
def blogs(request: Request) -> Response:
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def blog(request: Request, pk: int) -> Response:
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = BlogSerializer(blog, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        try:
            blog.delete()
            return Response({'message': 'blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'errorMessage': 'Failed to delete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)