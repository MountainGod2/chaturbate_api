import asyncio
from src.cbapi_client import CBApiClient


async def main():
    api_client = CBApiClient.from_env()
    async for event in api_client.get_formatted_events():
        print(event)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
