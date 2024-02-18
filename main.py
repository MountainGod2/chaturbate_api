import asyncio

from src.cbapi import CBApiClient


def main() -> None:
    if __name__ == "__main__":
        cb_api_client = CBApiClient.from_env()
        try:
            asyncio.run(cb_api_client.run())
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
