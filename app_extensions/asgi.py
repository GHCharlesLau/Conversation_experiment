# asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# 如果你有自定义 websocket 路由：
from routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")  # 或 otree.settings
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # ✅ 加上 HTTP 支持
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),  # 可选
})
