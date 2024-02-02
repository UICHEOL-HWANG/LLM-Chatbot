from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Post 

from schemas import Post_list

router = APIRouter(
    prefix="/api/post",
)

@router.get("/list", response_model=list[Post_list])
def post_list(db: Session = Depends(get_db)):
    _post_list = db.query(Post).order_by(Post.created_at.desc()).all()
    return _post_list