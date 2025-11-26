from fastapi import FastAPI
from app.database import engine, Base
from .routes import hashtags, comments, users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Analytics - Hashtag Engine")

# Routers
app.include_router(hashtags.router)
app.include_router(comments.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hashtag Engine is running!"}
