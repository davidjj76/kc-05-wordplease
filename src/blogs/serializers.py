from rest_framework import serializers

from blogs.models import Post


class PostsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'summary', 'media_url', 'published_at')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
