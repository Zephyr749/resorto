#!/bin/bash

# Resorto - Start Both Backend and Frontend
# This script starts both the backend API and frontend development server

echo "🚀 Starting Resorto..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
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

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Backend directory not found!${NC}"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Frontend directory not found!${NC}"
    exit 1
fi

# Check if backend virtual environment exists
if [ ! -d "backend/.venv" ]; then
    echo -e "${RED}❌ Backend virtual environment not found!${NC}"
    echo "Please run: cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}❌ Frontend dependencies not installed!${NC}"
    echo "Please run: cd frontend && npm install"
    exit 1
fi

echo -e "${BLUE}📦 Starting Backend API...${NC}"
cd backend
.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

echo -e "${BLUE}📦 Starting Frontend Dev Server...${NC}"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
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
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
