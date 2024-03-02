"""This module contains media purchase event handler"""

import logging


class MediaPurchaseEventHandler:
    """Handle media purchase event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle media purchase event"""
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        logging.info(f"{username} purchased {media_type} {media_name}")
        return {
            "event": "mediaPurchase",
            "username": username,
            "media_type": media_type,
            "media_name": media_name,
        }
