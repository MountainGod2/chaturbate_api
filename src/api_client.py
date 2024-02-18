import aiohttp
from aiolimiter import AsyncLimiter
import logging
import os
from dotenv import load_dotenv
from .formatter import Formatter
from .exceptions import FetchDataError
import asyncio

load_dotenv()


class CBApiClient:
    def __init__(self, url: str):
        self.url = url
        self.logger = self._setup_logger()
        self.limiter = AsyncLimiter(1000, 60)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    async def fetch_data(
        self, session: aiohttp.ClientSession, url: str, retry: int = 0
    ) -> dict:
        """Fetch data from the API."""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status >= 500:
                    self.logger.error(f"Server error: {response.status}, retrying...")
                    await asyncio.sleep(2**retry)  # Exponential backoff
                    return await self.fetch_data(session, url, retry + 1)
                else:
                    self.logger.error(f"Error fetching data: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            self.logger.error(f"An error occurred: {e}")
            raise FetchDataError("Error fetching data from API") from e

    async def fetch_events(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Fetch events from the API.

        Args:
            session (aiohttp.ClientSession): The aiohttp client session.
            url (str): The URL to fetch events from.
        """
        try:
            while True:
                data = await self.fetch_data(session, url)
                if data is None:
                    break

                self.process_events(data)

                next_url = data.get("nextUrl")
                if not next_url:
                    self.logger.info("No next URL found. Exiting.")
                    break

                url = next_url

        except aiohttp.ClientError as e:
            self.logger.error(f"An error occurred: {e}")

    def process_event(self, event: dict) -> None:
        method = event.get("method")
        event_object = event.get("object")
        self.logger.debug(f"Processing event: {method}, {event_object}")
        if method and event_object:
            formatter_func = getattr(Formatter(), f"format_{method}_event", None)
            if formatter_func:
                formatted_event = formatter_func(event_object)
                if formatted_event:
                    self.logger.info(formatted_event)
                else:
                    self.logger.warning(
                        f"Failed to format event: {method}, {event_object}"
                    )
            else:
                self.logger.warning(f"No formatter found for method: {method}")

    async def run(self) -> None:
        async with aiohttp.ClientSession() as session:
            await self.fetch_events(session, self.url)

    @classmethod
    def from_env(cls) -> "CBApiClient":
        url = os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url)
