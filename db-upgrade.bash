#!/bin/bash
set -e

echo "🗄️  Starting database setup..."

# Wait for PostgreSQL to be ready
MAX_RETRIES=30
RETRY_COUNT=0
DB_READY=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if python - <<PY
import os, sys, asyncio, asyncpg
async def check():
    try:
        await asyncpg.connect(f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}")
        print('db-ready')
    except Exception:
        sys.exit(1)
asyncio.run(check())
PY
  then
    DB_READY=1
    echo "✅ Database is ready"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "⏳ Waiting for database... ($RETRY_COUNT/$MAX_RETRIES)"
  sleep 1
done

if [ $DB_READY -eq 0 ]; then
  echo "❌ Database is not ready after $MAX_RETRIES attempts"
  exit 1
fi

# Initialize database with aerich
echo "🛠️  Running Aerich init-db..."
aerich init-db

echo "🛠️  Running Aerich migrations..."
aerich upgrade
echo "✅ Database setup complete"