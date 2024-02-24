import asyncio
import os

from dotenv import load_dotenv

from chaturbate_api.api_poller import ChaturbateAPIPoller
from chaturbate_api.exceptions import BaseURLNotFound


async def main():
    """Main entry point of the application."""
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")

    # Check if the base URL is set
    if not base_url:
        raise BaseURLNotFound

    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except BaseURLNotFound:
        pass
