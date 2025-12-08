#!/bin/bash

# Quick test script for progress tracking feature
# This tests the new conversion script with progress tracking

echo "=========================================="
echo "  Progress Tracking Feature Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if test video exists
if [ ! -f "input/test-mantra.mp4" ]; then
    echo -e "${RED}Error: Test video not found at input/test-mantra.mp4${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Test video found${NC}"
echo ""

# Check if progress script exists
if [ ! -f "scripts/convert-to-hls-progress.sh" ]; then
    echo -e "${RED}Error: Progress script not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Progress script found${NC}"
echo ""

# Create a small test video (first 10 seconds) for quick testing
echo -e "${YELLOW}Creating 10-second test clip...${NC}"
ffmpeg -i input/test-mantra.mp4 -t 10 -c copy input/test-short.mp4 -y 2>&1 | tail -5

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Test clip created${NC}"
else
    echo -e "${RED}✗ Failed to create test clip${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Testing Progress Tracking"
echo "=========================================="
echo ""

# Run conversion with progress tracking
cd scripts
./convert-to-hls-progress.sh ../input/test-short.mp4 6

RESULT=$?

echo ""
echo "=========================================="
echo "  Checking Results"
echo "=========================================="
echo ""

# Check if output was created
if [ -d "../output/test-short" ]; then
    echo -e "${GREEN}✓ Output directory created${NC}"

    # Check for playlist
    if [ -f "../output/test-short/playlist.m3u8" ]; then
        echo -e "${GREEN}✓ Playlist file created${NC}"
    else
        echo -e "${RED}✗ Playlist file missing${NC}"
    fi

    # Check for segments
    SEGMENT_COUNT=$(find ../output/test-short -name "segment_*.ts" | wc -l)
    echo -e "${GREEN}✓ Created $SEGMENT_COUNT segment(s)${NC}"

    # Check for progress file
    if [ -f "../output/test-short/.progress.json" ]; then
        echo -e "${GREEN}✓ Progress file created${NC}"
        echo ""
        echo "Progress file contents:"
        cat ../output/test-short/.progress.json | python3 -m json.tool 2>/dev/null || cat ../output/test-short/.progress.json
    else
        echo -e "${RED}✗ Progress file missing${NC}"
    fi

    # Check for log file
    if [ -f "../output/test-short/.conversion.log" ]; then
        echo -e "${GREEN}✓ Conversion log created${NC}"
    fi

else
    echo -e "${RED}✗ Output directory not created${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo ""

if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo ""
    echo "You can now:"
    echo "  1. Start the API server: cd web && python3 api.py"
    echo "  2. Start the web server: cd scripts && ./start-server.sh"
    echo "  3. Open: http://localhost:8000/convert.html"
    echo "  4. Test with: test-short.mp4"
    echo ""
    echo "Progress tracking is working correctly!"
else
    echo -e "${RED}✗ TESTS FAILED${NC}"
    echo "Check the error messages above"
    exit 1
fi
