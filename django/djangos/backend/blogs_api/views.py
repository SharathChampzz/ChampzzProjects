from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from backend.users_api.permissions import IsSuperUser

@api_view(['GET', 'POST'])
# @permission_classes([IsSuperUser]) # relaxing this check for the bot to work
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsSuperUser])
def blog(request: Request, id: int) -> Response:
    """
    Get, update, partially update, or delete a blog by id.

    Usage:
        GET /api/blogs/<id> - get a blog by id
        PUT /api/blogs/<id> - update a blog by id
        PATCH /api/blogs/<id> - partially update a blog by id
        DELETE /api/blogs/<id> - delete a blog by id

    Returns:
        - If GET request: the blog with the specified id or error message
        - If PUT or PATCH request: the updated blog or error message
        - If DELETE request: success message or error message
    """
    try:
        blog = Blog.objects.get(id=id)
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