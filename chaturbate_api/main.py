import asyncio
import os

import dotenv

from src.poller import ChaturbateAPIPoller

# Load environment variables
dotenv.load_dotenv()

# Get the base URL from the environment
BASE_URL = os.getenv("EVENTS_API_URL")


async def main():
    # Create a poller and get events
    poller = ChaturbateAPIPoller(BASE_URL)
    await poller.get_events(BASE_URL)


if __name__ == "__main__":
    asyncio.run(main())
