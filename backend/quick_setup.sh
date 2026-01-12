#!/bin/bash

# Quick setup script - run this once PostgreSQL is started
# Usage: ./quick_setup.sh

set -e

echo "🚀 Quick Database Setup"
echo ""

# Check PostgreSQL
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running"
    echo ""
    echo "Please start PostgreSQL first:"
    echo "  - Open Postgres.app from Applications, OR"
    echo "  - Run: brew services start postgresql@14"
    echo ""
    exit 1
fi

echo "✅ PostgreSQL is running"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Extract database name from .env
DB_NAME=$(python -c "from app.core.config import settings; import re; match = re.search(r'/([^/]+)(?:\?|$)', settings.DATABASE_URL); print(match.group(1) if match else 'strategic_futures_db')")

echo "📦 Database: $DB_NAME"
echo ""

# Create database if it doesn't exist
if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✅ Database '$DB_NAME' already exists"
else
    echo "📝 Creating database '$DB_NAME'..."
    createdb "$DB_NAME" || {
        echo "⚠️  Note: If creation failed, you may need to create it manually:"
        echo "   createdb $DB_NAME"
    }
    echo "✅ Database created"
fi

echo ""
echo "🔄 Running migrations..."
alembic upgrade head

echo ""
echo "✅ Setup complete! You can now start the server:"
echo "   uvicorn main:app --reload"
echo ""

