from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.hashtag_service import get_trending_hashtags, get_related_hashtags

router = APIRouter(prefix="/hashtags", tags=["hashtags"])

@router.get("/trending")
def trending_hashtags(limit: int = 5, db: Session = Depends(get_db)):
    return {"trending": get_trending_hashtags(db, limit)}

@router.get("/related/{hashtag_name}")
def related_hashtags(hashtag_name: str, db: Session = Depends(get_db)):
    return {"related": get_related_hashtags(db, hashtag_name)}
