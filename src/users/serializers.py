from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse


class BlogUrlField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        kwargs = { 'username': obj.get('username') }
        return reverse(view_name, kwargs=kwargs, request=request)

class UsersListSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    blog_url = BlogUrlField(view_name='user_blog', read_only=True)


class UserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return self.update(User(), validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate_username(self, username):
        if not self.instance and User.objects.filter(username=username).exists():
            # Creating user (no instance)
            # Not allowed repeated username
            raise ValidationError('Username already exists')

        if self.instance and self.instance.username != username and User.objects.filter(username=username).exists():
            # Updating user (user instance)
            # Not allowed repeated username, except his username
            raise ValidationError('Username already exists')

        return username

    def validate_email(self, email):
        if not self.instance and User.objects.filter(email=email).exists():
            # Creating user (no instance)
            # Not allowed repeated email
            raise ValidationError('Email already exists')

        if self.instance and self.instance.email != email and User.objects.filter(email=email).exists():
            # Updating user (user instance)
            # Not allowed repeated email, except his email
            raise ValidationError('Email already exists')

        return email

