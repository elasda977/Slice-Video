# 🚀 START HERE - HLS Video Platform

## ✅ Setup Already Complete!

Your Python + React video platform is ready to use!

---

## 🎯 Quick Start (30 seconds)

### Start the Application

```bash
cd /mnt/DATA/Project/video-segment-cutter
./start-dev.sh
```

This will start:
- ✅ **Backend API** on http://localhost:8001
- ✅ **Frontend** on http://localhost:3000

### Access the Application

Open your browser and go to:

**👉 http://localhost:3000**

---

## 📖 First Time Usage

### 1. Create an Account

1. Click **"Register"** in the top right
2. Fill in:
   - Username: (your choice)
   - Email: (your choice)
   - Password: (your choice)
3. Click **"Register"**

### 2. Login

1. Click **"Login"**
2. Enter your username and password
3. Click **"Login"**

### 3. Upload a Video

1. Click **"Upload"** in the navigation bar
2. Click the upload area or drag & drop a video file
3. Supported formats: **MP4, AVI, MKV, MOV**
4. Click **"Upload File"**
5. Wait for upload to complete

### 4. Convert the Video

1. Click **"Convert"** in the navigation bar
2. Enter the **filename** of the video you just uploaded (e.g., "myvideo.mp4")
3. Set **segment duration** (recommended: 6 seconds)
4. Click **"Start Conversion"**
5. Watch the **real-time progress** with stats:
   - Progress percentage
   - Current time / Total duration
   - Encoding speed
   - ETA (estimated time remaining)
   - Frame count

### 5. Play Your Video

1. Click **"Player"** in the navigation bar
2. Your converted video will appear in the library
3. Click on the video to select it
4. Video will start playing automatically
5. Use standard video controls (play, pause, seek, volume)

### 6. Manage Videos

1. Click **"Manage"** in the navigation bar
2. See all your videos with:
   - Status (pending, converting, completed, error)
   - Number of segments
   - File size
   - Creation date
3. Delete individual videos or cleanup all

---

## 🌐 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:8001 | REST API |
| **API Docs** | http://localhost:8001/docs | Interactive API documentation (Swagger) |
| **API Docs Alt** | http://localhost:8001/redoc | Alternative API docs (ReDoc) |

---

## 🎨 Features Overview

### ✅ User Authentication
- Register new accounts
- Login with JWT tokens
- Secure password hashing
- Protected routes

### ✅ Video Upload
- Upload through web interface
- Progress tracking
- File type validation
- Support for MP4, AVI, MKV, MOV

### ✅ Video Conversion
- Convert to HLS format
- Real-time progress updates
- Customizable segment duration
- Background processing

### ✅ Video Streaming
- HLS (HTTP Live Streaming)
- Works on all browsers
- Download protection (segmented files)
- Native controls

### ✅ Video Management
- View all videos
- Delete individual videos
- Bulk cleanup
- Disk usage statistics

---

## 🛑 Stop the Servers

Press **Ctrl+C** in the terminal where you ran `./start-dev.sh`

Both backend and frontend will stop automatically.

---

## 🔄 Restart the Servers

```bash
./start-dev.sh
```

That's it! The servers will start again.

---

## 🐛 Troubleshooting

### "Dependencies not installed"

Run setup first:
```bash
./setup.sh
```

### Port Already in Use

Kill existing processes:
```bash
pkill -f "python main.py"
pkill -f "vite"
```

Then restart:
```bash
./start-dev.sh
```

### Backend Won't Start

Check if FFmpeg is installed:
```bash
ffmpeg -version
```

If not installed:
```bash
# Arch Linux
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### Frontend Won't Start

Reinstall dependencies:
```bash
cd frontend
rm -rf node_modules
npm install
```

### Can't Login

1. Make sure backend is running (check http://localhost:8001/docs)
2. Check browser console for errors (F12 → Console)
3. Try registering a new account

---

## 📚 Documentation

Detailed documentation available:

- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete setup guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[README_NEW_STACK.md](README_NEW_STACK.md)** - Full technical documentation
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - What changed from old version

---

## 🎓 Technology Stack

### Backend (Python)
- **FastAPI** - Modern web framework
- **SQLite** - Database
- **SQLAlchemy** - ORM
- **FFmpeg** - Video processing
- **JWT** - Authentication

### Frontend (React)
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Zustand** - State management
- **HLS.js** - Video streaming
- **Axios** - HTTP client

---

## 💡 Tips

1. **Segment Duration:**
   - 6 seconds = Good balance
   - Shorter (3-4s) = Better download protection, more files
   - Longer (10s) = Fewer files, easier to download

2. **Video Formats:**
   - MP4 works best
   - H.264 video + AAC audio is optimal
   - Large files take longer to upload/convert

3. **Browser Support:**
   - Chrome/Firefox: Uses HLS.js
   - Safari: Native HLS support
   - All modern browsers supported

4. **Download Protection:**
   - Videos are split into small segments
   - Right-click save is disabled
   - Provides moderate protection (not DRM-level)

---

## 🎉 Example Workflow

```bash
# 1. Start servers
./start-dev.sh

# 2. Open browser
# → Go to http://localhost:3000
# → Register account
# → Login

# 3. Upload video
# → Click "Upload"
# → Select video file
# → Upload

# 4. Convert video
# → Click "Convert"
# → Enter filename
# → Start conversion
# → Watch progress

# 5. Play video
# → Click "Player"
# → Select video
# → Enjoy!
```

---

## ✨ What's New (vs Old Version)

- ✅ **User Authentication** - Secure login system
- ✅ **Database** - SQLite for metadata
- ✅ **File Upload** - Upload through web UI
- ✅ **React Frontend** - Modern single-page app
- ✅ **Real-time Progress** - Live conversion updates
- ✅ **API Documentation** - Auto-generated Swagger docs
- ✅ **Better UI** - Responsive, mobile-friendly design
- ✅ **Pure Python** - No more Bash scripts

---

## 📞 Need Help?

1. Check the terminal logs
2. Check browser console (F12)
3. Read the documentation files
4. Check API docs: http://localhost:8001/docs

---

## 🎊 You're All Set!

Everything is ready. Just run:

```bash
./start-dev.sh
```

And open **http://localhost:3000** in your browser.

Enjoy your new video platform! 🚀
