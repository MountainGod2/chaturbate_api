import asyncio
import logging
import os
import signal

from dotenv import load_dotenv

from chaturbate_api.src.api_poller import ChaturbateAPIPoller
from chaturbate_api.src.exceptions import BaseURLNotFound

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point of the application."""
    load_dotenv()
    base_url = os.getenv("EVENTS_API_URL")

    # Check if the base URL is set and raise exception if not
    if base_url is None:
        raise BaseURLNotFound(
            "Base URL not found. Set the EVENTS_API_URL environment variable and try again."
        )

    # Start the poller
    poller = ChaturbateAPIPoller(base_url)
    await poller.run()


async def shutdown(signal, loop):
    """Cleanup tasks before shutting down."""
    logger.info(f"Received exit signal {signal.name}, cleaning up...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    logger.info("Cancelled all tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    try:
        # Set up event loop
        logger.info("Starting Chaturbate API Poller...")
        loop = asyncio.get_event_loop()

        # Register signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, lambda sig=sig: asyncio.create_task(shutdown(sig, loop))
            )

        # Run the main coroutine
        loop.run_until_complete(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Received exit signal, exiting...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Exiting...")
