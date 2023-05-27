from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from database_conn import get_async_session
from models import User
from registration.manager import UserManager
from registration.schemas import UserSchemaReturn, UserSchemaCreate, LoginSchema
import bcrypt

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router_auth.post("/singin", status_code=201)
async def create_user(login_object: LoginSchema, Authorize: AuthJWT = Depends()):
    another_claims = {"foo": ["fiz", "baz"]}
    access_token = Authorize.create_access_token(subject=login_object.username, user_claims=another_claims)
    refresh_token = Authorize.create_refresh_token(subject=login_object.username)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router_auth.post("/signup", response_model=UserSchemaReturn, status_code=201)
async def create_user(user_object: UserSchemaCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserManager().create(User, session, user_object.dict())
