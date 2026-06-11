from django.urls import path

from api.v1.chats.views import (
    ChatRoomCreateAPIView,
    ChatRoomListAPIView,
    MessageListCreateAPIView,
)

urlpatterns = [
    path(
        "rooms/",
        ChatRoomListAPIView.as_view(),
        name="chatroom-list",
    ),
    path(
        "reports/<uuid:report_id>/rooms/",
        ChatRoomCreateAPIView.as_view(),
        name="chatroom-create",
    ),
    path(
        "rooms/<uuid:chatroom_id>/messages/",
        MessageListCreateAPIView.as_view(),
        name="message-list-create",
    ),
]
