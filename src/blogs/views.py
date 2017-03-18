from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from blogs.forms import PostForm
from blogs.models import Blog, Post


def published_posts(user):

    # Non authenticated: can see published posts
    # Non superuser: can see published posts and their own posts
    # Superuser: can see all posts
    if user.is_authenticated():
        if not user.is_superuser:
            # Can see his posts and published posts from other users (published before now)
            return (Q(blog__author__username=user.username) | Q(published_at__lte=timezone.now()))
    else:
        # Only can see published posts (published before now)
        return (Q(published_at__lte=timezone.now()))

    return Q()


class LatestPostsView(ListView):

    template_name = 'blogs/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related()\
            .filter(published_posts(self.request.user))


# @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/login/'), name='dispatch')
class BlogsView(ListView):

    template_name = 'blogs/list.html'
    context_object_name = 'blogs'
    queryset = Blog.objects.select_related()


class UserBlogView(ListView):

    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related()\
            .filter(blog__author__username=self.kwargs.get('username'))\
            .filter(published_posts(self.request.user))

    def get_context_data(self, **kwargs):
        context = super(UserBlogView, self).get_context_data(**kwargs)
        if len(self.object_list):
            context['blog'] = self.object_list[0].blog
        return context

    def render_to_response(self, context, **response_kwargs):
        if len(self.object_list) == 0:
            if self.request.user.username == self.kwargs.get('username'):
                return redirect('new_post')
            else:
                raise Http404("No blog / posts found.")

        return render(self.request, 'blogs/index.html', context)


class PostDetailView(DetailView):

    def get_queryset(self):
        return Post.objects.select_related() \
            .filter(blog__author__username=self.kwargs.get('username')) \
            .filter(id=self.kwargs.get('pk')) \
            .filter(published_posts(self.request.user))

    def render_to_response(self, context, **response_kwargs):
        if not self.object:
            raise Http404("No post found.")
        else:
            return render(self.request, 'blogs/detail.html', context)


class NewPostView(View):

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        """
        Shows new post form
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        try:
            blog = request.user.blog
            form = PostForm()
            context = {
                'blog': blog,
                'form': form
            }
            return render(request, 'blogs/new_post.html', context)

        except Blog.DoesNotExist:
            raise Http404("No blog found.")

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        """
        Creates a new post
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        try:
            new_post = Post(blog=request.user.blog)
            form = PostForm(request.POST, instance=new_post)
            context = dict()

            if form.is_valid():
                post = form.save()
                # Redirect to post detail
                return redirect('post_detail', username=post.blog.author, pk=post.pk)
            else:
                context['error'] = "Error submitting new post"

            context['form'] = form
            return render(request, 'blogs/new_post.html', context)

        except Blog.DoesNotExist:
            raise Http404("No blog found.")

