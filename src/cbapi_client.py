import aiohttp
from aiolimiter import AsyncLimiter
import logging
import asyncio
import re
import os


class CBApiClient:
    def __init__(self, url, limiter=None, logger=None):
        self.url = url
        self.logger = logger or logging.getLogger(__name__)
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
                        self.logger.error(
                            f"Server error: {response.status}, retrying..."
                        )
                        await asyncio.sleep(2**retry)  # Exponential backoff
                        return await self.fetch_data(session, url, retry + 1)
                    else:
                        self.logger.error(f"Error fetching data: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                self.logger.error(f"An error occurred: {e}")
                return None

    async def fetch_events(self, session, url):
        try:
            while True:
                data = await self.fetch_data(session, url)
                if data is None:
                    break

                events = data.get("events")
                if events:
                    self.logger.debug(f"Received events: {events}")

                    for event in events:
                        self.process_event(event)

                next_url = data.get("nextUrl")
                if not next_url:
                    self.logger.info("No next URL found. Exiting.")
                    break

                url = next_url

        except aiohttp.ClientError as e:
            self.logger.error(f"An error occurred: {e}")

    def process_event(self, event):
        method = event.get("method")
        event_object = event.get("object")
        self.logger.debug(f"Processing event: {method}, {event_object}")
        if method and event_object:
            formatter = self.formatters.get(method)
            if formatter:
                self.logger.debug(f"Calling formatter method for: {method}")
                formatted_message = formatter(event_object)
                if formatted_message:
                    self.logger.info(formatted_message)
                else:
                    self.logger.warning(f"No formatted message for method: {method}")
            else:
                self.logger.warning(f"No formatter found for method: {method}")

    @staticmethod
    def format_tip_event(event_object):
        tip_info = event_object.get("tip")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if tip_info and user_info and broadcaster:
            message = tip_info.get("message", "")

            # Use regular expressions to remove the prefix and trim spaces around the pipe symbol
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
    def from_env(cls, logger=None):
        url = os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url, logger=logger)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.fetch_events(session, self.url)
