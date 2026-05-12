from channels.generic.websocket import AsyncJsonWebsocketConsumer


class GraphQLWSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        if content.get("type") == "connection_init":
            await self.send_json({"type": "connection_ack"})

    async def send_notification(self, event):
        await self.send_json({
            "type": "data",
            "id": "1",
            "payload": {
                "data": {
                    # CAMELCASE — EXACT MATCH TO SUBSCRIPTION FIELD
                    "retrieveNewNotifications": event["notification"]
                }
            }
        })