from django.contrib.auth.models import User
from rest_framework import serializers

from blogs.models import Post
from rest_framework.reverse import reverse

from users.serializers import UserNameSerializer


class CategorySerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    abbreviation = serializers.CharField()
    name = serializers.CharField()


class BlogUrlField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        kwargs = { 'username': obj.get('username') }
        return reverse(view_name, kwargs=kwargs, request=request)


class BlogsListSerializer(serializers.ModelSerializer):

    blog_url = BlogUrlField(view_name='user_blog', read_only=True)
    posts = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'username', 'blog_url', 'posts')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('author',)

class PostReadSerializer(PostSerializer):

    author = UserNameSerializer()
    categories = CategorySerializer(many=True)

class PostListSerializer(PostReadSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'media_url', 'summary', 'published_at')
