from django.core.exceptions import ValidationError

from apps.core.exceptions import CampusEmailValidationError


def validate_campus_email(value: str) -> str:
    email = (value or "").strip().lower()
    if not email.endswith("@umkt.ac.id"):
        raise CampusEmailValidationError("Email harus menggunakan domain kampus @umkt.ac.id.")
    return email
