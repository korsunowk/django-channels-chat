from chat.consumers import ws_add, ws_disconnect
from chat.consumers import ws_message

from channels.routing import route

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
