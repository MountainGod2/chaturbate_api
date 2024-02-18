import re


class Formatter:
    def format_event(self, event_object: dict) -> str:
        method = event_object.get("method")
        event_object = event_object.get("object")
        if method and event_object:
            formatter_func = getattr(self, f"format_{method}_event", None)
            if formatter_func:
                return formatter_func(event_object)
        return None

    def format_tip_event(self, event_object: dict) -> str:
        tip_info = event_object.get("tip")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if tip_info and user_info and broadcaster:
            message = tip_info.get("message", "")

            # Use regular expressions to remove the prefix and trim spaces around the pipe symbol
            message = re.sub(r"^\s*\|\s*", "", message)
            message_str = f" with message: '{message}'" if message else ""

            return f"User {user_info['username']} tipped {tip_info['tokens']} tokens to broadcaster {broadcaster}{message_str}"
        return None

    def format_user_leave_event(self, event_object: dict) -> str:
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} left the channel of broadcaster {broadcaster}"
        return None

    def format_user_enter_event(self, event_object: dict) -> str:
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} entered the channel of broadcaster {broadcaster}"
        return None

    def format_chat_message_event(self, event_object: dict) -> str:
        message_info = event_object.get("message")
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if message_info and user_info and broadcaster:
            return f"User {user_info['username']} sent a message '{message_info['message']}' in the channel of broadcaster {broadcaster}"
        return None

    def format_unfollow_event(self, event_object: dict) -> str:
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} unfollowed broadcaster {broadcaster}"
        return None

    def format_follow_event(self, event_object: dict) -> str:
        user_info = event_object.get("user")
        broadcaster = event_object.get("broadcaster")

        if user_info and broadcaster:
            return f"User {user_info['username']} followed broadcaster {broadcaster}"
        return None
