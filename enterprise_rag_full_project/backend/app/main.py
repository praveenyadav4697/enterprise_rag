from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.routers import auth, upload, chat, history

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(upload.router, prefix="/documents", tags=["documents"])
app.include_router(chat.router, tags=["chat"])
app.include_router(history.router, tags=["history"])

@app.get("/")
def root():
    return {"status": "ok", "app": settings.app_name}

@app.get("/health")
def health():
    return {"status": "healthy"}
