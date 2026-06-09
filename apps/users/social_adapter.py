from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from apps.users.selectors import get_user_by_email
from apps.users.validators import validate_campus_email


class CampusSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email") or sociallogin.user.email
        picture = sociallogin.account.extra_data.get("picture", "").strip()
        try:
            normalized_email = validate_campus_email(email)
            sociallogin.user.email = normalized_email
        except ValidationError as exc:
            if request is not None:
                messages.error(request, " ".join(exc.messages))
                raise ImmediateHttpResponse(redirect("account_login")) from exc
            raise

        existing_user = get_user_by_email(normalized_email)
        
        if existing_user:
            if picture and existing_user.profile_picture != picture:
                existing_user.profile_picture = picture
                existing_user.save(update_fields=["profile_picture"])
                
            if request is not None and not sociallogin.is_existing:
                sociallogin.connect(request, existing_user)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        name = (data.get("name") or data.get("given_name") or "").strip()
        if name:
            user.name = name
        elif not user.name and user.email:
            user.name = user.email.split("@")[0]
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        picture = sociallogin.account.extra_data.get("picture", "").strip()
        fields_to_update: list[str] = []

        if not user.name and user.email:
            user.name = user.email.split("@")[0]
            fields_to_update.append("name")

        if picture and user.profile_picture != picture:
            user.profile_picture = picture
            fields_to_update.append("profile_picture")

        if user.has_usable_password():
            user.set_unusable_password()
            fields_to_update.append("password")

        if fields_to_update:
            user.save(update_fields=fields_to_update)
        return user
