import json
import logging
import unittest

import aiohttp
from aioresponses import aioresponses

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        logging.basicConfig(level=logging.DEBUG)

    async def asyncTearDown(self):
        pass  # Add any necessary cleanup code here

    @aioresponses()
    async def test_run_success(self, mocked_responses):
        mocked_responses.get(self.base_url, payload={"message": "success"}, status=200)

        client = ChaturbateAPIClient(self.base_url)
        await client.run()
        # Here you can add assertions if your run() method provides output or effects to verify

    @aioresponses()
    async def test_run_invalid_url(self, mocked_responses):
        invalid_base_url = "https://invalid_url.com"
        mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

        client = ChaturbateAPIClient(invalid_base_url)
        with self.assertRaises(ValueError):
            await client.run()

    @aioresponses()
    async def test_get_events_success(self, mocked_responses):
        mocked_responses.get(self.base_url, payload={"events": []}, status=200)

        client = ChaturbateAPIClient(self.base_url)
        await client.get_events(self.base_url)

    @aioresponses()
    async def test_get_events_invalid_url(self, mocked_responses):
        invalid_base_url = "https://invalid_url.com"
        mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

        client = ChaturbateAPIClient(invalid_base_url)
        with self.assertRaises(ValueError):
            await client.get_events(invalid_base_url)

    async def test_process_events(self):
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
        await client.process_events(events)

    async def test_process_event_unknown_method(self):
        client = ChaturbateAPIClient(self.base_url)
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }

        with self.assertLogs(level=logging.WARNING) as log:
            await client.process_event(unknown_method_event)

        # Verify that a warning log message contains the expected text
        self.assertTrue(any("unknownMethod" in message for message in log.output))

    @aioresponses()
    async def test_get_events_with_max_retry_reached(self, mocked_responses):
        # Simulate 5 failed requests to trigger retries
        for _ in range(5):
            mocked_responses.get(self.base_url, exception=aiohttp.ClientError())

        client = ChaturbateAPIClient(self.base_url)

        with self.assertRaises(aiohttp.ClientError):
            await client.get_events(self.base_url)

        # Assert that 5 requests (the initial + 4 retries) were made
        self.assertEqual(sum(len(req) for req in mocked_responses.requests.values()), 5)

    @aioresponses()
    async def test_get_events_handles_server_error(self, mocked_responses):
        mocked_responses.get(self.base_url, status=500)

        client = ChaturbateAPIClient(self.base_url)
        await client.get_events(self.base_url)
        # Add assertions here if necessary

    @aioresponses()
    async def test_get_events_handles_json_decode_error(self, mocked_responses):
        mocked_responses.get(self.base_url, body="Not a JSON", status=200)

        client = ChaturbateAPIClient(self.base_url)
        with self.assertRaises(json.decoder.JSONDecodeError):
            await client.get_events(self.base_url)


if __name__ == "__main__":
    unittest.main()
