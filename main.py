import asyncio
import logging
from src.cbapi_client import CBApiClient


def configure_logging():
    logging.basicConfig(level=logging.INFO)  # Configure root logger


def main():
    configure_logging()
    logger = logging.getLogger(__name__)

    try:
        cb_api_client = CBApiClient.from_env(logger=logger)
        asyncio.run(cb_api_client.run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
