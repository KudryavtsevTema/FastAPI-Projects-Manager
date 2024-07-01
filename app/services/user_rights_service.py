from fastapi import Depends, HTTPException

from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.users import oauth2_scheme
from app.services.auth_service import AuthService


class UserRightsService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def is_user_admin(self, username):
        user_type = await self.user_repository.get_user_type_from_db(username)
        if user_type != "admin":
            raise HTTPException(status_code=400, detail="У вас недостаточно прав")
        
async def get_user_rights_service(repository: UserRepository = Depends(get_user_repository)) -> UserRightsService:
    return UserRightsService(repository)

async def checking_admin(token = Depends(oauth2_scheme), 
                         user_rights_service: UserRightsService = Depends(get_user_rights_service)):
    decoded_jwt = await AuthService.decode_token(token)
    return await user_rights_service.is_user_admin(decoded_jwt.get("username"))