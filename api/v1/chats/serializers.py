from rest_framework import serializers

from apps.chats.models import ChatRoom, Message
from apps.reports.models import Report


class ReportCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("id", "title", "image", "status")
        read_only_fields = fields


class ChatParticipantSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()
    profile_picture = serializers.URLField(allow_null=True, required=False)


class ChatRoomSerializer(serializers.ModelSerializer):
    report = ReportCompactSerializer(read_only=True)
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ("id", "report", "user1", "user2", "created_at")
        read_only_fields = fields

    def get_user1(self, obj: ChatRoom):
        return ChatParticipantSerializer(obj.user1).data

    def get_user2(self, obj: ChatRoom):
        return ChatParticipantSerializer(obj.user2).data


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "chatroom", "sender", "message", "created_at")
        read_only_fields = ("id", "chatroom", "sender", "created_at")

    def get_sender(self, obj: Message):
        return ChatParticipantSerializer(obj.sender).data


class MessageWriteSerializer(serializers.Serializer):
    message = serializers.CharField()


class ChatRoomListSerializer(ChatRoomSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta(ChatRoomSerializer.Meta):
        fields = ChatRoomSerializer.Meta.fields + ("last_message",)
        read_only_fields = fields

    def get_last_message(self, obj: ChatRoom):
        messages = getattr(obj, "prefetched_messages", [])
        if messages:
            return MessageSerializer(messages[0]).data
        return None
