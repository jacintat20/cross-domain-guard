#!/usr/bin/env bash
set -e

echo "=== Running Local Unit and Integration Tests ==="
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
pytest tests/

echo "=== Building and Starting Container Stack ==="
docker compose up --build -d

echo "=== System Health Check ==="
sleep 2
curl -s http://localhost:8000/docs > /dev/null && echo "Guard Service is live at http://localhost:8000"