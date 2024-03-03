"""Tests for the Chaturbate API client."""

import json
import unittest

import aiohttp
from aioresponses import aioresponses

from chaturbate_api.client import ChaturbateAPIClient
from chaturbate_api.event_handlers import event_handlers
from chaturbate_api.exceptions import ChaturbateServerError


class TestChaturbateAPIClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the Chaturbate API client."""

    async def asyncSetUp(self: "TestChaturbateAPIClient") -> None:
        """Set up the test by creating a session."""
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self: "TestChaturbateAPIClient") -> None:
        """Tear down the test by closing the session."""
        await self.session.close()

    async def test_run_success(self: "TestChaturbateAPIClient") -> None:
        """Test the run method on successful event retrieval."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url, self.session, event_handlers)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, payload={"message": "success"}, status=200)

            await client.run()

        if not isinstance(client, ChaturbateAPIClient):
            msg = "Client is not an instance of ChaturbateAPIClient"
            raise TypeError(msg)
        if client.base_url != base_url:
            msg = "Base URL mismatch"
            raise AssertionError(msg)

    async def test_run_invalid_url(self: "TestChaturbateAPIClient") -> None:
        """Test the run method handles invalid URL appropriately."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url, self.session, event_handlers)

        with aioresponses() as mocked_responses:
            mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

            try:
                await client.run()
                msg = "Expected ValueError was not raised"
                raise AssertionError(msg)
            except ValueError as err:
                if "Invalid URL" not in str(err):
                    msg = "Unexpected error message"
                    raise AssertionError(msg) from err

    async def test_get_events_success(self: "TestChaturbateAPIClient") -> None:
        """Test successful event retrieval."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url, self.session, event_handlers)

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

            events, next_url = await client.get_events(base_url)

        if events != events_payload["events"]:
            msg = "Events mismatch"
            raise AssertionError(msg)

        if not isinstance(client, ChaturbateAPIClient):
            msg = "Client is not an instance of ChaturbateAPIClient"
            raise TypeError(msg)
        if client.base_url != base_url:
            msg = "Base URL mismatch"
            raise AssertionError(msg)

    async def test_get_events_invalid_url(self: "TestChaturbateAPIClient") -> None:
        """Test event retrieval with an invalid URL."""
        invalid_base_url = "https://invalid_url.com"
        client = ChaturbateAPIClient(invalid_base_url, self.session, event_handlers)

        with aioresponses() as mocked_responses:
            mocked_responses.get(invalid_base_url, exception=aiohttp.ClientError())

            try:
                await client.get_events(invalid_base_url)
                msg = "Expected ValueError was not raised"
                raise AssertionError(msg)
            except ValueError as err:
                if "Invalid URL" not in str(err):
                    msg = "Unexpected error message"
                    raise AssertionError(msg) from err

    async def test_process_event_unknown_method(
        self: "TestChaturbateAPIClient",
    ) -> None:
        """Test processing of an event with an unknown method."""
        unknown_method_event = {
            "method": "unknownMethod",
            "object": {"user": {"username": "test_user"}},
        }
        client = ChaturbateAPIClient(
            "https://events.testbed.cb.dev",
            self.session,
            event_handlers,
        )

        with self.assertLogs(level="WARNING") as log:
            await client.process_event(unknown_method_event)

        if not any("Unknown method" in message for message in log.output):
            msg = "Log message not found"
            raise AssertionError(msg)

    async def test_get_events_handles_server_error(
        self: "TestChaturbateAPIClient",
    ) -> None:
        """Test get_events method handles server errors correctly."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url, self.session, event_handlers)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, status=521)

            try:
                await client.get_events(base_url)
                msg = "Expected ChaturbateServerError was not raised"
                raise AssertionError(msg)
            except ChaturbateServerError:
                pass

    async def test_get_events_handles_json_decode_error(
        self: "TestChaturbateAPIClient",
    ) -> None:
        """Test get_events method handles JSON decode errors."""
        base_url = "https://events.testbed.cb.dev/events/user_name/api_key"
        client = ChaturbateAPIClient(base_url, self.session, event_handlers)

        with aioresponses() as mocked_responses:
            mocked_responses.get(base_url, body="Not a JSON", status=200)

            try:
                await client.get_events(base_url)
                msg = "Expected json.JSONDecodeError was not raised"
                raise AssertionError(msg)
            except json.JSONDecodeError:
                pass


if __name__ == "__main__":
    unittest.main()
