#!/bin/bash

# Database Setup Script for Strategic Futures AI
# This script checks PostgreSQL status and runs migrations

set -e

echo "🔍 Checking PostgreSQL status..."

# Check if PostgreSQL is running
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL is not running"
    echo ""
    echo "Please start PostgreSQL:"
    echo "  - If using Postgres.app: Open Postgres.app from Applications"
    echo "  - If using Homebrew: Run 'brew services start postgresql@14' (or your version)"
    echo "  - If using system service: Run 'sudo systemctl start postgresql' (Linux)"
    echo ""
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if database exists
echo "🔍 Checking if database exists..."
DB_NAME=$(python -c "from app.core.config import settings; import re; match = re.search(r'/([^/]+)$', settings.DATABASE_URL); print(match.group(1) if match else 'strategic_futures_db')")

# Extract connection details
DB_USER=$(python -c "from app.core.config import settings; import re; match = re.search(r'://([^:]+):', settings.DATABASE_URL); print(match.group(1) if match else 'user')")
DB_HOST=$(python -c "from app.core.config import settings; import re; match = re.search(r'@([^:]+):', settings.DATABASE_URL); print(match.group(1) if match else 'localhost')")

echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Host: $DB_HOST"

# Try to connect and check if database exists
if psql -h "$DB_HOST" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✅ Database '$DB_NAME' exists"
else
    echo "📝 Database '$DB_NAME' does not exist. Creating..."
    createdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" || {
        echo "❌ Failed to create database. You may need to create it manually:"
        echo "   createdb $DB_NAME"
        exit 1
    }
    echo "✅ Database '$DB_NAME' created"
fi

# Run migrations
echo ""
echo "🔄 Running Alembic migrations..."
alembic upgrade head

echo ""
echo "✅ Database setup complete!"
echo ""
echo "You can now start the backend server:"
echo "  uvicorn main:app --reload"

