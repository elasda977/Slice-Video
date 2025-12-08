# 📊 Progress Tracking Feature Guide

## Overview

The video conversion now includes **real-time progress tracking** that displays:
- Conversion percentage (0-100%)
- Current time / Total duration
- Encoding speed (e.g., 2.5x)
- Estimated time remaining (ETA)
- Current frame being processed
- Status messages

## 🆕 What's New

### 1. Enhanced Conversion Script
**File:** `scripts/convert-to-hls-progress.sh`

This new script replaces the basic conversion with advanced progress tracking:
- Parses FFmpeg output in real-time
- Generates JSON progress file (`.progress.json`)
- Calculates completion percentage
- Estimates time remaining
- Logs detailed conversion info

### 2. Progress Tracking API
**Endpoint:** `GET /api/progress/{video_name}`

Returns real-time conversion progress in JSON format:
```json
{
  "status": "converting",
  "progress": 45,
  "message": "Encoding in progress...",
  "duration": 300,
  "current_time": 135,
  "time_string": "00:02:15 / 00:05:00",
  "frame": "3240",
  "speed": "2.3x",
  "eta": "1m 52s"
}
```

### 3. New Convert Page
**File:** `web/convert.html`

A dedicated page for video conversion with:
- Video file selection
- Segment duration configuration
- Real-time progress bar
- Live statistics dashboard
- Conversion log display
- Auto-redirect to player on completion

## 🚀 How to Use

### Option 1: Web Interface (Recommended)

1. **Start the servers:**
   ```bash
   cd /mnt/DATA/Project/video-segment-cutter/scripts
   ./start-server.sh    # Web server (port 8000)
   ```

2. **Start the API server (in another terminal):**
   ```bash
   cd /mnt/DATA/Project/video-segment-cutter/web
   python3 api.py       # API server (port 8001)
   ```

3. **Open the convert page:**
   - Navigate to: `http://localhost:8000/convert.html`
   - Enter your video filename (must be in `input/` folder)
   - Set segment duration (default: 6 seconds)
   - Click "Start Conversion"

4. **Watch the progress:**
   - Progress bar updates every 500ms
   - View encoding speed, ETA, frames
   - Check conversion log for detailed output

5. **When complete:**
   - Click "Yes" to play the video immediately
   - Or go to Manage page to view all videos

### Option 2: Command Line

For direct command-line conversion with progress:

```bash
cd /mnt/DATA/Project/video-segment-cutter/scripts
./convert-to-hls-progress.sh ../input/myvideo.mp4 6
```

This will:
- Show progress bar in terminal
- Create `.progress.json` file in output folder
- Display speed, ETA, and completion stats

## 📁 Progress File Format

The progress file is stored at:
```
output/{video_name}/.progress.json
```

**Status values:**
- `initializing` - Getting video information
- `converting` - Encoding in progress
- `completed` - Conversion successful
- `error` - Conversion failed

**Example progress file:**
```json
{
  "status": "converting",
  "progress": 67,
  "message": "Encoding in progress...",
  "duration": 1200,
  "current_time": 804,
  "time_string": "00:13:24 / 00:20:00",
  "frame": "19296",
  "speed": "2.1x",
  "eta": "4m 15s"
}
```

**On completion:**
```json
{
  "status": "completed",
  "progress": 100,
  "message": "Conversion completed successfully!",
  "duration": 1200,
  "segments": 200,
  "output_size": "450M"
}
```

**On error:**
```json
{
  "status": "error",
  "progress": 0,
  "message": "Conversion failed. Check log file for details.",
  "error": "Invalid codec parameters..."
}
```

## 🔧 API Endpoints

### Start Conversion
```bash
POST http://localhost:8001/api/videos
Content-Type: application/json

{
  "command": "convert_single",
  "video": "myvideo.mp4",
  "segment_duration": 6
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversion started for myvideo.mp4",
  "video_id": "myvideo",
  "pid": 12345
}
```

