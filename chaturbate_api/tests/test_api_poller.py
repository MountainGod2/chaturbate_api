from unittest.mock import MagicMock, patch

import asynctest
from aiohttp import ClientResponse

from chaturbate_api.src.api_poller import ChaturbateAPIPoller


class TestChaturbateAPIPoller(asynctest.TestCase):
    def setUp(self):
        self.base_url = "http://test.com"
        self.poller = ChaturbateAPIPoller(self.base_url)

    @patch("aiohttp.ClientSession.get")
    async def test_get_events(self, mock_get):
        mock_resp = asynctest.MagicMock(spec=ClientResponse)
        mock_resp.status = 200
        mock_resp.json = asynctest.CoroutineMock(
            return_value={"nextUrl": "http://test.com/next", "events": []}
        )
        mock_get.return_value.__aenter__.return_value = mock_resp

        next_url = await self.poller.get_events(self.base_url)
        self.assertEqual(next_url, "http://test.com/next")

    @patch("chaturbate_api.src.api_poller.event_handlers")
    async def test_process_event(self, mock_event_handlers):
        mock_handler = MagicMock()
        mock_handler.handle = asynctest.CoroutineMock()
        mock_event_handlers.get.return_value = lambda: mock_handler

        await self.poller.process_event({"method": "test_method"})
        mock_handler.handle.assert_called_once()

    async def test_process_event_unknown_method(self):
        with self.assertLogs("chaturbate_api.src.api_poller", level="WARNING") as cm:
            await self.poller.process_event({"method": "unknown_method"})
        self.assertIn(
            "WARNING:chaturbate_api.src.api_poller:Unknown method: unknown_method",
            cm.output,
        )

    async def test_handle_server_error(self):
        with self.assertLogs("chaturbate_api.src.api_poller", level="ERROR") as cm:
            await self.poller.handle_server_error(500)
        self.assertIn(
            "ERROR:chaturbate_api.src.api_poller:Server error: 500, retrying in 5 seconds",
            cm.output,
        )


if __name__ == "__main__":
    asynctest.main()
