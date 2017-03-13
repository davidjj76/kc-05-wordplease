from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_list_or_404
from django.utils import timezone

from blogs.models import Blog, Post


def published_posts(user):

    # Non authenticated: can see published posts
    # Non superuser: can see published posts and their own posts
    # Superuser: can see all posts
    if user.is_authenticated():
        if not user.is_superuser:
            # Can see his posts and published posts from other users (published before now)
            return (Q(blog__owner__username=user.username) | Q(published_at__lte=timezone.now()))
    else:
        # Only can see published posts (published before now)
        return (Q(published_at__lte=timezone.now()))

    return Q()


def index(request):
    """
    Get latest posts
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    posts = get_list_or_404(Post.objects.select_related(), published_posts(request.user))
    return render(request, 'blogs/index.html', {'posts': posts})


def blogs(request):
    """
    Get blogs list
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    blogs = get_list_or_404(Blog.objects.select_related())
    return render(request, 'blogs/list.html', { 'blogs': blogs })


def user_blog(request, username):
    """
    Get user posts
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    posts = Post.objects.select_related()\
        .filter(blog__owner__username=username)\
        .filter(published_posts(request.user))

    if len(posts) == 0:
        raise Http404("No blog/posts found.")
    else:
        context = {
            'blog': posts[0].blog,
            'posts': posts
        }
        return render(request, 'blogs/index.html', context)


def post_detail(request, username, post_id):
    """
    Get post detail
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    posts = Post.objects.select_related()\
        .filter(blog__owner__username=username)\
        .filter(id=post_id)\
        .filter(published_posts(request.user))

    if len(posts) == 0:
        raise Http404("No post found.")
    else:
        return render(request, 'blogs/detail.html', { 'post': posts[0] })
