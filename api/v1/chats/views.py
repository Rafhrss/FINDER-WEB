from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.chats.serializers import (
    ChatRoomSerializer,
    MessageSerializer,
    MessageWriteSerializer,
)
from apps.chats.selectors import get_chatroom_by_id
from apps.chats.services import (
    cleanup_expired_chatrooms,
    create_chatroom,
    get_messages_for_chatroom,
    send_message,
)
from apps.reports.selectors import get_report_by_id


class ChatRoomCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        report = get_report_by_id(report_id)
        if not report:
            raise NotFound("Laporan tidak ditemukan.")
        try:
            chatroom, created = create_chatroom(report=report, initiator=request.user)
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(ChatRoomSerializer(chatroom).data, status=status_code)


class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_chatroom(self, chatroom_id: int):
        cleanup_expired_chatrooms()
        chatroom = get_chatroom_by_id(chatroom_id)
        if not chatroom:
            raise NotFound("Chat tidak ditemukan atau sudah kedaluwarsa.")
        return chatroom

    def get(self, request, chatroom_id: int):
        chatroom = self._get_chatroom(chatroom_id)
        try:
            chat_messages = get_messages_for_chatroom(
                chatroom=chatroom,
                requester=request.user,
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        serializer = MessageSerializer(chat_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, chatroom_id: int):
        chatroom = self._get_chatroom(chatroom_id)
        serializer = MessageWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            chat_message = send_message(
                chatroom=chatroom,
                sender=request.user,
                message=serializer.validated_data["message"],
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        return Response(MessageSerializer(chat_message).data, status=status.HTTP_201_CREATED)
