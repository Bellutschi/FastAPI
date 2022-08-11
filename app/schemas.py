from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# class for schema validation; inherits from pydantic
# checks the values in body for the data types in class Post (trys to cast the specified datatype)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # does the same thing as just default values
    # rating: Optional[int] = None



class PostCreate(PostBase):
    pass



class PostResponse(PostBase):
    id: int
    created_at: datetime

    # casts the sqlalchemy into pydantic
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: Optional[str]