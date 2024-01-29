from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas, database
import database


router = APIRouter()

@router.get('/users/')
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



