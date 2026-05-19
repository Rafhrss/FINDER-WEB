from rest_framework import serializers

from apps.users.models import User
from apps.users.validators import validate_campus_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "profile_picture")
        read_only_fields = ("id",)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=120)
    password = serializers.CharField(write_only=True, min_length=8)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    def validate_email(self, value: str) -> str:
        return validate_campus_email(value)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
