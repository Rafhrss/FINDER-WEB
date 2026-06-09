from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from google.auth.transport.requests import Request
from google.oauth2 import id_token as google_id_token
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.users.selectors import get_user_by_email
from apps.users.validators import validate_campus_email

GOOGLE_TOKEN_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}


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


def verify_google_id_token(*, raw_id_token: str) -> dict:
    allowed_client_ids = [
        client_id
        for client_id in settings.GOOGLE_OAUTH_ALLOWED_CLIENT_IDS
        if client_id
    ]
    if not allowed_client_ids:
        raise ValidationError("Google OAuth belum dikonfigurasi di server.")

    try:
        claims = google_id_token.verify_oauth2_token(
            raw_id_token,
            Request(),
            audience=None,
        )
    except ValueError as exc:
        raise ValidationError("ID token Google tidak valid.") from exc

    audience = claims.get("aud")
    if audience not in allowed_client_ids:
        raise ValidationError("ID token Google tidak sesuai untuk aplikasi ini.")

    issuer = claims.get("iss")
    if issuer not in GOOGLE_TOKEN_ISSUERS:
        raise ValidationError("Issuer token Google tidak valid.")

    if claims.get("email_verified") is not True:
        raise ValidationError("Email Google belum terverifikasi.")

    email = claims.get("email")
    if not email:
        raise ValidationError("Email tidak ditemukan pada token Google.")
    normalized_email = validate_campus_email(email)

    hosted_domain = (claims.get("hd") or "").strip().lower()
    superadmins = getattr(settings, "SUPERADMIN_EMAILS", [])
    if hosted_domain != settings.GOOGLE_WORKSPACE_DOMAIN and normalized_email not in superadmins:
        raise ValidationError("Akun Google harus berasal dari domain umkt.ac.id.")

    claims["email"] = normalized_email
    return claims


def upsert_user_from_google_claims(*, claims: dict) -> User:
    email = claims["email"]
    name = (claims.get("name") or claims.get("given_name") or "").strip()
    if not name:
        name = email.split("@")[0]

    user = get_user_by_email(email)
    if user is None:
        return User.objects.create_user(email=email, name=name, password=None)

    fields_to_update: list[str] = []
    if user.name != name:
        user.name = name
        fields_to_update.append("name")

    if user.has_usable_password():
        user.set_unusable_password()
        fields_to_update.append("password")

    if fields_to_update:
        user.save(update_fields=fields_to_update)
    return user


def login_with_google_id_token(*, raw_id_token: str) -> tuple[User, Token]:
    claims = verify_google_id_token(raw_id_token=raw_id_token)
    user = upsert_user_from_google_claims(claims=claims)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token
