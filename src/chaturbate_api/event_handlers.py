"""Module containing event handlers for Chaturbate API."""


class BroadcastStartEventHandler:
    """Handle broadcast start event"""

    @staticmethod
    async def handle(message) -> None:
        print("Broadcast started")


class BroadcastStopEventHandler:
    """Handle broadcast stop event"""

    @staticmethod
    async def handle(message) -> None:
        print("Broadcast stopped")


class UserEnterEventHandler:
    """Handle user enter event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        print(f"{username} entered the room")


class UserLeaveEventHandler:
    """Handle user leave event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        print(f"{username} left the room")


class FollowEventHandler:
    """Handle follow event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        print(f"{username} has followed")


class UnfollowEventHandler:
    """Handle unfollow event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        print(f"{username} has unfollowed")


class FanclubJoinEventHandler:
    """Handle fanclub join event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        print(f"{username} joined the fanclub")


class ChatMessageEventHandler:
    """Handle chat message event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        chat_message = message["object"]["message"]["message"]
        print(f"{username}: sent chat message: {chat_message}")


class PrivateMessageEventHandler:
    """Handle private message event"""

    @staticmethod
    async def handle(message) -> None:
        from_user = message["object"]["message"]["fromUser"]
        to_user = message["object"]["message"]["toUser"]
        private_message = message["object"]["message"]["message"]
        print(f"{from_user} sent private message to {to_user}: {private_message}")


class TipEventHandler:
    """Handle tip event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        tokens = message["object"]["tip"]["tokens"]
        is_anonymous = message["object"]["tip"].get("isAnon", False)
        has_message = message["object"]["tip"].get("message", "")
        has_message = has_message[3:] if has_message.startswith(" | ") else has_message
        anonymity_message = "anonymously " if is_anonymous else ""
        tip_message = f"with message: {has_message}" if has_message else ""
        print(f"{username} sent {tokens} tokens {anonymity_message}{tip_message}")


class RoomSubjectChangeEventHandler:
    """Handle room subject change event"""

    @staticmethod
    async def handle(message) -> None:
        subject = message["object"]["subject"]
        print(f"Room subject changed to: {subject}")


class MediaPurchaseEventHandler:
    """Handle media purchase event"""

    @staticmethod
    async def handle(message) -> None:
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        print(f"{username} has purchased {media_type} set: {media_name}")


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
