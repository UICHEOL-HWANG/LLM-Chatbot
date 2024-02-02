from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from models import User 
from schemas import UserCreate


pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

# 회원 생성
def create_user(db:Session,user_create:UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()
    

# 회원 가입 유무 
def get_existing_user(db:Session,user_create:UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) | 
        (User.email == user_create.email)
    ).first()
    
def get_user(db:Session,username:str):
    return db.query(User).filter(User.username == username).first()

