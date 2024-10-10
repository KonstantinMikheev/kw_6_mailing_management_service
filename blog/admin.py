from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'views_count', 'created_at', 'title', 'body')
    list_filter = ('created_at', 'title', 'is_published')
    search_fields = ('title', 'body')
