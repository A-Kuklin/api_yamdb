from datetime import datetime

import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import AccessToken

from auth_and_user.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'bio',
                  'email',
                  'role']

    def validate(self, data):
        if 'request' in self.context:
            if (self.context['request'].method == 'POST'
                    and User.objects.filter(email=data['email']).exists()):
                raise ParseError('Пользователь'
                                 ' с таким email уже существует')
            if (self.context['request'].method == 'POST'
                    and User.objects.filter(
                        username=data['username']).exists()):
                raise ParseError(
                    'Пользователь с таким username уже существует')
        return data


@csrf_exempt
class MyTokenSerilizer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        token = AccessToken()
        token.__setitem__("email", user.email)
        token.__setitem__("user_id", user.id)

        return token

    def validate(self, attrs):
        request = self.context['request']
        try:
            user = User.objects.get(
                email=request.data["email"],
                confirmation_code=request.data["confirmation_code"])
            now_date = datetime.now().replace(tzinfo=pytz.UTC)
            if user.data_confirmation_code < now_date:
                raise ValueError("Code is expired")
        except User.DoesNotExist:
            raise ValueError("User not found")
        return {"jwt": str(self.get_token(user))}
