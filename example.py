"""
This is an example of how to use the Chaturbate API client.
"""

import asyncio
from chaturbate_api.client import ChaturbateAPIClient


async def main():
    # Create a client (optionally passing the URL of the Chaturbate events API)
    client = ChaturbateAPIClient()

    # Get formatted events from the API and print them
    async for event in client.get_formatted_events():
        print(event)


if __name__ == "__main__":
    try:
        # Run the main coroutine
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
