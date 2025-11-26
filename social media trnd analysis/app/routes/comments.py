from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.schemas import CommentCreate, CommentResponse
from app.models import Comment, Hashtag, Post
from app.database import SessionLocal
from app.utils.comment_parser import parse_comment

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add a comment (supports nested by parent_id)
@router.post("/comments", response_model=CommentResponse)
def add_comment(comment: CommentCreate, parent_id: Optional[int] = None, db: Session = Depends(get_db)):
    parsed = parse_comment(comment.text)

    new_comment = Comment(
        text=parsed["cleaned"],
        sentiment=parsed["analysis"]["sentiment"],
        polarity=parsed["analysis"]["polarity"],
        subjectivity=parsed["analysis"]["subjectivity"],
        user_id=comment.user_id,
        post_id=comment.post_id,
        parent_id=parent_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# Get all comments (top-level with nested replies)
@router.get("/comments", response_model=List[CommentResponse])
def get_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.parent_id == None).all()

    def build_tree(comment):
        replies = db.query(Comment).filter(Comment.parent_id == comment.id).all()
        return CommentResponse(
            id=comment.id,
            text=comment.text,
            sentiment=comment.sentiment,
            polarity=comment.polarity,
            subjectivity=comment.subjectivity,
            user_id=comment.user_id,
            post_id=comment.post_id,
            parent_id=comment.parent_id,
            replies=[build_tree(reply) for reply in replies]
        )

    return [build_tree(c) for c in comments]


# Get a comment thread by id (with all nested replies)
@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment_thread(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    def build_tree(comment):
        replies = db.query(Comment).filter(Comment.parent_id == comment.id).all()
        return CommentResponse(
            id=comment.id,
            text=comment.text,
            sentiment=comment.sentiment,
            polarity=comment.polarity,
            subjectivity=comment.subjectivity,
            user_id=comment.user_id,
            post_id=comment.post_id,
            parent_id=comment.parent_id,
            replies=[build_tree(reply) for reply in replies]
        )

    return build_tree(comment)


# Get trending hashtags (by frequency of posts)
@router.get("/hashtags/trending")
def trending_hashtags(limit: int = 10, db: Session = Depends(get_db)):
    hashtags = (
        db.query(Hashtag, func.count(Post.id).label("freq"))
        .join(Hashtag.posts)
        .group_by(Hashtag.id)
        .order_by(func.count(Post.id).desc())
        .limit(limit)
        .all()
    )
    return [{"name": h.name, "frequency": freq} for h, freq in hashtags]


# Recommend hashtags based on co-occurrence
@router.get("/hashtags/recommend/{hashtag_id}")
def recommend_hashtags(hashtag_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).join(Post.hashtags).filter(Hashtag.id == hashtag_id).all()
    post_ids = [p.id for p in posts]

    co_tags = (
        db.query(Hashtag, func.count(Hashtag.id).label("freq"))
        .join(Post.hashtags)
        .filter(Post.id.in_(post_ids), Hashtag.id != hashtag_id)
        .group_by(Hashtag.id)
        .all()
    )

    result = []
    for tag, freq in co_tags:
        rate = freq / len(posts) if posts else 0
        if rate > 0.3:
            result.append({"name": tag.name, "co_occurrence_rate": rate})

    result = sorted(result, key=lambda x: x["co_occurrence_rate"], reverse=True)[:3]
    return result
