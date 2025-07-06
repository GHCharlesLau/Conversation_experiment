import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from otree.channels import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": consumers.WebSocketEndpoint, 
})
