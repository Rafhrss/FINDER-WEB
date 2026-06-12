from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "profile_picture")
        read_only_fields = ("id",)


class UserMeSerializer(UserSerializer):
    statistics = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("statistics",)

    def get_statistics(self, obj):
        from apps.reports.selectors import get_user_report_statistics
        return get_user_report_statistics(obj)


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(trim_whitespace=True, write_only=True)

    def validate_id_token(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("id_token wajib diisi.")
        return value
