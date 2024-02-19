import asyncio
from chaturbate_api.client import ChaturbateAPIClient


async def main():
    client = ChaturbateAPIClient()
    async for event in client.get_formatted_events():
        print(event)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
