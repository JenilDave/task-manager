from fastapi import APIRouter, HTTPException, Depends, status
from src.utils.db import get_db_session
from src.schema.user import CreateUserPayload, AuthToken
from src.service.user_service import create_user as create_user_service, validate_user_credentials, create_access_token
from src.service.common import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.api.deps import CurrentUser
from src.db.user import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create")
async def create_user(payload: CreateUserPayload, session=Depends(get_db_session)):

    new_user = create_user_service(session, username= f"{payload.first_name} {payload.last_name}", email=payload.email, hashed_password=hash_password(payload.password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"user_id": new_user.id, "username": new_user.username}

@router.post("/token")
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session=Depends(get_db_session)):

    is_valid = await validate_user_credentials(session, email=form_data.username, password=form_data.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = await create_access_token(data={"sub": form_data.username}, expires_delta=None)
    return AuthToken(
        access_token=token,
        token_type="bearer",
    )
