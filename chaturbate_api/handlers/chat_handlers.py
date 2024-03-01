"""This module contains the handler for chat message event"""


class ChatMessageEventHandler:
    """Handle chat message event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle chat message event"""
        username = message["object"]["user"]["username"]
        chat_message = message["object"]["message"]["message"]
        return {
            "event": "chatMessage",
            "username": username,
            "chat_message": chat_message,
        }
