from django.urls import include, path
from rest_framework.routers import DefaultRouter

from categories_genres_titles.viewsets import (CategoriesViewSet,
                                               GenresViewSet, TitlesViewSet)

users_router_v1 = DefaultRouter()

users_router_v1.register('categories', CategoriesViewSet,
                         basename='categories')
users_router_v1.register('genres', GenresViewSet,
                         basename='genres')
users_router_v1.register('titles', TitlesViewSet,
                         basename='titles')


urlpatterns = [
    path('v1/', include(users_router_v1.urls))
]
