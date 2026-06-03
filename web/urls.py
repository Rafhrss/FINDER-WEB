from django.urls import path

from web.views import (
    chat_room_view,
    home_view,
    login_view,
    logout_view,
    open_chatroom_view,
    profile_view,
    report_create_view,
    report_detail_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home_view, name="home"),
    path("reports/create/", report_create_view, name="report-create"),
    path("reports/<int:report_id>/", report_detail_view, name="report-detail"),
    path("reports/<int:report_id>/chat/", open_chatroom_view, name="open-chat"),
    path("profile/", profile_view, name="profile"),
    path("chats/<int:chatroom_id>/", chat_room_view, name="chat-room"),
]