### Get Progress
```bash
GET http://localhost:8001/api/progress/myvideo
```

**Response:** (see Progress File Format above)

### List All Videos
```bash
GET http://localhost:8001/api/videos
```

## 🎯 Progress Calculation

The script calculates progress using:

1. **Video Duration:** Extracted using `ffprobe`
2. **Current Time:** Parsed from FFmpeg output (`time=HH:MM:SS`)
3. **Progress %:** `(current_time / total_duration) * 100`
4. **Speed:** From FFmpeg output (`speed=X.XXx`)
5. **ETA:** `(remaining_time / speed)`

## 📊 Performance Tips

### Faster Encoding
- Use hardware acceleration (if available):
  ```bash
  ffmpeg -hwaccel cuda ...    # NVIDIA GPU
  ffmpeg -hwaccel vaapi ...   # AMD/Intel GPU
  ```

### Progress Update Frequency
- Web UI polls every 500ms (adjustable in `convert.html`)
- FFmpeg updates every ~200ms internally
- Progress file updated in real-time

### Batch Conversion
For multiple videos, the web UI shows sequential progress:
1. Video 1: 0% → 100%
2. Video 2: 0% → 100%
3. etc.

## 🐛 Troubleshooting

### Progress Not Updating
1. **Check API server is running:**
   ```bash
   curl http://localhost:8001/api/progress/test
   ```

2. **Check progress file exists:**
   ```bash
   ls -la output/myvideo/.progress.json
   ```

3. **Check conversion process:**
   ```bash
   ps aux | grep ffmpeg
   ```

### Progress Stuck at 0%
- Video duration couldn't be determined
- FFmpeg not outputting progress (check log file)
- Script doesn't have write permissions

### ETA Shows "calculating..."
- Speed is 0 or couldn't be parsed
- Video just started (wait a few seconds)
- FFmpeg speed data not available

## 📝 File Locations

```
video-segment-cutter/
├── scripts/
│   ├── convert-to-hls.sh           # Original script (no progress)
│   └── convert-to-hls-progress.sh  # NEW: With progress tracking
├── web/
│   ├── convert.html                # NEW: Conversion page
│   ├── api.py                      # Updated: Progress API
│   └── ...
└── output/
    └── {video_name}/
        ├── playlist.m3u8
        ├── segment_*.ts
        ├── .progress.json          # NEW: Progress tracking
        └── .conversion.log         # NEW: Detailed FFmpeg log
```

## 🔄 Comparison: Old vs New

### Old Script (`convert-to-hls.sh`)
```bash
./convert-to-hls.sh input/video.mp4
# ✓ Simple
# ✗ No progress feedback
# ✗ Can't track from web UI
# ✗ No ETA
```

### New Script (`convert-to-hls-progress.sh`)
```bash
./convert-to-hls-progress.sh input/video.mp4
# ✓ Real-time progress bar
# ✓ Speed and ETA display
# ✓ Web UI integration
# ✓ JSON progress file
# ✓ Detailed logging
```

## 🌐 Network Access

To monitor conversions from other devices:

1. **Find your IP:**
   ```bash
   ip addr show | grep "inet "
   ```

2. **Access from other devices:**
   ```
   http://YOUR_IP:8000/convert.html
   ```

3. **API endpoint:**
   ```
   http://YOUR_IP:8001/api/progress/{video_name}
   ```

## 💡 Future Enhancements

Potential improvements:
- [ ] Parallel batch processing (multiple videos at once)
- [ ] Websocket for real-time updates (instead of polling)
- [ ] Video thumbnail preview during conversion
- [ ] Pause/Resume capability
- [ ] Priority queue for conversions
- [ ] Email/notification on completion
- [ ] Quality presets (low/medium/high)
- [ ] Multi-bitrate adaptive streaming

## 📚 Related Documentation

- [README.md](README.md) - Project overview
- [START_HERE.txt](START_HERE.txt) - Getting started guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures

---

**Last Updated:** December 2025
