from django.contrib import admin
from import_export.admin import ImportMixin

from .models import Category, Genre, Title
from .resources import CategoryResource, GenreResource, TitleResource


class GenreAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = GenreResource
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class CategoryAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = TitleResource
    list_display = ('id', 'name', 'year', 'category', 'genres', 'description',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
