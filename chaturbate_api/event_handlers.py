"""Module containing event handlers for Chaturbate API."""

from .handlers.broadcast_handlers import (
    BroadcastStartEventHandler,
    BroadcastStopEventHandler,
)
from .handlers.chat_handlers import ChatMessageEventHandler
from .handlers.follow_handlers import (
    FollowEventHandler,
    UnfollowEventHandler,
)
from .handlers.media_handlers import MediaPurchaseEventHandler
from .handlers.message_handlers import PrivateMessageEventHandler
from .handlers.room_handlers import RoomSubjectChangeEventHandler
from .handlers.tip_handlers import TipEventHandler
from .handlers.user_handlers import (
    FanclubJoinEventHandler,
    UserEnterEventHandler,
    UserLeaveEventHandler,
)

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
