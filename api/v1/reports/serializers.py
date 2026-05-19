from rest_framework import serializers

from apps.reports.models import Report, ReportStatus


class ReportOwnerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
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
        return ReportOwnerSerializer(obj.user).data


class ReportWriteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=180)
    description = serializers.CharField()
    location = serializers.CharField(max_length=255)
    image = serializers.ImageField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=ReportStatus.choices, required=False)
