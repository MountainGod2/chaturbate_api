import asyncio

import aiohttp
from aiolimiter import AsyncLimiter

from .event_handlers import event_handlers

API_REQUEST_LIMIT = 2000
API_REQUEST_PERIOD = 60


class ChaturbateAPIPoller:
    """Chaturbate API Poller"""

    def __init__(self, base_url) -> None:
        self.base_url = base_url

    async def run(self) -> None:
        """Start the poller"""
        url = self.base_url
        while url:
            url = await self.get_events(url)

    async def get_events(self, url) -> str:
        """
        Get events from the Chaturbate API
        :param url: URL to get events from
        :return: URL to the next page of events
        """
        limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)
        async with limiter, aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        json_response = await response.json()
                        await self.process_events(json_response)
                        url = json_response.get("nextUrl")
                    if response.status == 404:
                        url = None
                    if response.status >= 500:
                        # Retry on server errors
                        print(f"Error: {response.status}, retrying in 5 seconds")
                        await asyncio.sleep(5)
                    else:
                        raise ValueError(f"Error: {response.status}")
            except aiohttp.ClientError as e:
                raise ValueError(f"Error: {e}")

        return url

    async def process_events(self, json_response) -> None:
        """
        Process events from the Chaturbate API
        :param json_response: JSON response from the API
        """
        for message in json_response.get("events", []):
            await self.process_event(message)

    async def process_event(self, message) -> None:
        """
        Process a single event
        :param message: Event message
        """
        method = message.get("method")
        handler_class = event_handlers.get(method)
        if handler_class:
            await handler_class().handle(message)
        else:
            print("Unknown method:", method)
