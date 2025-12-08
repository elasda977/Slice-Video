# 🔐 SSH Tunnel Access Guide

Since direct connection doesn't work, use SSH tunnel to access the HLS player.

---

## 🚀 Quick Start - SSH Tunnel

### On Your Laptop (One Command):

```bash
ssh -L 8000:localhost:8000 your-username@10.244.132.148
```

**Replace `your-username` with your actual SSH username**

Then open browser to:
```
http://localhost:8000
```

---

## 📝 Step-by-Step Setup

### Step 1: Create SSH Tunnel (on your laptop)

```bash
# Basic tunnel
ssh -L 8000:localhost:8000 user@10.244.132.148

# Or with ZeroTier IP
ssh -L 8000:localhost:8000 user@10.244.132.148

# Or with local IP (if on same WiFi)
ssh -L 8000:localhost:8000 user@192.168.1.26
```

**What this does:**
- Maps your laptop's port 8000 → server's port 8000
- All traffic goes through encrypted SSH tunnel
- Server thinks requests come from localhost

### Step 2: Keep Terminal Open

**Important:** Keep the terminal window open! If you close it, the tunnel stops.

You should see:
```
user@server:~$
```

Leave this running.

### Step 3: Open Browser

**On your laptop, open:**
```
http://localhost:8000
```

You'll see the HLS Video Player interface!

---

## 🎯 Better Method: Background Tunnel

Run tunnel in background so you can close terminal:

```bash
# Start tunnel in background
ssh -f -N -L 8000:localhost:8000 user@10.244.132.148

# Verify it's running
ps aux | grep "ssh.*8000"
```

**To stop the tunnel later:**
```bash
# Find the process
ps aux | grep "ssh.*8000"

# Kill it (replace PID with actual number)
kill <PID>
```

---

## 💡 Pro Method: Use SSH Config

Make it easier by adding to `~/.ssh/config`:

```bash
# Edit SSH config
nano ~/.ssh/config

# Add this:
Host hls-server
    HostName 10.244.132.148
    User your-username
    LocalForward 8000 localhost:8000
    ServerAliveInterval 60
```

**Then connect with:**
```bash
ssh hls-server
```

**Or background mode:**
```bash
ssh -f -N hls-server
```

---

## 🔧 Troubleshooting SSH Tunnel

### Problem: "bind: Address already in use"

**Cause:** Port 8000 already used on your laptop

**Fix:**
```bash
# Find what's using port 8000
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill that process
kill <PID>

# Or use different port
ssh -L 8888:localhost:8000 user@10.244.132.148
# Then access: http://localhost:8888
```

### Problem: "Connection refused"

**Cause:** Server not running on remote side

**Fix:**
```bash
# SSH to server
ssh user@10.244.132.148

# Check if server running
ps aux | grep "python.*8000"

# If not running, start it
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh

# Or start in background
cd /mnt/DATA/Project/video-segment-cutter/web
nohup python -m http.server 8000 --bind 127.0.0.1 > /tmp/hls-server.log 2>&1 &
```

### Problem: Tunnel disconnects

**Fix:** Use autossh for persistent tunnel

```bash
# Install autossh
sudo pacman -S autossh  # Arch
sudo apt install autossh  # Ubuntu

# Use autossh
autossh -M 0 -f -N -L 8000:localhost:8000 user@10.244.132.148
```

---

## 🖥️ Platform-Specific Instructions

### Linux/Mac

```bash
# Standard SSH tunnel
ssh -L 8000:localhost:8000 user@10.244.132.148

# Access at: http://localhost:8000
```

### Windows (PowerShell)

```powershell
# Using built-in SSH
ssh -L 8000:localhost:8000 user@10.244.132.148

# Access at: http://localhost:8000
```

### Windows (PuTTY)

1. Open PuTTY
2. Session → Host Name: `10.244.132.148`
3. Connection → SSH → Tunnels
4. Source port: `8000`
5. Destination: `localhost:8000`
6. Click "Add"
7. Click "Open"
8. Access: `http://localhost:8000`

---

## 🔐 Security Benefits

SSH Tunnel advantages:
- ✓ All traffic encrypted
- ✓ No firewall configuration needed
- ✓ Works through NAT
- ✓ Authentication via SSH keys
- ✓ Can forward multiple ports

---

## 📊 Complete Workflow

### On Server (One Time Setup):

```bash
# Navigate to project
cd /mnt/DATA/Project/video-segment-cutter

# Start server (runs in background)
cd web
nohup python -m http.server 8000 --bind 127.0.0.1 > /tmp/hls-server.log 2>&1 &

# Verify
ps aux | grep "python.*8000"
```

**Note:** Server binds to `127.0.0.1` (localhost only) for security since we're using SSH tunnel.

### On Laptop (Every Time):

```bash
# Create tunnel
ssh -L 8000:localhost:8000 user@10.244.132.148

# Open browser
# Visit: http://localhost:8000
```

---

## 🚀 Advanced: Multiple Services

Forward multiple ports at once:

```bash
# Forward port 8000 (web) and 8080 (another service)
ssh -L 8000:localhost:8000 -L 8080:localhost:8080 user@10.244.132.148
```

---

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Basic tunnel | `ssh -L 8000:localhost:8000 user@server` |
| Background tunnel | `ssh -f -N -L 8000:localhost:8000 user@server` |
| Different port | `ssh -L 9000:localhost:8000 user@server` |
| Kill tunnel | `pkill -f "ssh.*8000"` |
| Check tunnel | `ps aux \| grep "ssh.*8000"` |
| Access URL | `http://localhost:8000` |

---

## 🎬 Ready to Use!

**On your laptop, run:**
```bash
ssh -L 8000:localhost:8000 user@10.244.132.148
```

**Then open browser:**
```
http://localhost:8000
```

That's it! 🎉

---

**Remember:**
- Keep SSH terminal open (or use `-f -N` for background)
- Server must be running on remote machine
- Access via `localhost:8000` on your laptop
- All traffic is encrypted via SSH
