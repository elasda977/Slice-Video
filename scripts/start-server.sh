#!/bin/bash

# Start HLS Video Player Server
# This script starts a web server accessible from other devices on the network

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get server IP addresses
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  HLS Video Player Server${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Find the main LAN IP address
LAN_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | grep -v "docker" | grep -v "10\." | head -1 | awk '{print $2}' | cut -d'/' -f1)

if [ -z "$LAN_IP" ]; then
    echo -e "${RED}Warning: Could not detect LAN IP address${NC}"
    LAN_IP="<YOUR_IP>"
fi

# Find ZeroTier IP (if available)
ZT_IP=$(ip addr show | grep "inet " | grep "10\.244\." | head -1 | awk '{print $2}' | cut -d'/' -f1)

# Default port
PORT="${1:-8000}"

echo -e "${YELLOW}Server Information:${NC}"
echo -e "  Local IP:    ${GREEN}$LAN_IP${NC}"
if [ -n "$ZT_IP" ]; then
    echo -e "  ZeroTier:    ${GREEN}$ZT_IP${NC} (VPN)"
fi
echo -e "  Port:        ${GREEN}$PORT${NC}"
echo -e "  Directory:   ${GREEN}$(pwd)${NC}"
echo ""

echo -e "${YELLOW}Access URLs:${NC}"
echo -e "  From this computer:    ${GREEN}http://localhost:$PORT/player.html${NC}"
echo -e "  From same WiFi/LAN:    ${GREEN}http://$LAN_IP:$PORT/player.html${NC}"
if [ -n "$ZT_IP" ]; then
    echo -e "  From ZeroTier VPN:     ${GREEN}http://$ZT_IP:$PORT/player.html${NC}"
fi
echo ""

echo -e "${YELLOW}Playlist Path Example:${NC}"
echo -e "  ${GREEN}../output/your-video/playlist.m3u8${NC}"
echo ""

# Check if firewall might be blocking
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | grep "Status:" | awk '{print $2}')
    if [ "$UFW_STATUS" = "active" ]; then
        echo -e "${YELLOW}⚠ Firewall (ufw) is active. You may need to allow port $PORT:${NC}"
        echo -e "  ${GREEN}sudo ufw allow $PORT/tcp${NC}"
        echo ""
    fi
fi

if command -v firewall-cmd &> /dev/null; then
    FIREWALLD_STATUS=$(sudo firewall-cmd --state 2>/dev/null)
    if [ "$FIREWALLD_STATUS" = "running" ]; then
        echo -e "${YELLOW}⚠ Firewall (firewalld) is running. You may need to allow port $PORT:${NC}"
        echo -e "  ${GREEN}sudo firewall-cmd --add-port=$PORT/tcp --permanent${NC}"
        echo -e "  ${GREEN}sudo firewall-cmd --reload${NC}"
        echo ""
    fi
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Starting server on 0.0.0.0:$PORT${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Change to web directory
cd "$(dirname "$0")/../web" || exit 1

# Start Python HTTP server on all interfaces (0.0.0.0)
python -m http.server "$PORT" --bind 0.0.0.0
