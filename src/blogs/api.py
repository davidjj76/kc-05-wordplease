from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from blogs.models import Post
from blogs.permissions import PostPermission
from blogs.serializers import BlogsListSerializer, PostSerializer


class BlogsAPI(ListAPIView):
    """
    Lists (GET) blogs
    """
    serializer_class = BlogsListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('username',)
    queryset = User.objects.annotate(posts=Count('post'))\
        .values('id', 'username', 'posts')


class PostsAPI(CreateAPIView):
    """
    Create (POST) posts
    """
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT) and delete (DELETE) posts
    """
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
