#!/bin/bash

# Resorto - Development Mode with Live Logs
# This script starts both services and shows live logs

echo "🚀 Starting Resorto in Development Mode..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Resorto..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup INT TERM

# Check directories
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Backend or Frontend directory not found!${NC}"
    exit 1
fi

if [ ! -d "backend/.venv" ]; then
    echo -e "${RED}❌ Backend virtual environment not found!${NC}"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}❌ Frontend dependencies not installed!${NC}"
    exit 1
fi

# Start backend
echo -e "${BLUE}📦 Starting Backend API on port 8000...${NC}"
cd backend
.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend
echo -e "${BLUE}📦 Starting Frontend Dev Server on port 3000...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3

echo ""
echo -e "${GREEN}✅ Resorto is running!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Backend API:${NC}      http://localhost:8000"
echo -e "${GREEN}API Docs:${NC}         http://localhost:8000/docs"
echo -e "${GREEN}Frontend:${NC}         http://localhost:3000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}👀 Watching for changes (hot reload enabled)${NC}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
