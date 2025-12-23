# HLS Video Platform - Python + React Stack

A modern video streaming platform with download protection, converted to **FastAPI** (backend) and **React.js** (frontend).

## 🚀 New Technology Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLite** - Database for video metadata
- **SQLAlchemy** - ORM for database operations
- **JWT Authentication** - Secure user authentication
- **WebSockets** - Real-time progress updates
- **FFmpeg** - Video processing (same as before)

### Frontend
- **React.js** - Modern UI library
- **Vite** - Fast build tool
- **Zustand** - Lightweight state management
- **Axios** - HTTP client with interceptors
- **HLS.js** - Video streaming library
- **React Router** - Client-side routing

## 📁 New Project Structure

```
video-segment-cutter/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # Authentication utilities
│   ├── ffmpeg_converter.py   # Video conversion module
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── data/                 # SQLite database storage
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── api/              # API client utilities
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── store/            # Zustand stores
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── index.html            # HTML template
│
├── input/                     # Video input directory
├── output/                    # HLS output directory
└── [legacy files]            # Old web/ and scripts/
```

## 🔧 Installation & Setup

### Prerequisites
```bash
# Install system dependencies
sudo pacman -S python ffmpeg nodejs npm  # Arch Linux
# OR
sudo apt install python3 ffmpeg nodejs npm  # Ubuntu/Debian
```

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and change SECRET_KEY in production!
```

5. **Run the backend:**
```bash
python main.py
```

Backend will start on `http://localhost:8001`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run development server:**
```bash
npm run dev
```

Frontend will start on `http://localhost:3000`

## 🎯 Quick Start Guide

### 1. Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 2. Create an Account
1. Open `http://localhost:3000` in your browser
2. Click "Register" and create an account
3. Login with your credentials

### 3. Upload and Convert a Video
1. Go to "Upload" page
2. Select a video file (MP4, AVI, MKV, MOV)
3. Upload the file
4. Go to "Convert" page
5. Enter the filename and click "Start Conversion"
6. Watch real-time progress updates

### 4. Play Your Video
1. Go to "Player" page
2. Select a video from the library
3. Video plays with HLS streaming

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** `http://localhost:8001/docs`
- **ReDoc:** `http://localhost:8001/redoc`

### Main Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

#### Videos
- `GET /api/videos` - List all videos
- `GET /api/videos/{id}` - Get video details
- `DELETE /api/videos/{id}` - Delete a video
- `POST /api/videos/upload` - Upload video file

#### Conversion
- `POST /api/convert` - Start video conversion
- `GET /api/progress/{name}` - Get conversion progress
- `POST /api/convert/cancel/{name}` - Cancel conversion

#### Server
- `GET /api/status` - Get server status
- `DELETE /api/cleanup` - Delete all videos

## 🔐 Authentication Flow

1. User registers/logs in
2. Backend returns JWT access token
3. Frontend stores token in localStorage (via Zustand)
4. All API requests include token in Authorization header
5. Backend validates token on each request

## 🎬 Video Conversion Flow

### Old Flow (Bash):
```
User → Python API → Bash Script → FFmpeg → Files
```

### New Flow (Pure Python):
```
User → FastAPI → FFmpegConverter (async) → FFmpeg → Database + Files
     ↓
WebSocket (real-time progress)
```

## 🌐 Real-time Progress Updates

The new stack supports **two methods** for progress updates:

### 1. HTTP Polling (Current)
- Frontend polls `/api/progress/{name}` every 500ms
- Simple, works everywhere
- Used in Convert page

### 2. WebSocket (Available)
- Real-time bidirectional communication
- Connect to `ws://localhost:8001/ws/progress`
- More efficient for live updates

## 🚢 Production Deployment

### Backend Production

1. **Install production server:**
```bash
pip install gunicorn
```

2. **Run with Gunicorn:**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Frontend Production

1. **Build for production:**
```bash
cd frontend
npm run build
```

2. **Serve with Nginx/Apache:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files (videos)
    location /output {
        alias /path/to/output;
    }
}
```

## 🔒 Security Considerations

### Current Implementation
- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS protection
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)

### Production Recommendations
- 🔐 Change `SECRET_KEY` in .env
- 🔐 Use HTTPS in production
- 🔐 Add rate limiting
- 🔐 Implement refresh tokens
- 🔐 Add file size limits for uploads
- 🔐 Use PostgreSQL instead of SQLite
- 🔐 Add user roles/permissions

## 🆚 Comparison: Old vs New

| Feature | Old Stack | New Stack |
|---------|-----------|-----------|
| Backend | Python http.server + Bash | FastAPI (async Python) |
| Frontend | Plain HTML/CSS/JS | React.js + Vite |
| Database | File system only | SQLite + SQLAlchemy |
| Auth | None | JWT authentication |
| Progress | JSON file polling | WebSocket ready + polling |
| API Docs | None | Auto-generated (Swagger) |
| Type Safety | None | Pydantic schemas |
| State Management | None | Zustand |
| Routing | HTML files | React Router |
| Build Tool | None | Vite (fast HMR) |

## 🎨 Features

### Implemented ✅
- User registration and login
- JWT authentication
- File upload through web UI
- Video conversion with FFmpeg
- Real-time progress tracking
- Database storage for metadata
- Video library management
- HLS video player
- Responsive UI design
- WebSocket support

### Not Implemented (Future)
- User roles and permissions
- Video sharing/permissions
- Multiple quality versions
- Video thumbnails
- Search and filtering
- Batch operations
- Email notifications
- CDN integration

## 🐛 Troubleshooting

### Backend Issues

**Database errors:**
```bash
# Delete and recreate database
rm backend/data/video_platform.db
# Restart backend (auto-creates tables)
```

**FFmpeg not found:**
```bash
# Install FFmpeg
sudo pacman -S ffmpeg  # Arch
sudo apt install ffmpeg  # Ubuntu
```

### Frontend Issues

**Port already in use:**
```bash
# Change port in vite.config.js
server: { port: 3001 }
```

**API connection errors:**
```bash
# Check backend is running on port 8001
# Check proxy configuration in vite.config.js
```

## 📦 Migration from Old Stack

If you have existing converted videos:

1. **Database will auto-populate on first run**
2. **Existing videos in `output/` are accessible**
3. **Old `web/` and `scripts/` can be kept as backup**
4. **No data migration needed**

## 🔄 Development Workflow

```bash
# Start development
cd backend && source venv/bin/activate && python main.py &
cd frontend && npm run dev

# Make changes
# - Edit backend files (auto-reload with uvicorn --reload)
# - Edit frontend files (HMR with Vite)

# Build for production
cd frontend && npm run build

# Deploy
# - Copy backend/ to server
# - Copy frontend/dist to server
# - Configure Nginx/Apache
```

## 📄 License

Same as original project.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

For issues, please check:
1. Backend logs in terminal
2. Frontend console in browser DevTools
3. Network tab for API errors
4. FFmpeg is installed and in PATH

---

**Converted by Claude Code** | FastAPI + React.js Stack | 2024
