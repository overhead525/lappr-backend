import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SocketsConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = "default_room"
        self.room_group_name = f'sockets_{self.room_name}'

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sockets_message',
                'message': message
            }
        )

    async def sockets_message(self, event):
        message = event['message']
        print(f'{self.scope}')

        await self.send(text_data=json.dumps({
            'message': message
        }))
