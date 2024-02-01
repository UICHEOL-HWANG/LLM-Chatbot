from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db 
from router import users
import schemas

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
    