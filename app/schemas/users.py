from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

class BaseUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class DetailedUser(BaseUser):
    full_name: str
    email: str
    password: str

class UserResponse(BaseUser):
    username: str
    email: str | None = None
    full_name: str | None = None
    type_id: str
