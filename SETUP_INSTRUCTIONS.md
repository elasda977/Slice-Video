# Setup Instructions

## 🚀 Quick Setup (2 Steps)

### Step 1: Run Setup Script

```bash
cd /mnt/DATA/Project/video-segment-cutter
./setup.sh
```

This will:
- ✅ Check for Python, Node.js, and FFmpeg
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Create `.env` configuration file
- ✅ Create necessary directories

**Time:** 2-5 minutes (depending on internet speed)

### Step 2: Start the Application

```bash
./start-dev.sh
```

This will:
- ✅ Start backend server on http://localhost:8001
- ✅ Start frontend server on http://localhost:3000
- ✅ Open both in background

**Done!** Open http://localhost:3000 in your browser.

---

## 🔧 Manual Setup (If Scripts Don't Work)

### Prerequisites

Install these first:

**Arch Linux:**
```bash
sudo pacman -S python nodejs npm ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-venv nodejs npm ffmpeg
```

**macOS:**
```bash
brew install python node ffmpeg
```

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Start backend
python main.py
```

Backend will run on **http://localhost:8001**

### Frontend Setup

Open a **new terminal**:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start frontend
npm run dev
```

Frontend will run on **http://localhost:3000**

---

## ✅ Verify Installation

### Check Backend

Open http://localhost:8001/docs

You should see the **Swagger API documentation**.

### Check Frontend

Open http://localhost:3000

You should see the **HLS Video Platform** homepage.

### Test Registration

1. Click "Register"
2. Create an account
3. Login
4. You should see the Convert, Player, Manage, Upload pages

---

## 🐛 Troubleshooting

### "Virtual environment not found"

**Solution:** Run the setup script first:
```bash
./setup.sh
```

### "Python command not found"

**Solution:** Install Python 3:
```bash
# Arch Linux
sudo pacman -S python

# Ubuntu/Debian
sudo apt install python3 python3-venv

# macOS
brew install python
```

### "Node command not found"

**Solution:** Install Node.js:
```bash
# Arch Linux
sudo pacman -S nodejs npm

# Ubuntu/Debian
sudo apt install nodejs npm

# macOS
brew install node
```

### "FFmpeg not found"

**Solution:** Install FFmpeg:
```bash
# Arch Linux
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### "Port 8001 already in use"

**Solution:** Kill the process:
```bash
# Find and kill process on port 8001
sudo lsof -ti:8001 | xargs kill -9

# Or change port in backend/config.py
PORT = 8002
```

### "Port 3000 already in use"

**Solution:** Kill the process:
```bash
# Find and kill process on port 3000
sudo lsof -ti:3000 | xargs kill -9

# Or change port in frontend/vite.config.js
server: { port: 3001 }
```

### "Module not found" errors

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database errors

**Solution:** Delete and recreate database:
```bash
rm backend/data/video_platform.db
# Restart backend - it will auto-create tables
```

---

## 📁 Directory Structure Check

After setup, you should have:

```
video-segment-cutter/
├── backend/
│   ├── venv/              ← Virtual environment (created by setup)
│   ├── data/              ← Database directory (created by setup)
│   ├── .env               ← Config file (created by setup)
│   └── [Python files]
│
├── frontend/
│   ├── node_modules/      ← Dependencies (created by setup)
│   └── [React files]
│
├── input/                 ← Video input directory
├── output/                ← HLS output directory
├── setup.sh              ← Run this first ✅
└── start-dev.sh          ← Run this to start ✅
```

---

## 🔄 Common Workflows

### First Time Setup
```bash
./setup.sh
./start-dev.sh
```

### Daily Development
```bash
./start-dev.sh
# Work on your code
# Ctrl+C to stop
```

### Restart Servers
```bash
# Stop servers (Ctrl+C)
# Then start again
./start-dev.sh
```

### Update Dependencies

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Clean Installation
```bash
# Remove everything
rm -rf backend/venv backend/data
rm -rf frontend/node_modules

# Re-run setup
./setup.sh
```

---

## 📞 Need Help?

1. **Check the logs** in terminal where servers are running
2. **Check browser console** (F12 → Console tab)
3. **Read the docs:**
   - [README_NEW_STACK.md](README_NEW_STACK.md) - Full documentation
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
4. **API Documentation:** http://localhost:8001/docs

---

## ✨ Next Steps

Once setup is complete:

1. ✅ Register a user account
2. ✅ Upload a video
3. ✅ Convert to HLS format
4. ✅ Watch the video
5. ✅ Explore the API docs
6. ✅ Customize the application

Enjoy your HLS Video Platform! 🎉
