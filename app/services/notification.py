import datetime
import logging

import sqlalchemy as sa
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.notification import Notification, notification_seen_users
from app.models.user import User
from app.responses.notification import NotificationDataResponse, NotificationResponse
from app.responses.paginated_response import PaginationParam
from app.schemas.notification import NotificationRequest
from app.services.base_service import fetch_paginated_data

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(self, from_user_id, request: NotificationRequest):
        new_notification = Notification(
            from_user_id=from_user_id,
            description=request.description,
            type=request.type,
            target=request.target,
            created_by=from_user_id,
            date=datetime.datetime.now()
        )

        self.session.add(new_notification)
        await self.session.commit()
        return new_notification

    async def mark_as_seen(self, notification_id, user_id, is_admin: bool):
        try:
            if is_admin:
                target_condition = Notification.target == 'admin'
            else:
                target_condition = Notification.target == f'customer:{user_id}'

            stmt = (
                select(Notification)
                .options(joinedload(Notification.seen_users))
                .where(and_(Notification.id == notification_id, target_condition))
            )
            result = await self.session.execute(stmt)
            notification = result.scalar()

            if notification is None:
                logger.debug(f"Notification {notification_id} not found")
                return {
                    "data": None,
                    "message": "Notification not found"
                }

            user = await self.session.get(User, user_id)
            if user is None:
                logger.debug(f"User {user_id} not found")
                return {
                    "data": None,
                    "message": "User not found"
                }

            # Check if the user is already in the seen_users list
            if user_id not in [u.id for u in notification.seen_users]:
                insert_stmt = insert(notification_seen_users).values(notification_id=notification_id, user_id=user_id)
                await self.session.execute(insert_stmt)
                logger.debug(f"User {user_id} added to seen_users of notification {notification_id}")

                try:
                    await self.session.commit()
                    logger.debug(f"Notification {notification_id} marked as seen by user {user_id}")
                    return {
                        "data": True,
                        "message": "Notification marked as seen"
                    }
                except sa.exc.IntegrityError as e:
                    logger.error(f"IntegrityError: {e}")
                    await self.session.rollback()
                    return {
                        "data": False,
                        "message": f"Notification already marked as seen by this user {user_id}"
                    }
            else:
                logger.debug(f"Notification {notification_id} already marked as seen by user {user_id}")
                return {
                    "data": False,
                    "message": "Notification already marked as seen by this user"
                }
        except Exception as e:
            logger.error(f"Error in mark_as_seen: {e}")
            await self.session.rollback()
            raise

    async def mark_as_all_seen(self, user_id, is_admin: bool):
        try:
            if is_admin:
                target_condition = Notification.target == 'admin'
            else:
                target_condition = Notification.target == f'customer:{user_id}'

            stmt = (
                select(Notification)
                .options(joinedload(Notification.seen_users))
                .where(target_condition)
            )

            result = await self.session.execute(stmt)
            notifications = result.scalars().unique().all()

            for notification in notifications:
                if user_id not in [user.id for user in notification.seen_users]:
                    insert_stmt = (insert(notification_seen_users)
                                   .values(notification_id=notification.id, user_id=user_id))
                    await self.session.execute(insert_stmt)

            await self.session.commit()
            logger.debug("All notifications marked as seen")
            return {
                "data": True,
                "message": "All notifications marked as seen"
            }
        except Exception as e:
            logger.error(f"Error in mark_as_all_seen: {e}")
            await self.session.rollback()
            raise

    async def get_unseen_notifications(self, user_id, pagination: PaginationParam, is_admin: bool):
        try:
            if is_admin:
                target_condition = Notification.target == 'admin'
            else:
                target_condition = Notification.target == f'customer:{user_id}'

            subquery = (
                select(notification_seen_users.c.notification_id)
                .where(and_(notification_seen_users.c.user_id == user_id, target_condition))
            ).scalar_subquery()

            stmt = (
                select(Notification)
                .where(~Notification.id.in_(subquery), target_condition)
                .order_by(Notification.created_at.desc())
            )

            return await fetch_paginated_data(
                session=self.session,
                stmt=stmt,
                entity=Notification,
                pagination=pagination,
                data_response_model=NotificationDataResponse,
                order_by_field=Notification.created_at,
                message="Notifications fetched successfully"
            )
        except Exception as e:
            logger.error(f"Error in get_notifications: {e}")
            raise

    # async def get_unseen_notifications(self, user_id, pagination: PaginationParam):
    #     try:
    #         subquery = (
    #             select(notification_seen_users.c.notification_id)
    #             .where(and_(notification_seen_users.c.user_id == user_id, Notification.target == 'admin'))
    #         ).scalar_subquery()
    #
    #         stmt = (
    #             select(Notification)
    #             .where(~Notification.id.in_(subquery))
    #             .order_by(Notification.created_at.desc())
    #         )
    #
    #         return await fetch_paginated_data(
    #             session=self.session,
    #             stmt=stmt,
    #             entity=Notification,
    #             pagination=pagination,
    #             data_response_model=NotificationDataResponse,
    #             order_by_field=Notification.created_at,
    #             message="Notifications fetched successfully"
    #         )
    #     except Exception as e:
    #         logger.error(f"Error in get_notifications: {e}")
    #         raise

    # async def get_seen_notifications(self, user_id, pagination: PaginationParam):
    #     try:
    #         subquery = (
    #             select(notification_seen_users.c.notification_id)
    #             .where(and_(notification_seen_users.c.user_id == user_id))
    #         ).scalar_subquery()
    #
    #         stmt = (
    #             select(Notification)
    #             .where(Notification.id.in_(subquery))
    #             .order_by(Notification.created_at.desc())
    #         )
    #
    #         return await fetch_paginated_data(
    #             session=self.session,
    #             stmt=stmt,
    #             entity=Notification,
    #             pagination=pagination,
    #             data_response_model=NotificationDataResponse,
    #             order_by_field=Notification.created_at,
    #             message="Seen notifications fetched successfully"
    #         )
    #     except Exception as e:
    #         logger.error(f"Error in get_seen_notifications: {e}")
    #         raise

    async def get_seen_notifications(self, user_id, pagination: PaginationParam, is_admin: bool):
        try:
            if is_admin:
                target_condition = Notification.target == 'admin'
            else:
                target_condition = Notification.target == f'customer:{user_id}'

            subquery = (
                select(notification_seen_users.c.notification_id)
                .where(and_(notification_seen_users.c.user_id == user_id, target_condition))
            ).scalar_subquery()

            stmt = (
                select(Notification)
                .where(Notification.id.in_(subquery), target_condition)
                .order_by(Notification.created_at.desc())
            )

            return await fetch_paginated_data(
                session=self.session,
                stmt=stmt,
                entity=Notification,
                pagination=pagination,
                data_response_model=NotificationDataResponse,
                order_by_field=Notification.created_at,
                message="Seen notifications fetched successfully"
            )
        except Exception as e:
            logger.error(f"Error in get_seen_notifications: {e}")
            raise

    async def get_notification(self, notification_id):
        notification = await self.session.get(Notification, notification_id)

        if notification is None:
            return NotificationResponse(
                data=None,
                message="Notification not found"
            )

        return NotificationResponse(
            data=NotificationDataResponse.from_entity(notification),
            message="Notification fetched successfully"
        )
