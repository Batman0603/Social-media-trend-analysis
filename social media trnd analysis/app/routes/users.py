from fastapi import APIRouter, HTTPException, status, Depends
from app.models import User, Post, Comment, Hashtag
from app.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from pydantic import BaseModel

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/reports/engagement")
def engagement_report(db: Session = Depends(get_db)):
    results = db.query(
        User.id,
        User.username,
        func.count(Post.id).label("post_count"),
        func.count(Comment.id).label("comment_count"),
        func.count(Hashtag.id).label("hashtag_count")
    )\
    .outerjoin(Post, Post.user_id == User.id)\
    .outerjoin(Comment, Comment.user_id == User.id)\
    .outerjoin(Post.hashtags)\
    .group_by(User.id).all()
    return [
        {
            "user_id": r.id,
            "username": r.username,
            "post_count": r.post_count,
            "comment_count": r.comment_count,
            "hashtag_count": r.hashtag_count
        } for r in results
    ]

@router.get("/reports/most-engaged")
def most_engaged_users(limit: int = 5, db: Session = Depends(get_db)):
    results = db.query(
        User.id,
        User.username,
        (func.count(Post.id) + func.count(Comment.id)).label("engagement")
    )\
    .outerjoin(Post, Post.user_id == User.id)\
    .outerjoin(Comment, Comment.user_id == User.id)\
    .group_by(User.id)\
    .order_by(desc("engagement"))\
    .limit(limit).all()
    return [
        {
            "user_id": r.id,
            "username": r.username,
            "engagement": r.engagement
        } for r in results
    ]

class UserWithPost(BaseModel):
    username: str
    post_content: str

@router.post("/users/with-post", status_code=status.HTTP_201_CREATED)
def create_user_with_post(data: UserWithPost, db: Session = Depends(get_db)):
    from sqlalchemy.exc import SQLAlchemyError
    try:
        with db.begin():
            user = User(username=data.username)
            db.add(user)
            db.flush()
            post = Post(content=data.post_content, user_id=user.id)
            db.add(post)
        return {"user_id": user.id, "post_id": post.id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed")
