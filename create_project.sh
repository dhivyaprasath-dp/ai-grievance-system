#!/usr/bin/env bash
set -euo pipefail

WORKDIR="$(pwd)"

echo "📁 Creating AI-Powered Grievance System skeleton..."

mkdir -p backend/app/api backend/app/nlp backend/app/tests frontend/css frontend/js data docs .github/workflows

# Create placeholder README
echo "# AI-Powered Grievance Redressal System" > README.md

# Create Docker Compose
cat > docker-compose.yml <<'EOF'
version: '3.8'
services:
  backend:
    build: ./backend
    env_file:
      - .env.example
    ports:
      - "5000:5000"
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD=rootpassword
      MYSQL_DATABASE=grievance_db
      MYSQL_USER=grievance_user
      MYSQL_PASSWORD=grievance_pass
    ports:
      - "3306:3306"
EOF

echo "Skeleton created successfully at $WORKDIR"

