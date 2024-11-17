from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_frontend_user, get_current_user
from app.responses.paginated_response import PaginationParam
from app.services.notification import NotificationService

frontend_notification_router = APIRouter(
    prefix="/notification",
    dependencies=[Depends(get_frontend_user)],
    responses={404: {"description": "Not Found!"}},
)


@frontend_notification_router.get("/unseen", status_code=200)
async def get_notifications_unseen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    notification_service = NotificationService(session)
    return await notification_service.get_unseen_notifications(user.id, pagination, is_admin=False)


@frontend_notification_router.get("/seen", status_code=200)
async def get_notifications_seen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    notification_service = NotificationService(session)
    return await notification_service.get_seen_notifications(user.id, pagination, is_admin=False)


@frontend_notification_router.post("/seen/{notification_id}", status_code=201)
async def mark_notification_as_seen(
        notification_id: str,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    notification_service = NotificationService(session)
    return await notification_service.mark_as_seen(notification_id, user.id, is_admin=False)


@frontend_notification_router.post("/seen-all", status_code=201)
async def mark_notification_as_all_seen(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    notification_service = NotificationService(session)
    return await notification_service.mark_as_all_seen(user.id, is_admin=False)
