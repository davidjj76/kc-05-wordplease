from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Blog(models.Model):

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["owner__username"]

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["abbreviation"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


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

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def status(self):
        return "Published" if self.published_at <= timezone.now() else "Draft"

    def tagged_with(self):
        return ", ".join([c.name for c in self.categories.all()])
