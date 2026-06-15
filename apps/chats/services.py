from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.chats.models import ChatRoom, Message
from apps.chats.selectors import get_chatroom_for_user_and_report, list_messages
from apps.core.exceptions import ChatParticipantValidationError, ChatReadOnlyError

READ_WRITE_WINDOW_DAYS = 2
EXPIRE_WINDOW_DAYS = 7


def ensure_chat_participant(*, chatroom: ChatRoom, user) -> None:
    if user.id not in {chatroom.user1_id, chatroom.user2_id}:
        raise ChatParticipantValidationError("Hanya participant chat yang bisa mengakses chat.")


def is_chat_writable(*, chatroom: ChatRoom, now=None) -> bool:
    current_time = now or timezone.now()
    return (current_time - chatroom.created_at) <= timedelta(days=READ_WRITE_WINDOW_DAYS)


def cleanup_expired_chatrooms(*, now=None) -> int:
    current_time = now or timezone.now()
    cutoff = current_time - timedelta(days=EXPIRE_WINDOW_DAYS)
    deleted_count, _ = ChatRoom.objects.filter(created_at__lt=cutoff).delete()
    return deleted_count


def cleanup_all_stale_chatrooms(*, now=None) -> dict:
    current_time = now or timezone.now()
    
    # 1. Hapus chat yang sudah expired (> 7 hari)
    expired_cutoff = current_time - timedelta(days=EXPIRE_WINDOW_DAYS)
    expired_count, _ = ChatRoom.objects.filter(created_at__lt=expired_cutoff).delete()
    
    # 2. Hapus chat yang ditinggalkan (> 1 jam, 0 pesan)
    abandoned_cutoff = current_time - timedelta(hours=1)
    abandoned_count, _ = ChatRoom.objects.filter(
        created_at__lt=abandoned_cutoff,
        messages__isnull=True
    ).delete()
    
    return {
        "expired_deleted": expired_count,
        "abandoned_deleted": abandoned_count
    }


def create_chatroom(*, report, initiator) -> tuple[ChatRoom, bool]:
    cleanup_expired_chatrooms()

    if report.user_id == initiator.id:
        raise ValidationError("Pemilik laporan tidak bisa chat dengan dirinya sendiri.")

    existing_chatroom = get_chatroom_for_user_and_report(user=initiator, report=report)
    if existing_chatroom:
        return existing_chatroom, False

    chatroom = ChatRoom(report=report, user1=report.user, user2=initiator)
    chatroom.full_clean()
    chatroom.save()
    return chatroom, True


def get_messages_for_chatroom(*, chatroom: ChatRoom, requester):
    cleanup_expired_chatrooms()
    ensure_chat_participant(chatroom=chatroom, user=requester)
    if not ChatRoom.objects.filter(id=chatroom.id).exists():
        raise ValidationError("Chat sudah kedaluwarsa dan dihapus.")
    return list_messages(chatroom=chatroom)


def send_message(*, chatroom: ChatRoom, sender, message: str) -> Message:
    cleanup_expired_chatrooms()
    ensure_chat_participant(chatroom=chatroom, user=sender)

    if not ChatRoom.objects.filter(id=chatroom.id).exists():
        raise ValidationError("Chat sudah kedaluwarsa dan dihapus.")
    if not is_chat_writable(chatroom=chatroom):
        raise ChatReadOnlyError("Chat sudah readonly setelah 2 hari.")

    body = (message or "").strip()
    if not body:
        raise ValidationError("Pesan tidak boleh kosong.")

    chat_message = Message(chatroom=chatroom, sender=sender, message=body)
    chat_message.full_clean()
    chat_message.save()
    return chat_message
