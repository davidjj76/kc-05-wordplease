"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blogs.api import BlogsAPI, PostsAPI, PostDetailAPI
from blogs.views import LatestPostsView, BlogsView, UserBlogView, PostDetailView, NewPostView
from users.api import UsersAPI, UserDetailAPI
from users.views import LoginView, SignupView, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LatestPostsView.as_view(), name='index'),
    url(r'^blogs/$', BlogsView.as_view(), name='blogs'),
    url(r'^blogs/(?P<username>[0-9a-zA-Z_-]+)/$', UserBlogView.as_view(), name='user_blog'),
    url(r'^blogs/(?P<username>[0-9a-zA-Z_-]+)/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^new-post/$', NewPostView.as_view(), name='new_post'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^logout/$', logout, name='logout'),

    # API Users
    url(r'^api/1.0/users/$', UsersAPI.as_view(), name='users_api'),
    url(r'^api/1.0/users/(?P<pk>[0-9]+)/$', UserDetailAPI.as_view(), name='user_detail_api'),

    # API Blogs
    url(r'^api/1.0/blogs/$', BlogsAPI.as_view(), name='blogs_api'),

    # API Posts
    url(r'^api/1.0/posts/$', PostsAPI.as_view(), name='posts_api'),
    url(r'^api/1.0/posts/(?P<pk>[0-9]+)/$', PostDetailAPI.as_view(), name='post_detail_api')

]
