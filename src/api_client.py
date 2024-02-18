import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
import logging
import os
from dotenv import load_dotenv
from . import formatter

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
        async with self.limiter:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status >= 500:
                        self.logger.error(
                            f"Server error: {response.status}, retrying..."
                        )
                        await asyncio.sleep(2**retry)  # Exponential backoff
                        return await self.fetch_data(session, url, retry + 1)
                    else:
                        self.logger.error(f"Error fetching data: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                self.logger.error(f"An error occurred: {e}")
                return None

    async def fetch_events(self, session: aiohttp.ClientSession, url: str) -> None:
        try:
            while True:
                data = await self.fetch_data(session, url)
                if data is None:
                    break

                events = data.get("events")
                if events:
                    self.logger.debug(f"Received events: {events}")

                    for event in events:
                        self.process_event(event)

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
            formatter_func = getattr(formatter, f"format_{method}_event", None)
            if formatter_func:
                self.logger.debug(f"Calling formatter method for: {method}")
                formatted_message = formatter_func(event_object)
                if formatted_message:
                    self.logger.info(formatted_message)
                else:
                    self.logger.warning(f"No formatted message for method: {method}")
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


def main() -> None:
    cb_api_client = CBApiClient.from_env()
    try:
        asyncio.run(cb_api_client.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
