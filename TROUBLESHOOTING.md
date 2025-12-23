# Troubleshooting Guide

## ❌ Common Issues and Solutions

### 1. **Error: ECONNREFUSED - Can't connect to backend**

**Symptoms:**
```
[vite] http proxy error: /api/videos
AggregateError [ECONNREFUSED]
```

**Solution:**

**Option A - Use restart script:**
```bash
./restart-backend.sh
```

**Option B - Manual restart:**
```bash
# Kill old backend
pkill -f main.py

# Start backend
cd backend
source venv/bin/activate
python main.py
```

**Check if running:**
```bash
curl http://localhost:8001/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T..."
}
```

---

### 2. **Error: email-validator not installed**

**Fix:**
Already fixed in code - `EmailStr` replaced with `str` in schemas.py

---

### 3. **Error: greenlet library required**

**Fix:**
```bash
cd backend
source venv/bin/activate
pip install greenlet
```

Or re-run setup:
```bash
./setup.sh
```

---

### 4. **Can't upload videos**

**Check:**
1. Backend is running:
   ```bash
   curl http://localhost:8001/health
   ```

2. Input directory exists:
   ```bash
   ls -la input/
   ```

3. Frontend is connected:
   - Open http://localhost:3000
   - Open browser console (F12)
   - Look for API errors

**Fix:**
```bash
# Restart both servers
./start-dev.sh
```

---

### 5. **Frontend won't start**

**Error:** `Port 3000 already in use`

**Fix:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Restart frontend
cd frontend
npm run dev
```

---

### 6. **Backend won't start**

**Error:** `Port 8001 already in use`

**Fix:**
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9

# Restart backend
./restart-backend.sh
```

---

### 7. **Database errors**

**Symptoms:**
- Videos not showing
- Can't save uploads
- Database locked errors

**Fix:**
```bash
# Reset database
rm backend/data/video_platform.db

# Restart backend (will recreate DB)
./restart-backend.sh
```

---

### 8. **Upload stuck at 100%**

**Symptoms:**
- Upload shows 100% but doesn't convert
- No conversion progress shown

**Check backend logs:**
```bash
tail -f /tmp/backend.log
```

**Common causes:**
- FFmpeg not installed
- File permissions issue
- Backend crashed

**Fix:**
```bash
# Check FFmpeg
ffmpeg -version

# If not installed:
sudo pacman -S ffmpeg  # Arch
sudo apt install ffmpeg  # Ubuntu

# Restart backend
./restart-backend.sh
```

---

### 9. **Conversion fails**

**Check:**
1. Video file is valid format (MP4, AVI, MKV, MOV)
2. File isn't corrupted
3. Enough disk space

**View conversion logs:**
```bash
# Check specific video conversion log
ls -la output/[video-name]/.conversion.log
cat output/[video-name]/.conversion.log
```

---

### 10. **Missing dependencies**

**Full reinstall:**
```bash
# Backend
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
rm -rf node_modules
npm install
```

Or use setup script:
```bash
./setup.sh
```

---

## 🔍 Diagnostic Commands

### Check Server Status

**Backend:**
```bash
curl http://localhost:8001/health
curl http://localhost:8001/api/status
```

**Frontend:**
```bash
curl http://localhost:3000
```

### Check Processes

```bash
# Backend process
ps aux | grep main.py

# Frontend process
ps aux | grep vite

# Check ports
netstat -tlnp | grep -E '3000|8001'
# or
ss -tlnp | grep -E '3000|8001'
```

### View Logs

**Backend:**
```bash
tail -f /tmp/backend.log
```

**Frontend:**
Open browser console (F12 → Console)

**Conversion logs:**
```bash
ls output/*/. conversion.log
cat output/[video-name]/.conversion.log
```

---

## 🛠️ Quick Fixes

### Restart Everything
```bash
# Kill all
pkill -f main.py
pkill -f vite

# Start all
./start-dev.sh
```

### Just Backend
```bash
./restart-backend.sh
```

### Just Frontend
```bash
cd frontend
npm run dev
```

### Fresh Start
```bash
# Clean everything
rm -rf backend/venv backend/data
rm -rf frontend/node_modules

# Reinstall
./setup.sh

# Start
./start-dev.sh
```

---

## 📞 Getting Help

### Check These First:

1. ✅ Backend running on port 8001?
2. ✅ Frontend running on port 3000?
3. ✅ FFmpeg installed?
4. ✅ Database file exists?
5. ✅ Input/output directories exist?

### Collect Debug Info:

```bash
# System info
uname -a
python --version
node --version
ffmpeg -version

# Server status
curl http://localhost:8001/health
curl http://localhost:8001/api/status

# Process status
ps aux | grep -E 'main.py|vite'

# Port status
ss -tlnp | grep -E '3000|8001'

# Recent logs
tail -50 /tmp/backend.log
```

---

## 🚀 After Fixing

**Verify everything works:**

1. **Backend health:**
   ```bash
   curl http://localhost:8001/health
   ```

2. **Frontend loads:**
   Open http://localhost:3000

3. **Upload test:**
   - Go to http://localhost:3000/upload
   - Select a small video file
   - Click "Upload & Process"
   - Watch progress

4. **Check dashboard:**
   - Go to http://localhost:3000/dashboard
   - Should show uploaded video

---

## 📝 Prevention

### Always use start script:
```bash
./start-dev.sh
```

### Before uploading large files:
```bash
# Check disk space
df -h

# Check backend is healthy
curl http://localhost:8001/health
```

### Regular maintenance:
```bash
# Clean old videos
rm -rf output/*

# Check logs
tail -f /tmp/backend.log
```

---

## 🆘 Emergency Reset

**If nothing works:**

```bash
# 1. Stop everything
pkill -f main.py
pkill -f vite

# 2. Clean everything
rm -rf backend/venv backend/data backend/__pycache__
rm -rf frontend/node_modules frontend/dist

# 3. Reinstall
./setup.sh

# 4. Start fresh
./start-dev.sh
```

**Note:** This will delete:
- ❌ All uploaded videos
- ❌ All converted videos
- ❌ All database records
- ✅ Code files preserved

---

**Need more help?** Check the logs and documentation files in the project root.
