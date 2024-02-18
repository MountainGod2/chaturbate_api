import aiohttp
import asyncio
from aiolimiter import AsyncLimiter
import logging
import os
from dotenv import load_dotenv
from formatter import (
    format_tip_event,
    format_user_leave_event,
    format_user_enter_event,
    format_chat_message_event,
    format_unfollow_event,
    format_follow_event,
)

load_dotenv()


class CBApiClient:
    def __init__(self, url):
        self.url = url
        self.logger = self._setup_logger()
        self.limiter = AsyncLimiter(1000, 60)
        self.formatters = {
            "tip": format_tip_event,
            "userLeave": format_user_leave_event,
            "userEnter": format_user_enter_event,
            "chatMessage": format_chat_message_event,
            "unfollow": format_unfollow_event,
            "follow": format_follow_event,
        }

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    async def fetch_data(self, session, url, retry=0):
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

    async def fetch_events(self, session, url):
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

    def process_event(self, event):
        method = event.get("method")
        event_object = event.get("object")
        self.logger.debug(f"Processing event: {method}, {event_object}")
        if method and event_object:
            formatter = self.formatters.get(method)
            if formatter:
                self.logger.debug(f"Calling formatter method for: {method}")
                formatted_message = formatter(event_object)
                if formatted_message:
                    self.logger.info(formatted_message)
                else:
                    self.logger.warning(f"No formatted message for method: {method}")
            else:
                self.logger.warning(f"No formatter found for method: {method}")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            await self.fetch_events(session, self.url)

    @classmethod
    def from_env(cls):
        url = os.getenv("EVENTS_API_URL")
        if not url:
            raise ValueError("The EVENTS_API_URL environment variable is not set.")
        return cls(url)


def main():
    cb_api_client = CBApiClient.from_env()
    try:
        asyncio.run(cb_api_client.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
