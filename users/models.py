from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": ("email already exists"),
        },
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField()
    username = models.TextField(null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
