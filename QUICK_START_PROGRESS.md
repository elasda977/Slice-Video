# 🚀 Quick Start - Progress Tracking Feature

Get up and running with the new real-time progress tracking in **under 2 minutes**!

## 📋 Prerequisites

- FFmpeg installed (`ffmpeg -version`)
- Python 3 installed (`python3 --version`)
- A video file in the `input/` folder

## ⚡ 2-Minute Setup

### Step 1: Start the Servers (30 seconds)

Open **two terminal windows**:

**Terminal 1 - Web Server:**
```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts
./start-server.sh
```
✅ You should see: `Server running on port 8000`

**Terminal 2 - API Server:**
```bash
cd /mnt/DATA/Project/video-segment-cutter/web
python3 api.py
```
✅ You should see: `API Server running on port 8001...`

### Step 2: Open the Convert Page (10 seconds)

In your web browser, go to:
```
http://localhost:8000/convert.html
```

### Step 3: Convert a Video (1 minute)

1. **Enter filename:** Type `test-mantra.mp4` (or click "custom" to enter your own)
2. **Set segment duration:** Leave at `6` seconds (or adjust 1-30)
3. **Click:** "Start Conversion"
4. **Watch:** Real-time progress updates every 500ms!

### Step 4: View Your Video (20 seconds)

When complete:
- Click **"Yes"** on the popup to auto-play
- Or go to: `http://localhost:8000/player.html`

**Done!** 🎉

---

## 📊 What You'll See

### Progress Dashboard
```
┌─────────────────────────────────────────────┐
│  [████████████████████░░░░░░░░] 67%         │
├─────────────────────────────────────────────┤
│  Status:        Converting                   │
│  Time:          00:02:15 / 00:05:00         │
│  Speed:         2.3x                         │
│  ETA:           1m 52s                       │
│  Frame:         3240                         │
│  Message:       Encoding in progress...      │
└─────────────────────────────────────────────┘
```

### Live Console Log
```
[14:23:45] Starting conversion...
[14:23:46] Video: test-mantra.mp4
[14:23:46] Conversion started successfully
[14:23:47] Tracking ID: test-mantra
[14:25:38] ✓ Conversion completed successfully!
[14:25:38] Segments created: 42
[14:25:38] Total size: 245M
```

---

## 🧪 Quick Test (Optional)

Test the feature with a short video clip:

```bash
cd /mnt/DATA/Project/video-segment-cutter
./test-progress.sh
```

This will:
- ✅ Create a 10-second test clip
- ✅ Run conversion with progress tracking
- ✅ Verify all output files
- ✅ Check progress JSON format
- ⏱️ Takes ~30 seconds total

---

## 🎯 Common Use Cases

### Case 1: Quick Preview
```bash
# Convert just 30 seconds for testing
ffmpeg -i input/video.mp4 -t 30 -c copy input/preview.mp4
# Then convert preview.mp4 with progress tracking
```

### Case 2: Different Segment Sizes
- **3 seconds:** Fast startup, more files
- **6 seconds:** Balanced (recommended)
- **10 seconds:** Fewer files, slower startup

### Case 3: Monitor from Phone
```bash
# On your computer, find your IP:
ip addr show | grep "inet " | grep -v "127.0.0.1"

# On your phone, open:
http://YOUR_IP:8000/convert.html
```

---

## 🔧 Troubleshooting

### Problem: API not responding
```bash
# Check if API is running:
curl http://localhost:8001/api/videos

# If not, restart:
cd /mnt/DATA/Project/video-segment-cutter/web
python3 api.py
```

### Problem: Progress stuck at 0%
```bash
# Check the progress file:
cat output/your-video/.progress.json

# Check if conversion is running:
ps aux | grep ffmpeg

# Check the log:
tail -f output/your-video/.conversion.log
```

### Problem: "No videos found"
```bash
# List input folder:
ls -la input/

# Add a video:
cp /path/to/video.mp4 input/
```

---

## 📱 Network Access

### Access from Other Devices

1. **Find your computer's IP:**
   ```bash
   hostname -I | awk '{print $1}'
   ```

2. **On other devices, use:**
   - Web UI: `http://YOUR_IP:8000/convert.html`
   - API: `http://YOUR_IP:8001/api/progress/video-name`

3. **Note:** Make sure firewall allows ports 8000 and 8001

---

## 💡 Pro Tips

### Tip 1: Keep Terminals Open
Leave both terminal windows open while converting. The API server needs to be running for progress tracking to work.

### Tip 2: Multiple Conversions
You can queue multiple conversions by:
1. Start first video
2. Wait for completion (or monitor progress)
3. Start next video

### Tip 3: Check Progress from Terminal
```bash
# Watch progress file update in real-time:
watch -n 1 cat output/your-video/.progress.json

# Or use jq for pretty formatting:
watch -n 1 "cat output/your-video/.progress.json | jq"
```

### Tip 4: Background Conversions
```bash
# Start conversion in background:
cd scripts
nohup ./convert-to-hls-progress.sh ../input/video.mp4 &

# Check progress via API:
curl http://localhost:8001/api/progress/video
```

---

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Read Full Guide:** [PROGRESS_TRACKING_GUIDE.md](PROGRESS_TRACKING_GUIDE.md)
2. **Explore API:** Try API endpoints with `curl` or Postman
3. **Customize:** Modify segment duration, video quality
4. **Integrate:** Use the API in your own applications

---

## 📚 Commands Cheat Sheet

```bash
# Start servers
cd scripts && ./start-server.sh                    # Web (Terminal 1)
cd web && python3 api.py                           # API (Terminal 2)

# Convert with progress
cd scripts && ./convert-to-hls-progress.sh ../input/video.mp4

# Check progress (API)
curl http://localhost:8001/api/progress/video-name

# List all videos
curl http://localhost:8001/api/videos

# Test feature
./test-progress.sh

# View progress file
cat output/video-name/.progress.json | jq

# Monitor in real-time
watch -n 1 cat output/video-name/.progress.json
```

---

## 🆘 Need Help?

- **Documentation:** See [README.md](README.md)
- **Detailed Guide:** See [PROGRESS_TRACKING_GUIDE.md](PROGRESS_TRACKING_GUIDE.md)
- **Changelog:** See [CHANGELOG.md](CHANGELOG.md)
- **FFmpeg Help:** Run `ffmpeg -h` or visit [ffmpeg.org](https://ffmpeg.org)

---

**Happy Converting! 🎬**

Last Updated: December 2025
