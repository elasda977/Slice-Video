# 🔧 Troubleshooting Connection Issues

## ✅ Server Status (Checked: Dec 7, 2025)

**Server is NOW RUNNING** on port 8000 ✓
- Local IP: `http://192.168.1.26:8000/player.html`
- ZeroTier: `http://10.244.132.148:8000/player.html`
- Listening on: `0.0.0.0:8000` (all interfaces)
- Status: Both IPs tested successfully from server

---

## 🔍 Why You're Getting "Can't Reach" Error

The server is working! The issue is likely on **your laptop side**. Here's how to fix it:

---

## 📱 STEP-BY-STEP FIX (Run on Your Laptop)

### Option 1: Download and Run Diagnostic Script

**On your laptop:**

```bash
# Download the diagnostic script from server
scp user@server:/mnt/DATA/Project/video-segment-cutter/diagnose-connection.sh ~/

# Make it executable
chmod +x ~/diagnose-connection.sh

# Run it
./diagnose-connection.sh
```

This will tell you exactly what's wrong!

### Option 2: Manual Checks (Do These on Your Laptop)

#### Check 1: Can you ping the server?

```bash
# Try local IP
ping 192.168.1.26

# Try ZeroTier IP
ping 10.244.132.148
```

**Expected:** Should see replies (0% packet loss)

**If ping fails:**
- ❌ Local IP fails → Not on same WiFi
- ❌ ZeroTier IP fails → Not on same ZeroTier network

#### Check 2: Is ZeroTier running on your laptop?

```bash
zerotier-cli info
```

**If command not found:**
- ❌ ZeroTier not installed on your laptop
- Install from: https://www.zerotier.com/download/

**If "connection failed":**
```bash
# Start ZeroTier service (Linux)
sudo systemctl start zerotier-one

# Check status
sudo systemctl status zerotier-one
```

#### Check 3: Are you on the same ZeroTier network?

```bash
zerotier-cli listnetworks
```

**Expected:** Should see a network with IP like `10.244.x.x`

**If no 10.244.x.x IP:**
- ❌ Not on the same ZeroTier network
- You need to join the server's network

**To join:**
```bash
# On server, find network ID
sudo zerotier-cli listnetworks

# On laptop, join that network
sudo zerotier-cli join <network-id>

# Authorize at https://my.zerotier.com
```

#### Check 4: Can you reach the port?

```bash
# Test with netcat
nc -zv 10.244.132.148 8000

# Or with telnet
telnet 10.244.132.148 8000

# Or with curl
curl -I http://10.244.132.148:8000/player.html
```

**Expected:** Connection successful, HTTP 200 OK

**If connection refused:**
- Check server is still running
- Try the local IP instead: `192.168.1.26`

---

## 🌐 Common Issues and Solutions

### Issue 1: "This site can't be reached"

**Causes:**
1. Not on same network (WiFi or ZeroTier)
2. Server not running
3. Wrong IP address

**Fix:**
```bash
# On laptop, test connectivity
ping 10.244.132.148

# If ping works but browser doesn't:
curl http://10.244.132.148:8000/player.html

# If curl works, it's a browser issue
# Try: Clear browser cache or use incognito mode
```

### Issue 2: "Connection timeout"

**Causes:**
1. Firewall blocking on laptop
2. Not on same network
3. Server offline

**Fix:**
```bash
# On laptop, check your firewall
sudo ufw status    # Linux
# Temporarily disable to test:
sudo ufw disable

# Re-enable after testing:
sudo ufw enable
```

### Issue 3: ZeroTier IP not working but Local IP works

**Causes:**
1. Laptop not on ZeroTier network
2. ZeroTier service not running
3. Using RELAY instead of DIRECT connection

**Fix:**
```bash
# Check ZeroTier peers
zerotier-cli peers | grep DIRECT

# Restart ZeroTier
sudo systemctl restart zerotier-one

# Check your laptop's ZeroTier IP
ip addr show | grep 10.244
```

### Issue 4: Both IPs not working

**Causes:**
1. Server not running
2. Completely different networks

**Fix:**
```bash
# Via SSH, check if server is running:
ps aux | grep "python.*8000"

# If not running, start it:
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh

# Or use background mode:
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000 --bind 0.0.0.0 &
```

---

## 🎯 Quick Decision Tree

