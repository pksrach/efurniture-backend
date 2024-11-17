from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_current_user
from app.responses.paginated_response import PaginationParam
from app.services.notification import NotificationService

notification_router = APIRouter(
    prefix="/notifications",
    tags=["Backend Notification API"],
    responses={404: {"description": "Not Found!"}}
)


@notification_router.get("/unseen", status_code=200)
async def get_notifications_unseen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    notification_service = NotificationService(session)
    return await notification_service.get_unseen_notifications(user.id, pagination, is_admin=True)


@notification_router.get("/seen", status_code=200)
async def get_notifications_unseen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    notification_service = NotificationService(session)
    return await notification_service.get_seen_notifications(user.id, pagination, is_admin=True)


@notification_router.get("/{notification_id}", status_code=200)
async def get_notification(
        notification_id: str,
        session: AsyncSession = Depends(get_session)
):
    notification_service = NotificationService(session)
    return await notification_service.get_notification(notification_id)


@notification_router.post("/seen/{notification_id}", status_code=201)
async def mark_notification_as_seen(
        notification_id: str,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    notification_service = NotificationService(session)
    return await notification_service.mark_as_seen(notification_id, user.id, is_admin=True)


@notification_router.post("/seen-all", status_code=201)
async def mark_notification_as_all_seen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    notification_service = NotificationService(session)
    response = await notification_service.mark_as_all_seen(user.id, is_admin=True)
    return response
