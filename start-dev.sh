#!/bin/bash

# Development startup script for HLS Video Platform
# Starts both backend and frontend servers

echo "🚀 Starting HLS Video Platform Development Servers..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if setup was run
if [ ! -d "backend/venv" ] || [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}❌ Dependencies not installed!${NC}"
    echo -e "${YELLOW}Please run setup first:${NC}"
    echo ""
    echo "  ./setup.sh"
    echo ""
    exit 1
fi

echo ""
echo -e "${BLUE}Starting Backend Server (port 8001)...${NC}"

# Start backend in background
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait a bit for backend to start
sleep 2

echo -e "${BLUE}Starting Frontend Server (port 3000)...${NC}"

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Both servers are running!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8001"
echo "📚 API Docs:  http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Kill any remaining processes
    pkill -f "python main.py" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    echo -e "${GREEN}✓ Servers stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait indefinitely
wait
