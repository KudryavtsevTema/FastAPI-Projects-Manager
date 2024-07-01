from fastapi import Depends, HTTPException

from app.models.users_models import User, UserTypes
from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.users import UserInDB, UserResponse, UserSchema
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_credentials(self, decoded_token):
        user =  await self.repository.get_user_from_db(decoded_token.get("username"))
        return UserResponse(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            type_id=UserTypes(user.type_id).name
            )

    async def create_user(self, data: UserInDB):
        user = await self.repository.get_user_from_db(data.username)
        if user:
            raise HTTPException(status_code=400, detail=f"Пользователь с таким именем существует")
        
        hashed_password = await AuthService.get_password_hash(data.password)
        model = User(
            username=data.username, 
            full_name=data.full_name, 
            email=data.email, 
            hashed_password=hashed_password, 
            disabled=False
        )
        created_user = await self.repository.create_user_to_db(model)
        return UserSchema(username=created_user.username, 
                          email=created_user.email, 
                          full_name=created_user.full_name
                          )
        
        
async def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)