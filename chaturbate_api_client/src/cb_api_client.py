import aiohttp
from aiolimiter import AsyncLimiter
import asyncio
import re
import os


class CBApiClient:
    def __init__(self, url, limiter=None):
        self.url = url
        self.limiter = limiter or AsyncLimiter(1000, 60)
        self.formatters = {
            "tip": self.format_tip_event,
            "userLeave": self.format_user_leave_event,
            "userEnter": self.format_user_enter_event,
            "chatMessage": self.format_chat_message_event,
            "unfollow": self.format_unfollow_event,
            "follow": self.format_follow_event,
        }

    async def fetch_data(self, session, url, retry=0):
        async with self.limiter:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status >= 500:
                        await asyncio.sleep(2**retry)  # Exponential backoff
                        return await self.fetch_data(session, url, retry + 1)
                    else:
                        return None
            except aiohttp.ClientError:
                return None

    async def fetch_events(self, session, url):
        try:
            while True:
                data = await self.fetch_data(session, url)
                if data is None:
                    break

                events = data.get("events")
                if events:
                    for event in events:
                        yield self.process_event(event)

                next_url = data.get("nextUrl")
                if not next_url:
                    break

                url = next_url

        except aiohttp.ClientError:
            pass

    def process_event(self, event):
        method = event.get("method")
        event_object = event.get("object")
        if method and event_object:
            formatter = self.formatters.get(method)
            if formatter:
                return formatter(event_object)
        return None

    @staticmethod
    def format_tip_event(event_object):
        tip_info = event_object.get("tip")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if tip_info and user_info and broadcaster:
            message = tip_info.get("message", "")
            message = re.sub(r"^\s*\|\s*", "", message)
            message_str = f" with message: '{message}'" if message else ""
            return f"User {user_info['username']} tipped {tip_info['tokens']} tokens to broadcaster {broadcaster}{message_str}"
        return None

    @staticmethod
    def format_user_leave_event(event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} left the channel of broadcaster {broadcaster}"
        return None

    @staticmethod
    def format_user_enter_event(event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} entered the channel of broadcaster {broadcaster}"
        return None

    @staticmethod
    def format_chat_message_event(event_object):
        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a message '{message_info['message']}' in the channel of broadcaster {broadcaster}"
        return None

    @staticmethod
    def format_unfollow_event(event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} unfollowed broadcaster {broadcaster}"
        return None

    @staticmethod
    def format_follow_event(event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} followed broadcaster {broadcaster}"
        return None

    @classmethod
    def from_env(cls):
        url = os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url)

    async def get_formatted_events(self):
        async with aiohttp.ClientSession() as session:
            async for event in self.fetch_events(session, self.url):
                yield event
