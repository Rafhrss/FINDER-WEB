from web.views.auth import login_view, logout_view
from web.views.chats import chat_room_view, open_chatroom_view
from web.views.home import home_view
from web.views.profile import profile_view
from web.views.reports import report_detail_view

__all__ = [
    "chat_room_view",
    "home_view",
    "login_view",
    "logout_view",
    "open_chatroom_view",
    "profile_view",
    "report_detail_view",
]
