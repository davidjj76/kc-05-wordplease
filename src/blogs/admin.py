from django.contrib import admin
from django.utils import timezone

from blogs.models import Category, Post


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'published_at', 'status', 'tagged_with')
    list_filter = ('author', 'categories', StatusListFilter)
    search_fields = ('title', 'summary', 'body')
