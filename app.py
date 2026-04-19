from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Base, Blog, engine


class BlogCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    tags: list[str] = Field(..., min_length=1)


def init_db() -> None:
    """Create database tables from models (safe to call on every startup)."""
    Base.metadata.create_all(bind=engine)


def _blog_as_dict(blog: Blog) -> dict:
    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "category": blog.category,
        "tags": blog.tags,
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
    }


def list_blogs(db: Session) -> list[dict]:
    stmt = select(Blog).order_by(Blog.id)
    rows = db.scalars(stmt).all()
    return [_blog_as_dict(b) for b in rows]


def create_blog(db: Session, payload: BlogCreate) -> dict:
    blog = Blog(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        tags=payload.tags,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return _blog_as_dict(blog)
