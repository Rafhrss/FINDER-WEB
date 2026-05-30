import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import UserManager
from apps.users.validators import validate_campus_email


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True, validators=[validate_campus_email])
    name = models.CharField(max_length=120)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
