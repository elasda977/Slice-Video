# 🚀 Start Servers Guide

## ✅ Servers Status

**Both servers are now running:**

- ✅ **Web Server:** Port 8000 (serving HTML/CSS/JS)
- ✅ **API Server:** Port 8001 (handling commands)

---

## 🔐 SSH Tunnel Setup (IMPORTANT!)

To access the manage page with executable buttons, you need to forward **BOTH** ports:

### New SSH Tunnel Command:

```bash
ssh -L 8000:localhost:8000 -L 8001:localhost:8001 your-username@10.244.132.148
```

**Or in background:**
```bash
ssh -f -N -L 8000:localhost:8000 -L 8001:localhost:8001 your-username@10.244.132.148
```

---

## 🌐 Access URLs (on your laptop)

After creating the SSH tunnel:

- **Home Page:** `http://localhost:8000`
- **Player:** `http://localhost:8000/player.html`
- **Upload:** `http://localhost:8000/upload.html`
- **Manage:** `http://localhost:8000/manage.html` ← **New interactive page!**

---

## 🎮 **New Manage Page Features**

The manage page now has **executable buttons** instead of just commands:

### 📹 Video Library
- **Auto-loads** all converted videos
- **Play button** - Opens video in player
- **Delete button** - Removes video with confirmation
- **Refresh button** - Reloads video list

### ⚡ Quick Actions
1. **Check Disk Usage** - Shows space used by videos
2. **Convert All Videos** - Batch converts all input videos
3. **Clean All Output** - Deletes all converted videos (double confirmation)
4. **Restart Server** - Restarts the web server

### 📋 Command Output Log
- **Real-time output** from all commands
- **Color-coded messages** (green=success, red=error, yellow=warning)
- **Scrollable** terminal-style display
- **Clear button** to reset log

---

## 🔄 Start/Stop Servers

### Start Both Servers:
```bash
# Web server (already running)
cd /mnt/DATA/Project/video-segment-cutter/web
nohup python -m http.server 8000 --bind 0.0.0.0 > /tmp/hls-server.log 2>&1 &

# API server (already running)
nohup python3 api.py > /tmp/hls-api.log 2>&1 &
```

### Check Server Status:
```bash
# Check if both are running
ss -tulpn | grep -E "(8000|8001)"

# Should show:
# tcp   LISTEN   0.0.0.0:8000   (web server)
# tcp   LISTEN   0.0.0.0:8001   (API server)
```

### Stop Servers:
```bash
# Stop web server
pkill -f "python.*8000"

# Stop API server
pkill -f "api.py"
```

---

## 🧪 Test the Manage Page

1. **Create SSH tunnel** with both ports:
   ```bash
   ssh -L 8000:localhost:8000 -L 8001:localhost:8001 user@10.244.132.148
   ```

2. **Open manage page:**
   ```
   http://localhost:8000/manage.html
   ```

3. **You should see:**
   - Video library showing "test-mantra" video
   - 4 executable action buttons
   - Green terminal-style log output at bottom

4. **Try clicking "Check Disk Usage"**
   - Should show output in the log
   - Output appears in green text

5. **Try clicking on the "test-mantra" video**
   - Click "Play" to watch it
   - Click "Delete" to remove it (with confirmation)

---

## 🎯 Quick Reference

| Component | Port | Purpose |
|-----------|------|---------|
| Web Server | 8000 | Serves HTML/CSS/JS files |
| API Server | 8001 | Executes commands & returns results |
| SSH Tunnel | Both | Forward both ports to laptop |

---

## 💡 Pro Tips

### Auto-start servers on boot:
Create a systemd service or add to crontab:
```bash
@reboot cd /mnt/DATA/Project/video-segment-cutter/web && python -m http.server 8000 --bind 0.0.0.0 &
@reboot cd /mnt/DATA/Project/video-segment-cutter/web && python3 api.py &
```

### Monitor server logs:
```bash
# Web server log
tail -f /tmp/hls-server.log

# API server log
tail -f /tmp/hls-api.log
```

### Kill stuck servers:
```bash
# Nuclear option - kill all Python HTTP servers
pkill -9 -f "http.server"
pkill -9 -f "api.py"
```

---

## ✅ Current Status

**Everything is READY!** 🎉

✅ Web server running on port 8000
✅ API server running on port 8001
✅ Test video "test-mantra" available
✅ Interactive manage page created
✅ All features working

**Just create the SSH tunnel and access:** `http://localhost:8000/manage.html`

---

**Enjoy your new interactive management interface!** 🚀
