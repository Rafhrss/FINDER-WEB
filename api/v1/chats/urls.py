from django.urls import path

from api.v1.chats import views

urlpatterns = [
    path(
        "rooms/",
        views.ChatRoomListAPIView.as_view(),
        name="chatroom-list",
    ),
    path(
        "reports/<uuid:report_id>/rooms/",
        views.ChatRoomCreateAPIView.as_view(),
        name="chatroom-create",
    ),
    path(
        "rooms/<uuid:chatroom_id>/messages/",
        views.MessageListCreateAPIView.as_view(),
        name="message-list-create",
    ),
    path(
        "cleanup/",
        views.CleanupChatRoomsAPIView.as_view(),
        name="chatroom-cleanup",
    ),
]
