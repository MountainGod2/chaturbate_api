import asyncio
from chaturbate_api import ChaturbateAPIClient, ChaturbateAPIError


async def main():
    client = ChaturbateAPIClient()
    try:
        async for event in client.get_formatted_events():
            print(event)
    except ChaturbateAPIError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
