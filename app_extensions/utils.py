from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def live_send_cross_dyno(group_id: str, message: dict):
    """
    向某个玩家组（通过 WebSocket) 跨 dyno 发送消息。

    参数：
    - group_id: 你定义的 Redis WebSocket 消费者 group 名（例如 'group_1')
    - message: 传输的数据内容（必须为 dict)
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"group_{group_id}",
        {
            "type": "group.message",
            "message": message
        }
    )
