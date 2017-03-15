from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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
        # Validate if username exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def validate_email(self, email):
        # Validate if email exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email
