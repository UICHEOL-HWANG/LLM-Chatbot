from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from models import User

router = APIRouter()

@router.post('/users/')
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



