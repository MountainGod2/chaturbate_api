import asyncio

from src.api_client import CBApiClient


def main() -> None:
    """Main function to run the CBApiClient."""
    cb_api_client = CBApiClient.from_env()
    try:
        asyncio.run(cb_api_client.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
