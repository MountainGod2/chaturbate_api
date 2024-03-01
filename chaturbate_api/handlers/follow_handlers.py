"""This module contains follow event handlers"""


class FollowEventHandler:
    """Handle follow event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle follow event"""
        username = message["object"]["user"]["username"]
        return {
            "event": "follow",
            "username": username,
            "message": f"{username} has followed",
        }


class UnfollowEventHandler:
    """Handle unfollow event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle unfollow event"""
        username = message["object"]["user"]["username"]
        return {
            "event": "unfollow",
            "username": username,
            "message": f"{username} has unfollowed",
        }
