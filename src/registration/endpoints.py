from fastapi import APIRouter, Depends, HTTPException
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
async def login(login_object: LoginSchema, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_async_session)):
    user_manager = UserManager()
    user_obj = await user_manager.get_user_by_username(login_object.username, session)
    if not user_obj:
        raise HTTPException(status_code=401, detail="User with this email does not exist")
    if not await user_manager.validate_password(user_obj, login_object.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    access_token = Authorize.create_access_token(subject=login_object.username)
    refresh_token = Authorize.create_refresh_token(subject=login_object.username)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router_auth.post("/signup", response_model=UserSchemaReturn, status_code=201)
async def singup(user_object: UserSchemaCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserManager().create(User, session, user_object.dict())
