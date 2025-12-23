# 🏗️ System Architecture - Video Segment Cutter v2.0

## Overview

This document describes the architecture of the Video Segment Cutter with real-time progress tracking.

## System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │              │  │              │  │              │  │              ││
│  │  index.html  │  │ convert.html │  │ player.html  │  │ manage.html  ││
│  │              │  │              │  │              │  │              ││
│  │  Home Page   │  │   Convert    │  │  Watch       │  │  Manage      ││
│  │              │  │   with       │  │  Videos      │  │  Videos      ││
│  │              │  │  Progress    │  │              │  │              ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘│
│         │                 │                 │                 │         │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────┘
          │                 │                 │                 │
          │        HTTP     │                 │        HTTP     │
          │     Port 8000   │                 │     Port 8000   │
          ├─────────────────┴─────────────────┴─────────────────┤
          │                                                       │
          │              Web Server (Python HTTP)                │
          │                                                       │
          └───────────────────────────┬───────────────────────────┘
                                      │
                              Serves static files
                                      │
          ┌───────────────────────────┴───────────────────────────┐
          │                                                         │
    ┌─────▼─────┐                                         ┌────────▼────────┐
    │           │                                         │                 │
    │  style    │                                         │     output/     │
    │  .css     │                                         │                 │
    │           │                                         │   Symlinked     │
    └───────────┘                                         │   for web       │
                                                          │   access        │
                                                          └─────────────────┘
                 HTTP API
                Port 8001
          ┌─────────────────┐
          │                 │
          │   api.py        │──────────┐
          │                 │          │
          │  Flask-like     │          │
          │  HTTP Server    │          │
          │                 │          │
          └────┬────────────┘          │
               │                       │
               │                       │
    ┌──────────▼────────────┐          │
    │                       │          │
    │   API Endpoints       │          │
    │                       │          │
    │  GET  /api/videos     │          │
    │  GET  /api/progress/  │          │
    │  POST /api/videos     │          │
    │       (convert)       │          │
    │                       │          │
    └──────┬────────────────┘          │
           │                           │
           │ Spawns Process            │ Reads Progress
           │                           │
    ┌──────▼─────────────────┐         │
    │                        │         │
    │  convert-to-hls-       │         │
    │  progress.sh           │         │
    │                        │         │
    │  Bash Script           │         │
    │                        │         │
    └───────┬────────────────┘         │
            │                          │
            │ Executes                 │
            │                          │
    ┌───────▼────────────────┐         │
    │                        │         │
    │       FFmpeg           │         │
    │                        │         │
    │  Video Encoder         │         │
    │                        │         │
    │  -progress pipe:1      │         │
    │                        │         │
    └───────┬────────────────┘         │
            │                          │
            │ stdout                   │
            │                          │
    ┌───────▼────────────────┐         │
    │                        │         │
    │   Progress Parser      │         │
    │   (Bash regex)         │         │
    │                        │         │
    │  - Parse time=         │         │
    │  - Parse speed=        │         │
    │  - Parse frame=        │         │
    │  - Calculate %         │         │
    │  - Calculate ETA       │         │
    │                        │         │
    └───────┬────────────────┘         │
            │                          │
            │ Writes JSON              │
            │                          │
    ┌───────▼────────────────┐         │
    │                        │         │
    │  .progress.json        │◄────────┘
    │                        │
    │  Status: converting    │
    │  Progress: 67%         │
    │  Speed: 2.3x           │
    │  ETA: 1m 52s           │
    │  Frame: 4824           │
    │  Time: 00:03:21        │
    │                        │
    └────────────────────────┘

```

## Data Flow

### 1. Conversion Initiation
```
User (Browser)
    │
    │ Click "Start Conversion"
    ▼
convert.html (JavaScript)
    │
    │ POST /api/videos
    │ { command: "convert_single", video: "test.mp4" }
    ▼
api.py (Python)
    │
    │ subprocess.Popen()
    ▼
convert-to-hls-progress.sh (Bash)
    │
    │ Starts FFmpeg process
    ▼
FFmpeg (C binary)
    │
    │ Begins encoding
    └─→ Outputs to: output/test/segment_*.ts
                    output/test/playlist.m3u8
```

### 2. Progress Tracking Loop
```
FFmpeg
    │
    │ -progress pipe:1
    │ time=00:03:21.45 frame=4824 fps=115 speed=2.3x
    ▼
Bash Script (Parser)
    │
    │ Regex extraction:
    │ - time → current_time (201 seconds)
    │ - speed → 2.3x
    │ - frame → 4824
    │
    │ Calculations:
    │ - progress = (201 / 300) * 100 = 67%
    │ - eta = (300 - 201) / 2.3 = 43 seconds
    │
    ▼
.progress.json
    │
    │ JSON format:
    │ {
    │   "status": "converting",
    │   "progress": 67,
    │   "speed": "2.3x",
    │   "eta": "43s"
    │ }
    │
    │ (Updated every ~200ms)
    │
    │
    │ ◄───────────────────────┐
    │                         │
    │ HTTP GET                │
    │                         │
