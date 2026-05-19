from apps.users.models import User


def get_user_by_email(email: str) -> User | None:
    return User.objects.filter(email=email.strip().lower()).first()


def get_user_by_id(user_id: int) -> User | None:
    return User.objects.filter(id=user_id).first()
