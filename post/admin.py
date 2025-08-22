from urllib.parse import urlencode
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse_lazy

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    classes = ['collapse']

    @admin.display(boolean=True)
    def is_reply(self, obj):
        return bool(obj.parent_id)

    readonly_fields = ('is_reply',)
    fields = ('author', 'content', 'is_reply')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_date')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_help_text = 'You can search based on the category name.'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display_links = ('title', 'display_image')
    list_display = ('title', 'author', 'short_date', 'status', 'display_image', 'show_likes')
    search_help_text = 'You can search based on the post title.'
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author',)
    search_fields = ('title',)
    filter_horizontal = ('category',)
    list_filter = ('status','category')
    list_per_page = 3
    inlines = (CommentInline,)
    readonly_fields = ('preview_image',)
    fieldsets = (
        (None, {
            'fields': (('main_topic', 'title'),( 'slug', 'author'), 'category'),
        }),
        ('Content', {
            'fields': ('body', 'image','preview_image', 'read_time'),
        }),
        ('Metadata', {
            'fields': ('status',)
        }),
    )
    @admin.display(description='Likes❤')
    def show_likes(self,obj):
        color = 'green'
        likes = obj.likes.count()
        if 1 <= likes <= 4:
            color = 'yellow'
        elif likes == 0:
            color = 'red'
        url = (
            reverse_lazy('admin:post_like_changelist') + '?' + urlencode({'post__id': f'{obj.id}'})
        )
        return format_html('<a style="color:{}" href="{}">{}</a>', color, url, likes)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    autocomplete_fields = ('author','post')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'is_reply']
    autocomplete_fields = ('author', 'post')

    @admin.display(boolean=True)
    def is_reply(self, obj):
        return bool(obj.parent_id)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('author', 'subject')
    autocomplete_fields = ('author',)
