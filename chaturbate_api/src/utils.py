from src.event_handlers import (
    BroadcastStartEventHandler,
    BroadcastStopEventHandler,
    UserEnterEventHandler,
    UserLeaveEventHandler,
    FollowEventHandler,
    UnfollowEventHandler,
    FanclubJoinEventHandler,
    ChatMessageEventHandler,
    PrivateMessageEventHandler,
    TipEventHandler,
    RoomSubjectChangeEventHandler,
    MediaPurchaseEventHandler,
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
