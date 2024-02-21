import aiohttp
from aiolimiter import AsyncLimiter
from .event_handlers import (
    BroadcastStartEventHandler,
    BroadcastStopEventHandler,
    ChatMessageEventHandler,
    FanclubJoinEventHandler,
    FollowEventHandler,
    MediaPurchaseEventHandler,
    PrivateMessageEventHandler,
    RoomSubjectChangeEventHandler,
    TipEventHandler,
    UnfollowEventHandler,
    UserEnterEventHandler,
    UserLeaveEventHandler,
)

API_REQUEST_LIMIT = 2000
API_REQUEST_PERIOD = 60


event_handlers = {
    "broadcastStart": BroadcastStartEventHandler,
    "broadcastStop": BroadcastStopEventHandler,
    "userEnter": UserEnterEventHandler,
    "userLeave": UserLeaveEventHandler,
    "follow": FollowEventHandler,
    "unfollow": UnfollowEventHandler,
    "fanclubJoin": FanclubJoinEventHandler,
    "chatMessage": ChatMessageEventHandler,
    "privateMessage": PrivateMessageEventHandler,
    "tip": TipEventHandler,
    "roomSubjectChange": RoomSubjectChangeEventHandler,
    "mediaPurchase": MediaPurchaseEventHandler,
}


class ChaturbateAPIPoller:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_events(self, url):
        limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)
        async with limiter:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            json_response = await response.json()
                            await self.process_events(json_response)
                            next_url = json_response.get("nextUrl")
                            if next_url:
                                await self.get_events(next_url)
                        else:
                            print("Error:", response.status)
                except Exception as e:
                    print("Error:", e)

    async def process_events(self, json_response):
        for message in json_response.get("events", []):
            await self.process_event(message)

    async def process_event(self, message):
        method = message.get("method")
        handler_class = event_handlers.get(method)
        if handler_class:
            await handler_class().handle(message)
        else:
            print("Unknown method:", method)
