import uuid

from django.conf import settings
from django.db import models


class ReportStatus(models.TextChoices):
    LOST = "LOST", "Hilang"
    FOUND = "FOUND", "Menemukan"
    CLAIMED = "CLAIMED", "Selesai"


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    title = models.CharField(max_length=180)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=ReportStatus.choices,
        default=ReportStatus.LOST,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"
