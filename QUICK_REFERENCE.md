# 🎬 Video Segment Cutter - Quick Reference Guide

> **Purpose**: Convert videos to HLS format for web streaming with download protection (like YouTube)

---

## 📍 Project Location
```
/mnt/DATA/Project/video-segment-cutter/
```

---

## ⚡ Quick Usage (3 Steps)

### Step 1: Add Your Video
```bash
# Copy video to input folder
cp /path/to/your/video.mp4 /mnt/DATA/Project/video-segment-cutter/input/
```

### Step 2: Convert to HLS
```bash
# Navigate to scripts folder
cd /mnt/DATA/Project/video-segment-cutter/scripts

# Convert the video
./convert-to-hls.sh ../input/your-video.mp4

# With custom segment duration (optional)
./convert-to-hls.sh ../input/your-video.mp4 10
# (10 = 10 seconds per segment, default is 6)
```

### Step 3: View the Video
```bash
# Start web server
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000

# Open browser to: http://localhost:8000/player.html
# Enter path: ../output/your-video/playlist.m3u8
# Click "Load Video"
```

---

## 📂 File Structure Quick Reference

```
video-segment-cutter/
├── input/                          # ← PUT YOUR VIDEOS HERE
│   └── myvideo.mp4
│
├── output/                         # ← HLS OUTPUT (auto-created)
│   └── myvideo/
│       ├── playlist.m3u8          # ← Master playlist
│       ├── segment_000.ts         # ← Video chunks
│       ├── segment_001.ts
│       └── ...
│
├── scripts/
│   └── convert-to-hls.sh          # ← CONVERSION SCRIPT
│
└── web/
    └── player.html                # ← OPEN IN BROWSER
```

---

## 🔧 Common Commands

### Check if FFmpeg is Installed
```bash
ffmpeg -version
```

### Install FFmpeg (if needed)
```bash
# Arch Linux
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### Convert Single Video
```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts
./convert-to-hls.sh ../input/video.mp4
```

### Convert Multiple Videos
```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts

