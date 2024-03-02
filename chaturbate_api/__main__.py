import asyncio
import logging
import signal

from chaturbate_api.client import ChaturbateAPIClient
from chaturbate_api.exceptions import BaseURLNotFound

# Configure logger to debug level to get detailed logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point of the application."""
    poller = ChaturbateAPIClient()
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
        logger.info("Starting Chaturbate API Poller...")
        loop = asyncio.get_event_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, lambda sig=sig: asyncio.create_task(shutdown(sig, loop))
            )

        loop.run_until_complete(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Received exit signal, exiting...")
    except BaseURLNotFound as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Exiting...")
