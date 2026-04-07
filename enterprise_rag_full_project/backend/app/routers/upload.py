from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import SessionLocal
from app.db import crud
from app.services.text_utils import chunk_text

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        text = raw.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode uploaded file")

    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="File has no readable text")

    user_row = crud.get_user_by_username(db, user["sub"])
    if not user_row:
        raise HTTPException(status_code=401, detail="User not found")

    doc = crud.create_document(db, user_row.id, file.filename or "document.txt", text)
    chunks = chunk_text(text)

    for idx, chunk in enumerate(chunks):
        crud.add_chunk(db, doc.id, idx, chunk)

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "chunks_created": len(chunks),
    }
