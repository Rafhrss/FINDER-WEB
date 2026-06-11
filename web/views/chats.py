import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from apps.chats.selectors import get_chatroom_by_id, list_chatrooms_for_user
from apps.chats.services import (
    cleanup_expired_chatrooms,
    create_chatroom,
    get_messages_for_chatroom,
    is_chat_writable,
    send_message,
)
from apps.reports.models import Report


@login_required
def open_chatroom_view(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    try:
        chatroom, _ = create_chatroom(report=report, initiator=request.user)
    except ValidationError as exc:
        messages.error(request, " ".join(exc.messages))
        return redirect("web:report-detail", report_id=report_id)
    return redirect("web:chat-room", chatroom_id=chatroom.id)


@login_required
def chat_list_view(request):
    cleanup_expired_chatrooms()
    chatrooms = list_chatrooms_for_user(user=request.user)
    return render(request, "web/chat_list.html", {"chatrooms": chatrooms})


@login_required
def chat_room_view(request, chatroom_id: uuid.UUID):
    cleanup_expired_chatrooms()
    chatroom = get_chatroom_by_id(chatroom_id)
    if not chatroom:
        messages.error(request, "Chat tidak ditemukan atau sudah kedaluwarsa.")
        return redirect("web:home")

    try:
        room_messages = get_messages_for_chatroom(chatroom=chatroom, requester=request.user)
    except ValidationError as exc:
        messages.error(request, " ".join(exc.messages))
        return redirect("web:home")
    except PermissionDenied as exc:
        raise PermissionDenied(str(exc)) from exc

    can_send = is_chat_writable(chatroom=chatroom)

    if request.method == "POST":
        try:
            send_message(
                chatroom=chatroom,
                sender=request.user,
                message=request.POST.get("message", ""),
            )
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        except PermissionDenied as exc:
            messages.error(request, str(exc))
        return redirect("web:chat-room", chatroom_id=chatroom.id)

    all_chatrooms = list_chatrooms_for_user(user=request.user)

    context = {
        "chatroom": chatroom,
        "chat_messages": room_messages,
        "can_send": can_send,
        "chatrooms": all_chatrooms,
    }
    return render(request, "web/chat_room.html", context)
