from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, Form, Header, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import select

from src.core.sql.dependencies import get_async_session

from .dependencies import blacklist, check_token, create_token
from .env import JWT_expire_in, refresh_token_expire_in
from .models import Admin
from .schemas import AdminSchema

auth_router = APIRouter(prefix="/auth", tags=["Admin authorization"])


async def check_jwt(authorization: Annotated[str, Header()]):
    key = authorization.replace("Bearer ", "")
    key = await check_token(key)
    if key is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="JWT token is invalid or outdated")


@auth_router.post("/login")
async def login(
    username: str = Form(..., description="A username of registered admin", min_length=1, max_length=200),
    password: str = Form(..., description="Password of registered user", min_length=8, max_length=50),
    session=Depends(get_async_session),
):
    query = select(Admin).where(Admin.username == username)
    result = (await session.execute(query)).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    admin = AdminSchema.model_validate(result)
    admin_passwd = admin.password
    user_passwd = password.encode("utf-8")
    if not bcrypt.checkpw(user_passwd, admin_passwd):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password!")

    # create JWT token
    jwt_token = await create_token(
        data={
            "sub": result.id.hex,
            "type": "access",
        },
        expire_in=JWT_expire_in,
    )

    # create refresh token
    refresh_token = await create_token(
        data={
            "sub": result.id.hex,
            "type": "refresh",
        },
        expire_in=refresh_token_expire_in,
    )

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"jwt": jwt_token, "refresh": refresh_token})


@auth_router.get("/logout")
async def logout(authorization: Annotated[str, Header()], refresh: Annotated[str, Header()]):
    try:
        await blacklist(authorization, 20 * 60)  # 20 minutes
        await blacklist(refresh, 24 * 60 * 60)  # 24 hours
    except Exception as e:
        logger.error(f"Trying to logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not blacklist session credentials. Please try again",
        ) from e


@auth_router.get("/refresh")
async def refresh(refresh: Annotated[str, Header()]):
    # Да, эта хуйня через 15 часов потребует перезайти, но! Кому вообще надо больше 15 часов сидеть в админке?
    # Если так надо, то можно сделать отдельный эндпоинт, чтоб по JWT обновлял refresh
    key = refresh
    refresh_payload = await check_token(key)
    if refresh_payload is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Refresh token is invalid or outdated")

    if refresh_payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type!")

    jwt_token = await create_token(
        data={
            "sub": refresh_payload.get("sub"),
            "type": "access",
        },
        expire_in=JWT_expire_in,
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={"jwt_token": jwt_token})


@auth_router.post("/default")
async def set_default_admin(
    username: str = Form(..., description="A username of registered admin", min_length=1, max_length=200),
    password: str = Form(..., description="Password of registered user", min_length=8, max_length=50),
    session=Depends(get_async_session),
):
    users = (await session.execute(select(Admin))).first()
    if users:
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content="Default administrator already exists. Ask your Administrator to include you",
        )

    new_admin = AdminSchema(username=username, password=password)
    new_admin = Admin(**new_admin.model_dump())
    session.add(new_admin)
    await session.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Successfully created default admin!")
