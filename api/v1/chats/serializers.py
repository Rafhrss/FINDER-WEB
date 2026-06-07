from rest_framework import serializers

from apps.chats.models import ChatRoom, Message


class ChatParticipantSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()


class ChatRoomSerializer(serializers.ModelSerializer):
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
