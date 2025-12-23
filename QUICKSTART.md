# Quick Start Guide - New Python + React Stack

## 🚀 30-Second Setup

### Option 1: Automatic (Recommended)

```bash
cd /mnt/DATA/Project/video-segment-cutter
./start-dev.sh
```

This script will:
1. Create virtual environment (if needed)
2. Install all dependencies
3. Start both backend and frontend
4. Open http://localhost:3000 in your browser

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 First Steps

1. **Open** http://localhost:3000
2. **Register** a new account
3. **Upload** a video (Upload page)
4. **Convert** the video (Convert page)
5. **Watch** real-time progress
6. **Play** your video (Player page)

## 🎯 Main Pages

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Landing page with features |
| Register | `/register` | Create account |
| Login | `/login` | Sign in |
| Upload | `/upload` | Upload video files |
| Convert | `/convert` | Convert videos to HLS |
| Player | `/player` | Watch videos |
| Manage | `/manage` | Manage video library |

## 🔧 Ports

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

## 📝 Test Account

For testing, you can create any account:
```
Username: testuser
Email: test@example.com
Password: password123
```

## 🎬 Example Workflow

```bash
# 1. Start servers
./start-dev.sh

# 2. In browser:
#    - Go to http://localhost:3000
#    - Register account
#    - Login

# 3. Upload video:
#    - Click "Upload" in navbar
#    - Select a video file
#    - Click "Upload File"

# 4. Convert video:
#    - Click "Convert" in navbar
#    - Enter filename (e.g., "myvideo.mp4")
#    - Set segment duration (6 seconds)
#    - Click "Start Conversion"
#    - Watch real-time progress

# 5. Play video:
#    - Click "Player" in navbar
#    - Select video from library
#    - Enjoy HLS streaming!
```

## 🐛 Common Issues

### Backend won't start
```bash
# Install FFmpeg
sudo pacman -S ffmpeg  # Arch
sudo apt install ffmpeg  # Ubuntu

# Recreate virtual environment
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Kill existing processes
pkill -f "python main.py"
pkill -f "vite"

# Or change ports in:
# - backend/config.py (PORT = 8002)
# - frontend/vite.config.js (port: 3001)
```

### Database errors
```bash
# Reset database
rm backend/data/video_platform.db
# Restart backend (auto-creates tables)
```

## 📚 Learn More

- **Full Documentation:** [README_NEW_STACK.md](README_NEW_STACK.md)
- **API Documentation:** http://localhost:8001/docs (when running)
- **Original Project:** [README.md](README.md)

## 🎨 Tech Stack Overview

**Backend:**
- FastAPI (Python web framework)
- SQLite (Database)
- FFmpeg (Video processing)
- JWT (Authentication)

**Frontend:**
- React.js (UI library)
- Vite (Build tool)
- Zustand (State management)
- HLS.js (Video streaming)

## 💡 Next Steps

After setup:
1. ✅ Explore the API documentation
2. ✅ Try uploading different video formats
3. ✅ Experiment with segment durations
4. ✅ Test on mobile devices
5. ✅ Check the Manage page for statistics

---

Need help? Check the full documentation or create an issue!
