from pydantic import BaseModel, EmailStr, conint
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserReturn(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    user: UserReturn

    class Config:
        orm_mode = True

class Post(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostVoteOut(BaseModel):
    Post: PostOut
    votes: int

    class Config:
        orm_mode = True