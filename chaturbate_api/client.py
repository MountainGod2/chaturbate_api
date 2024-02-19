"""
A client for the Chaturbate API.
"""

from .api_client import CBApiClient
from .exceptions import ChaturbateAPIError, APICallError, AuthenticationError


class ChaturbateAPIClient:
    """
    A client for the Chaturbate API.

    Args:
        url (str, optional): The URL of the Chaturbate events API. If not provided, the URL will be read from the
            EVENTS_API_URL environment variable.

    Attributes:
        api_client (CBApiClient): The underlying API client.
    """

    def __init__(self, url=None):
        """
        Initialize the client.

        Args:
            url (str, optional): The URL of the Chaturbate events API. If not provided, the URL will be read from the
                EVENTS_API_URL environment variable.
        """

        self.api_client = CBApiClient.from_env(url)

    def get_formatted_events(self):
        """
        Get formatted events from the Chaturbate API.

        Yields:
            dict: The next formatted event from the API.

        Raises:
            ChaturbateAPIError: An error occurred.
        """

        try:
            return self.api_client.get_formatted_events()
        except APICallError as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
        except AuthenticationError as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
        except Exception as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
