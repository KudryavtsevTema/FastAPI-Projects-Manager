from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.tokens import Token
from app.schemas.users import DetailedUser, UserResponse
from app.services.auth import AuthService, checking_credentials, get_auth_service
from app.services.user_rights import UserRightsService, checking_admin, get_user_rights_service
from app.services.users import UserService, get_user_service


secure_router = APIRouter()

@secure_router.get("/me", response_model=UserResponse)
async def read_users_me(
    user_service: Annotated[UserService, Depends(get_user_service)], 
    current_credential = Depends(checking_credentials)
    ):
    return await user_service.get_common(current_credential)

@secure_router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ):
    return await auth_service.check_credentials(form_data)

@secure_router.post("/registry")
async def create_user(
    body: DetailedUser, 
    user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    return await user_service.create_user(body)

@secure_router.patch("/update")
async def update_rights(
    username: str,
    user_rights_service: UserRightsService = Depends(get_user_rights_service),
    current_credential = Depends(checking_credentials),
    is_admin = Depends(checking_admin)):
    return await user_rights_service.update_to_superuser(username)

    


