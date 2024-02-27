import asyncio
import logging
import unittest
from unittest.mock import patch

import vcr

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        logging.basicConfig(level=logging.DEBUG)

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_get_events_success(self):
        # Given
        client = ChaturbateAPIClient(self.base_url)
        loop = asyncio.get_event_loop()

        # When
        try:
            loop.run_until_complete(asyncio.wait_for(client.run(), timeout=2))
        except asyncio.TimeoutError:
            self.fail("Timeout occurred while running the test")

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_get_events_invalid_url(self):
        # Given
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)
        loop = asyncio.get_event_loop()

        # When
        with self.assertRaises(ValueError):
            loop.run_until_complete(asyncio.wait_for(client.run(), timeout=2))

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_process_events(self):
        # Given
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
        loop = asyncio.get_event_loop()

        # When
        loop.run_until_complete(client.process_events(events))

        # Then: Ensure events are processed correctly

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_process_event_unknown_method(self):
        # Given
        client = ChaturbateAPIClient(self.base_url)
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }
        loop = asyncio.get_event_loop()

        # When
        with self.assertLogs(level=logging.WARNING):
            loop.run_until_complete(client.process_event(unknown_method_event))

        # Then: Ensure a warning log is generated for unknown method

    @vcr.use_cassette("fixtures/chaturbate_api_events.yaml")
    def test_handle_server_error(self):
        # Given
        client = ChaturbateAPIClient(self.base_url)
        status_code = 503
        loop = asyncio.get_event_loop()

        # When
        with patch.object(asyncio, "sleep") as mock_sleep:
            loop.run_until_complete(client.handle_server_error(status_code))

        # Then
        mock_sleep.assert_called_once_with(5)


if __name__ == "__main__":
    unittest.main()
