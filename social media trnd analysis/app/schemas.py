from pydantic import BaseModel
from typing import List

class HashtagBase(BaseModel):
    name: str

class HashtagCreate(HashtagBase):
    pass

class HashtagOut(HashtagBase):
    id: int
    frequency: int | None = None
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    content: str

class PostOut(PostBase):
    id: int
    hashtags: List[HashtagOut] = []
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str
    user_id: int
    post_id: int

from typing import Optional, List

class CommentResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    polarity: float
    subjectivity: float
    user_id: int
    post_id: int
    parent_id: Optional[int] = None
    replies: List['CommentResponse'] = []

    class Config:
        from_attributes = True

CommentResponse.model_rebuild()