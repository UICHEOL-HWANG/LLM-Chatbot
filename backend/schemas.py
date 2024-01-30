from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    username: str
    email: str
    password1 : str
    password2 : str 
    
    # 유효성 검증 
    
    @field_validator('username','password1','password2','email')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError("빈 값 불가")
        return v 
    @field_validator('password2')
    def password_match(cls,v,info:FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError("비밀번호 불일치")
        return v
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True