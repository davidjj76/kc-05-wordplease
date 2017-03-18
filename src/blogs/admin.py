from django.contrib import admin
from django.utils import timezone

from blogs.models import Category, Blog, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'abbreviation')


class StatusListFilter(admin.SimpleListFilter):

    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('DR', 'Draft'),
            ('PB', 'Published')
        )
    def queryset(self, request, queryset):

        if self.value() == 'DR':
            return queryset.filter(published_at__gt=timezone.now())

        if self.value() == 'PB':
            return queryset.filter(published_at__lte=timezone.now())


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ('author', 'title')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'blog', 'get_author', 'published_at', 'status', 'tagged_with')
    list_filter = ('blog__author', 'categories', StatusListFilter)
    search_fields = ('title', 'summary', 'body')

    def get_author(self, obj):
        return obj.blog.author
    get_author.short_description = 'author'
    get_author.admin_order_field = 'blog__author'