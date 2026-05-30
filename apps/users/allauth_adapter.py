from allauth.account.adapter import DefaultAccountAdapter

from apps.users.validators import validate_campus_email


class CampusAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        email = super().clean_email(email)
        return validate_campus_email(email)
