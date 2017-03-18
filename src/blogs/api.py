from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blogs.models import Blog, Post
from blogs.serializers import BlogsListSerializer, PostsListSerializer, PostSerializer


class BlogsAPI(ListAPIView):
    """
    Lists (GET) blogs
    """
    serializer_class = BlogsListSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', '')
        order = self.request.query_params.get('order', '')
        order_by = '-author__username' if order == 'des' else 'author__username'
        return Blog.objects.all().select_related('author_username')\
            .values('id', 'title', 'author__username')\
            .filter(author__username__startswith=username)\
            .order_by(order_by)


class PostsAPI(ListCreateAPIView):
    """
    Lists (GET) and create (POST) posts
    """
    queryset = Post.objects.all().select_related()

    def get_serializer_class(self):
        return PostsListSerializer if self.request.method == 'GET' else PostSerializer

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT) and delete (DELETE) posts
    """
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer
