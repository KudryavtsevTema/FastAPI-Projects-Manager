from http import HTTPStatus

from fastapi import Depends, HTTPException

from app.models.users import UserTypes, Users, UsersDetails
from app.repositories.user import UserRepository, get_user_repository
from app.schemas.users import DetailedUser, UserResponse
from app.services.auth import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_common(self, decoded_token):
        user =  await self.user_repository.get_full(decoded_token.get("username"))
        return UserResponse(
            username=user.username,
            email=user.details.email,
            full_name=user.details.full_name,
            type_id=UserTypes(user.type_id).name
            )

    async def create_user(self, data: DetailedUser):
        if not self.is_exist(data.username):
            raise HTTPException(status_code=400, detail=f"Пользователь с таким именем существует")
        hashed_password = await AuthService.get_password_hash(data.password)
        model = Users(
            username=data.username,
            details=UsersDetails(
                full_name=data.full_name,
                email=data.email,
                hashed_password=hashed_password
            )
        )
        created_user = await self.user_repository.create_user_to_db(model)
        return None
    
    async def is_exist(self, username):
        user = await self.user_repository.get_common(username)
        if user:
            return True
        else:
            return False
        
        
async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)