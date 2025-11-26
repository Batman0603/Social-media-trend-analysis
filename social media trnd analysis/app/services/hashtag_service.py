from sqlalchemy.orm import Session
from collections import Counter
from .. import models

def get_trending_hashtags(db: Session, limit: int = 5):
    hashtags = db.query(models.Hashtag).all()
    counter = Counter()

    for ht in hashtags:
        counter[ht.name] = len(ht.posts)

    return counter.most_common(limit)

def get_related_hashtags(db: Session, hashtag_name: str):
    hashtag = db.query(models.Hashtag).filter(models.Hashtag.name == hashtag_name).first()
    if not hashtag:
        return []

    co_occurrence = Counter()
    for post in hashtag.posts:
        for ht in post.hashtags:
            if ht.name != hashtag_name:
                co_occurrence[ht.name] += 1

    total_posts = len(hashtag.posts)
    return [ht for ht, count in co_occurrence.items() if (count / total_posts) > 0.3]
