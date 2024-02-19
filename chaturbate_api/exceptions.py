"""Module defining custom exceptions for the Chaturbate API client."""


class ChaturbateAPIError(Exception):
    """Base class for Chaturbate API errors."""


class APICallError(ChaturbateAPIError):
    """Error raised when there is an issue with API calls."""


class AuthenticationError(ChaturbateAPIError):
    """Error raised when authentication fails."""
