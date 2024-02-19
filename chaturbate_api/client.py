# chaturbate_api/client.py

from .api_client import CBApiClient
from .exceptions import ChaturbateAPIError, APICallError, AuthenticationError


class ChaturbateAPIClient:
    def __init__(self, url=None):
        self.api_client = CBApiClient.from_env(url)

    def get_formatted_events(self):
        try:
            return self.api_client.get_formatted_events()
        except APICallError as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
        except AuthenticationError as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
        except Exception as e:
            raise ChaturbateAPIError(f"An error occurred: {e}")
