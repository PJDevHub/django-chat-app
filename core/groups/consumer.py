import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import GroupMessage, Group
from django.contrib.auth.models import User


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.room_group_name = f"group_{self.group_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data["message"]
        sender_id = data["sender"]

        sender = await self.get_user(sender_id)

        # SAVE MESSAGE
        await self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "group_message",
                "message": message,
                "sender": sender.username
            }
        )


    async def group_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))


    @database_sync_to_async
    def save_message(self, sender, message):

        group = Group.objects.get(id=self.group_id)

        GroupMessage.objects.create(
            group=group,
            sender=sender,
            message=message
        )


    @database_sync_to_async
    def get_user(self, user_id):

        return User.objects.get(id=user_id)
    