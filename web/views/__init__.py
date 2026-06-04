from web.views.auth import logout_view
from web.views.chats import chat_list_view, chat_room_view, open_chatroom_view
from web.views.home import home_view
from web.views.profile import profile_view
from web.views.reports import report_create_view, report_detail_view, my_reports_view, report_delete_view
from web.views.search import search_view

__all__ = [
    "chat_room_view",
    "chat_list_view",
    "home_view",
    "logout_view",
    "open_chatroom_view",
    "profile_view",
    "report_create_view",
    "report_detail_view",
    "my_reports_view",
    "report_delete_view",
    "search_view",
]
