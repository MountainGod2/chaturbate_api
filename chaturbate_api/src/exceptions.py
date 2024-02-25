"""This module contains the custom exceptions for the Chaturbate API client."""


class BaseURLNotFound(Exception):
    """Raised when the base URL of the events API is not found in the environment variables."""

    pass
