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

    list_display = ('title', 'get_author', 'media_url', 'summary', 'published_at', 'status')
    list_filter = ('author', 'categories', StatusListFilter)
    search_fields = ('title', 'summary', 'body')

    fieldsets = (
        ('Author and Title', {
            'fields': ('author', 'title'),
            }
        ),
        ('Main content', {
            'fields': ('summary', 'body'),
            }
        ),
        ('Multimedia content', {
            'fields': ('media_url',),
            'classes': ('collapse', 'extrapretty')
            }
        ),
        ('Published', {
            'fields': ('published_at',),
            'description': 'Set publication date of post (you can save as draft publishing at future date)'
            }
        ),
        ('Tagged with', {
            'fields': ('categories',),
            'description': 'At least one category'
            }
        )
    )

    def get_author(self, obj):
        return obj.author.username
    get_author.short_description = 'author'
    get_author.admin_order_field = 'author__username'