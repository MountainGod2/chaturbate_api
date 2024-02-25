import asyncio
import json
import logging
from typing import Any, Dict

import aiohttp
from aiolimiter import AsyncLimiter

from .constants import API_REQUEST_LIMIT, API_REQUEST_PERIOD
from .event_handlers import event_handlers

logger = logging.getLogger(__name__)


class ChaturbateAPIPoller:
    """Chaturbate API Poller."""

    def __init__(self, base_url: str) -> None:
        """Initialize the poller with the base URL."""
        self.base_url = base_url

    async def run(self) -> None:
        """Start the poller."""
        url = self.base_url
        while url:
            url = await self.get_events(url)

    async def get_events(self, url: str) -> str:
        """Get events from the Chaturbate API."""
        if not url.startswith("https://events.testbed.cb.dev") and not url.startswith(
            "https://eventsapi.chaturbate.com"
        ):
            raise ValueError("Invalid URL format")

        limiter = AsyncLimiter(API_REQUEST_LIMIT, API_REQUEST_PERIOD)
        async with limiter, aiohttp.ClientSession() as session:
            try:
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
            except aiohttp.ClientError as e:
                logger.error(f"Error: {e}")
            except Exception:
                logger.exception("An unexpected error occurred")

        return url

    async def process_events(self, json_response: Dict[str, Any]) -> None:
        """Process events from the Chaturbate API."""
        for message in json_response.get("events", []):
            await self.process_event(message)

    async def process_event(self, message: Dict[str, Any]) -> None:
        """Process a single event."""
        method = message.get("method")
        handler_class = event_handlers.get(method)
        if handler_class:
            await handler_class().handle(message)
        else:
            logger.warning("Unknown method: %s", method)

    async def handle_server_error(self, status_code: int) -> None:
        """Handle server errors."""
        logger.error(f"Server error: {status_code}, retrying in 5 seconds")
        await asyncio.sleep(5)
