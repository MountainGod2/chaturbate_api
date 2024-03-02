"""This module contains the custom exceptions for the Chaturbate API client."""


class BaseURLNotFound(Exception):
    """Raised when the base URL of the events API is not found in the environment variables."""

    def __init__(self) -> None:
        super().__init__(
            "Base URL not found. Set the EVENTS_API_URL environment variable and try again.",
        )
