from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from src.utils.constants import SECRET_KEY, ALGORITHM
from src.utils.db import get_db_session
from src.service.user_service import get_user_by_email
from src.schema.user import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session=Depends(get_db_session),
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[UserOut, Depends(get_current_user)]