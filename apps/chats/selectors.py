from django.db.models import Q

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


def list_messages(*, chatroom: ChatRoom):
    return Message.objects.select_related("sender").filter(chatroom=chatroom)
