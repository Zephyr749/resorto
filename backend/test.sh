#!/bin/bash

# Run tests with virtual environment
echo "Running tests..."
if [ -d ".venv" ]; then
    .venv/bin/python -m pytest tests/ -v --tb=short
else
    python -m pytest tests/ -v --tb=short
fi
