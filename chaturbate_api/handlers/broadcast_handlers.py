"""This module contains handlers for broadcast events"""


class BroadcastStartEventHandler:
    """Handle broadcast start event"""

    @staticmethod
    async def handle() -> dict:
        """Handle broadcast start event."""
        return {"event": "broadcastStart", "message": "Broadcast started"}


class BroadcastStopEventHandler:
    """Handle broadcast stop event"""

    @staticmethod
    async def handle() -> dict:
        """Handle broadcast stop event"""
        return {"event": "broadcastStop", "message": "Broadcast stopped"}
