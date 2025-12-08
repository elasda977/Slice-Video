#!/bin/bash

# Quick Test Setup Script
# This script helps you quickly test the HLS video player

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  HLS Video Player - Quick Test Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Get server IP
LAN_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | grep -v "docker" | grep -v "10\." | head -1 | awk '{print $2}' | cut -d'/' -f1)

echo -e "${YELLOW}Step 1: Checking firewall...${NC}"
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | grep "Status:" | awk '{print $2}')
    if [ "$UFW_STATUS" = "active" ]; then
        echo -e "${YELLOW}  Firewall is active. Running:${NC}"
        echo -e "  ${GREEN}sudo ufw allow 8000/tcp${NC}"
        sudo ufw allow 8000/tcp
    else
        echo -e "${GREEN}  ✓ Firewall is inactive or port is open${NC}"
    fi
else
    echo -e "${GREEN}  ✓ UFW not found, checking firewalld...${NC}"
    if command -v firewall-cmd &> /dev/null; then
        FIREWALLD_STATUS=$(sudo firewall-cmd --state 2>/dev/null)
        if [ "$FIREWALLD_STATUS" = "running" ]; then
            echo -e "${YELLOW}  Firewalld is running. Opening port 8000...${NC}"
            sudo firewall-cmd --add-port=8000/tcp --permanent
            sudo firewall-cmd --reload
        fi
    else
        echo -e "${GREEN}  ✓ No firewall detected${NC}"
    fi
fi
echo ""

echo -e "${YELLOW}Step 2: Checking for test video...${NC}"
if [ ! -f "input/"*.mp4 ] && [ ! -f "input/"*.avi ] && [ ! -f "input/"*.mkv ]; then
    echo -e "${YELLOW}  No video found in input/ folder${NC}"
    echo ""
    echo -e "${YELLOW}  Do you want to download a test video? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}  Downloading sample video...${NC}"
        cd input || exit 1
        curl -o test-sample.mp4 \
            https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 \
            || wget https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 \
               -O test-sample.mp4
        cd ..

        if [ -f "input/test-sample.mp4" ]; then
            echo -e "${GREEN}  ✓ Test video downloaded${NC}"
            TEST_VIDEO="input/test-sample.mp4"
        else
            echo -e "${RED}  ✗ Failed to download test video${NC}"
            echo -e "${YELLOW}  Please manually copy a video to input/ folder${NC}"
            TEST_VIDEO=""
        fi
    else
        echo -e "${YELLOW}  Please copy a video file to: $(pwd)/input/${NC}"
        exit 0
    fi
else
    TEST_VIDEO=$(ls input/*.mp4 input/*.avi input/*.mkv 2>/dev/null | head -1)
    echo -e "${GREEN}  ✓ Found: $TEST_VIDEO${NC}"
fi
echo ""

if [ -n "$TEST_VIDEO" ]; then
    echo -e "${YELLOW}Step 3: Converting video to HLS...${NC}"
    cd scripts || exit 1
    ./convert-to-hls.sh "../$TEST_VIDEO" 6
    cd ..

    BASENAME=$(basename "$TEST_VIDEO" | sed 's/\.[^.]*$//')
    echo ""
    echo -e "${GREEN}  ✓ Conversion complete!${NC}"
    echo -e "${YELLOW}  Output: output/$BASENAME/${NC}"
    echo ""
fi

echo -e "${YELLOW}Step 4: Starting web server...${NC}"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Server is starting...${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}  Access from your laptop:${NC}"
echo -e "  ${GREEN}http://$LAN_IP:8000/player.html${NC}"
echo ""
echo -e "${BLUE}  Playlist path to enter:${NC}"
if [ -n "$TEST_VIDEO" ]; then
    BASENAME=$(basename "$TEST_VIDEO" | sed 's/\.[^.]*$//')
    echo -e "  ${GREEN}../output/$BASENAME/playlist.m3u8${NC}"
else
    echo -e "  ${GREEN}../output/your-video-name/playlist.m3u8${NC}"
fi
echo ""
echo -e "${YELLOW}  Press Ctrl+C to stop the server${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""

cd scripts || exit 1
./start-server.sh 8000
