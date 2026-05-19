from django.contrib.auth.base_user import BaseUserManager

from apps.users.validators import validate_campus_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("Email wajib diisi.")
        email = validate_campus_email(self.normalize_email(email))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser harus punya is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser harus punya is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)