```
Can you ping 10.244.132.148 from laptop?
├── YES → Can you telnet/nc to port 8000?
│   ├── YES → Browser cache issue
│   │   └── Fix: Clear cache, use incognito, or try different browser
│   └── NO → Server not running
│       └── Fix: Start server on server machine
└── NO → Not on same network
    ├── Check: zerotier-cli listnetworks
    ├── Is ZeroTier running? sudo systemctl status zerotier-one
    └── Are you on same network? Should see 10.244.x.x IP
```

---

## 📋 Checklist for Your Laptop

Run through this checklist on your laptop:

- [ ] ZeroTier installed: `which zerotier-cli`
- [ ] ZeroTier running: `sudo systemctl status zerotier-one`
- [ ] On ZeroTier network: `zerotier-cli listnetworks | grep 10.244`
- [ ] Can ping server: `ping 10.244.132.148`
- [ ] Can reach port: `nc -zv 10.244.132.148 8000`
- [ ] Tried in browser: `http://10.244.132.148:8000/player.html`
- [ ] Tried incognito mode
- [ ] Tried different browser

---

## 🚀 Quick Test Commands (Copy-Paste on Laptop)

```bash
echo "=== Testing Server Connectivity ==="

echo "1. Testing ping..."
ping -c 3 10.244.132.148 && echo "✓ Ping OK" || echo "✗ Ping FAILED"

echo "2. Testing port 8000..."
nc -zv 10.244.132.148 8000 2>&1 | grep -q succeeded && echo "✓ Port OK" || echo "✗ Port FAILED"

echo "3. Testing HTTP..."
curl -I http://10.244.132.148:8000/player.html 2>&1 | grep -q "200 OK" && echo "✓ HTTP OK" || echo "✗ HTTP FAILED"

echo "4. Checking ZeroTier..."
zerotier-cli listnetworks 2>&1 | grep -q "10.244" && echo "✓ ZeroTier OK" || echo "✗ ZeroTier NOT CONFIGURED"

echo ""
echo "If all tests pass, try opening in browser:"
echo "http://10.244.132.148:8000/player.html"
```

---

## 📞 Still Not Working?

### Get Server Logs

Via SSH on server:
```bash
# Check if server is running
ps aux | grep "python.*8000"

# View server logs
tail -f /tmp/hls-server.log

# Check what's listening on port 8000
ss -tulpn | grep 8000
```

### Test from Server Side

```bash
# On server, test local access
curl http://localhost:8000/player.html
curl http://127.0.0.1:8000/player.html
curl http://10.244.132.148:8000/player.html
curl http://192.168.1.26:8000/player.html
```

All should return HTML content (HTTP 200 OK).

---

## 💡 Alternative Solutions

### Use SSH Tunnel (If Nothing Else Works)

From your laptop:
```bash
# Create SSH tunnel
ssh -L 8000:localhost:8000 user@10.244.132.148

# Then access via:
http://localhost:8000/player.html
```

### Use Local Network IP Instead

If ZeroTier doesn't work, use local IP:
```
http://192.168.1.26:8000/player.html
```

(Only works if on same WiFi)

---

## 🔍 Advanced Diagnostics

### Check Routing Table (Laptop)

```bash
# See how laptop routes to server
ip route get 10.244.132.148

# Should show route via ZeroTier interface
```

### Check if Browser Blocks Local IPs

Some browsers block private IP ranges. Try:
- Chrome with `--allow-insecure-localhost` flag
- Firefox: about:config → network.proxy.allow_bypass_localhost
- Or use `curl` to verify it's not a browser issue

### Packet Capture

```bash
# On laptop, capture packets while trying to connect
sudo tcpdump -i any host 10.244.132.148 and port 8000

# Then try accessing in browser
# Check if SYN packets are sent
```

---

## ✅ What We Know So Far

**Server Side (Verified ✓):**
- ✓ Server is running on port 8000
- ✓ Bound to 0.0.0.0 (all interfaces)
- ✓ Responds to requests from server itself
- ✓ ZeroTier interface is UP
- ✓ Firewall allows connections

**Laptop Side (Needs Checking):**
- ? Is laptop on same ZeroTier network?
- ? Can laptop ping the server?
- ? Is ZeroTier service running on laptop?
- ? Can laptop reach port 8000?

**Next Step:** Run diagnostic script on your laptop to identify the exact issue.

---

**Server IP:** `10.244.132.148:8000`
**Server Status:** ✓ Running and responding
**Issue Location:** Likely on laptop side
**Fix:** Follow the steps above to diagnose and fix
