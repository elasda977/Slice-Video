#!/bin/bash

# Setup script for HLS Video Platform
# Run this ONCE to install all dependencies

set -e  # Exit on any error

echo "🔧 Setting up HLS Video Platform..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3:"
    echo "  sudo pacman -S python  # Arch Linux"
    echo "  sudo apt install python3 python3-venv  # Ubuntu/Debian"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
echo ""

# Check for Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found!${NC}"
    echo "Please install Node.js:"
    echo "  sudo pacman -S nodejs npm  # Arch Linux"
    echo "  sudo apt install nodejs npm  # Ubuntu/Debian"
    exit 1
fi
NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
echo -e "${GREEN}✓ Found Node: $NODE_VERSION${NC}"
echo -e "${GREEN}✓ Found npm: $NPM_VERSION${NC}"
echo ""

# Check for FFmpeg
echo -e "${BLUE}Checking FFmpeg...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠ FFmpeg not found!${NC}"
    echo "FFmpeg is required for video conversion."
    echo "Install it with:"
    echo "  sudo pacman -S ffmpeg  # Arch Linux"
    echo "  sudo apt install ffmpeg  # Ubuntu/Debian"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
    echo -e "${GREEN}✓ Found: $FFMPEG_VERSION${NC}"
fi
echo ""

# Setup Backend
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend setup complete!${NC}"
cd ..
echo ""

# Setup Frontend
echo -e "${BLUE}Setting up Frontend...${NC}"
cd frontend

# Remove old node_modules if exists
if [ -d "node_modules" ]; then
    echo "Removing old node_modules..."
    rm -rf node_modules package-lock.json
fi

# Install dependencies
echo "Installing Node.js dependencies (this may take a few minutes)..."
npm install

echo -e "${GREEN}✓ Frontend setup complete!${NC}"
cd ..
echo ""

# Create .env file
echo -e "${BLUE}Setting up environment...${NC}"
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}⚠ Remember to change SECRET_KEY in backend/.env for production!${NC}"
else
    echo ".env file already exists, skipping..."
fi
echo ""

# Create data directory
mkdir -p backend/data
echo -e "${GREEN}✓ Data directory created${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To start the application, run:"
echo -e "${BLUE}  ./start-dev.sh${NC}"
echo ""
echo "Or manually start servers:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
