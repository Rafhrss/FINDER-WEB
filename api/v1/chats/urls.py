from django.urls import path

from api.v1.chats.views import ChatRoomCreateAPIView, MessageListCreateAPIView

urlpatterns = [
    path(
        "reports/<int:report_id>/rooms/",
        ChatRoomCreateAPIView.as_view(),
        name="chatroom-create",
    ),
    path(
        "rooms/<int:chatroom_id>/messages/",
        MessageListCreateAPIView.as_view(),
        name="message-list-create",
    ),
]
