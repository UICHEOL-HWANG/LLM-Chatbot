from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm


from database import get_db 
import schemas

from .users import pwd_context
from . import users 

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta, datetime

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


router = APIRouter(
    prefix="/api/user",
)

@router.post("/create",status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create:schemas.UserCreate,db:Session = Depends(get_db)):
    user = users.get_existing_user(db,user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail = "이미 존재하는 사용자"
                            )
    users.create_user(db=db,user_create=_user_create)

# 로그인 

@router.post("/login",response_model=schemas.Token)
def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(),
                           db:Session = Depends(get_db)
                           ):
    # 비밀번호 검증 
    user = users.get_user(db,form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="계정 혹은 비밀번호가 잘못됨",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    data = {
        "sub" : user.username,
        "exp" : datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
    