from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.core.security import get_current_user
from app.db.session import SessionLocal
from app.db import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/history")
def history(user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_row = crud.get_user_by_username(db, user["sub"])
    if not user_row:
        raise HTTPException(status_code=401, detail="User not found")

    chats = crud.list_chats_for_user(db, user_row.id, limit=20)
    return [
        {
            "id": c.id,
            "query": c.query,
            "response": c.response,
            "sources": json.loads(c.sources or "[]"),
        }
        for c in chats
    ]
