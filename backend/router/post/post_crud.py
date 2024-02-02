from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Post,User
from database import get_db
from schemas import Post_create, Post_list,Post_Detail,PostUpdate

from router.users.users_router import get_current_user

router = APIRouter(
    prefix="/api/post",
)



@router.post("/create", response_model=Post_list)
def create_post(post: Post_create, db: Session = Depends(get_db),
                current_user : User = Depends(get_current_user)
                ):
    new_post = Post(title=post.title, content=post.content, user_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=Post_Detail)
def read_post_detail(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}",response_model=Post_Detail)
def update_post(post_id: int, post_data:PostUpdate,db: Session=Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail="올바른 값이 아닙니다.")
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}",status_code=204)
def delete_post(post_id: int,db:Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail="올바른 값이 아닙니다.")
    db.delete(post)
    db.commit()
    return {"detail": "성공적으로 삭제 베이비"}