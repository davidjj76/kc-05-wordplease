from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blogs.models import Blog, Post
from blogs.serializers import BlogsListSerializer, PostsListSerializer, PostSerializer


class BlogsAPI(ListAPIView):
    """
    Lists (GET) blogs
    """
    serializer_class = BlogsListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('author__username', 'title')
    ordering_fields = ('author__username', 'title')
    queryset = Blog.objects.all().select_related('author_username')\
            .values('id', 'title', 'author__username')


class PostsAPI(ListCreateAPIView):
    """
    Lists (GET) and create (POST) posts
    """
    queryset = Post.objects.all().select_related()

    def get_serializer_class(self):
        return PostsListSerializer if self.request.method == 'GET' else PostSerializer

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT) and delete (DELETE) posts
    """
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        serializer.save(blog=self.request.user.blog)
