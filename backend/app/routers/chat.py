import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import SessionLocal
from app.db import crud
from app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from app.services.rag import retrieve, generate_answer

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_row = crud.get_user_by_username(db, user["sub"])
    if not user_row:
        raise HTTPException(status_code=401, detail="User not found")

    documents = crud.list_documents_for_user(db, user_row.id)
    chunks = crud.list_chunks_for_user(db, user_row.id)

    ranked = retrieve(payload.query, chunks=chunks, documents=documents, top_k=5)
    answer = generate_answer(payload.query, ranked)

    source_items = [
        SourceItem(
            document_id=s.document_id,
            filename=s.filename,
            chunk_index=s.chunk_index,
            content=s.content,
        )
        for s in ranked
    ]

    crud.save_chat(
        db,
        user_row.id,
        payload.query,
        answer,
        sources=json.dumps([item.model_dump() for item in source_items], ensure_ascii=False),
    )

    return ChatResponse(answer=answer, sources=source_items)
