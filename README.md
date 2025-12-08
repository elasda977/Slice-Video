# 🎬 Video Segment Cutter - HLS Video Streaming

Convert videos to HLS format (.m3u8 + .ts segments) for streaming on websites with download protection, similar to YouTube.

## 🆕 What's New in v2.0 - Real-Time Progress Tracking!

**Just Added:** Live conversion progress with detailed statistics!
- 📊 Real-time progress bar (0-100%)
- ⏱️ Live ETA and encoding speed
- 🎯 Frame-by-frame tracking
- 🌐 Beautiful web interface
- 📱 Monitor from any device

👉 **[Quick Start Guide](QUICK_START_PROGRESS.md)** | **[Full Documentation](PROGRESS_TRACKING_GUIDE.md)** | **[Changelog](CHANGELOG.md)**

## 📋 Features

- **🆕 Real-Time Progress Tracking**: Watch conversions with live stats and ETA
- **Download Protection**: Videos are split into small segments, making it difficult to download the complete file
- **Browser-Native Playback**: Works in all modern browsers without plugins
- **Easy Conversion**: Simple bash script to convert any video to HLS format
- **Web Player Included**: Ready-to-use HTML5 video player with HLS support
- **Right-Click Protection**: Disabled context menu and download shortcuts
- **Adaptive Streaming Ready**: Can be extended to support multiple quality levels

## 🏗️ Project Structure

```
video-segment-cutter/
├── input/              # Place your original videos here
├── output/             # Converted HLS videos (auto-generated)
│   └── videoname/
│       ├── playlist.m3u8    # Master playlist
│       └── segment_*.ts     # Video segments
├── scripts/
│   └── convert-to-hls.sh    # Conversion script
├── web/
│   └── player.html          # Video player interface
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **FFmpeg** must be installed:
   ```bash
   # Arch Linux
   sudo pacman -S ffmpeg

   # Ubuntu/Debian
   sudo apt install ffmpeg

   # macOS
   brew install ffmpeg
   ```

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

### Usage

#### Step 1: Place Your Video

Copy your video file to the `input/` directory:
```bash
cp /path/to/your/video.mp4 input/
```

#### Step 2: Convert to HLS

Run the conversion script:
```bash
cd scripts
./convert-to-hls.sh ../input/video.mp4
```

**With custom segment duration:**
```bash
./convert-to-hls.sh ../input/video.mp4 10
# Creates 10-second segments (default is 6 seconds)
```

#### Step 3: Play the Video

1. Open `web/player.html` in your browser
2. Enter the playlist path: `../output/video/playlist.m3u8`
3. Click "Load Video"

**Or serve via HTTP server:**
```bash
# Python 3
cd web
python -m http.server 8000

# Node.js
npx http-server web -p 8000
```

Then visit: `http://localhost:8000/player.html`

## 🎯 How It Works

### HLS (HTTP Live Streaming)

1. **Segmentation**: FFmpeg splits the video into small chunks (typically 6-10 seconds)
2. **Playlist**: Creates an `.m3u8` file that lists all video segments in order
3. **Streaming**: Browser downloads and plays segments sequentially
4. **Protection**: Users can't easily download the complete video

### FFmpeg Parameters Explained

```bash
-profile:v baseline    # Maximum compatibility with devices
-level 3.0            # H.264 level for baseline profile
-hls_time 6           # Each segment is 6 seconds long
-hls_list_size 0      # Keep all segments in playlist
-hls_segment_filename # Naming pattern for segment files
-f hls                # Output format: HLS
```

## 🛡️ Download Protection Levels

This solution provides **moderate protection**:

✅ **What it prevents:**
- Simple right-click "Save Video As"
- Keyboard shortcuts (Ctrl+S)
- Browser's built-in download button
- Casual users from easily downloading

⚠️ **What it doesn't prevent:**
- Browser developer tools (Network tab)
- Dedicated download tools (youtube-dl, etc.)
- Screen recording
- Segment concatenation with FFmpeg

