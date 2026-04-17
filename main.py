from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db

app = FastAPI()


@app.get("/posts")
def postBlog():
    return "Hi"


@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
