import json
from channels .generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """What to do when someone connects to this chatroom."""
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.channel_layer.accept()
        
        # Send a message to the group
        await self.channel_layer.group_send(self.room_group_name, {'type': 'test_message', 'tester': 'Welcome!'})

    async def test_message(self, event):
        tester = event['tester']
        await self.send(text_data=json.dumps({'tester': tester}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
