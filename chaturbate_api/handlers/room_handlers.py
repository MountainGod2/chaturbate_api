"""This module contains the handler for room subject change event"""


class RoomSubjectChangeEventHandler:
    """Handle room subject change event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle room subject change event"""
        subject = message["object"]["subject"]
        return {"event": "roomSubjectChange", "subject": subject}
