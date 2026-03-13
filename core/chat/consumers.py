import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message
from users.models import UserProfile
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
import json


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):


# connect to WebSocket
    async def connect(self):

        user = self.scope["user"]

        await sync_to_async(
            UserProfile.objects.filter(user=user).update
        )(is_online=True)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

# disconnect from WebSocket
    async def disconnect(self, close_code):

        user = self.scope["user"]

        await sync_to_async(
            UserProfile.objects.filter(user=user).update
        )(
            is_online=False,
            last_seen=timezone.now()
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

async def receive(self, text_data):

    data = json.loads(text_data)

    event_type = data.get("type", "message")

    if event_type == "typing":

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "typing_event",
                "sender": data["sender"]
            }
        )

    else:

        message = data["message"]
        sender_id = data["sender"]
        receiver_id = data["receiver"]

        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)

        msg = await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message,
            status="sent"
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "status": "sent"
            }
        )
    async def chat_message(self, event):

        message = event["message"]
        sender = event["sender"]
        message_id = event["message_id"]
        status = event["status"]

        # update message status to delivered
        await sync_to_async(Message.objects.filter(id=message_id).update)(
            status="delivered"
        )

        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "message_id": message_id,
            "status": "delivered"
        }))


async def typing_event(self, event):

    sender = event["sender"]

    await self.send(text_data=json.dumps({
        "type": "typing",
        "sender": sender
    }))
    
    
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
        sender = data["sender"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender
            }
        )


    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))


    async def group_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))