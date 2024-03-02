"""Module for the Chaturbate API client."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from aiolimiter import AsyncLimiter

from chaturbate_api.exceptions import BaseURLNotFound

from .constants import API_REQUEST_LIMIT, API_REQUEST_PERIOD
from .event_handlers import event_handlers

logger = logging.getLogger(__name__)


class ChaturbateAPIClient:
    """Chaturbate API Client.

    This class represents a client for retrieving events from the Chaturbate API.
    It provides methods to initialize the client, start the client, and handle events.

    Attributes
    ----------
        base_url (str): The base URL for the API.
        session (aiohttp.ClientSession): The aiohttp client session.
        event_handlers (Dict[str, Any]): A dictionary of event handlers.

    """

    def __init__(self, base_url: str, session, event_handlers) -> None:
        """Initialize the Chaturbate API client.

        Args:
        ----
            base_url (str): The base URL for the API.
            session (aiohttp.ClientSession): The aiohttp client session.
            event_handlers (Dict[str, Any]): A dictionary of event handlers.

        """
        self.base_url = base_url
        self.session = session
        self.event_handlers = event_handlers
        self.limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)

    async def run(self) -> None:
        """Start the client and continuously retrieve events from the API."""
        logger.debug(f"Base URL: {self.base_url}")

        if self.base_url is None:
            msg = "Base URL not found. Set the EVENTS_API_URL environment variable and try again."
            raise BaseURLNotFound(
                msg,
            )
        url = self.base_url

        while url:
            events, next_url = await self.get_events(
                url,
            )  # Adjust get_events to return next_url
            await self.process_events(events)
            url = next_url  # Update the URL for the next iteration

    async def get_events(self, url: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Get events from the Chaturbate API.

        Args:
        ----
            url (str): The URL to get events from.

        Returns:
        -------
            List[Dict[str, Any]]: List of events.
            str: The next URL to get events from.

        """
        if not url.startswith("https://events.testbed.cb.dev") and not url.startswith(
            "https://eventsapi.chaturbate.com",
        ):
            msg = "Invalid URL format"
            raise ValueError(msg)
        async with self.limiter:
            async with self.session.get(url) as response:
                if response.status == 200:
                    json_response = await response.json()
                    events = json_response.get("events", [])
                    next_url = json_response.get("nextUrl")
                    return events, next_url
                elif response.status == 404:
                    return []
                elif response.status >= 500:
                    asyncio.sleep(5)
                    return await self.get_events(url)
                else:
                    msg = f"Error: {response.status}"
                    raise ValueError(msg)
            return (
                [],
                None,
            )

    async def process_events(self, events: List[Dict[str, Any]]) -> None:
        """Process events from the Chaturbate API.

        Args:
        ----
            events (List[Dict[str, Any]]): List of events to process.

        Returns:
        -------
            None

        """
        for event in events:
            await self.process_event(event)

    async def process_event(self, event: Dict[str, Any]) -> None:
        """Process a single event.

        Args:
        ----
            event (Dict[str, Any]): The event to process.

        Returns:
        -------
            None

        """
        method = event.get("method")
        obj = event.get("object")
        handler_class = event_handlers.get(method)
        formatted_obj = json.dumps(obj, indent=4)

        logger.debug(f"Processing event: {method}\n{formatted_obj}")
        if handler_class:
            handler = handler_class()
            await handler.handle(event)
        else:
            logger.warning(f"Unknown method: {method}")
