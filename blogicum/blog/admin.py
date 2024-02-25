from django.contrib import admin

from .models import Post, Category, Location, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'author',
        'category',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'category',
    )
    list_per_page = 15
    search_fields = (
        'title',
        'text',
        'author',
    )
    list_filter = (
        'category',
        'author',
        'location',
    )
    list_display_links = (
        'title',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'created_at',
        'slug',
    )
    list_editable = (
        'is_published',
    )
    list_per_page = 15
    search_fields = (
        'title',
        'description',
    )
    list_display_links = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    list_per_page = 15
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    list_display_links = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author',
        'created_at',
    )

    list_per_page = 15
    search_fields = (
        'post',
        'author',
    )
    list_display_links = (
        'post',
    )


admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Управление проектом "Блогикум"'
admin.site.site_title = 'Блогикум'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
