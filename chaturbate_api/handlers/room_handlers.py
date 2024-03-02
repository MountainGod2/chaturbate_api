"""This module contains the handler for room subject change event"""

import logging


class RoomSubjectChangeEventHandler:
    """Handle room subject change event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle room subject change event"""
        subject = message["object"]["subject"]
        logging.info(f"Room subject changed to: {subject}")
        return {"event": "roomSubjectChange", "subject": subject}
