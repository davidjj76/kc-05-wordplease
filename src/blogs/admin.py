from django.contrib import admin
from django.utils import timezone

from blogs.models import Blog, Category, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'abbreviation')


class StatusListFilter(admin.SimpleListFilter):

    title = 'Status'
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'blog', 'get_owner', 'published_at', 'status', 'tagged_with')
    list_filter = ('blog', 'blog__owner', 'categories', StatusListFilter)

    def get_owner(self, obj):
        return obj.blog.owner

    get_owner.short_description = 'Owner'
    get_owner.admin_order_field = 'blog__owner'
