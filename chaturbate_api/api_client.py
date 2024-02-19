# chaturbate_api/api_client.py

import aiohttp
import asyncio
import os
import re
from aiolimiter import AsyncLimiter


class CBApiClient:
    def __init__(self, url, limiter=None):
        self.url = url
        self.limiter = limiter or AsyncLimiter(1000, 60)
        self.formatters = {
            "broadcastStart": self.format_broadcast_start_event,
            "broadcastStop": self.format_broadcast_stop_event,
            "chatMessage": self.format_chat_message_event,
            "fanclubJoin": self.format_fanclub_join_event,
            "follow": self.format_follow_event,
            "mediaPurchase": self.format_media_purchase_event,
            "privateMessage": self.format_private_message_event,
            "roomSubjectChange": self.format_room_subject_change_event,
            "tip": self.format_tip_event,
            "unfollow": self.format_unfollow_event,
            "userEnter": self.format_user_enter_event,
            "userLeave": self.format_user_leave_event,
        }

    @classmethod
    def from_env(cls, url=None):
        url = url or os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url)

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

    def format_broadcast_start_event(self, event_object):
        broadcaster = event_object.get("broadcaster")

        if broadcaster:
            return f"Broadcaster {broadcaster} started a broadcast"
        return None

    def format_broadcast_stop_event(self, event_object):
        broadcaster = event_object.get("broadcaster")

        if broadcaster:
            return f"Broadcaster {broadcaster} stopped a broadcast"
        return None

    def format_chat_message_event(self, event_object):
        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a message '{message_info['message']}' in the channel of broadcaster {broadcaster}"
        return None

    def format_fanclub_join_event(self, event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} joined the fan club of broadcaster {broadcaster}"
        return None

    def format_follow_event(self, event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} followed broadcaster {broadcaster}"
        return None

    def format_media_purchase_event(self, event_object):
        media_info = event_object.get("media")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if media_info and user_info and broadcaster:
            return f"User {user_info['username']} purchased media {media_info['name']} for {media_info['tokens']} tokens from broadcaster {broadcaster}"
        return None

    def format_private_message_event(self, event_object):
        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a private message '{message_info['message']}' to broadcaster {broadcaster}"
        return None

    def format_room_subject_change_event(self, event_object):
        subject_info = event_object.get("subject")
        broadcaster = event_object.get("broadcaster")

        if subject_info and broadcaster:
            return f"Broadcaster {broadcaster} changed the room subject to '{subject_info['subject']}'"
        return None

    def format_tip_event(self, event_object):
        tip_info = event_object.get("tip")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if tip_info and user_info and broadcaster:
            message = tip_info.get("message", "")
            message = re.sub(r"^\s*\|\s*", "", message)
            message_str = f" with message: '{message}'" if message else ""
            return f"User {user_info['username']} tipped {tip_info['tokens']} tokens to broadcaster {broadcaster}{message_str}"
        return None

    def format_unfollow_event(self, event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} unfollowed broadcaster {broadcaster}"
        return None

    def format_user_enter_event(self, event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} entered the channel of broadcaster {broadcaster}"
        return None

    def format_user_leave_event(self, event_object):
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} left the channel of broadcaster {broadcaster}"
        return None

    async def get_formatted_events(self):
        async with aiohttp.ClientSession() as session:
            async for event in self.fetch_events(session, self.url):
                yield event
