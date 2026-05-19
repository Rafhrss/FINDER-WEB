from django.contrib import admin

from apps.chats.models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "user1", "user2", "created_at")
    search_fields = ("report__title", "user1__email", "user2__email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chatroom", "sender", "created_at")
    search_fields = ("message", "sender__email")
