from unittest.mock import MagicMock, patch

import asynctest
from aiohttp import ClientResponse

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(asynctest.TestCase):
    def setUp(self):
        self.base_url = "https://eventsapi.chaturbate.com"
        self.poller = ChaturbateAPIClient(self.base_url)

    @patch("aiohttp.ClientSession.get")
    async def test_get_events(self, mock_get):
        mock_resp = MagicMock(spec=ClientResponse)
        mock_resp.status = 200
        mock_resp.json = asynctest.CoroutineMock(
            return_value={
                "nextUrl": "https://eventsapi.chaturbate.com/next",
                "events": [],
            }
        )
        mock_get.return_value.__aenter__.return_value = mock_resp

        next_url = await self.poller.get_events(self.base_url)
        self.assertEqual(next_url, "https://eventsapi.chaturbate.com/next")

    @patch("chaturbate_api.client.event_handlers")
    async def test_process_event(self, mock_event_handlers):
        mock_handler = MagicMock()
        mock_handler.handle = asynctest.CoroutineMock()
        mock_event_handlers.get.return_value = lambda: mock_handler

        await self.poller.process_event({"method": "test_method"})
        mock_handler.handle.assert_called_once()

    async def test_process_event_unknown_method(self):
        with self.assertLogs("chaturbate_api.client", level="WARNING") as cm:
            await self.poller.process_event({"method": "unknown_method"})
        self.assertIn(
            "WARNING:chaturbate_api.client:Unknown method: unknown_method",
            cm.output,
        )

    async def test_handle_server_error(self):
        with self.assertLogs("chaturbate_api.client", level="ERROR") as cm:
            await self.poller.handle_server_error(500)
        self.assertIn(
            "ERROR:chaturbate_api.client:Server error: 500, retrying in 5 seconds",
            cm.output,
        )


if __name__ == "__main__":
    asynctest.main()
