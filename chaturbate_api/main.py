import asyncio
import os

from dotenv import load_dotenv
from .src.poller import ChaturbateAPIPoller


async def main():
    """Main entry point of the application"""

    # Load environment variables
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")

    # Check if EVENTS_API_URL is set
    if not base_url:
        print("EVENTS_API_URL not set in .env file")
        return

    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()


if __name__ == "__main__":
    asyncio.run(main())
