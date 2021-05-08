from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = models.CharField(max_length=100,
                                blank=True,
                                null=True)
    bio = models.CharField(max_length=200,
                           null=True,
                           blank=True)
    email = models.EmailField(max_length=100,
                              unique=True,
                              null=False)
    username = models.CharField(max_length=100,
                                unique=True,
                                blank=True,
                                null=False,
                                default=email)
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default="user")
    confirmation_code = models.CharField(max_length=8,
                                         null=True,
                                         blank=True)
    data_confirmation_code = models.DateTimeField(
        null=False,
        blank=False,
        default=datetime.now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