### Additional Protection Options

For stronger protection, consider:

1. **DRM (Digital Rights Management)**
   - Widevine, PlayReady, FairPlay
   - Requires license server

2. **Token-Based Authentication**
   - Generate time-limited URLs
   - Server-side validation

3. **Video Encryption**
   - AES-128 encryption for segments
   - Requires key delivery server

4. **Watermarking**
   - Embed user IDs in video
   - Deter redistribution

## 📊 Advanced Usage

### Multiple Quality Levels (Adaptive Bitrate)

Create different quality versions:

```bash
# High quality (1080p)
./convert-to-hls.sh ../input/video.mp4 6

# Medium quality (720p)
ffmpeg -i ../input/video.mp4 -vf scale=1280:720 -b:v 2500k \
  -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "../output/video/720p_%03d.ts" \
  ../output/video/720p.m3u8

# Low quality (480p)
ffmpeg -i ../input/video.mp4 -vf scale=854:480 -b:v 1000k \
  -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "../output/video/480p_%03d.ts" \
  ../output/video/480p.m3u8
```

### Customize Segment Duration

Smaller segments = faster start time, more HTTP requests
Larger segments = slower start time, fewer HTTP requests

```bash
# 3-second segments (faster start)
./convert-to-hls.sh ../input/video.mp4 3

# 10-second segments (fewer files)
./convert-to-hls.sh ../input/video.mp4 10
```

## 🔧 Troubleshooting

### Video won't play

1. **Check file path**: Ensure the `.m3u8` path is correct
2. **Use HTTP server**: Some browsers require HTTP (not file://)
3. **Check console**: Open browser DevTools for errors
4. **CORS issues**: If serving from different domain, configure CORS headers

### Conversion failed

1. **Check FFmpeg**: Verify it's installed (`ffmpeg -version`)
2. **Check input file**: Ensure video file exists and is valid
3. **Check permissions**: Ensure write access to output directory
4. **Check disk space**: Ensure enough space for output files

### Playback stuttering

1. **Reduce segment duration**: Use larger segments (10s instead of 6s)
2. **Optimize bitrate**: Lower the video quality/bitrate
3. **Check network**: Ensure stable internet connection
4. **Preload settings**: Adjust browser preload settings

## 📝 Example Workflow

```bash
# 1. Navigate to project
cd /mnt/DATA/Project/video-segment-cutter

# 2. Copy video to input
cp ~/Videos/myvideo.mp4 input/

# 3. Convert to HLS
cd scripts
./convert-to-hls.sh ../input/myvideo.mp4

# 4. Start web server
cd ../web
python -m http.server 8000

# 5. Open browser
# Visit: http://localhost:8000/player.html
# Enter: ../output/myvideo/playlist.m3u8
# Click: Load Video
```

## 🌐 Deployment to Website

### Option 1: Static Hosting (GitHub Pages, Netlify)

```bash
# Upload the entire web/ and output/ folders
# Ensure .m3u8 and .ts files have correct MIME types
```

### Option 2: Server with Proper MIME Types

Configure your web server:

**Nginx:**
```nginx
location ~ \.m3u8$ {
    types { application/vnd.apple.mpegurl m3u8; }
}
location ~ \.ts$ {
    types { video/mp2t ts; }
}
```

**Apache (.htaccess):**
```apache
AddType application/vnd.apple.mpegurl .m3u8
AddType video/mp2t .ts
```

## 📚 Resources

- [FFmpeg HLS Documentation](https://ffmpeg.org/ffmpeg-formats.html#hls-2)
- [HLS.js Library](https://github.com/video-dev/hls.js)
- [Apple HLS Specification](https://developer.apple.com/streaming/)

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Note**: While this solution provides basic download protection, determined users can still capture content. For commercial applications requiring strong DRM, consider enterprise solutions like AWS Elemental MediaConvert with DRM integration.
