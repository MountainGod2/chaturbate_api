"""This module contains the tip event handler."""

import logging


class TipEventHandler:
    """Handle tip event."""

    @staticmethod
    async def handle(message) -> dict:
        """Handle tip event."""
        username = message["object"]["user"]["username"]
        tokens = message["object"]["tip"]["tokens"]
        is_anonymous = message["object"]["tip"].get("isAnon", False)
        has_message = message["object"]["tip"].get("message", "")
        has_message = has_message[3:] if has_message.startswith(" | ") else has_message
        tip_message = f"with message: {has_message}" if has_message else ""
        if is_anonymous:
            logging.info(f"Anonymous tip of {tokens} tokens {tip_message}")
        else:
            logging.info(f"{username} tipped {tokens} tokens {tip_message}")
        return {
            "event": "tip",
            "username": username,
            "tokens": tokens,
            "is_anonymous": is_anonymous,
            "message": tip_message,
        }
