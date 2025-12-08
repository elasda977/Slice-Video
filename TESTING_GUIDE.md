# 🧪 Testing Guide - External Access via SSH

> **Your Server IP:** `192.168.1.26`
> **Access from laptop:** Connect to the same network and use the IP above

---

## 🚀 Quick Start - Test Now

### Step 1: Open Firewall Port (If Needed)

Run these commands on the **server** (via SSH):

```bash
# Check if firewall is active
sudo ufw status

# If active, allow port 8000
sudo ufw allow 8000/tcp
sudo ufw reload

# Verify
sudo ufw status | grep 8000
```

**Alternative (firewalld):**
```bash
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### Step 2: Start the Server

```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh
```

**Or use custom port:**
```bash
./start-server.sh 8080
```

### Step 3: Access from Your Laptop

**From your laptop's browser, visit:**
```
http://192.168.1.26:8000/player.html
```

---

## 📝 Testing Without Video (Quick Test)

You can test the player immediately without converting a video:

1. Start the server (Step 2 above)
2. Open in laptop browser: `http://192.168.1.26:8000/player.html`
3. You should see the player interface (video won't load without playlist, but interface should show)

---

## 🎬 Full Test with Sample Video

### Option A: Use Existing Video

If you have a video file somewhere:

```bash
# Copy to input folder
cp /path/to/your/video.mp4 /mnt/DATA/Project/video-segment-cutter/input/

# Convert to HLS
cd /mnt/DATA/Project/video-segment-cutter/scripts
./convert-to-hls.sh ../input/video.mp4

# Start server
./start-server.sh
```

**Then on laptop:**
1. Visit: `http://192.168.1.26:8000/player.html`
2. Enter path: `../output/video/playlist.m3u8`
3. Click "Load Video"

### Option B: Download Test Video

Download a small test video first:

```bash
# Go to input folder
cd /mnt/DATA/Project/video-segment-cutter/input

# Download a small test video (Creative Commons)
wget https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 \
  -O test-video.mp4

# Or use curl
curl -o test-video.mp4 \
  https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4

# Convert it
cd ../scripts
./convert-to-hls.sh ../input/test-video.mp4

# Start server
./start-server.sh
```

**On laptop browser:**
- URL: `http://192.168.1.26:8000/player.html`
- Playlist: `../output/test-video/playlist.m3u8`

---

## 🔍 Troubleshooting External Access

### Problem: Can't connect from laptop

**1. Check if server is running:**
```bash
# On server, check if port 8000 is listening
ss -tulpn | grep 8000
# or
netstat -tulpn | grep 8000
```

Should show: `0.0.0.0:8000`

**2. Test from server itself:**
```bash
# On the server, test local access
curl http://localhost:8000/player.html
```

Should return HTML content.

**3. Check firewall:**
```bash
# Test if port is open (from server)
sudo iptables -L -n | grep 8000

# Or check with nmap (if installed)
nmap -p 8000 192.168.1.26
```

**4. Test connectivity from laptop:**

From your laptop terminal:
```bash
# Ping the server
ping 192.168.1.26

# Check if port is accessible
telnet 192.168.1.26 8000
# or
nc -zv 192.168.1.26 8000
```

**5. Check if on same network:**
```bash
# On laptop, check your IP
ip addr show | grep "inet "
# or
ifconfig | grep "inet "
```

Your laptop should have IP like `192.168.1.X` (same subnet).

### Problem: "Connection refused"

**Cause:** Firewall blocking port

**Fix:**
```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or disable firewall temporarily (for testing only!)
sudo ufw disable
# Remember to re-enable: sudo ufw enable
```

### Problem: "Connection timeout"

**Possible causes:**
1. Not on same network
2. Server's firewall blocking
3. Router firewall blocking

**Fix:**
```bash
# Make sure server binds to 0.0.0.0, not 127.0.0.1
# The start-server.sh script already does this
./start-server.sh
```

### Problem: Player loads but video won't play

**Fix:** Check the playlist path is correct:
- Path should be: `../output/videoname/playlist.m3u8`
- Check files exist:
```bash
ls -lh /mnt/DATA/Project/video-segment-cutter/output/
```

---

## 🌐 Network Configuration Quick Reference

### Current Server IPs:
```
Local Network:  192.168.1.26    ← Use this from laptop
ZeroTier VPN:   10.244.132.148
Docker:         172.17.0.1
Localhost:      127.0.0.1
```

### Access Matrix:

| From | URL to use |
|------|------------|
| Server itself | `http://localhost:8000/player.html` |
| Laptop on same WiFi/LAN | `http://192.168.1.26:8000/player.html` |
| Via ZeroTier VPN | `http://10.244.132.148:8000/player.html` |

---

## 💡 Pro Tips

### Keep Server Running in Background

```bash
# Start in background with nohup
cd /mnt/DATA/Project/video-segment-cutter/scripts
nohup ./start-server.sh 8000 > server.log 2>&1 &

# Check if running
ps aux | grep python.*8000

# Stop it later
pkill -f "python.*8000"
```

### Use Screen/Tmux (Better)

```bash
# Start screen session
screen -S hls-server

# Run server
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh

# Detach: Press Ctrl+A then D
# Reattach: screen -r hls-server
```

### Check Server Logs

```bash
# If using nohup
tail -f /mnt/DATA/Project/video-segment-cutter/scripts/server.log

# Watch access logs in real-time
# (Python http.server prints to stdout)
```

---

## ✅ Testing Checklist

- [ ] Firewall port 8000 is open
- [ ] Server started with `./start-server.sh`
- [ ] Server shows IP: `192.168.1.26`
- [ ] Can access from laptop browser
- [ ] Video file copied to `input/`
- [ ] Video converted with `convert-to-hls.sh`
- [ ] Output exists in `output/videoname/`
- [ ] Playlist loads in player
- [ ] Video plays successfully

---

## 🆘 Quick Help Commands

```bash
# Start everything from scratch
cd /mnt/DATA/Project/video-segment-cutter

# Check current directory contents
ls -lh

# View server script
cat scripts/start-server.sh

# Check if server is running
ps aux | grep python | grep 8000

# Kill server if stuck
pkill -f "python.*8000"

# Check what's using port 8000
ss -tulpn | grep 8000
```

---

## 📞 Need Help?

1. Check server logs
2. Verify firewall settings
3. Confirm network connectivity
4. Review this guide's troubleshooting section
5. Check README.md for more details

---

**Server IP:** `192.168.1.26`
**Laptop URL:** `http://192.168.1.26:8000/player.html`
**Default Port:** `8000`
