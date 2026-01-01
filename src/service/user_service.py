from src.db.user import User
from src.service.common import hash_password, verify_password
from src.utils.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    result = await db_session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    return user

def create_user(db_session, username: str, email: str, hashed_password: str) -> User:
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db_session.add(new_user)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    db_session.refresh(new_user)
    return new_user

async def validate_user_credentials(db_session: AsyncSession, email: str, password: str) -> bool:
    user = await db_session.execute(select(User).where(User.email == email))
    if not user:
        return False
    user = user.scalar_one()
    if user:
        print("user:", user.hashed_password, hash_password(password))
    return verify_password(password, user.hashed_password)

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
