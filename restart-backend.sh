#!/bin/bash

# Restart Backend Script

echo "🔄 Restarting Backend Server..."

# Kill existing backend
echo "Stopping old backend process..."
pkill -f "main.py" 2>/dev/null || true
sleep 1

# Start new backend
echo "Starting backend server..."
cd /mnt/DATA/Project/video-segment-cutter/backend
source venv/bin/activate
nohup python main.py > /tmp/backend.log 2>&1 &

sleep 3

# Check if it started
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Backend server started successfully!"
    echo "📍 Running on: http://localhost:8001"
    echo "📚 API Docs: http://localhost:8001/docs"
    echo ""
    echo "View logs: tail -f /tmp/backend.log"
else
    echo "❌ Failed to start backend server"
    echo "Check logs: cat /tmp/backend.log"
    exit 1
fi
