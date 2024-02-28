import asyncio
import json
import logging
from typing import Any, Dict

import aiohttp
from aiolimiter import AsyncLimiter

from .constants import API_REQUEST_LIMIT, API_REQUEST_PERIOD
from .event_handlers import event_handlers

logger = logging.getLogger(__name__)


class ChaturbateAPIClient:
    """
    Chaturbate API Client.

    This class represents a client for retrieving events from the Chaturbate API.
    It provides methods to initialize the client, start the client, and handle events.

    Attributes:
        base_url (str): The base URL for the API.

    """

    def __init__(self, base_url: str) -> None:
        """
        Initialize the client with the base URL.

        Args:
            base_url (str): The base URL for the API.

        Returns:
            None
        """
        self.base_url = base_url

    async def run(self) -> None:
        """
        Start the client.

        This method starts the client and continuously retrieves events from the specified URL.

        Returns:
            None
        """
        url = self.base_url
        while url:
            url = await self.get_events(url)

    async def get_events(self, url: str) -> str:
        """
        Get events from the Chaturbate API.

        Args:
            url (str): The URL to fetch events from.

        Returns:
            str: The next URL to fetch events from.

        Raises:
            ValueError: If the URL format is invalid.
        """
        if not url.startswith("https://events.testbed.cb.dev") and not url.startswith(
            "https://eventsapi.chaturbate.com"
        ):
            raise ValueError("Invalid URL format")

        limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)
        retry_count = 5
        while retry_count > 0:
            try:
                async with limiter, aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            try:
                                json_response = await response.json()
                                await self.process_events(json_response)
                                url = json_response.get("nextUrl")
                            except json.JSONDecodeError as e:
                                logger.error(f"Error decoding JSON response: {e}")
                        elif response.status == 404:
                            url = None
                        elif response.status >= 500:
                            await self.handle_server_error(response.status)
                        else:
                            raise ValueError(f"Error: {response.status}")
                break
            except aiohttp.ClientError as e:
                logger.error(f"Error: {e}")
                retry_count -= 1
                if retry_count == 0:
                    logger.error("Max retry attempts reached. Exiting.")
                    raise
                logger.info(f"Retrying request. Attempts left: {retry_count}")
                await asyncio.sleep(5)

        return url

    async def process_events(self, json_response: Dict[str, Any]) -> None:
        """
        Process events from the Chaturbate API.

        Args:
            json_response (Dict[str, Any]): The JSON response containing the events.

        Returns:
            None
        """
        for message in json_response.get("events", []):
            await self.process_event(message)

    async def process_event(self, message: Dict[str, Any]) -> None:
        """
        Process a single event.

        Args:
            message (Dict[str, Any]): The event message to be processed.

        Returns:
            None

        """
        method = message.get("method")
        handler_class = event_handlers.get(method)
        if handler_class:
            await handler_class().handle(message)
        else:
            logger.warning("Unknown method: %s", method)

    async def handle_server_error(self, status_code: int) -> None:
        """
        Handle server errors.

        Args:
            status_code (int): The HTTP status code indicating the server error.

        Returns:
            None

        """
        logger.error(f"Server error: {status_code}, retrying in 5 seconds")
        await asyncio.sleep(5)
