from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.db import models
from passlib.hash import pbkdf2_sha256

def create_user(db: Session, username: str, password: str):
    user = models.User(username=username, password_hash=pbkdf2_sha256.hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.execute(select(models.User).where(models.User.username == username)).scalar_one_or_none()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and pbkdf2_sha256.verify(password, user.password_hash):
        return user
    return None

def create_document(db: Session, user_id: int, filename: str, content: str):
    doc = models.Document(user_id=user_id, filename=filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def add_chunk(db: Session, document_id: int, chunk_index: int, content: str):
    chunk = models.Chunk(document_id=document_id, chunk_index=chunk_index, content=content)
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk

def list_chunks_for_user(db: Session, user_id: int):
    stmt = (
        select(models.Chunk)
        .join(models.Document, models.Chunk.document_id == models.Document.id)
        .where(models.Document.user_id == user_id)
        .order_by(models.Chunk.id.asc())
    )
    return list(db.execute(stmt).scalars().all())

def list_documents_for_user(db: Session, user_id: int):
    stmt = select(models.Document).where(models.Document.user_id == user_id).order_by(desc(models.Document.id))
    return list(db.execute(stmt).scalars().all())

def save_chat(db: Session, user_id: int, query: str, response: str, sources: str):
    chat = models.Chat(user_id=user_id, query=query, response=response, sources=sources)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def list_chats_for_user(db: Session, user_id: int, limit: int = 20):
    stmt = (
        select(models.Chat)
        .where(models.Chat.user_id == user_id)
        .order_by(desc(models.Chat.id))
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())
