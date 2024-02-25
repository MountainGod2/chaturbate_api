"""Module containing event handlers for Chaturbate API."""
import logging

logger = logging.getLogger(__name__)


class BroadcastStartEventHandler:
    """Handle broadcast start event"""

    @staticmethod
    async def handle() -> None:
        """Handle broadcast start event."""
        logger.info("Broadcast started")


class BroadcastStopEventHandler:
    """Handle broadcast stop event"""

    @staticmethod
    async def handle() -> None:
        """Handle broadcast stop event"""
        logger.info("Broadcast stopped")


class UserEnterEventHandler:
    """Handle user enter event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle user enter event"""
        username = message["object"]["user"]["username"]
        logger.info(f"{username} entered the room")


class UserLeaveEventHandler:
    """Handle user leave event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle user leave event"""
        username = message["object"]["user"]["username"]
        logger.info(f"{username} left the room")


class FollowEventHandler:
    """Handle follow event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle follow event"""
        username = message["object"]["user"]["username"]
        logger.info(f"{username} has followed")


class UnfollowEventHandler:
    """Handle unfollow event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle unfollow event"""
        username = message["object"]["user"]["username"]
        logger.info(f"{username} has unfollowed")


class FanclubJoinEventHandler:
    """Handle fanclub join event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle fanclub join event"""
        username = message["object"]["user"]["username"]
        logger.info(f"{username} joined the fanclub")


class ChatMessageEventHandler:
    """Handle chat message event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle chat message event"""
        username = message["object"]["user"]["username"]
        chat_message = message["object"]["message"]["message"]
        logger.info(f"{username}: sent chat message: {chat_message}")


class PrivateMessageEventHandler:
    """Handle private message event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle private message event"""
        from_user = message["object"]["message"]["fromUser"]
        to_user = message["object"]["message"]["toUser"]
        private_message = message["object"]["message"]["message"]
        logger.info(f"{from_user} sent private message to {to_user}: {private_message}")


class TipEventHandler:
    """Handle tip event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle tip event"""
        username = message["object"]["user"]["username"]
        tokens = message["object"]["tip"]["tokens"]
        is_anonymous = message["object"]["tip"].get("isAnon", False)
        has_message = message["object"]["tip"].get("message", "")
        has_message = has_message[3:] if has_message.startswith(" | ") else has_message
        anonymity_message = "anonymously " if is_anonymous else ""
        tip_message = f"with message: {has_message}" if has_message else ""
        logger.info(f"{username} sent {tokens} tokens {anonymity_message}{tip_message}")


class RoomSubjectChangeEventHandler:
    """Handle room subject change event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle room subject change event"""
        subject = message["object"]["subject"]
        logger.info(f"Room subject changed to: {subject}")


class MediaPurchaseEventHandler:
    """Handle media purchase event"""

    @staticmethod
    async def handle(message) -> None:
        """Handle media purchase event"""
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        logger.info(f"{username} has purchased {media_type} set: {media_name}")


event_handlers = {
    "broadcastStart": BroadcastStartEventHandler,
    "broadcastStop": BroadcastStopEventHandler,
    "userEnter": UserEnterEventHandler,
    "userLeave": UserLeaveEventHandler,
    "follow": FollowEventHandler,
    "unfollow": UnfollowEventHandler,
    "fanclubJoin": FanclubJoinEventHandler,
    "chatMessage": ChatMessageEventHandler,
    "privateMessage": PrivateMessageEventHandler,
    "tip": TipEventHandler,
    "roomSubjectChange": RoomSubjectChangeEventHandler,
    "mediaPurchase": MediaPurchaseEventHandler,
}