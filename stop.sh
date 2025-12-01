#!/bin/bash

# Resorto - Stop Both Backend and Frontend
# This script stops all running Resorto processes

echo "🛑 Stopping Resorto..."

# Find and kill backend process (uvicorn)
BACKEND_PID=$(ps aux | grep "uvicorn main:app" | grep -v grep | awk '{print $2}')
if [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
    echo "✅ Backend stopped (PID: $BACKEND_PID)"
else
    echo "ℹ️  Backend not running"
fi

# Find and kill frontend process (vite on port 3000)
FRONTEND_PID=$(lsof -ti:3000)
if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Frontend stopped (PID: $FRONTEND_PID)"
else
    echo "ℹ️  Frontend not running"
fi

# Clean up log files
if [ -f "backend.log" ]; then
    rm backend.log
    echo "🗑️  Cleaned backend.log"
fi

if [ -f "frontend.log" ]; then
    rm frontend.log
    echo "🗑️  Cleaned frontend.log"
fi

echo ""
echo "✅ Resorto stopped successfully"
