# Enterprise RAG Platform

A GitHub-ready full-stack project with:
- FastAPI backend
- PostgreSQL database
- JWT authentication
- Document upload
- RAG-style retrieval
- Chat history
- Streamlit frontend
- Docker + docker-compose

## Quick start with Docker
1. Create `backend/.env` from `backend/.env.example`
2. Run:
```bash
docker compose up --build
```

Open:
- Backend docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

## Local development
Use Python `3.11` for local development. The current backend dependency pins do not install cleanly on Python `3.14`, so do not reuse a root `.venv` created with `3.14`.

Backend:
```bash
cd backend
py -3.11 -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
# create backend/.env from backend/.env.example and set DATABASE_URL to match your local PostgreSQL credentials
uvicorn app.main:app --reload
```

If you are running PostgreSQL locally, either:
- create a `ragdb` database with user `raguser` and password `ragpass`, or
- update `backend/.env` so `DATABASE_URL` matches your existing PostgreSQL user, password, host, port, and database.

Frontend:
```bash
cd frontend
py -3.11 -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- This project uses a safe local retrieval engine, so it works without an LLM API key.
- If you add `OPENAI_API_KEY`, you can later plug in a model in `app/services/llm.py`.
- PostgreSQL is used for users, documents, chunks, and chat history.
