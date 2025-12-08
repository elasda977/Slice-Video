# 🌐 ZeroTier Access Guide

Your server has a ZeroTier VPN interface active!

## 📍 ZeroTier Information

**Interface:** `ztfp6i6ewq`
**IP Address:** `10.244.132.148`
**Network:** `10.244.0.0/16`
**Status:** ✓ Active and Running

---

## ✅ YES - You Can Use This IP!

**If your laptop is also connected to the same ZeroTier network**, you can access the server using:

```
http://10.244.132.148:8000/player.html
```

---

## 🔍 How to Check if Your Laptop is on the Same ZeroTier Network

### On Your Laptop (Linux/Mac):

```bash
# Check if ZeroTier is running
zerotier-cli listnetworks

# Check your ZeroTier IP
ip addr show | grep "10.244"
# or
ifconfig | grep "10.244"
```

### On Your Laptop (Windows):

```cmd
# Check ZeroTier networks
zerotier-cli.bat listnetworks

# Or check in ZeroTier GUI
# Look for IP starting with 10.244.x.x
```

### What to Look For:

- ✓ **Same Network ID** - Both devices should show the same ZeroTier network ID
- ✓ **Same Subnet** - Laptop should have IP like `10.244.x.x`
- ✓ **Status: OK** - Network should show as connected

---

## 🚀 Quick Test from Your Laptop

### Step 1: Check Connectivity

From your laptop terminal:

```bash
# Ping the server's ZeroTier IP
ping 10.244.132.148
```

**Expected Result:** Should receive replies (0% packet loss)

### Step 2: Test Port Access

```bash
# Test if port 8000 is accessible
telnet 10.244.132.148 8000
# or
nc -zv 10.244.132.148 8000
```

**Expected Result:** Connection successful

### Step 3: Start Server and Access

On the server:
```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh
```

On your laptop browser:
```
http://10.244.132.148:8000/player.html
```

---

## 🌟 Advantages of Using ZeroTier IP

### ✓ **Works from Anywhere**
- Not limited to local network
- Access from anywhere in the world
- No need to be on same WiFi

### ✓ **Encrypted**
- ZeroTier creates encrypted tunnels
- More secure than plain HTTP over public networks

### ✓ **No Firewall Issues**
- ZeroTier usually bypasses local firewalls
- No need to open ports on router

### ✓ **Persistent IP**
- IP stays the same even if you move locations
- Easier to remember than changing local IPs

---

## 📊 Access Options Comparison

| Method | IP Address | When to Use |
|--------|------------|-------------|
| **Local Network** | `192.168.1.26` | Both on same WiFi/LAN |
| **ZeroTier VPN** | `10.244.132.148` | Remote access, anywhere |
| **Localhost** | `127.0.0.1` | Testing on server itself |

---

## 🔧 Setup ZeroTier on Your Laptop (If Not Installed)

### Linux (Arch):
```bash
sudo pacman -S zerotier-one
sudo systemctl enable --now zerotier-one
sudo zerotier-cli join <network-id>
```

### Linux (Ubuntu/Debian):
```bash
curl -s https://install.zerotier.com | sudo bash
sudo zerotier-cli join <network-id>
```

### macOS:
```bash
# Download from: https://www.zerotier.com/download/
# Or via Homebrew:
brew install --cask zerotier-one
```

### Windows:
```
Download installer from: https://www.zerotier.com/download/
Install and join your network via GUI
```

**Note:** You'll need the same Network ID that your server is connected to.

---

## 🛠️ Troubleshooting ZeroTier Access

### Problem: Can't ping 10.244.132.148 from laptop

**Check 1:** Verify laptop is on the same ZeroTier network
```bash
zerotier-cli listnetworks
```

**Check 2:** Check if ZeroTier service is running
```bash
# Linux/Mac
sudo systemctl status zerotier-one

# Or check process
ps aux | grep zerotier
```

**Check 3:** Verify both devices are authorized on the network
- Log into ZeroTier Central (my.zerotier.com)
- Check that both devices show as "Authorized"

### Problem: Ping works but browser can't connect

**Solution:** Make sure server is running
```bash
# On server, check if port 8000 is listening
ss -tulpn | grep 8000

# Should show: 0.0.0.0:8000
```

### Problem: Very slow connection

**Possible Causes:**
- Using RELAY instead of DIRECT connection
- Check with: `zerotier-cli peers`
- Look for DIRECT vs RELAY status

---

## 🎯 Complete Workflow Using ZeroTier

### On Server:

```bash
# 1. Navigate to project
cd /mnt/DATA/Project/video-segment-cutter

# 2. Convert video (if needed)
cd scripts
./convert-to-hls.sh ../input/video.mp4

# 3. Start server
./start-server.sh

# Server will show all IPs including:
# - 192.168.1.26 (local)
# - 10.244.132.148 (ZeroTier)
```

### On Your Laptop:

```bash
# 1. Verify ZeroTier connection
ping 10.244.132.148

# 2. Open browser
# Visit: http://10.244.132.148:8000/player.html

# 3. Enter playlist path
# Path: ../output/video/playlist.m3u8

# 4. Click "Load Video"
```

---

## 💡 Pro Tips for ZeroTier

### Assign a Static IP

You can assign a static IP to your server in ZeroTier Central:
1. Go to my.zerotier.com
2. Select your network
3. Find your server's device
4. Assign a managed IP (e.g., `10.244.132.100`)

### Create a Hostname

Use your hosts file to create a friendly name:

**On your laptop:**
```bash
# Linux/Mac
sudo nano /etc/hosts

# Add line:
10.244.132.148  myserver.zt

# Now access via:
# http://myserver.zt:8000/player.html
```

**On Windows:**
```
Edit: C:\Windows\System32\drivers\etc\hosts

Add line:
10.244.132.148  myserver.zt
```

---

## 🔒 Security Considerations

**Current Setup:**
- ✓ ZeroTier traffic is encrypted
- ✓ Only devices on your ZeroTier network can access
- ⚠ HTTP is not encrypted (use HTTPS for production)

**For Production Use:**
- Add HTTPS with SSL certificate
- Implement authentication
- Use firewall rules in ZeroTier network settings
- Consider ZeroTier flow rules for access control

---

## 📞 Quick Commands

```bash
# Check ZeroTier status on laptop
zerotier-cli info

# List your networks
zerotier-cli listnetworks

# Test server connectivity
ping 10.244.132.148

# Test port access
telnet 10.244.132.148 8000

# Access player
# Browser: http://10.244.132.148:8000/player.html
```

---

## ✅ Testing Checklist

- [ ] Laptop has ZeroTier installed
- [ ] Laptop is on the same ZeroTier network
- [ ] Can ping `10.244.132.148` from laptop
- [ ] Server is running on port 8000
- [ ] Firewall allows port 8000 (usually not needed with ZeroTier)
- [ ] Browser can access `http://10.244.132.148:8000/player.html`
- [ ] Video playlist loads and plays

---

**Server ZeroTier IP:** `10.244.132.148`
**Access URL:** `http://10.244.132.148:8000/player.html`
**Network Range:** `10.244.0.0/16`