# Loop through all MP4 files in input/
for video in ../input/*.mp4; do
    ./convert-to-hls.sh "$video"
done
```

### Start Web Server (Multiple Options)
```bash
# Option 1: Python 3
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000

# Option 2: Python 2
python -m SimpleHTTPServer 8000

# Option 3: Node.js
npx http-server -p 8000

# Option 4: PHP
php -S localhost:8000
```

### View Output Files
```bash
# List all converted videos
ls -lh /mnt/DATA/Project/video-segment-cutter/output/

# Check specific video segments
ls -lh /mnt/DATA/Project/video-segment-cutter/output/myvideo/
```

---

## 🎯 Segment Duration Guide

| Duration | Use Case | Pros | Cons |
|----------|----------|------|------|
| 3-4 sec  | Fast start time | Quick loading | More files, more requests |
| 6 sec    | **DEFAULT** | Balanced | Good for most cases |
| 10 sec   | Fewer files | Less HTTP overhead | Slower start time |
| 15+ sec  | Long videos | Minimal files | Noticeable buffering |

**Example:**
```bash
# Fast start (3 seconds per segment)
./convert-to-hls.sh ../input/video.mp4 3

# Standard (6 seconds - default)
./convert-to-hls.sh ../input/video.mp4

# Fewer files (10 seconds per segment)
./convert-to-hls.sh ../input/video.mp4 10
```

---

## 🌐 Accessing the Player

### Local Access (file://)
```
Just open: /mnt/DATA/Project/video-segment-cutter/web/player.html
Path: ../output/your-video/playlist.m3u8
```

### Via HTTP Server (recommended)
```bash
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000

# Then visit: http://localhost:8000/player.html
```

### From Another Computer (LAN)
```bash
# 1. Find your IP address
ip addr show | grep "inet "

# 2. Start server
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000

# 3. Access from another device
# http://YOUR_IP:8000/player.html
# Example: http://192.168.1.100:8000/player.html
```

---

## 🛠️ Troubleshooting Quick Fixes

### Problem: "FFmpeg not found"
```bash
# Check if installed
which ffmpeg

# Install it
sudo pacman -S ffmpeg  # Arch
sudo apt install ffmpeg  # Ubuntu
```

### Problem: "Permission denied"
```bash
# Make script executable
chmod +x /mnt/DATA/Project/video-segment-cutter/scripts/convert-to-hls.sh
```

### Problem: "Video won't play in browser"
```bash
# Use HTTP server instead of file://
cd /mnt/DATA/Project/video-segment-cutter/web
python -m http.server 8000
```

### Problem: "Port 8000 already in use"
```bash
# Use different port
python -m http.server 8080
# Then visit: http://localhost:8080/player.html
```

### Problem: "Output folder full of old videos"
```bash
# Clean up output folder
rm -rf /mnt/DATA/Project/video-segment-cutter/output/*
# (Keep .gitkeep file if using git)
```

---

## 💡 Pro Tips

### Batch Convert All Videos
```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts

# Convert all MP4 files
for video in ../input/*.mp4; do
    echo "Converting: $video"
    ./convert-to-hls.sh "$video"
done
```

### Check Video Info Before Converting
```bash
ffmpeg -i input/your-video.mp4
# Shows: duration, resolution, codec, bitrate, etc.
```

### Calculate Approximate Output Size
```
Original Size ÷ Compression Ratio ≈ Output Size
- Typical compression: 70-90% of original
- HLS overhead: +5-10% (metadata files)
```

### Customize Quality
```bash
# Edit the script and add quality parameters:
# For lower quality (smaller files):
-b:v 1000k -s 1280x720

# For higher quality:
-b:v 5000k -s 1920x1080
```

---

## 📋 Complete Workflow Example

```bash
# 1. Navigate to project
cd /mnt/DATA/Project/video-segment-cutter

# 2. Check what videos you have
ls -lh input/

# 3. Convert a specific video
cd scripts
./convert-to-hls.sh ../input/my-tutorial.mp4 6

# 4. Verify output was created
ls -lh ../output/my-tutorial/

# 5. Start web server
cd ../web
python -m http.server 8000

# 6. Open browser
#    URL: http://localhost:8000/player.html
#    Playlist: ../output/my-tutorial/playlist.m3u8
#    Click: Load Video

# 7. Stop server when done (Ctrl+C)
```

---

## 🔐 Download Protection Features

**What prevents easy downloading:**
- ✅ Video split into 50-100+ small segments
- ✅ Right-click disabled on video
- ✅ Ctrl+S (Save) shortcuts blocked
- ✅ No direct download URL
- ✅ Browser download button hidden

**What doesn't prevent:**
- ❌ Browser DevTools (Network tab)
- ❌ Screen recording software
- ❌ Dedicated video downloaders
- ❌ FFmpeg segment merging

**Note:** This provides moderate protection suitable for casual content. For commercial/premium content, add DRM encryption.

---

## 📞 Quick Help

- Full docs: `README.md`
- Script location: `/mnt/DATA/Project/video-segment-cutter/scripts/convert-to-hls.sh`
- Player location: `/mnt/DATA/Project/video-segment-cutter/web/player.html`
- FFmpeg docs: https://ffmpeg.org/documentation.html

---

## 🚀 One-Liner Shortcuts

```bash
# Complete workflow in one go
cd /mnt/DATA/Project/video-segment-cutter/scripts && \
./convert-to-hls.sh ../input/video.mp4 && \
cd ../web && \
python -m http.server 8000

# Convert and auto-open browser (Linux with xdg-open)
cd /mnt/DATA/Project/video-segment-cutter/scripts && \
./convert-to-hls.sh ../input/video.mp4 && \
cd ../web && \
python -m http.server 8000 & \
sleep 2 && \
xdg-open http://localhost:8000/player.html

# Create alias for quick access (add to ~/.bashrc)
alias hls-convert='cd /mnt/DATA/Project/video-segment-cutter/scripts && ./convert-to-hls.sh'
alias hls-serve='cd /mnt/DATA/Project/video-segment-cutter/web && python -m http.server 8000'
```

---

**Last Updated:** December 2025
**Location:** `/mnt/DATA/Project/video-segment-cutter/`
