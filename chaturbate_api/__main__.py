import asyncio
import os

from dotenv import load_dotenv

from chaturbate_api.api_poller import ChaturbateAPIPoller


async def main():
    """Main entry point of the application."""
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")
    if not base_url:
        print(
            "You can get the URL from the Chatubate settings here: https://chaturbate.com/statsapi/authtoken/"
        )
        print()
        print("Set the URL in the .env file like this:")
        print("EVENTS_API_URL=https://chaturbate.com/api/v1/events/")
        print("Then run the poller again.")
        print()
        raise ValueError("EVENTS_API_URL not set in .env file")
    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
