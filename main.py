from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import BlogCreate, create_blog, init_db, list_blogs
from db import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def post_blog(payload: BlogCreate, db: Session = Depends(get_db)):
    return create_blog(db, payload)


@app.get("/getBlogs")
def get_blogs(db: Session = Depends(get_db)):
    return list_blogs(db)


@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
