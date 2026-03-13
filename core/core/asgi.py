import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat.routing
from chat.routing import websocket_urlpatterns as chat_ws
from groups.routing import websocket_urlpatterns as group_ws

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter(
{
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
}
)

application = ProtocolTypeRouter({

    "http": get_asgi_application(),

    "websocket": URLRouter(
        chat_ws + group_ws
    ),

})