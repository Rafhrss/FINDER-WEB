import uuid

from django.conf import settings
from django.db import models
from django.db.models import F, Q

from apps.reports.models import Report


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="chat_rooms",
    )
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_rooms_as_user1",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_rooms_as_user2",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["report", "user1", "user2"],
                name="unique_chatroom_per_report_pair",
            ),
            # Memastikan user1 dan user2 tidak boleh orang yang sama
            # Ini mencegah seseorang membuat ruang obrolan (ChatRoom) dengan dirinya sendiri
            models.CheckConstraint(
                condition=~Q(user1=F("user2")),
                name="chatroom_distinct_users",
            ),
        ]

    def __str__(self) -> str:
        return f"Chat Report#{self.report_id}: {self.user1_id}-{self.user2_id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Message#{self.id} by {self.sender_id}"
