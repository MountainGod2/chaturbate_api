import json
import logging
from typing import Any, Dict, List

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

    async def get_events(self, url: str) -> List[Dict[str, Any]]:
        """
        Get events from the Chaturbate API.

        Args:
            url (str): The URL to fetch events from.

        Returns:
            List[Dict[str, Any]]: List of event dictionaries.

        Raises:
            ValueError: If the URL format is invalid.
            aiohttp.ClientError: If there is an error with the HTTP request.
        """
        if not url.startswith("https://events.testbed.cb.dev") and not url.startswith(
            "https://eventsapi.chaturbate.com"
        ):
            raise ValueError("Invalid URL format")
        limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)
        try:
            async with limiter, aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        json_response = await response.json()
                        events = json_response.get("events", [])
                        return events
                    elif response.status == 404:
                        return []
                    elif response.status >= 500:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                        )
                    else:
                        raise ValueError(f"Error: {response.status}")
        except aiohttp.ClientError as e:
            raise e

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
            event_data = await handler_class().handle(message)
            print(json.dumps(event_data))
        else:
            logger.warning("Unknown method: %s", method)
