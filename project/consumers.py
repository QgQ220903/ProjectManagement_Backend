import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "projects"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "fetch":
            await self.send_projects()

    async def project_update(self, event):
        await self.send(text_data=json.dumps({"type": "update"}))

    async def send_projects(self):
        await self.send(text_data=json.dumps({"type": "update"}))

