import base64
import logging
import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.database import get_session
from app.config.settings import get_settings
from app.constants.roles import Roles
from app.models.user import User

settings = get_settings()

# Define special characters for password validation
SPECIAL_CHARACTERS = set('@#$%=:?.|~>')

# Initialize the password context for hashing and verification
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_token = HTTPBearer(
    scheme_name="Bearer",
    auto_error=True,
    description="Bearer Token",
    bearerFormat="JWT"
)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_ctx.hash(password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_ctx.verify(plain_pass, hashed_pass)


def is_password_strong_enough(password: str) -> bool:
    """Check if the password meets the strength requirements."""
    return (
            len(password) >= 8 and
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in SPECIAL_CHARACTERS for char in password)
    )


def is_password_long_enough(password: str) -> bool:
    """Check if the password has a length of at least 8 characters."""
    return len(password) >= 8


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
        return payload
    except jwt.ExpiredSignatureError:
        logging.debug("JWT Error: Token has expired")
    except jwt.InvalidTokenError:
        logging.debug("JWT Error: Invalid token")
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
    return None


def generate_token(user: User, expiry: timedelta, options: dict = None):
    if user is None:
        raise ValueError("User object cannot be None")

    expire = datetime.now() + expiry
    user_id = str(user.id)
    role = Roles.get_name(user.role)
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "dict": dict() if options is None else options
    }

    secret = settings.JWT_SECRET
    algo = settings.JWT_ALGORITHM

    token = jwt.encode(payload, secret, algorithm=algo, headers={"typ": "JWT", "alg": algo})
    return token


async def get_token_user(token: str, db: AsyncSession):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        try:
            # Ensure the payload contains required fields
            if 'sub' not in payload:
                raise HTTPException(status_code=400, detail="Invalid token payload: 'sub' not found")

            # Extract the user ID from the token payload
            user_id = payload.get('sub')  # 'sub' is the user ID, assumed to be a UUID

            # Query the database to verify the user exists
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return user  # Return the user if found

        except (ValueError, TypeError) as e:
            logging.error(f"Token decoding error: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid token payload")
    else:
        raise HTTPException(status_code=400, detail="Invalid token")


async def load_user(emailOrUsername: str, db: AsyncSession) -> User:
    try:
        stmt = select(User).where(or_(User.email == emailOrUsername, User.username == emailOrUsername))
        result = await db.execute(stmt)
        user = result.scalars().first()
    except Exception:
        logging.info(f"User Not Found, Email or Username: {emailOrUsername}")
        user = None
    return user


async def token_scheme(credentials: HTTPAuthorizationCredentials = Depends(bearer_token)) -> str:
    return credentials.credentials


async def get_current_user(token: str = Depends(token_scheme), db: AsyncSession = Depends(get_session)):
    user = await get_token_user(token=token, db=db)
    if user:
        return user

    raise HTTPException(status_code=401, detail="Not authorized")


async def get_backend_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [Roles.ADMIN, Roles.USER, Roles.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this route"
        )
    return current_user


async def get_frontend_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in [Roles.CUSTOMER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this route, you are not a customer"
        )
    return current_user
