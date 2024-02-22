"""Main module for running the Chaturbate API poller."""
import os

from dotenv import load_dotenv
from poller import ChaturbateAPIPoller


async def main():
    """Main entry point of the application."""
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")
    if not base_url:
        raise ValueError("EVENTS_API_URL not set in .env file")
    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()
