#!/bin/bash

# Video to HLS Converter Script with Progress Tracking
# Converts video files to HLS format (.m3u8 + .ts segments)
# Outputs progress information to a JSON file for web UI

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}Error: FFmpeg is not installed${NC}"
    echo "Install it with: sudo pacman -S ffmpeg (Arch) or sudo apt install ffmpeg (Ubuntu)"
    exit 1
fi

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage: $0 <input-video-file> [segment-duration]${NC}"
    echo "Example: $0 input/myvideo.mp4 6"
    echo ""
    echo "Parameters:"
    echo "  input-video-file    : Path to the video file to convert"
    echo "  segment-duration    : (Optional) Duration of each .ts segment in seconds (default: 6)"
    exit 1
fi

INPUT_FILE="$1"
SEGMENT_DURATION="${2:-6}"  # Default 6 seconds if not specified

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}Error: Input file '$INPUT_FILE' not found${NC}"
    exit 1
fi

# Get the filename without extension
FILENAME=$(basename "$INPUT_FILE")
BASENAME="${FILENAME%.*}"

# Create output directory
OUTPUT_DIR="../output/$BASENAME"
mkdir -p "$OUTPUT_DIR"

# Progress file location
PROGRESS_FILE="$OUTPUT_DIR/.progress.json"
LOG_FILE="$OUTPUT_DIR/.conversion.log"

# Initialize progress file
echo '{"status":"initializing","progress":0,"message":"Starting conversion..."}' > "$PROGRESS_FILE"

echo -e "${GREEN}Converting video to HLS format...${NC}"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_DIR"
echo "Segment Duration: ${SEGMENT_DURATION}s"
echo "Progress tracking: $PROGRESS_FILE"
echo ""

# Get video duration in seconds using ffprobe
echo -e "${BLUE}Analyzing video...${NC}"
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT_FILE" 2>/dev/null)

if [ -z "$DURATION" ]; then
    echo -e "${YELLOW}Warning: Could not determine video duration${NC}"
    DURATION=0
fi

DURATION_INT=${DURATION%.*}  # Convert to integer
echo "Video duration: ${DURATION_INT}s"
echo ""

# Update progress: analyzing complete
echo "{\"status\":\"converting\",\"progress\":1,\"message\":\"Starting encoding...\",\"duration\":$DURATION_INT}" > "$PROGRESS_FILE"

