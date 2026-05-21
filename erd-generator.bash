#!/bin/bash

# PostgreSQL connection parameters
DB_HOST="${DATABASE_HOST:-localhost}"
DB_PORT="${DATABASE_PORT:-5432}"
DB_USER="${DATABASE_USER:-postgres}"
DB_PASSWORD="${DATABASE_PASSWORD:-postgres}"
DB_NAME="${DATABASE_NAME:-youtube_notifier}"

# Generate ERD from PostgreSQL
eralchemy -i "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}" \
  -o db-schema.png \
  --exclude-tables aerich \
  --exclude-columns created_at updated_at