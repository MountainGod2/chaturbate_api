"""Package providing a client for the Chaturbate events API."""

# Import submodules
from .client import ChaturbateAPIClient
from .exceptions import ChaturbateAPIError, APICallError, AuthenticationError

__all__ = [
    "ChaturbateAPIClient",
    "ChaturbateAPIError",
    "APICallError",
    "AuthenticationError",
]
