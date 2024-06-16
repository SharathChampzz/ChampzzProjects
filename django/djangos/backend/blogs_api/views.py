from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET', 'POST'])
def blogs(request: Request) -> Response:
    """
    Get all blogs or create a new blog.

    Usage:
        GET /api/blogs - get all blogs
        POST /api/blogs - create a new blog

    Returns:
        - If GET request: a list of all blogs
        - If POST request: the created blog or error message
    """
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
    """
    Get, update, partially update, or delete a blog by id.

    Usage:
        GET /api/blogs/<pk> - get a blog by id
        PUT /api/blogs/<pk> - update a blog by id
        PATCH /api/blogs/<pk> - partially update a blog by id
        DELETE /api/blogs/<pk> - delete a blog by id

    Returns:
        - If GET request: the blog with the specified id or error message
        - If PUT or PATCH request: the updated blog or error message
        - If DELETE request: success message or error message
    """
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'errorMessage': 'Provided blog id doesnot exists'}, status=status.HTTP_404_NOT_FOUND)
    
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