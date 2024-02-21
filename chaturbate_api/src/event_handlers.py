class BroadcastStartEventHandler:
    @staticmethod
    async def handle(message):
        print("Broadcast started")


class BroadcastStopEventHandler:
    @staticmethod
    async def handle(message):
        print("Broadcast stopped")


class UserEnterEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        print(f"{username} entered the room")


class UserLeaveEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        print(f"{username} left the room")


class FollowEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        print(f"{username} has followed")


class UnfollowEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        print(f"{username} has unfollowed")


class FanclubJoinEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        print(f"{username} joined the fanclub")


class ChatMessageEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        chat_message = message["object"]["message"]["message"]
        print(f"{username}: sent chat message: {chat_message}")


class PrivateMessageEventHandler:
    @staticmethod
    async def handle(message):
        from_user = message["object"]["message"]["fromUser"]
        to_user = message["object"]["message"]["toUser"]
        private_message = message["object"]["message"]["message"]
        print(f"{from_user} sent private message to {to_user}: {private_message}")


class TipEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        tokens = message["object"]["tip"]["tokens"]
        is_anonymous = message["object"]["tip"].get("isAnon", False)
        has_message = message["object"]["tip"].get("message", "")
        has_message = has_message[3:] if has_message.startswith(" | ") else has_message
        anonymity_message = "anonymously " if is_anonymous else ""
        tip_message = f"with message: {has_message}" if has_message else ""
        print(f"{username} sent {tokens} tokens {anonymity_message}{tip_message}")


class RoomSubjectChangeEventHandler:
    @staticmethod
    async def handle(message):
        subject = message["object"]["subject"]
        print(f"Room subject changed to: {subject}")


class MediaPurchaseEventHandler:
    @staticmethod
    async def handle(message):
        username = message["object"]["user"]["username"]
        media_type = message["object"]["media"]["type"]
        media_name = message["object"]["media"]["name"]
        print(f"{username} has purchased {media_type} set: {media_name}")
