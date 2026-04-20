from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import BlogCreate, create_blog, delete_blog, get_blog, init_db, list_blogs, update_blog
from db import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def post_blog(payload: BlogCreate, db: Session = Depends(get_db)):
    return create_blog(db, payload)


@app.get("/blogs")
def get_blogs(db: Session = Depends(get_db)):
    return list_blogs(db)


@app.get("/blogs/{blog_id}")
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    row = get_blog(db, blog_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return row


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    if not delete_blog(db, blog_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")


@app.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def update_blog_by_id(
    blog_id: int,
    payload: BlogCreate,
    db: Session = Depends(get_db),
):
    row = update_blog(db, blog_id, payload)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return row



@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
