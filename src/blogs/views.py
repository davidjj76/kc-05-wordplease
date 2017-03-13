from django.shortcuts import render

from blogs.models import Post


def index(request):
    """
    Get latest post
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    posts = Post.objects.all()
    return render(request, 'blogs/index.html', { 'posts': posts })
