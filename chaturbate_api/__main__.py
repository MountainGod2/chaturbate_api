import asyncio
import os

from dotenv import load_dotenv

from chaturbate_api.src.api_poller import ChaturbateAPIPoller
from chaturbate_api.src.exceptions import BaseURLNotFound


async def main():
    """Main entry point of the application."""
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")

    # Check if the base URL is set and raise exception if not
    if base_url is None:
        raise BaseURLNotFound(
            "Base URL not found. Set the EVENTS_API_URL environment variable and try again."
        )

    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
