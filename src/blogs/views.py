from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from blogs.forms import PostForm
from blogs.models import Post


def published_posts(user):

    # Non authenticated: can see published posts
    # Non superuser: can see published posts and their own posts
    # Superuser: can see all posts
    if user.is_authenticated():
        if not user.is_superuser:
            # Can see his posts and published posts from other users (published before now)
            return (Q(author__username=user.username) | Q(published_at__lte=timezone.now()))
    else:
        # Only can see published posts (published before now)
        return (Q(published_at__lte=timezone.now()))

    return Q()


class LatestPostsView(ListView):

    template_name = 'blogs/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related().filter(published_posts(self.request.user))


# @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/login/'), name='dispatch')
class BlogsView(ListView):

    template_name = 'blogs/list.html'
    context_object_name = 'blogs'
    queryset = User.objects.select_related()


class UserBlogView(ListView):

    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related()\
            .filter(author__username=self.kwargs.get('username'))\
            .filter(published_posts(self.request.user))

    def get_context_data(self, **kwargs):
        context = super(UserBlogView, self).get_context_data(**kwargs)
        if User.objects.filter(username=self.kwargs.get('username')).exists():
            context['blog'] = self.kwargs.get('username')
        return context

    def render_to_response(self, context, **response_kwargs):
        if context.get('blog'):
            return render(self.request, 'blogs/index.html', context)
        else:
            raise Http404("No blog found.")


class PostDetailView(DetailView):

    def get_queryset(self):
        return Post.objects.select_related() \
            .filter(author__username=self.kwargs.get('username')) \
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
        form = PostForm()
        context = {
            'blog': request.user.username,
            'form': form
        }
        return render(request, 'blogs/new_post.html', context)

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        """
        Creates a new post
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        new_post = Post(author=request.user)
        form = PostForm(request.POST, instance=new_post)
        context = dict()

        if form.is_valid():
            post = form.save()
            # Redirect to post detail
            return redirect('post_detail', username=post.author, pk=post.pk)
        else:
            context['error'] = "Error submitting new post"

        context['blog'] = request.user.username
        context['form'] = form
        return render(request, 'blogs/new_post.html', context)

