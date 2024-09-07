import base64
import logging
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime,timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.database import get_session
from app.models.user import User
from app.models.user_token import UserToken
from app.config.settings import get_settings

settings = get_settings()


# Define special characters for password validation
SPECIAL_CHARACTERS = set('@#$%=:?.|~>')

# Initialize the password context for hashing and verification
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)


async def get_token_user(token: str, db: AsyncSession):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        try:
            user_token_id = int(str_decode(payload.get('r')))
            user_id = int(str_decode(payload.get('sub')))
            access_key = payload.get('a')
        except (ValueError, TypeError) as e:
            # Handle decoding or conversion errors
            raise HTTPException(status_code=400, detail="Invalid token payload")

        stmt = select(UserToken).options(joinedload(UserToken.user)).filter(
            UserToken.access_key == access_key,
            UserToken.id == user_token_id,
            UserToken.user_id == user_id,
            UserToken.expires_at > datetime.utcnow()
        )
        result = await db.execute(stmt)
        user_token = result.scalars().first()
        
        if user_token:
            return user_token.user
    return None

async def load_user(email: str, db: AsyncSession) -> User:
    try:
        stmt = select(User).filter(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
    except Exception as user_exec:
        logging.info(f"User Not Found, Email: {email}")
        user = None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    user = await get_token_user(token=token, db=db)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authorised.")