# Function to parse FFmpeg progress
parse_progress() {
    local duration=$1
    local progress_file=$2

    while IFS= read -r line; do
        # Extract time from FFmpeg output (format: time=00:01:23.45)
        if [[ $line =~ time=([0-9]{2}):([0-9]{2}):([0-9]{2})\.([0-9]{2}) ]]; then
            hours=${BASH_REMATCH[1]#0}  # Remove leading zero
            minutes=${BASH_REMATCH[2]#0}
            seconds=${BASH_REMATCH[3]#0}

            # Convert to total seconds
            current_time=$((hours * 3600 + minutes * 60 + seconds))

            # Calculate progress percentage
            if [ "$duration" -gt 0 ]; then
                progress=$((current_time * 100 / duration))
                if [ $progress -gt 100 ]; then
                    progress=100
                fi
            else
                progress=0
            fi

            # Extract speed (format: speed=1.23x)
            speed="0x"
            if [[ $line =~ speed=([0-9.]+)x ]]; then
                speed="${BASH_REMATCH[1]}x"
            fi

            # Extract frame number
            frame="0"
            if [[ $line =~ frame=\ *([0-9]+) ]]; then
                frame="${BASH_REMATCH[1]}"
            fi

            # Calculate ETA
            eta="calculating..."
            if [[ $speed =~ ([0-9.]+) ]] && [ "$duration" -gt 0 ] && (( $(echo "${BASH_REMATCH[1]} > 0" | bc -l) )); then
                speed_val="${BASH_REMATCH[1]}"
                remaining=$((duration - current_time))
                eta_seconds=$(echo "scale=0; $remaining / $speed_val" | bc)

                eta_hours=$((eta_seconds / 3600))
                eta_minutes=$(((eta_seconds % 3600) / 60))
                eta_secs=$((eta_seconds % 60))

                if [ $eta_hours -gt 0 ]; then
                    eta="${eta_hours}h ${eta_minutes}m"
                elif [ $eta_minutes -gt 0 ]; then
                    eta="${eta_minutes}m ${eta_secs}s"
                else
                    eta="${eta_secs}s"
                fi
            fi

            # Format current time
            current_hours=$((current_time / 3600))
            current_minutes=$(((current_time % 3600) / 60))
            current_secs=$((current_time % 60))

            duration_hours=$((duration / 3600))
            duration_minutes=$(((duration % 3600) / 60))
            duration_secs=$((duration % 60))

            time_str=$(printf "%02d:%02d:%02d / %02d:%02d:%02d" \
                $current_hours $current_minutes $current_secs \
                $duration_hours $duration_minutes $duration_secs)

            # Update progress file
            cat > "$progress_file" <<EOF
{
  "status": "converting",
  "progress": $progress,
  "message": "Encoding in progress...",
  "duration": $duration,
  "current_time": $current_time,
  "time_string": "$time_str",
  "frame": "$frame",
  "speed": "$speed",
  "eta": "$eta"
}
EOF

            # Print to console
            printf "\r${BLUE}Progress: ${GREEN}%3d%%${NC} | Time: %s | Speed: %s | ETA: %s | Frame: %s" \
                "$progress" "$time_str" "$speed" "$eta" "$frame"
        fi
    done
}

# Run FFmpeg with progress output
echo "{\"status\":\"converting\",\"progress\":0,\"message\":\"Encoding started...\"}" > "$PROGRESS_FILE"

ffmpeg -i "$INPUT_FILE" \
    -c:v libx264 \
    -c:a aac \
    -start_number 0 \
    -hls_time "$SEGMENT_DURATION" \
    -hls_list_size 0 \
    -hls_segment_filename "$OUTPUT_DIR/segment_%03d.ts" \
    -f hls \
    -progress pipe:1 \
    "$OUTPUT_DIR/playlist.m3u8" 2> "$LOG_FILE" | parse_progress "$DURATION_INT" "$PROGRESS_FILE"

FFMPEG_EXIT_CODE=${PIPESTATUS[0]}

echo ""  # New line after progress bar

# Check if conversion was successful
if [ $FFMPEG_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Conversion successful!${NC}"

    # Count segments
    SEGMENT_COUNT=$(find "$OUTPUT_DIR" -name "segment_*.ts" | wc -l)

    # Get output size
    OUTPUT_SIZE=$(du -sh "$OUTPUT_DIR" | cut -f1)

    # Update progress file with completion
    cat > "$PROGRESS_FILE" <<EOF
{
  "status": "completed",
  "progress": 100,
  "message": "Conversion completed successfully!",
  "duration": $DURATION_INT,
  "segments": $SEGMENT_COUNT,
  "output_size": "$OUTPUT_SIZE"
}
EOF

    echo ""
    echo "Files created:"
    echo "  - Playlist: $OUTPUT_DIR/playlist.m3u8"
    echo "  - Segments: $SEGMENT_COUNT files"
    echo "  - Total size: $OUTPUT_SIZE"
    echo ""
    echo "To view the video, open: web/player.html"
    echo "Then select the playlist: output/$BASENAME/playlist.m3u8"
else
    echo -e "${RED}✗ Conversion failed${NC}"

    # Update progress file with error
    ERROR_MSG=$(tail -n 5 "$LOG_FILE" | tr '\n' ' ')
    cat > "$PROGRESS_FILE" <<EOF
{
  "status": "error",
  "progress": 0,
  "message": "Conversion failed. Check log file for details.",
  "error": "$ERROR_MSG"
}
EOF

    echo "Check log file for details: $LOG_FILE"
    exit 1
fi
