from django import forms

from blogs.models import Blog, Post


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title']
        labels = {
            'title': 'Blog title'
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'summary', 'body', 'media_url', 'published_at', 'categories']
