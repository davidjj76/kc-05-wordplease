from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from blogs.models import Post
from blogs.serializers import PostSerializer, PostsListSerializer


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
