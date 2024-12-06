from django.contrib import admin

from .models import Post, Location, Category


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'category',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
    )
    list_editable = (
        'description',
        'slug',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.empty_value_display = 'Не задано'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
