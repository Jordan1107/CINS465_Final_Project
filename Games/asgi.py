"""
ASGI config for Games project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from chess.consumers import GameRoom
from django.core.asgi import get_asgi_application
from django.urls import path
import chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Games.settings')
django.setup()

application = get_asgi_application()

WebSocket_pattern = [
        path('ws/game/<room_code>' , GameRoom)
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket':AuthMiddlewareStack(URLRouter(
            WebSocket_pattern
        )),
    }
)
