from django.contrib.auth.models import User
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blogs.models import Post
from blogs.serializers import BlogsListSerializer, PostsListSerializer, PostSerializer


class BlogsAPI(ListAPIView):
    """
    Lists (GET) blogs
    """
    serializer_class = BlogsListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'title')
    ordering_fields = ('username', 'title')
    queryset = User.objects.all().values('id', 'username')


class PostsAPI(ListCreateAPIView):
    """
    Lists (GET) and create (POST) posts
    """
    queryset = Post.objects.all().select_related()

    def get_serializer_class(self):
        return PostsListSerializer if self.request.method == 'GET' else PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT) and delete (DELETE) posts
    """
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
