from django.db.models import Max, Prefetch, Q

from apps.chats.models import ChatRoom, Message


def get_chatroom_by_id(chatroom_id: int) -> ChatRoom | None:
    return (
        ChatRoom.objects.select_related("report", "user1", "user2")
        .filter(id=chatroom_id)
        .first()
    )


def get_chatroom_for_user_and_report(*, user, report) -> ChatRoom | None:
    return (
        ChatRoom.objects.select_related("report", "user1", "user2")
        .filter(report=report)
        .filter(Q(user1=user) | Q(user2=user))
        .first()
    )


def list_chatrooms_for_user(*, user):
    message_queryset = Message.objects.select_related("sender").order_by("-created_at")
    return (
        ChatRoom.objects.select_related("report", "user1", "user2")
        .filter(Q(user1=user) | Q(user2=user))
        .annotate(last_message_at=Max("messages__created_at"))
        .prefetch_related(
            Prefetch(
                "messages",
                queryset=message_queryset,
                to_attr="prefetched_messages",
            ),
        )
        .order_by("-last_message_at", "-created_at")
    )


def list_messages(*, chatroom: ChatRoom):
    return Message.objects.select_related("sender").filter(chatroom=chatroom)
