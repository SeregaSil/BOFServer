from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    code: str

class UserAuth(UserBase):
    user_id: int

    class Config:
        orm_mode = True
