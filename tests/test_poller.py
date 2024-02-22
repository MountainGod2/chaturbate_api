import asyncio
import json
import pytest
from aioresponses import aioresponses
from src.chaturbate_api.poller import ChaturbateAPIPoller

# Sample JSON response for testing
SAMPLE_JSON_RESPONSE = {
    "events": [
        {"method": "broadcastStart"},
        {"method": "userEnter", "object": {"user": {"username": "test_user"}}}
    ],
    "nextUrl": "https://example.com/next"
}


@pytest.mark.asyncio
async def test_poller_run():
    # Mocking the HTTP response
    with aioresponses() as m:
        m.get("https://example.com/events", payload=json.dumps(SAMPLE_JSON_RESPONSE), status=200)
        m.get("https://example.com/next", payload=json.dumps(SAMPLE_JSON_RESPONSE), status=200)

        # Creating poller instance and running it
        poller = ChaturbateAPIPoller("https://example.com/events")
        await poller.run()

    # Add assertions here based on the expected behavior of the poller


@pytest.mark.asyncio
async def test_poller_process_events():
    # Create a ChaturbateAPIPoller instance
    poller = ChaturbateAPIPoller("https://example.com/events")

    # Mocking the HTTP response
    with aioresponses() as m:
        m.get("https://example.com/events", payload=json.dumps(SAMPLE_JSON_RESPONSE), status=200)

        # Getting events from mocked response
        json_response = await poller.get_events("https://example.com/events")

        # Processing events
        await poller.process_events(json_response)

    # Add assertions here based on the expected behavior of the event processing


@pytest.mark.asyncio
async def test_poller_process_event():
    # Create a ChaturbateAPIPoller instance
    poller = ChaturbateAPIPoller("https://example.com/events")

    # Sample event message for testing
    sample_event_message = {"method": "userEnter", "object": {"user": {"username": "test_user"}}}

    # Process a single event
    await poller.process_event(sample_event_message)

    # Add assertions here based on the expected behavior of processing a single event
