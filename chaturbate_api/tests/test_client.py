import json
import unittest

import aiohttp
from aioresponses import aioresponses

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the Chaturbate API client."""

    async def asyncSetUp(self):
        """Set up test case."""
        self.base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        self.client = ChaturbateAPIClient(self.base_url)

    async def asyncTearDown(self):
        """Tear down test case."""
        pass  # Cleanup resources if necessary

    @aioresponses()
    async def test_run_success(self, mocked_responses):
        """Test the run method on successful event retrieval."""
        mocked_responses.get(self.base_url, payload={"message": "success"}, status=200)

        await self.client.run()

        self.assertIsInstance(self.client, ChaturbateAPIClient)
        self.assertEqual(self.client.base_url, self.base_url)

    @aioresponses()
    async def test_run_invalid_url(self, mocked_responses):
        """Test the run method handles invalid URL appropriately."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)
        mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

        with self.assertRaises(ValueError):
            await client.run()

    @aioresponses()
    async def test_get_events_success(self, mocked_responses):
        """Test successful event retrieval."""
        mocked_responses.get(self.base_url, payload={"events": []}, status=200)

        await self.client.get_events(self.base_url)
        # Add specific assertions here

        self.assertIsInstance(self.client, ChaturbateAPIClient)
        self.assertEqual(self.client.base_url, self.base_url)

    @aioresponses()
    async def test_get_events_invalid_url(self, mocked_responses):
        """Test event retrieval with an invalid URL."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)
        mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

        with self.assertRaises(ValueError):
            await client.get_events(invalid_base_url)

    async def test_process_events(self):
        """Test processing of events."""
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
        await self.client.process_events(events)
        # Verify the process_events behavior, possibly by mocking the event handler calls

    async def test_process_event_unknown_method(self):
        """Test processing of an event with an unknown method."""
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }

        with self.assertLogs(level="WARNING") as log:
            await self.client.process_event(unknown_method_event)

        self.assertTrue(any("Unknown method" in message for message in log.output))

    @aioresponses()
    async def test_get_events_with_max_retry_reached(self, mocked_responses):
        """Test get_events method when maximum retry attempts are reached."""
        mocked_responses.get(self.base_url, exception=aiohttp.ClientError())

        with self.assertRaises(aiohttp.ClientError):
            await self.client.get_events(self.base_url)

    @aioresponses()
    async def test_get_events_handles_server_error(self, mocked_responses):
        """Test get_events method handles server errors correctly."""
        mocked_responses.get(self.base_url, status=500)

        await self.client.get_events(self.base_url)
        # Add assertions here if necessary

    @aioresponses()
    async def test_get_events_handles_json_decode_error(self, mocked_responses):
        """Test get_events method handles JSON decode errors."""
        mocked_responses.get(self.base_url, body="Not a JSON", status=200)

        with self.assertRaises(json.JSONDecodeError):
            await self.client.get_events(self.base_url)


if __name__ == "__main__":
    unittest.main()
