#!/bin/bash

# Video to HLS Converter Script
# Converts video files to HLS format (.m3u8 + .ts segments)
# This makes videos streamable but harder to download

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

echo -e "${GREEN}Converting video to HLS format...${NC}"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_DIR"
echo "Segment Duration: ${SEGMENT_DURATION}s"
echo ""

# FFmpeg command to convert to HLS
ffmpeg -i "$INPUT_FILE" \
    -c:v libx264 \
    -c:a aac \
    -start_number 0 \
    -hls_time "$SEGMENT_DURATION" \
    -hls_list_size 0 \
    -hls_segment_filename "$OUTPUT_DIR/segment_%03d.ts" \
    -f hls \
    "$OUTPUT_DIR/playlist.m3u8"

# Check if conversion was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Conversion successful!${NC}"
    echo ""
    echo "Files created:"
    echo "  - Playlist: $OUTPUT_DIR/playlist.m3u8"
    echo "  - Segments: $OUTPUT_DIR/segment_*.ts"
    echo ""
    echo "To view the video, open: web/player.html"
    echo "Then select the playlist: output/$BASENAME/playlist.m3u8"
else
    echo -e "${RED}✗ Conversion failed${NC}"
    exit 1
fi
