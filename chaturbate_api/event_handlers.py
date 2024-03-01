"""Module containing event handlers for Chaturbate API."""


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


class UserEnterEventHandler:
    """Handle user enter event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle user enter event"""
        username = message["object"]["user"]["username"]
        return {
            "event": "userEnter",
            "username": username,
            "message": f"{username} entered the room",
        }


class UserLeaveEventHandler:
    """Handle user leave event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle user leave event"""
        username = message["object"]["user"]["username"]
        return {
            "event": "userLeave",
            "username": username,
            "message": f"{username} left the room",
        }


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


class FanclubJoinEventHandler:
    """Handle fanclub join event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle fanclub join event"""
        username = message["object"]["user"]["username"]
        return {
            "event": "fanclubJoin",
            "username": username,
            "message": f"{username} joined the fanclub",
        }


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


class PrivateMessageEventHandler:
    """Handle private message event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle private message event"""
        from_user = message["object"]["message"]["fromUser"]
        to_user = message["object"]["message"]["toUser"]
        private_message = message["object"]["message"]["message"]
        return {
            "event": "privateMessage",
            "from_user": from_user,
            "to_user": to_user,
            "private_message": private_message,
        }


class TipEventHandler:
    """Handle tip event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle tip event"""
        username = message["object"]["user"]["username"]
        tokens = message["object"]["tip"]["tokens"]
        is_anonymous = message["object"]["tip"].get("isAnon", False)
        has_message = message["object"]["tip"].get("message", "")
        has_message = has_message[3:] if has_message.startswith(" | ") else has_message
        tip_message = f"with message: {has_message}" if has_message else ""
        return {
            "event": "tip",
            "username": username,
            "tokens": tokens,
            "is_anonymous": is_anonymous,
            "message": tip_message,
        }


class RoomSubjectChangeEventHandler:
    """Handle room subject change event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle room subject change event"""
        subject = message["object"]["subject"]
        return {"event": "roomSubjectChange", "subject": subject}


class MediaPurchaseEventHandler:
    """Handle media purchase event"""

    @staticmethod
    async def handle(message) -> dict:
        """Handle media purchase event"""
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        return {
            "event": "mediaPurchase",
            "username": username,
            "media_type": media_type,
            "media_name": media_name,
        }


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
