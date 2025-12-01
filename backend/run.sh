#!/bin/bash

# Run the FastAPI application
echo "Starting FastAPI server..."
echo "API docs available at: http://localhost:8000/docs"

if [ -d ".venv" ]; then
    .venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi
