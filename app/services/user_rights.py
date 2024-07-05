from http import HTTPStatus
from fastapi import Depends, HTTPException

from app.repositories.user import UserRepository, get_user_repository
from app.schemas.users import oauth2_scheme
from app.services.auth import AuthService
from app.services.users import UserService, get_user_service


class UserRightsService:
    def __init__(self, user_repository: UserRepository, user_service: UserService):
        self.user_repository = user_repository
        self.user_service = user_service
    
    async def is_user_admin(self, username):
        user_type = await self.user_repository.get_user_type_from_db(username)
        if user_type != "super_admin":
            raise HTTPException(status_code=400, detail="У вас недостаточно прав")
        
    async def update_to_superuser(self, username):
        if await self.user_service.is_exist(username):
            if not await self.user_repository.update_to_superuser(username):
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User {username} already superuser")
            return None
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User {username} not exists")
        
async def get_user_rights_service(
        repository: UserRepository = Depends(get_user_repository),
        user_service: UserService = Depends(get_user_service)):
    return UserRightsService(repository, user_service)

async def checking_admin(token = Depends(oauth2_scheme), 
                         user_rights_service: UserRightsService = Depends(get_user_rights_service)):
    decoded_jwt = await AuthService.decode_token(token)
    return await user_rights_service.is_user_admin(decoded_jwt.get("username"))