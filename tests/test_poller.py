"""Test cases for Chaturbate API Poller."""
import unittest
from unittest.mock import patch, MagicMock

from chaturbate_api.poller import ChaturbateAPIPoller


class TestChaturbateAPIPoller(unittest.TestCase):
    """Test Chaturbate API Poller."""
    @patch("chaturbate_api.poller.aiohttp.ClientSession.get")
    @patch("chaturbate_api.poller.asyncio.sleep")
    async def test_get_events_success(self, mock_sleep, mock_get):
        """Test get_events method with a successful response."""
        # Mock response from Chaturbate API
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = {"events": [], "nextUrl": None}
        mock_get.return_value.__aenter__.return_value = mock_response

        poller = ChaturbateAPIPoller("https://example.com/api")
        await poller.get_events("https://example.com/api/events")

        # Assert that event processing is called
        self.assertTrue(mock_response.json.called)
        self.assertTrue(mock_sleep.called)

    # Add more test cases for error handling, event processing, etc.


if __name__ == "__main__":
    unittest.main()
