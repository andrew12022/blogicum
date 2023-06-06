from django.contrib import admin

from blog.models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'is_published',
        'created_at',
        'author',
        'location',
        'category',
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'author',
        'location',
        'category',
    )
    list_display_links = (
        'title',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
    )
    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    inlines = (
        PostInline,
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
