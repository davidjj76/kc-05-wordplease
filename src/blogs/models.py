from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Post(models.Model):

    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    media_url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
