
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()
    with open("app/data/sample_posts.json") as f:
        posts_data = json.load(f)

    users = {}
    for post in posts_data:
        username = post["user"]
        # Check if user already exists in DB
        user = db.query(models.User).filter_by(username=username).first()
        if not user:
            user = models.User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        users[username] = user

        new_post = models.Post(content=post["content"], author=users[username])
        db.add(new_post)

        for word in post["content"].split():
            if word.startswith("#"):
                hashtag_text = word[1:]
                hashtag = db.query(models.Hashtag).filter_by(name=hashtag_text).first()
                if not hashtag:
                    hashtag = models.Hashtag(name=hashtag_text)
                    db.add(hashtag)
                    db.commit()
                    db.refresh(hashtag)
                new_post.hashtags.append(hashtag)

        db.commit()

if __name__ == "__main__":
    seed()
    print("✅ Database seeded with sample posts and hashtags!")
