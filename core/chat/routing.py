from django.urls import re_path
from . import consumers
from .consumers import GroupChatConsumer

websocket_urlpatterns = [

    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/group/(?P<group_id>\w+)/$', GroupChatConsumer.as_asgi())

]