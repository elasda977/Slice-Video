# 📋 Changelog - Video Segment Cutter

## [2.0.0] - December 2025 - Progress Tracking Update

### ✨ New Features

#### 1. Real-Time Progress Tracking
- **New Script:** `scripts/convert-to-hls-progress.sh`
  - Shows live progress bar in terminal
  - Outputs encoding speed (e.g., 2.5x realtime)
  - Calculates and displays ETA
  - Tracks current frame count
  - Displays time elapsed vs total duration

- **Progress File:** `.progress.json`
  - JSON-formatted progress data
  - Updated in real-time during conversion
  - Accessible via API for web UI

- **Conversion Log:** `.conversion.log`
  - Detailed FFmpeg output
  - Useful for debugging failed conversions

#### 2. New Web Interface
- **Convert Page:** `web/convert.html`
  - Dedicated conversion interface
  - Video file selection
  - Adjustable segment duration
  - Live progress dashboard with 6 stats:
    - Status indicator
    - Time elapsed/remaining
    - Encoding speed
    - ETA calculation
    - Frame counter
    - Status messages
  - Real-time conversion log
  - Auto-redirect to player on completion

#### 3. Enhanced API
- **New Endpoint:** `GET /api/progress/{video_name}`
  - Returns real-time conversion progress
  - JSON format with all tracking data

- **New Endpoint:** `POST /api/videos` (command: `convert_single`)
  - Start single video conversion from API
  - Background process handling
  - Returns video ID for progress tracking

### 🔧 Improvements

#### Navigation Updates
- Replaced "Upload" with "Convert" in main navigation
- Updated all pages (index, player, manage, upload)
- Better user flow from home → convert → watch

#### Code Quality
- Added comprehensive error handling
- Progress calculation with bc for floating-point math
- Better process management for background conversions
- Improved log formatting and readability

### 📚 Documentation

#### New Files
- `PROGRESS_TRACKING_GUIDE.md` - Complete feature documentation
- `test-progress.sh` - Automated testing script
- `CHANGELOG.md` - This file

#### Updated Files
- Navigation menus across all HTML pages
- API documentation inline comments

### 🎯 Technical Details

#### Progress Calculation Algorithm
```
1. Extract video duration with ffprobe
2. Parse FFmpeg time output (HH:MM:SS)
3. Calculate: progress = (current_time / duration) * 100
4. Extract speed from FFmpeg (e.g., "2.3x")
5. Calculate ETA: remaining_time / speed
6. Update JSON file every frame
```

#### Polling System
- Web UI polls API every 500ms
- FFmpeg outputs progress every ~200ms
- Progress file written on every update
- No performance impact on encoding

#### Status States
- `initializing` - Video analysis in progress
- `converting` - Active encoding
- `completed` - Success, all files created
- `error` - Failed, check log file

### 🚀 Performance

#### Encoding Speed
- No performance overhead from progress tracking
- Uses FFmpeg's native progress output
- File I/O optimized for minimal impact

#### Network Efficiency
- Lightweight JSON responses (~500 bytes)
- Efficient polling interval (500ms)
- No video streaming during conversion

### 🔄 Migration Guide

#### For Existing Users

**Old workflow:**
```bash
cd scripts
./convert-to-hls.sh ../input/video.mp4
# No feedback until complete
```

**New workflow (Command Line):**
```bash
cd scripts
./convert-to-hls-progress.sh ../input/video.mp4
# Shows: [Progress: 45% | Time: 00:02:30 / 00:05:00 | Speed: 2.3x | ETA: 1m 52s]
```

**New workflow (Web UI):**
```bash
# Terminal 1: Start web server
cd scripts
./start-server.sh

# Terminal 2: Start API server
cd web
python3 api.py

# Browser: http://localhost:8000/convert.html
# - Select video
# - Watch real-time progress
# - Auto-redirect to player
```

#### Backward Compatibility
- Old script still available: `convert-to-hls.sh`
- All existing functionality preserved
- No breaking changes to output format
- Existing videos still playable

### 🧪 Testing

#### Automated Test
```bash
cd /mnt/DATA/Project/video-segment-cutter
./test-progress.sh
```

Tests verify:
- Script execution
- Progress file creation
- Output file generation
- JSON format validity
- Log file creation

#### Manual Testing Checklist
- [ ] Start both servers (web + API)
- [ ] Access convert page
- [ ] Select test video
- [ ] Verify progress updates
- [ ] Check all 6 statistics display
- [ ] Confirm ETA accuracy
- [ ] Verify completion redirect
- [ ] Check output files created

### 📊 Statistics

#### File Changes
- **New Files:** 4
  - `scripts/convert-to-hls-progress.sh` (267 lines)
  - `web/convert.html` (380 lines)
  - `PROGRESS_TRACKING_GUIDE.md` (400+ lines)
  - `test-progress.sh` (120 lines)

- **Modified Files:** 6
  - `web/api.py` (+80 lines)
  - `web/index.html` (navigation update)
  - `web/player.html` (navigation update)
  - `web/manage.html` (navigation update)
  - `web/upload.html` (navigation update)

- **Total Lines Added:** ~1,300+

#### Features Added
- 1 new conversion script
- 1 new web page
- 2 new API endpoints
- 6 progress statistics
- 1 test automation script
- 3 documentation files

### 🐛 Bug Fixes
- None (new feature release)

### 🔒 Security Notes
- Progress files stored in hidden directory (`.progress.json`)
- No sensitive data in progress output
- API still requires localhost/network access
- Command injection prevention in place

### ⚠️ Known Limitations
1. **Sequential Processing:** Batch conversions run one at a time
2. **No Pause/Resume:** Once started, conversion runs to completion
3. **Progress File Cleanup:** Manual deletion required
4. **API Authentication:** None (localhost only recommended)

### 🔮 Future Roadmap
- [ ] Parallel batch processing
- [ ] WebSocket for real-time updates
- [ ] Pause/Resume capability
- [ ] Video thumbnail generation
- [ ] Quality preset selection
- [ ] Email notifications
- [ ] Progress history/analytics
- [ ] Multi-bitrate encoding

---

## [1.0.0] - December 2025 - Initial Release

### Features
- HLS video conversion with FFmpeg
- Web-based video player
- Video management interface
- Upload interface (UI only)
- Network access support (LAN/ZeroTier)
- Download protection
- Basic API for video operations

---

**Project:** Video Segment Cutter - HLS Video Platform
**Repository:** `/mnt/DATA/Project/video-segment-cutter`
**Documentation:** See README.md and PROGRESS_TRACKING_GUIDE.md
