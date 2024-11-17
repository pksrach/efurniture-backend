from uuid import UUID

import pytz
from pydantic import BaseModel

from app.config.settings import get_settings
from app.models.notification import Notification
from app.responses.base import BaseResponse

settings = get_settings()


class NotificationDataResponse(BaseModel):
    id: str | UUID
    date: str | None
    from_user_id: str | UUID
    description: str | None
    type: str | None
    target: str | None

    @classmethod
    def from_entity(cls, notification) -> 'NotificationDataResponse':
        if notification is None:
            return cls(
                id="",
                date="",
                from_user_id="",
                description="",
                type="",
                target=""
            )

        env_timezone = settings.TIMEZONE
        local_tz = pytz.timezone(env_timezone)

        if notification.date:
            if notification.date.tzinfo is None:
                notification.date = pytz.utc.localize(notification.date)

        local_dt = notification.date.astimezone(local_tz)

        return cls(
            id=notification.id,
            date=local_dt.strftime("%d-%m-%Y %I:%M %p"),
            from_user_id=notification.from_user_id,
            description=notification.description,
            type=notification.type,
            target=notification.target
        )


class NotificationResponse(BaseResponse):
    data: NotificationDataResponse | None

    @classmethod
    def from_entity(cls, notification: 'Notification') -> 'NotificationResponse':
        return cls(
            data=NotificationDataResponse.from_entity(notification),
            message="Notification fetched successfully"
        )


class NotificationListResponse(BaseResponse):
    data: list[NotificationDataResponse]

    @classmethod
    def from_entities(cls, notifications: list['Notification']) -> 'NotificationListResponse':
        return cls(
            data=[NotificationDataResponse.from_entity(notification) for notification in notifications],
            message="Notifications fetched successfully"
        )
