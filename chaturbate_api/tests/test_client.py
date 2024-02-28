import asyncio
import json
import logging
import unittest
from unittest.mock import MagicMock, patch

import aiohttp
import vcr

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        logging.basicConfig(level=logging.DEBUG)
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_run_success(self):
        client = ChaturbateAPIClient(self.base_url)
        self.loop.run_until_complete(client.run())

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_run_invalid_url(self):
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)

        async def test():
            with self.assertRaises(ValueError):
                await client.run()

        self.loop.run_until_complete(asyncio.wait_for(test(), timeout=2))

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_get_events_success(self):
        client = ChaturbateAPIClient(self.base_url)

        async def test():
            await client.get_events(self.base_url)

        self.loop.run_until_complete(asyncio.wait_for(test(), timeout=2))

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_get_events_invalid_url(self):
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)

        async def test():
            with self.assertRaises(ValueError):
                await client.get_events(invalid_base_url)

        self.loop.run_until_complete(asyncio.wait_for(test(), timeout=2))

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_process_events(self):
        client = ChaturbateAPIClient(self.base_url)
        events = {
            "events": [
                {
                    "method": "chatMessage",
                    "object": {
                        "user": {"username": "test_user"},
                        "message": {"message": "hi"},
                    },
                }
            ],
            "nextUrl": None,
        }

        async def test():
            await client.process_events(events)

        self.loop.run_until_complete(test())

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_process_event_unknown_method(self):
        client = ChaturbateAPIClient(self.base_url)
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }

        async def test():
            with self.assertLogs(level=logging.WARNING):
                await client.process_event(unknown_method_event)

        self.loop.run_until_complete(test())

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_get_events_with_max_retry_reached(self):
        # Mocking the client session to always return a server error
        mock_get = MagicMock(side_effect=aiohttp.ClientError())

        # Mocking asyncio.sleep to avoid waiting during retries
        with patch("asyncio.sleep"):
            with patch("aiohttp.ClientSession.get", mock_get):
                client = ChaturbateAPIClient(self.base_url)

                # We expect the method to raise an exception after reaching the maximum retry count
                with self.assertRaises(aiohttp.ClientError):
                    self.loop.run_until_complete(client.get_events(self.base_url))

            # Check that the request was retried 5 times (max retry count)
            self.assertEqual(mock_get.call_count, 5)

    @patch("aiohttp.ClientSession.get")
    def test_get_events_handles_server_error(self, mock_get):
        mock_response = MagicMock(status=500)
        mock_get.return_value.__aenter__.return_value = mock_response

        client = ChaturbateAPIClient(self.base_url)
        self.loop.run_until_complete(client.get_events(self.base_url))

    @patch("aiohttp.ClientSession.get")
    def test_get_events_handles_json_decode_error(self, mock_get):
        mock_response = MagicMock(status=200)
        mock_response.json.side_effect = json.JSONDecodeError(
            "Error decoding JSON", "{}", 0
        )
        mock_get.return_value.__aenter__.return_value = mock_response

        client = ChaturbateAPIClient(self.base_url)
        self.loop.run_until_complete(client.get_events(self.base_url))


if __name__ == "__main__":
    unittest.main()
