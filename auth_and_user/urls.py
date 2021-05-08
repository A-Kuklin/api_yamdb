from django.urls import include, path
from rest_framework.routers import DefaultRouter

from auth_and_user import views
from auth_and_user.views import MeViewSet, MyTokenView, UsersViewSet

router = DefaultRouter()

router.register(r'^users/me$', MeViewSet, basename='me')

urlpatterns = [
    path('v1/users/me/', MeViewSet.as_view(
        {'get': 'list',
         'patch': 'partial_update'})),
    path('v1/users/', UsersViewSet.as_view(
        {'get': 'list',
         'post': 'create'})),
    path('v1/users/<str:username>/', UsersViewSet.as_view(
        {'get': 'list',
         'patch': 'partial_update',
         'delete': 'destroy'})),
    path('v1/', include(router.urls)),
    path('v1/auth/email/', views.authorization),
    path('v1/auth/token/', MyTokenView.as_view(), name='token_obtain_pair'),
]
