import json
import unittest

import aiohttp
import pytest
from aioresponses import aioresponses

from chaturbate_api.client import ChaturbateAPIClient


class TestChaturbateAPIClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the Chaturbate API client."""

    async def test_run_success(self) -> None:
        """Test the run method on successful event retrieval."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, payload={"message": "success"}, status=200)

            await client.run()

        assert isinstance(client, ChaturbateAPIClient)
        assert client.base_url == base_url

    async def test_run_invalid_url(self) -> None:
        """Test the run method handles invalid URL appropriately."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)

        with aioresponses() as mocked_responses:
            mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

            with pytest.raises(ValueError):
                await client.run()

    async def test_get_events_success(self) -> None:
        """Test successful event retrieval."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url)

        events_payload = {
            "events": [
                {
                    "method": "chatMessage",
                    "object": {
                        "user": {"username": "test_user"},
                        "message": {"message": "hi"},
                    },
                },
            ],
            "nextUrl": None,
        }

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, payload=events_payload, status=200)

            events = await client.get_events(base_url)

            assert events == events_payload["events"]

        assert isinstance(client, ChaturbateAPIClient)
        assert client.base_url == base_url

    async def test_get_events_invalid_url(self) -> None:
        """Test event retrieval with an invalid URL."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url)

        with aioresponses() as mocked_responses:
            mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

            with pytest.raises(ValueError):
                await client.get_events(invalid_base_url)

    async def test_process_event_unknown_method(self) -> None:
        """Test processing of an event with an unknown method."""
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }

        client = ChaturbateAPIClient("https://events.testbed.cb.dev")

        with self.assertLogs(level="WARNING") as log:
            await client.process_event(unknown_method_event)

        assert any("Unknown method" in message for message in log.output)

    async def test_get_events_handles_server_error(self) -> None:
        """Test get_events method handles server errors correctly."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, status=500)

            with pytest.raises(aiohttp.ClientResponseError) as cm:
                await client.get_events(base_url)

            assert cm.exception.status == 500

    async def test_get_events_handles_json_decode_error(self) -> None:
        """Test get_events method handles JSON decode errors."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, body="Not a JSON", status=200)

            with pytest.raises(json.JSONDecodeError):
                await client.get_events(base_url)


if __name__ == "__main__":
    unittest.main()
