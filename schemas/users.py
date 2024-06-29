from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    type_id: int