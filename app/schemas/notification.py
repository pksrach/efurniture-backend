from pydantic import BaseModel


class NotificationRequest(BaseModel):
    description: str
    type: str
    target: str
