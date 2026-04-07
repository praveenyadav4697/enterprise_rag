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
Backend:
```bash
cd backend
python -m venv .venv
# activate your venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
python -m venv .venv
# activate your venv
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- This project uses a safe local retrieval engine, so it works without an LLM API key.
- If you add `OPENAI_API_KEY`, you can later plug in a model in `app/services/llm.py`.
- PostgreSQL is used for users, documents, chunks, and chat history.
