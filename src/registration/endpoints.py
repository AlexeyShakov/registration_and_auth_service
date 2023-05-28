from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from database_conn import get_async_session
from models import User
from registration.manager import UserManager
from registration.schemas import UserSchemaReturn, UserSchemaCreate, LoginSchema, TokenSchema
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
    additional_info = {"id": user_obj.id}
    access_token = Authorize.create_access_token(subject=login_object.username, user_claims=additional_info)
    refresh_token = Authorize.create_refresh_token(subject=login_object.username, user_claims=additional_info)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router_auth.post("/signup", response_model=UserSchemaReturn, status_code=201)
async def singup(user_object: UserSchemaCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserManager().create(User, session, user_object.dict())

@router_auth.post("/userbytoken", response_model=UserSchemaReturn, status_code=201)
async def user_by_token(token: TokenSchema, session: AsyncSession = Depends(get_async_session)):
    pass
