from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.users.validators import validate_campus_email


def register_user(
    *,
    email: str,
    name: str,
    password: str,
    profile_picture=None,
) -> User:
    normalized_email = validate_campus_email(email)
    return User.objects.create_user(
        email=normalized_email,
        name=name.strip(),
        password=password,
        profile_picture=profile_picture,
    )


def authenticate_user(*, email: str, password: str) -> User:
    normalized_email = validate_campus_email(email)
    user = authenticate(email=normalized_email, password=password)
    if not user:
        raise ValidationError("Email atau password tidak valid.")
    return user


def login_user(*, email: str, password: str) -> tuple[User, Token]:
    user = authenticate_user(email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token


def logout_user(*, user: User) -> None:
    Token.objects.filter(user=user).delete()
