import json
import random
import string
from datetime import datetime, timedelta

from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from urllib3.exceptions import HTTPError

from auth_and_user.models import User
from auth_and_user.serializers import MyTokenSerilizer, UsersSerializer


@csrf_exempt
def authorization(request: WSGIRequest):
    body = json.loads(request.body)
    email = body['email']
    letters = string.ascii_uppercase + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(8))
    date = datetime.now() + timedelta(hours=1)
    user = None
    try:
        user = User.objects.get(email=email)
        user.confirmation_code = rand_string
        user.data_confirmation_code = date
    except User.DoesNotExist:
        user = User(email=email, username=email, confirmation_code=rand_string,
                    data_confirmation_code=date)
        user.set_unusable_password()
    finally:
        user.save()
        send_mail('Confirmation code',
                  rand_string,
                  'example@ya.ru',
                  [email]
                  )

    print(email, rand_string)
    print(User.objects.get(email='example@yandex.ru'))
    return Response(status=status.HTTP_200_OK)


class MyTokenView(TokenViewBase):
    serializer_class = MyTokenSerilizer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            try:
                serializer = UsersSerializer(
                    User.objects.get(username=username))
                return JsonResponse(serializer.data)
            except HTTPError:
                return HttpResponse(status=404)
        return super().list(request, args, kwargs)

    def partial_update(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if 'role' in request.data:
                    if request.data['role'] == 'admin':
                        user.is_staff = True
                        user.is_superuser = True
                    if request.data['role'] == 'user':
                        user.is_staff = False
                        user.is_superuser = False
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
        except HTTPError:
            return HttpResponse(status=404)

    def destroy(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except HTTPError:
            return HttpResponse(status=404)


class MeViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def list(self, request, *args, **kwargs):
        serializer = UsersSerializer(User.objects.get(
            username=request.user.username))
        return JsonResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = UsersSerializer(User.objects.get(
            username=request.user.username),
            data=request.data,
            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return HttpResponse(status=404)
