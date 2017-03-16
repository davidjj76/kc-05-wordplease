from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from blogs.models import Post
from blogs.serializers import PostSerializer


class PostsAPI(ListCreateAPIView):
    """
    Lists (GET) and create (POST) Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
