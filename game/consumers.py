import time
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket 연결 시도")
        self.group_name = 'some_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("WebSocket 연결 성공")
        
    async def disconnect(self, close_code):
        print(f"WebSocket 연결 종료, 코드: {close_code}")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))