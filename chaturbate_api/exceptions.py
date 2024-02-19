class ChaturbateAPIError(Exception):
    """Base class for Chaturbate API errors."""

    pass


class APICallError(ChaturbateAPIError):
    """Error raised when there is an issue with API calls."""

    pass


class AuthenticationError(ChaturbateAPIError):
    """Error raised when authentication fails."""

    pass
