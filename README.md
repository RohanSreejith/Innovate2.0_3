# Innovate2.0_3 - NYAYA-VAANI System

**NYAYA-VAANI** is a production-grade, AI-powered legal assistance platform designed to democratize access to legal information in India. The system leverages advanced NLP, OCR, and multimodal AI to help users understand Indian legal codes, file FIRs, generate legal documents, and query legal databases.

## 🌟 Features

- **Legal Document OCR**: Extract and structure information from scanned legal documents using PaddleOCR
- **Intelligent Legal Search**: Vector-based semantic search across IPC sections, BSA (Bharatiya Sakshya Adhiniyam), and case laws
- **FIR Generation**: Automated First Information Report generation with structured data extraction
- **Legal Template Service**: Generate legal documents based on user queries
- **Multimodal AI Integration**: Support for text, voice, and image inputs
- **Real-time Metrics**: Prometheus-based observability for system monitoring
- **Production Architecture**: Event-driven, distributed system with proper isolation of heavy ML workloads

## 🏗️ Architecture

The system uses a **distributed event-driven architecture** to ensure heavy machine-learning NLP/OCR tasks do not crash the primary API event loop:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│   Celery    │
│  Frontend   │     │   Backend    │     │   Worker    │
│ (Vite + TS) │◀────│  (Async)     │◀────│ (OCR Tasks) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                     │
                           │                     │
                    ┌──────▼──────┐       ┌─────▼──────┐
                    │  ChromaDB   │       │   Redis    │
                    │ Vector Store│       │   Queue    │
                    └─────────────┘       └────────────┘
```

### Key Components

1. **FastAPI Backend** (`backend/app/main.py`): Core entry point routing asynchronous HTTP traffic
2. **LangGraph State Machine** (`backend/app/agents/`): Deterministic execution graph with SQLite-backed checkpoints
3. **ChromaDB** (`backend/app/services/vector_store.py`): Local vector database with SentenceTransformer embeddings
4. **Celery Worker** (`backend/app/workers/`): Isolated process for heavy ML models (PaddleOCR ~500MB+)
5. **Redis**: Message broker linking FastAPI and Celery
6. **APScheduler**: Automated civic data ingestion
7. **Model Context Protocol (MCP)**: Server wrapper exposing backend functions

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Redis
- PostgreSQL (recommended for production) or SQLite (development)
- Docker (optional, for containerized deployment)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/RohanSreejith/Innovate2.0_3.git
cd Innovate2.0_3/Nyaana_vaas\ -\ Copy
```

#### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite+aiosqlite:///./nyaya_vaani.db
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
REDIS_URL=redis://localhost:6379
EOF
```

#### 3. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file (if needed)
echo "VITE_API_URL=http://localhost:8000" > .env
```

#### 4. Prepare Datasets (Optional but Recommended)

Follow the instructions in [`DATASET_INSTRUCTIONS.md`](Nyaana_vaas%20-%20Copy/DATASET_INSTRUCTIONS.md) to download and place the required datasets:
- Indian Penal Code (IPC) sections
- Bharatiya Sakshya Adhiniyam (BSA) documents
- Case laws and judgments
- FIR data (optional)

## 🏃 Running the Application

### Development Mode

**Important**: Do not run this application monolithically on a single thread. You must run multiple components separately.

#### Terminal 1: Start Redis (Docker)
```bash
docker run -d -p 6379:6379 redis
```

Or install and run Redis locally:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
redis-server

# macOS
brew install redis
brew services start redis
```

#### Terminal 2: Start Backend API
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 3: Start Celery Worker (Critical for OCR)
```bash
cd backend
source venv/bin/activate
celery -A app.services.job_queue.celery_app worker --loglevel=info --concurrency=1 --max-memory-per-child=1024000
```

**Note**: The `--max-memory-per-child` flag prevents OOM crashes from the heavy PaddleOCR model.

#### Terminal 4: Start Frontend
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

### Production Deployment

For production, use PostgreSQL instead of SQLite:

```bash
# Start PostgreSQL & Redis
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:15
docker run -d -p 6379:6379 redis

