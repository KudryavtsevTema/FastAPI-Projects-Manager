from schemas.token import Token
from schemas.users import UserResponse
from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from schemas.users import User, UserInDB
from services.auth_service import AuthService, checking_credentials, get_auth_service
from services.user_service import UserService, get_user_service


secure_router = APIRouter()

@secure_router.get("/me", response_model=UserResponse)
async def read_users_me(user_service: Annotated[UserService, Depends(get_user_service)], 
                        current_credential = Depends(checking_credentials)):
    return await user_service.get_user_by_credentials(current_credential)

@secure_router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    return await auth_service.check_credentials(form_data)

@secure_router.post("/registry", response_model=User)
async def registry(body: UserInDB, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body)