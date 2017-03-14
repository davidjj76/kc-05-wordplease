from django import forms

from blogs.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'summary', 'body', 'media_url', 'published_at', 'categories']
