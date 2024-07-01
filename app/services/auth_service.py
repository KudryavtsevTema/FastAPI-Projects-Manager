from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
import jwt
from passlib.context import CryptContext
import argon2

from app.schemas.users import oauth2_scheme
from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.token import Token
from app.settings import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    @staticmethod
    async def get_password_hash(password: str):
        return pwd_context.hash(password)
    
    @staticmethod
    async def decode_token(token):
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return decoded_token

    async def check_credentials(self, form_data) -> Token:
        user = await self.user_repository.get_user_from_db(form_data.username)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь с данным логином не существует")
        
        if not await self.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверный пароль")
        
        return await self.create_access_token(data={"username": form_data.username})

    async def validate_token(self, token):
        try:
            decoded_jwt = await self.decode_token(token)
            user = await self.user_repository.get_user_from_db(decoded_jwt.get("username"))
            if not user:
                raise Exception()
            return decoded_jwt
        except Exception as e:
            raise HTTPException(status_code=400, detail="Все хуйня, давай по-новой")
            
    async def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        token = Token(access_token=encoded_jwt)
        return token
    

async def get_auth_service(repository: UserRepository = Depends(get_user_repository)):
    return AuthService(repository)

async def checking_credentials(token=Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)) -> dict:
    return await auth_service.validate_token(token)



