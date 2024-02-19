"""Module providing a low-level client for interacting with the Chaturbate events API."""

import aiohttp
import asyncio
import os
import re
from aiolimiter import AsyncLimiter


class CBApiClient:
    """
    A client for the Chaturbate events API.

    Args:
        url (str): The URL of the Chaturbate events API.
        limiter (aiolimiter.AsyncLimiter, optional): An async limiter to use for rate limiting API requests.

    Attributes:
        url (str): The URL of the Chaturbate events API.
        limiter (aiolimiter.AsyncLimiter): An async limiter to use for rate limiting API requests.
        formatters (dict): A dictionary of event formatters.
    """

    def __init__(self, url, limiter=None):
        """
        Initialize the client.

        Args:
            url (str): The URL of the Chaturbate events API.
            limiter (aiolimiter.AsyncLimiter, optional): An async limiter to use for rate limiting API requests.
        """

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
        """
        Create a client from the environment.

        Args:
            url (str, optional): The URL of the Chaturbate events API. If not provided, the URL will be read from the
                EVENTS_API_URL environment variable.

        Returns:
            CBApiClient: The client.
        """
        url = url or os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url)

    async def fetch_data(self, session, url, retry=0):
        """
        Fetch data from the API.

        Args:
            session (aiohttp.ClientSession): The aiohttp client session to use for the request.
            url (str): The URL of the API endpoint.
            retry (int, optional): The number of times the request has been retried.

        Returns:
            dict: The response data, or None if an error occurred.
        """

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
        """
        Fetch events from the API.

        Args:
            session (aiohttp.ClientSession): The aiohttp client session to use for the request.
            url (str): The URL of the API endpoint.

        Yields:
            dict: The next event from the API.
        """

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
        """
        Process an event from the API.

        Args:
            event (dict): The event data.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        method = event.get("method")
        event_object = event.get("object")
        if method and event_object:
            formatter = self.formatters.get(method)
            if formatter:
                return formatter(event_object)
        return None

    def format_broadcast_start_event(self, event_object):
        """
        Format a broadcast start event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        broadcaster = event_object.get("broadcaster")

        if broadcaster:
            return f"Broadcaster {broadcaster} started a broadcast"
        return None

    def format_broadcast_stop_event(self, event_object):
        """
        Format a broadcast stop event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        broadcaster = event_object.get("broadcaster")

        if broadcaster:
            return f"Broadcaster {broadcaster} stopped a broadcast"
        return None

    def format_chat_message_event(self, event_object):
        """
        Format a chat message event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a message '{message_info['message']}' in the channel of broadcaster {broadcaster}"
        return None

    def format_fanclub_join_event(self, event_object):
        """
        Format a fan club join event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} joined the fan club of broadcaster {broadcaster}"
        return None

    def format_follow_event(self, event_object):
        """
        Format a follow event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} followed broadcaster {broadcaster}"
        return None

    def format_media_purchase_event(self, event_object):
        """
        Format a media purchase event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        media_info = event_object.get("media")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if media_info and user_info and broadcaster:
            return f"User {user_info['username']} purchased media {media_info['name']} for {media_info['tokens']} tokens from broadcaster {broadcaster}"
        return None

    def format_private_message_event(self, event_object):
        """
        Format a private message event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a private message '{message_info['message']}' to broadcaster {broadcaster}"
        return None

    def format_room_subject_change_event(self, event_object):
        """
        Format a room subject change event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        subject_info = event_object.get("subject")
        broadcaster = event_object.get("broadcaster")

        if subject_info and broadcaster:
            return f"Broadcaster {broadcaster} changed the room subject to '{subject_info['subject']}'"
        return None

    def format_tip_event(self, event_object):
        """
        Format a tip event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

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
        """
        Format an unfollow event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} unfollowed broadcaster {broadcaster}"
        return None

    def format_user_enter_event(self, event_object):
        """
        Format a user enter event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} entered the channel of broadcaster {broadcaster}"
        return None

    def format_user_leave_event(self, event_object):
        """
        Format a user leave event.

        Args:
            event_object (dict): The event object.

        Returns:
            str: The formatted event, or None if the event could not be formatted.
        """

        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} left the channel of broadcaster {broadcaster}"
        return None

    async def get_formatted_events(self):
        """
        Get formatted events from the Chaturbate API.

        Yields:
            str: The next formatted event from the API.
        """

        async with aiohttp.ClientSession() as session:
            async for event in self.fetch_events(session, self.url):
                yield event
