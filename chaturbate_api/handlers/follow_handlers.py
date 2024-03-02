"""This module contains follow event handlers."""

import logging


class FollowEventHandler:
    """Handle follow event."""

    @staticmethod
    async def handle(message) -> dict:
        """Handle follow event."""
        username = message["object"]["user"]["username"]
        logging.info(f"{username} has followed")
        return {
            "event": "follow",
            "username": username,
            "message": f"{username} has followed",
        }


class UnfollowEventHandler:
    """Handle unfollow event."""

    @staticmethod
    async def handle(message) -> dict:
        """Handle unfollow event."""
        username = message["object"]["user"]["username"]
        logging.info(f"{username} has unfollowed")
        return {
            "event": "unfollow",
            "username": username,
            "message": f"{username} has unfollowed",
        }