# Update .env with PostgreSQL URL
DATABASE_URL=postgresql+asyncpg://postgres:secret@localhost:5432/postgres

# Start FastAPI with multiple workers
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Start Celery worker
celery -A app.services.job_queue.celery_app worker --loglevel=info --concurrency=1 --max-memory-per-child=1024000

# Build and serve frontend
cd frontend
npm run build
npm run preview
```

## 📊 Monitoring & Observability

Prometheus metrics are available at `/metrics` endpoint, tracking:
- Vector DB query latency
- Escalation queue hits
- API request rates
- Error rates

## 🧪 Testing

```bash
cd backend
pytest tests/
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/ocr/process`: Process images with OCR
- `POST /api/legal/search`: Search legal database
- `POST /api/fir/generate`: Generate FIR documents
- `GET /api/metrics`: System metrics
- `POST /api/multimodal/query`: Multimodal query processing

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: Google ADK, LiteLLM, Groq, SentenceTransformers
- **OCR**: PaddleOCR
- **Vector Database**: ChromaDB
- **State Management**: LangGraph with SQLite checkpoints
- **Task Queue**: Celery + Redis
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Monitoring**: Prometheus

### Frontend
- **Framework**: React 19
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Framer Motion, Lucide React
- **Charts**: Recharts
- **Routing**: React Router

## 🔒 Security Features

- Rate limiting via SlowAPI
- Input validation and sanitization
- Security guardrails for AI queries
- Circuit breaker pattern for external API calls
- Audit logging for all operations

## 📁 Project Structure

```
Innovate2.0_3/
└── Nyaana_vaas - Copy/
    ├── backend/
    │   ├── app/
    │   │   ├── agents/         # LangGraph state machines
    │   │   ├── api/            # API routes
    │   │   ├── db/             # Database models
    │   │   ├── guardrails/     # Security filters
    │   │   ├── llm/            # LLM client integrations
    │   │   ├── mcp/            # Model Context Protocol
    │   │   ├── services/       # Business logic
    │   │   ├── state/          # State management
    │   │   ├── utils/          # Utility functions
    │   │   ├── workers/        # Celery workers
    │   │   └── main.py         # FastAPI entry point
    │   ├── tests/              # Test suite
    │   └── requirements.txt    # Python dependencies
    ├── frontend/
    │   ├── src/
    │   │   ├── components/     # React components
    │   │   ├── pages/          # Page components
    │   │   ├── state/          # State management
    │   │   └── App.tsx         # Main app component
    │   ├── package.json        # Node dependencies
    │   └── vite.config.ts      # Vite configuration
    ├── README.md               # This file
    └── DATASET_INSTRUCTIONS.md # Dataset setup guide
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of Innovate 2.0 hackathon submission.

## 🆘 Troubleshooting

### Common Issues

1. **OCR not working**: Ensure Celery worker is running and Redis is accessible
2. **Vector search returning no results**: Check if datasets are properly loaded in `backend/app/data/`
3. **Frontend can't connect to backend**: Verify CORS settings and API URL in `.env`
4. **Memory issues**: Reduce Celery concurrency or increase `--max-memory-per-child` value

### Getting Help

- Check the [API Documentation](http://localhost:8000/docs) when backend is running
- Review logs in `backend/backend.log`
- Inspect Celery worker logs for OCR-related issues

## 🎯 Roadmap

- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] Mobile application
- [ ] Advanced case law analytics
- [ ] Integration with government legal databases
- [ ] Voice-to-text FIR filing
- [ ] Real-time legal consultation chatbot

## 👥 Authors

- Rohan Sreejith ([@RohanSreejith](https://github.com/RohanSreejith))

## 🙏 Acknowledgments

- Indian legal framework and datasets
- Open-source community
- Innovate 2.0 organizers
