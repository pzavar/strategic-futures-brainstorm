# Quick Start Guide 🚀

This is a condensed guide to get you up and running in under 5 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.11+)
python --version

# Check Node.js version (need 18+)
node --version

# Check PostgreSQL (need 14+)
psql --version

# Start PostgreSQL if not running
brew services start postgresql@14  # macOS
# OR
sudo systemctl start postgresql    # Linux
```

## 1. Clone & Setup API Keys (2 minutes)

```bash
# Clone the repo
git clone https://github.com/yourusername/strategic-futures-brainstorm.git
cd strategic-futures-brainstorm

# Setup backend environment
cd backend
cp .env.example .env
```

**Edit `backend/.env` and add your API keys:**
- Get Groq key: https://console.groq.com/keys
- Get Tavily key: https://app.tavily.com/

```bash
# Setup frontend environment  
cd ../frontend
cp .env.example .env
# (Default values are fine for local dev)
```

## 2. Backend Setup (2 minutes)

```bash
cd ../backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb strategic_futures_db
alembic upgrade head
```

## 3. Frontend Setup (1 minute)

```bash
cd ../frontend
npm install
```

## 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 5. Access the App

Open your browser: **http://localhost:5173**

1. Register an account
2. Login
3. Enter a company name
4. Watch the AI work! 🎉

## Troubleshooting

**Database connection failed?**
```bash
# Make sure PostgreSQL is running
pg_isready
brew services restart postgresql@14
```

**Port already in use?**
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

**Module not found?**
```bash
# Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

For detailed troubleshooting, see the main README.md or TROUBLESHOOTING.md files.
