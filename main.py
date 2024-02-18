import asyncio
import logging
from src.cbapi_client import CBApiClient


def configure_logging():
    logging.basicConfig(level=logging.INFO)  # Configure root logger


async def main():
    api_client = CBApiClient.from_env()
    async for event in api_client.get_formatted_events():
        print(event)


if __name__ == "__main__":
    asyncio.run(main())
