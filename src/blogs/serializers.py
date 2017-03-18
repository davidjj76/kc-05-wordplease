from django.contrib.auth.models import User
from rest_framework import serializers

from blogs.models import Post
from rest_framework.reverse import reverse

from users.serializers import UserSerializer


class BlogUrlField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        kwargs = { 'username': obj.get('username') }
        return reverse(view_name, kwargs=kwargs, request=request)


class BlogsListSerializer(serializers.ModelSerializer):

    blog_url = BlogUrlField(view_name='user_blog', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'blog_url')


class PostsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'summary', 'media_url', 'published_at')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("blog",)
