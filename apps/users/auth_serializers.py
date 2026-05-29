from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from apps.users.validators import validate_campus_email


class CampusLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        if email:
            attrs["email"] = validate_campus_email(email)
        return super().validate(attrs)


class CampusRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=120)

    def validate_email(self, email):
        return validate_campus_email(email)

    def validate_name(self, value):
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Nama wajib diisi.")
        return name

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["name"] = self.validated_data.get("name", "")
        return data

    def custom_signup(self, request, user):
        user.name = self.validated_data.get("name", "").strip()
        user.save(update_fields=["name"])
