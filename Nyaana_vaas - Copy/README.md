# NYAYA-VAANI System - Production Architecture

The system has been fully refactored for production-grade robustness.

## Architecture & Data Flow

This system uses a distributed event-driven architecture to ensure heavy machine-learning NLP/OCR tasks do not crash the primary API event loop. 

1. **FastAPI (`backend/app/main.py`)**: The core entry point, routing asynchronous HTTP traffic. Runs purely concurrent non-blocking tasks.
2. **LangGraph State (`backend/app/agents/langgraph_pipeline.py`)**: A deterministic execution graph orchestrating security filtering and logic, with SQLite-backed checkpoint state mapping.
3. **ChromaDB (`backend/app/services/vector_store.py`)**: A local vector database containing dense embeddings (SentenceTransformers) for accurate legal search querying.
4. **Celery Worker (`backend/app/workers/ocr_worker.py`)**: A **critical** dedicated worker queue layer. PaddleOCR is a heavy ~500MB+ Machine Learning model that maxes out CPU. We load it *only* inside the isolated Celery worker process, preventing global memory crashes limits on Uvicorn.
5. **Redis Queue**: The message broker linking FastAPI and Celery.
6. **APScheduler**: Fired within the FastAPI lifespan to ingest automated civic data every night.
7. **Model Context Protocol (MCP)**: Server wrapper exposing the backend functions logically.

## Deployment Instructions (Production)
Do not run this application monolithically on a single thread. You must run the multi-container components. For production, PostgreSQL is highly recommended for the Audit Logs instead of the default SQLite dev fallback.

1. **Start PostgreSQL & Redis (Docker)**:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:15
docker run -d -p 6379:6379 redis
```

2. **Configure Database & Start FastAPI API**:
```bash
# In .env: DATABASE_URL=postgresql+asyncpg://postgres:secret@localhost:5432/postgres
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

3. **Start OCR Celery Worker (Hardened for OOM Protection)**:
*PaddleOCR is a heavy model. We restrict concurrency and add a memory limit (`--max-memory-per-child`) to prevent out-of-memory (OOM) cascading crashes.*
```bash
cd backend
celery -A app.services.job_queue.celery_app worker --loglevel=info --concurrency=1 --max-memory-per-child=1024000
```

4. **Start Frontend Client**:
```bash
cd frontend
npm run dev
```

5. **Observability Metrics**:
Prometheus metrics are available at `/metrics` mapping vector DB latency and Escalation Queue hits.
