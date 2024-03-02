"""Entry point for the Chaturbate API client."""

import asyncio
import logging
import sys

import aiohttp

from chaturbate_api.client import ChaturbateAPIClient
from chaturbate_api.config.config import EVENTS_API_URL
from chaturbate_api.event_handlers import event_handlers
from chaturbate_api.exceptions import BaseURLNotFound

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


async def main() -> None:
    """Run the main coroutine for the Chaturbate API client.

    Raises
    ------
        BaseURLNotFound: If BASE_URL is None.

    Returns
    -------
        None

    """
    # Ensure BASE_URL is not None
    if EVENTS_API_URL is None:
        raise BaseURLNotFound

    # Initialize aiohttp session
    async with aiohttp.ClientSession() as session:
        # Initialize the Chaturbate API client with the base URL,
        # session, and event handlers
        client = ChaturbateAPIClient(
            base_url=EVENTS_API_URL,
            session=session,
            event_handlers=event_handlers,
        )

        try:
            # Start the client to continuously retrieve and process events
            await client.run()
        except Exception:
            logging.exception("An error occurred")
            sys.exit(1)


if __name__ == "__main__":
    # Run the main coroutine
    asyncio.run(main())
