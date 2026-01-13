# Strategic Futures AI 🔮

> An AI-powered web application that generates diverse future scenarios and strategic recommendations for companies using a multi-agent LangGraph pipeline.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up API Keys](#2-set-up-api-keys)
  - [3. Backend Setup](#3-backend-setup)
  - [4. Frontend Setup](#4-frontend-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Strategic Futures AI is a powerful tool that helps organizations explore potential future scenarios and develop strategic recommendations. It leverages a sophisticated 3-agent pipeline powered by **Groq's Llama 3.1 70B** and **Tavily's web search** to:

1. **Research Agent**: Conducts comprehensive industry research, competitive landscape analysis, and identifies emerging trends
2. **Scenario Agent**: Generates 4 diverse future scenarios based on strategic axes (certainty vs. uncertainty, opportunity vs. threat)
3. **Strategy Agent**: Develops 2-3 actionable strategic recommendations for each scenario

The application provides real-time progress updates using Server-Sent Events (SSE), allowing users to watch the AI agents work through each stage of the analysis.

## ✨ Features

- 🤖 **Multi-Agent AI Pipeline**: Three specialized agents working in sequence
- 📡 **Real-time Progress Tracking**: Live updates via Server-Sent Events
- 🔍 **Comprehensive Research**: Industry insights, competitive analysis, and trend identification
- 🎲 **Diverse Scenario Planning**: 4 distinct future scenarios based on strategic frameworks
- 💡 **Actionable Strategies**: Concrete recommendations for each scenario
- 📊 **Analysis History**: Save and revisit previous analyses
- 🔐 **Secure Authentication**: JWT-based user authentication
- 🎨 **Modern UI**: Clean, responsive interface built with React and TailwindCSS

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM and database toolkit
- **Alembic** - Database migrations
- **LangGraph** - Multi-agent orchestration
- **Groq API** - Fast LLM inference (Llama 3.1 70B)
- **Tavily API** - AI-powered web search
- **JWT** - Secure authentication

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** ([Download](https://www.python.org/downloads/))
- **Node.js 18 or higher** ([Download](https://nodejs.org/))
- **PostgreSQL 14 or higher** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))

You'll also need API keys from:
- **Groq** (free tier available): [https://console.groq.com/keys](https://console.groq.com/keys)
- **Tavily** (free tier available): [https://app.tavily.com/](https://app.tavily.com/)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/strategic-futures-brainstorm.git
cd strategic-futures-brainstorm
```

### 2. Set Up API Keys

#### Obtain Your API Keys

**Groq API Key:**
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Click "Create API Key"
4. Copy your API key (save it securely - you won't see it again!)

**Tavily API Key:**
1. Visit [https://app.tavily.com/](https://app.tavily.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Copy your API key

#### Configure Backend Environment

```bash
cd backend
cp .env.example .env
```

Open `backend/.env` in your text editor and replace the placeholder values:

```bash
# Update these with your actual values:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/strategic_futures_db
GROQ_API_KEY=your_actual_groq_api_key_here
TAVILY_API_KEY=your_actual_tavily_api_key_here

# Generate a secure JWT secret (you can use: openssl rand -hex 32)
JWT_SECRET=your_secure_random_string_here

# Leave these as default for local development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### Configure Frontend Environment

```bash
cd ../frontend
cp .env.example .env
```

The default values should work for local development:

```bash
VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
# Navigate to backend directory (if not already there)
cd backend

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create PostgreSQL database
createdb strategic_futures_db

# Run database migrations
alembic upgrade head
```

**Note:** If you don't have PostgreSQL running, start it first:
- **macOS** (Homebrew): `brew services start postgresql@14`
- **macOS** (Postgres.app): Open Postgres.app from Applications
- **Linux**: `sudo systemctl start postgresql`
- **Windows**: Start PostgreSQL service from Services panel

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

## 🎮 Running the Application

You'll need **two terminal windows** - one for the backend and one for the frontend.

### Terminal 1: Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start the Frontend

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Access the Application

Open your browser and navigate to: **[http://localhost:5173](http://localhost:5173)**

1. Create an account (Register)
2. Log in
3. Enter a company name to analyze
4. Watch the AI agents work in real-time!

## 📁 Project Structure

```
strategic-futures-brainstorm/
├── backend/
│   ├── app/
│   │   ├── agents/              # LangGraph AI agents
│   │   │   ├── pipeline.py      # Agent orchestration
│   │   │   ├── research_agent.py
│   │   │   ├── scenario_agent.py
│   │   │   └── strategy_agent.py
│   │   ├── api/
│   │   │   ├── routes/          # API endpoints
│   │   │   │   ├── analyses.py  # Analysis CRUD + streaming
│   │   │   │   └── auth.py      # Authentication
│   │   │   └── dependencies.py  # Dependency injection
│   │   ├── core/
│   │   │   ├── config.py        # Configuration settings
│   │   │   ├── database.py      # Database connection
│   │   │   └── security.py      # JWT authentication
│   │   ├── models/              # SQLAlchemy database models
│   │   │   ├── analysis.py
│   │   │   ├── scenario.py
│   │   │   ├── strategy.py
│   │   │   └── user.py
│   │   └── services/            # External API clients
│   │       ├── groq_service.py  # Groq LLM integration
│   │       └── tavily_service.py # Tavily search integration
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Unit and integration tests
│   ├── main.py                  # FastAPI application entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── CompanyInput.tsx
│   │   │   ├── AnalysisStatus.tsx
│   │   │   ├── AnalysisResults.tsx
│   │   │   ├── ScenarioCard.tsx
│   │   │   ├── StrategyCard.tsx
│   │   │   └── ...
│   │   ├── pages/               # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Login.tsx
│   │   │   └── AnalysisViewPage.tsx
│   │   ├── services/            # API clients
│   │   │   ├── api.ts           # REST API client
│   │   │   ├── auth.ts          # Authentication service
│   │   │   └── sse.ts           # Server-Sent Events client
│   │   ├── hooks/               # Custom React hooks
│   │   │   ├── useAuth.tsx
│   │   │   ├── useAnalysis.ts
│   │   │   └── useAnalysisStream.ts
│   │   └── App.tsx              # Root component
│   ├── package.json             # Node.js dependencies
│   └── .env.example             # Environment variables template
│
└── README.md                    # This file
```

## 📚 API Documentation

Once the backend is running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and receive JWT token |
| POST | `/api/analyses` | Create a new analysis |
| GET | `/api/analyses` | List all user's analyses |
| GET | `/api/analyses/{id}` | Get specific analysis details |
| GET | `/api/analyses/{id}/stream` | SSE stream for real-time updates |

## 🔧 Troubleshooting

### Database Connection Issues

**Error:** `could not connect to server: Connection refused`

**Solution:** Ensure PostgreSQL is running:
```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql@14

# Or restart it
brew services restart postgresql@14
```

### API Key Issues

**Error:** `401 Unauthorized` or `Invalid API key`

**Solution:** 
1. Verify your API keys in `backend/.env`
2. Make sure there are no extra spaces or quotes around the keys
3. Regenerate keys if needed from the respective platforms

### Port Already in Use

**Error:** `Address already in use`

**Solution:** 
```bash
# Find what's using port 8000 (backend)
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --reload --port 8001
```

### Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Issues

**Error:** npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Need More Help?

Check the `TROUBLESHOOTING.md` file in the backend directory or open an issue on GitHub.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to:
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing fast LLM inference
- **Tavily** for AI-powered web search capabilities
- **LangGraph** for multi-agent orchestration framework

---

**Built with ❤️ for strategic foresight and scenario planning**

For questions or feedback, please open an issue on GitHub.

