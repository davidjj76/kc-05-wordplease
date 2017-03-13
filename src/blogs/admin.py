from django.contrib import admin

from blogs.models import Blog, Category, Post

admin.site.register([Blog, Category, Post])
