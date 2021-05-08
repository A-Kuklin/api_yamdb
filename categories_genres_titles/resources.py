from import_export import fields, resources
from import_export.widgets import ManyToManyWidget

from .models import Category, Genre, Title


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug',)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)


class TitleResource(resources.ModelResource):
    genre = fields.Field(
        column_name='genre',
        widget=ManyToManyWidget(Genre, 'pk')
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description',)
