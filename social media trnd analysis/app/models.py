from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .database import Base

# Many-to-many relationship between posts and hashtags
post_hashtag = Table(
    "post_hashtag",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("hashtag_id", ForeignKey("hashtags.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    hashtags = relationship("Hashtag", secondary=post_hashtag, back_populates="posts")


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    posts = relationship("Post", secondary=post_hashtag, back_populates="hashtags")

    @property
    def frequency(self):
        return len(self.posts)

# Indexes for optimal search (must be at module level, after class definitions)
user_username_index = Index('ix_users_username', User.username)
hashtag_name_index = Index('ix_hashtags_name', Hashtag.name)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    sentiment = Column(String(20), default="neutral")   # positive/negative/neutral
    polarity = Column(Float, default=0.0)
    subjectivity = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    replies = relationship("Comment", backref="parent", remote_side=[id])

# Indexes for optimal search (must be at module level, after class definitions)
user_username_index = Index('ix_users_username', User.username)
hashtag_name_index = Index('ix_hashtags_name', Hashtag.name)
