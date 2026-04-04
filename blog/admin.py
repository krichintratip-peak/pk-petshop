from django.contrib import admin
from .models import Post, Author


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'date_updated']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('related_categories',)
    search_fields = ['title', 'description', 'body']


admin.site.register(Author)