api.py (Python)              │
    │                         │
    │ /api/progress/test      │
    │                         │
    ▼                         │
convert.html                  │
    │                         │
    │ Update UI:              │
    │ - Progress bar: 67%     │
    │ - Speed: 2.3x           │
    │ - ETA: 43s              │
    │                         │
    └─────────────────────────┘
         Poll every 500ms
```

### 3. File Structure During Conversion
```
output/
└── test-video/
    ├── playlist.m3u8           ← HLS master playlist
    ├── segment_000.ts          ← Video segment 1
    ├── segment_001.ts          ← Video segment 2
    ├── segment_002.ts          ← Video segment 3
    ├── ...
    ├── .progress.json          ← Live progress data (updated continuously)
    └── .conversion.log         ← Detailed FFmpeg log
```

## Component Details

### Frontend (Web UI)

#### convert.html
- **Purpose:** Main conversion interface with progress tracking
- **Technology:** HTML5, CSS3, Vanilla JavaScript
- **Features:**
  - Video selection dropdown
  - Segment duration input
  - Real-time progress bar
  - 6-stat dashboard
  - Live console log
  - Auto-redirect on completion
- **API Communication:** HTTP polling (500ms interval)
- **Dependencies:** style.css

#### player.html
- **Purpose:** HLS video playback
- **Technology:** HTML5 Video, HLS.js
- **Features:**
  - Native HLS support (Safari)
  - HLS.js fallback (Chrome, Firefox)
  - Download protection
  - Right-click disabled

#### manage.html
- **Purpose:** Video library management
- **Technology:** HTML5, JavaScript
- **Features:**
  - List all converted videos
  - Delete videos
  - View video metadata
  - Quick actions (batch convert, clean all)

### Backend (API Server)

#### api.py
- **Language:** Python 3
- **Framework:** Standard library (http.server)
- **Port:** 8001
- **Endpoints:**
  - `GET /api/videos` - List all videos
  - `GET /api/progress/{name}` - Get conversion progress
  - `POST /api/videos` - Execute commands (convert, delete, etc.)
  - `GET /api/disk-usage` - Check storage usage
  - `GET /api/server-status` - Check server status

- **Features:**
  - CORS enabled (for cross-origin requests)
  - Background process management
  - JSON progress file reading
  - Subprocess spawning for conversions

### Conversion Engine

#### convert-to-hls-progress.sh
- **Language:** Bash
- **Dependencies:** FFmpeg, ffprobe, bc (for math)
- **Input:** Video file path, segment duration
- **Output:** 
  - HLS playlist (.m3u8)
  - Video segments (.ts files)
  - Progress file (.progress.json)
  - Conversion log (.conversion.log)

- **Process:**
  1. Validate input file
  2. Extract video duration (ffprobe)
  3. Start FFmpeg with progress output
  4. Parse FFmpeg stdout in real-time
  5. Calculate progress percentage
  6. Calculate ETA
  7. Write JSON progress file
  8. Update console with progress bar

#### FFmpeg
- **Purpose:** Video transcoding engine
- **Configuration:**
  - Codec: H.264 (libx264)
  - Audio: AAC
  - Format: HLS
  - Segment duration: 6 seconds (default)
  - Output: Segmented .ts files + .m3u8 playlist

### File System

#### Directory Structure
```
video-segment-cutter/
├── input/                    # Source videos
│   └── test-video.mp4
│
├── output/                   # Converted videos
│   └── test-video/
│       ├── playlist.m3u8     # HLS playlist
│       ├── segment_*.ts      # Video segments
│       ├── .progress.json    # Progress tracking
│       └── .conversion.log   # FFmpeg output
│
├── scripts/                  # Conversion scripts
│   ├── convert-to-hls.sh           # Original (no progress)
│   ├── convert-to-hls-progress.sh  # With progress tracking
│   └── start-server.sh             # Web server starter
│
├── web/                      # Web interface
│   ├── index.html
│   ├── convert.html
│   ├── player.html
│   ├── manage.html
│   ├── upload.html
│   ├── api.py
│   ├── style.css
│   └── output -> ../output   # Symlink for serving files
│
└── docs/                     # Documentation
    ├── README.md
    ├── PROGRESS_TRACKING_GUIDE.md
    ├── QUICK_START_PROGRESS.md
    ├── CHANGELOG.md
    └── ARCHITECTURE.md (this file)
