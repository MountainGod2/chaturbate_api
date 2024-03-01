"""This module contains event handlers"""

from .handlers import (
    BroadcastStartEventHandler,
    BroadcastStopEventHandler,
    ChatMessageEventHandler,
    FanclubJoinEventHandler,
    FollowEventHandler,
    MediaPurchaseEventHandler,
    PrivateMessageEventHandler,
    RoomSubjectChangeEventHandler,
    TipEventHandler,
    UnfollowEventHandler,
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
