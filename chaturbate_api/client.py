"""Module defining the Chaturbate API client."""

from .api_client import CBApiClient
from .exceptions import ChaturbateAPIError, APICallError, AuthenticationError


class ChaturbateAPIClient:
    """Client for interacting with the Chaturbate API."""

    def __init__(self, url=None):
        """
        Initialize the client.

        Args:
            url (str, optional): The URL of the Chaturbate events API. If not provided, the URL will be read from the
                EVENTS_API_URL environment variable.
        """
        self.api_client = CBApiClient.from_env(url)

    async def get_formatted_events(self):
        """
        Get formatted events from the Chaturbate API.

        Yields:
            str: The next formatted event from the API.

        Raises:
            ChaturbateAPIError: An error occurred during API interaction.
        """
        try:
            async with self.api_client.get_formatted_events() as events:
                async for event in events:
                    yield event
        except (APICallError, AuthenticationError) as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
