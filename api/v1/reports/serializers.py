from rest_framework import serializers

from apps.reports.models import Report, ReportStatus


class ReportOwnerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "id",
            "user",
            "title",
            "description",
            "location",
            "image",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at")

    def get_user(self, obj: Report):
        request = self.context.get("request")
        if request and request.user.is_anonymous:
            return None
        return ReportOwnerSerializer(obj.user).data


class ReportWriteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=180)
    description = serializers.CharField()
    location = serializers.CharField(max_length=255)
    image = serializers.ImageField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=ReportStatus.choices, required=False)

    def validate_image(self, value):
        if not value:
            return value
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Ukuran file gambar tidak boleh melebihi 5MB.")
        if value.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise serializers.ValidationError("Format gambar harus berupa JPG, JPEG, atau PNG.")
        return value

