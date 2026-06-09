from django.urls import path

from web.views import (
    chat_room_view,
    home_view,
    terms_of_service_view,
    logout_view,
    open_chatroom_view,
    profile_view,
    report_create_view,
    report_detail_view,
    search_view,
    ai_search_view,
    chat_list_view,
    my_reports_view,
    report_delete_view,
    about_view,
)

urlpatterns = [
    path("logout/", logout_view, name="logout"),
    path("", home_view, name="home"),
    path("terms/", terms_of_service_view, name="terms"),
    path("about/", about_view, name="about"),
    path("search/", search_view, name="search"),
    path("search/ai/", ai_search_view, name="ai-search"),
    path("reports/create/", report_create_view, name="report-create"),
    path("reports/<uuid:report_id>/", report_detail_view, name="report-detail"),
    path("reports/<uuid:report_id>/chat/", open_chatroom_view, name="open-chat"),
    path("reports/<uuid:report_id>/delete/", report_delete_view, name="report-delete"),
    path("chats/", chat_list_view, name="chat-list"),
    path("profile/", profile_view, name="profile"),
    path("my-reports/", my_reports_view, name="my-reports"),
    path("chats/<uuid:chatroom_id>/", chat_room_view, name="chat-room")
]
