# Strategic Futures AI

A web application that generates diverse future scenarios and strategic recommendations for companies using a 3-agent LangGraph pipeline powered by Groq (Llama 3.1 70B) and Tavily search.

## Features

- **3-Agent Pipeline**: Research → Scenario Generation → Strategy Recommendations
- **Real-time Updates**: Server-Sent Events (SSE) for live progress tracking
- **Comprehensive Analysis**: Industry research, competitive landscape, emerging trends
- **Diverse Scenarios**: 4 future scenarios based on multiple strategic axes
- **Strategic Recommendations**: 2-3 actionable strategies per scenario

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL + SQLAlchemy + Alembic
- LangGraph for multi-agent orchestration
- Groq API (Llama 3.1 70B)
- Tavily API for web search
- JWT authentication

### Frontend
- Vite + React + TypeScript
- TailwindCSS
- Server-Sent Events for real-time updates

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and database URL
```

5. Initialize database:
```bash
# Create PostgreSQL database
createdb strategic_futures_db

# Run migrations
alembic upgrade head
```

6. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Run the development server:
```bash
npm run dev
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `GROQ_API_KEY`: Groq API key
- `TAVILY_API_KEY`: Tavily API key
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Frontend (.env)
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/analyses` - Create new analysis
- `GET /api/analyses` - List user's analyses
- `GET /api/analyses/{id}` - Get analysis details
- `GET /api/analyses/{id}/stream` - SSE stream for real-time progress

## Project Structure

```
backend/
  app/
    agents/          # LangGraph agents
    services/        # External API clients
    models/          # SQLAlchemy models
    api/             # FastAPI routes
    core/            # Configuration and utilities
  alembic/           # Database migrations

frontend/
  src/
    components/      # React components
    pages/           # Page components
    services/        # API clients
    hooks/           # Custom React hooks
```

## License

MIT