```

## Technology Stack

### Core Technologies
- **FFmpeg** - Video encoding/transcoding
- **Bash** - Script automation and process management
- **Python 3** - API server
- **HTML5/CSS3** - User interface
- **JavaScript (ES6+)** - Client-side logic

### Libraries & Tools
- **HLS.js** - HTML5 video player for HLS (for non-Safari browsers)
- **http.server** - Python's built-in web server
- **subprocess** - Python process management
- **bc** - Bash calculator for floating-point math
- **ffprobe** - Video metadata extraction

### Standards & Protocols
- **HLS (HTTP Live Streaming)** - Apple's streaming protocol
- **HTTP/1.1** - Web communication
- **JSON** - Data interchange format
- **REST** - API design pattern

## Performance Characteristics

### Resource Usage
| Component | CPU | Memory | Disk I/O | Network |
|-----------|-----|--------|----------|---------|
| FFmpeg | High (80-100%) | ~200MB | High (write) | None |
| Bash Script | Low (1-2%) | ~10MB | Low (1KB/200ms) | None |
| Python API | Low (0-5%) | ~30MB | Low (read) | Low (1KB/s) |
| Web UI | Low (0-1%) | ~50MB | None | Low (1KB/s) |

### Scaling Limits
- **Concurrent Conversions:** 1 (sequential processing)
- **Video File Size:** Tested up to 5GB
- **Video Duration:** No theoretical limit
- **Concurrent Web Clients:** Limited by network bandwidth

### Bottlenecks
1. **FFmpeg encoding** - CPU intensive
2. **Disk write speed** - For large files
3. **Sequential processing** - One video at a time

## Security Considerations

### Current Security Posture
- **API Authentication:** ❌ None (localhost only)
- **Input Validation:** ⚠️ Basic (file existence checks)
- **Command Injection:** ✅ Prevented (no shell injection in subprocess)
- **CORS:** ⚠️ Allow all origins (for development)
- **File Access:** ⚠️ No sandboxing
- **Download Protection:** ✅ Video segmentation

### Recommendations for Production
1. Add API authentication (token-based)
2. Implement rate limiting
3. Restrict CORS to specific domains
4. Add file upload validation
5. Implement user permissions
6. Use HTTPS for all communication
7. Add input sanitization
8. Implement file access sandboxing

## Deployment Architecture

### Development Setup
```
┌─────────────────────────┐
│     Developer Machine    │
│                         │
│  ┌──────────────────┐  │
│  │  Web Server      │  │
│  │  :8000           │  │
│  └──────────────────┘  │
│                         │
│  ┌──────────────────┐  │
│  │  API Server      │  │
│  │  :8001           │  │
│  └──────────────────┘  │
│                         │
│  Access: localhost      │
└─────────────────────────┘
```

### Production Setup (Recommended)
```
         Internet
             │
             ▼
      ┌─────────────┐
      │   Nginx     │
      │  (Reverse   │
      │   Proxy)    │
      │   :80/:443  │
      └──────┬──────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
   ┌────────┐  ┌────────┐
   │  Web   │  │  API   │
   │ Server │  │ Server │
   │ :8000  │  │ :8001  │
   └────────┘  └────────┘
        │         │
        └────┬────┘
             │
        ┌────▼─────┐
        │  FFmpeg  │
        │ Workers  │
        └──────────┘
```

## API Contract

### Progress JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["initializing", "converting", "completed", "error"]
    },
    "progress": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
    },
    "message": {
      "type": "string"
    },
    "duration": {
      "type": "integer",
      "description": "Total video duration in seconds"
    },
    "current_time": {
      "type": "integer",
      "description": "Current position in seconds"
    },
    "time_string": {
      "type": "string",
      "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2} / [0-9]{2}:[0-9]{2}:[0-9]{2}$"
    },
    "frame": {
      "type": "string",
      "description": "Current frame number"
    },
    "speed": {
      "type": "string",
      "pattern": "^[0-9.]+x$"
    },
    "eta": {
      "type": "string",
      "description": "Estimated time remaining"
    }
  },
  "required": ["status", "progress", "message"]
}
```

## Error Handling

### Error Flow
```
User Action
    │
    ▼
Frontend Validation
    │
    ├─→ Invalid input → Show error message
    │
    ▼
API Request
    │
    ├─→ Network error → Show error + retry option
    ├─→ 404 Not Found → Show "Video not found"
    ├─→ 500 Server Error → Show error details
    │
    ▼
Conversion Process
    │
    ├─→ FFmpeg error → Log + set status to "error"
    ├─→ File permission error → Log + abort
    ├─→ Disk full → Log + abort
    │
    ▼
Success
```

### Error States
1. **Input validation errors** - Shown immediately in UI
2. **API errors** - Shown in console log, retry available
3. **Conversion errors** - Logged to .conversion.log, status set to "error"

## Monitoring & Logging

### Log Files
- **Conversion Log:** `output/{video}/.conversion.log`
  - FFmpeg detailed output
  - Error messages
  - Warnings

- **Progress File:** `output/{video}/.progress.json`
  - Real-time status
  - Performance metrics
  - Completion status

### Monitoring Points
1. **Conversion progress** - Via .progress.json
2. **Server health** - Via /api/server-status
3. **Disk usage** - Via /api/disk-usage
4. **Process list** - Via ps/top commands

## Future Architecture Enhancements

### Planned Improvements
1. **Queue System** - Redis/RabbitMQ for job queuing
2. **Worker Pool** - Multiple FFmpeg workers for parallel processing
3. **WebSocket** - Replace polling with real-time push
4. **Database** - PostgreSQL for video metadata
5. **Authentication** - JWT token-based auth
6. **CDN Integration** - CloudFront/CloudFlare for distribution
7. **Microservices** - Split API into smaller services

---

**Document Version:** 2.0
**Last Updated:** December 2025
**Maintainer:** Development Team
