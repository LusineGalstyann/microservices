from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str = "body"
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
class PostPublic(BaseModel):
    title: str
    published: Optional[bool] = True

    model_config = {
        "from_attributes": True
    }
class TokenData(BaseModel):
    id: Optional[str] = None
class UserOut(BaseModel):

    id: int
    email: EmailStr
    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None