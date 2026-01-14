# Strategic Futures AI

An AI-powered web application that generates diverse future scenarios and strategic recommendations for companies using a multi-agent LangGraph pipeline.

## Overview

Strategic Futures AI helps organizations explore potential future scenarios and develop strategic recommendations. It uses a 3-agent pipeline powered by Groq's Llama 3.1 70B and Tavily's web search:

1. **Research Agent** - Conducts industry research, competitive landscape analysis, and identifies emerging trends
2. **Scenario Agent** - Generates 4 diverse future scenarios based on strategic axes
3. **Strategy Agent** - Develops actionable strategic recommendations for each scenario

The application provides real-time progress updates using Server-Sent Events (SSE).

## Key Features

- Multi-agent AI pipeline with specialized research, scenario, and strategy agents
- Real-time progress tracking via Server-Sent Events
- Comprehensive industry research and competitive analysis
- Diverse scenario planning based on strategic frameworks
- Actionable recommendations for each scenario
- Analysis history to save and revisit previous analyses
- Modern, responsive UI built with React and TailwindCSS

## Tech Stack

**Backend**
- FastAPI - Python web framework
- PostgreSQL - Database
- SQLAlchemy & Alembic - ORM and migrations
- LangGraph - Multi-agent orchestration
- Groq API - LLM inference (Llama 3.1 70B)
- Tavily API - Web search

**Frontend**
- React & TypeScript
- Vite - Build tool
- TailwindCSS - Styling
- React Router - Routing
- Axios - HTTP client

## Prerequisites

You'll need the following installed:
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git

You'll also need API keys (free tiers available):
- Groq: [https://console.groq.com/keys](https://console.groq.com/keys)
- Tavily: [https://app.tavily.com/](https://app.tavily.com/)

## Getting Started

### 1. Clone and Configure

```bash
git clone https://github.com/pzavar/strategic-futures-brainstorm.git
cd strategic-futures-brainstorm
```

### 2. Set Up Environment Variables

Create `backend/.env` file with your values:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/strategic_futures_db
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Create `frontend/.env` file (default values should work for local development):
```bash
VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Ensure PostgreSQL is running, then create database
createdb strategic_futures_db

# Run migrations
alembic upgrade head
```

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

## Running the Application

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open your browser to [http://localhost:5173](http://localhost:5173)

1. Enter a company name to analyze
2. Watch the AI agents work in real-time

## Project Structure

```
strategic-futures-brainstorm/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangGraph AI agents (pipeline, research, scenario, strategy)
│   │   ├── api/              # API routes (analyses) and dependencies
│   │   ├── core/             # Configuration, database, security
│   │   ├── models/           # SQLAlchemy models (analysis, scenario, strategy, search_query)
│   │   └── services/         # External API clients (Groq, Tavily)
│   ├── alembic/              # Database migrations
│   ├── tests/                # Unit and integration tests
│   └── main.py               # FastAPI entry point
│
└── frontend/
    └── src/
        ├── components/       # React components
        ├── pages/            # Page components
        ├── services/         # API clients (REST, SSE)
        ├── hooks/            # Custom React hooks
        └── App.tsx           # Root component
```

## API Documentation

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI documentation.

**Key Endpoints:**
- `POST /api/analyses` - Create a new analysis
- `GET /api/analyses` - List all analyses
- `GET /api/analyses/{id}` - Get specific analysis details
- `GET /api/analyses/{id}/stream` - SSE stream for real-time updates

## Troubleshooting

**Database Connection Issues**
```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (macOS)
brew services start postgresql@14
```

**API Key Issues**
- Verify API keys in `backend/.env`
- Ensure no extra spaces or quotes around keys
- Regenerate keys if needed

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn main:app --reload --port 8001
```

**Module Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

For more help, see `TROUBLESHOOTING.md` in the backend directory.

## Contributing

Contributions are welcome! 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow the existing code style, add tests for new features, and update documentation as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Groq for fast LLM inference
- Tavily for AI-powered web search
- LangGraph for multi-agent orchestration

---

For questions or feedback, please open an issue on GitHub.

