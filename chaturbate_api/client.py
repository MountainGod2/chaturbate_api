"""Module for the Chaturbate API client."""

import logging
import os
from typing import Any, Dict, List

import aiohttp
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv

from chaturbate_api.exceptions import BaseURLNotFound

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

    def __init__(self) -> None:
        """
        Initialize the client with the base URL.

        Args:
            base_url (str): The base URL for the API.

        Returns:
            None
        """
        self.base_url = os.getenv("EVENTS_API_URL")

    async def run(self) -> None:
        """
        Start the client and continuously retrieve events from the API.
        """
        load_dotenv()
        logger.debug("Environment variables loaded.")
        logger.debug(f"Base URL: {self.base_url}")

        if self.base_url is None:
            raise BaseURLNotFound(
                "Base URL not found. Set the EVENTS_API_URL environment variable and try again."
            )
        url = self.base_url

        while url:
            events, next_url = await self.get_events(
                url
            )  # Adjust get_events to return next_url
            await self.process_events(events)
            url = next_url  # Update the URL for the next iteration

    async def get_events(self, url: str) -> (List[Dict[str, Any]], str):
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
        async with limiter, aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    json_response = await response.json()
                    events = json_response.get("events", [])
                    next_url = json_response.get(
                        "nextUrl"
                    )  # Hypothetical field containing the next URL
                    return events, next_url
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
        return [], None  # Return an empty list and None if no more events or on error

    async def process_events(self, events: List[Dict[str, Any]]) -> None:
        """
        Process events from the Chaturbate API.

        Args:
            events (List[Dict[str, Any]]): List of events to process.

        Returns:
            None
        """
        for event in events:
            await self.process_event(event)

    async def process_event(self, event: Dict[str, Any]) -> None:
        """
        Process a single event.

        Args:
            event (Dict[str, Any]): The event to process.

        Returns:
            None
        """
        method = event.get("method")
        handler_class = event_handlers.get(method)
        logger.debug(f"Processing event: {event}")
        if handler_class:
            handler = handler_class()
            await handler.handle(event)
        else:
            logger.warning(f"Unknown method: {method}")
