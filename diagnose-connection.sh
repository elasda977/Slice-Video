#!/bin/bash

# Connection Diagnostic Script
# Run this on your LAPTOP to diagnose connection issues

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SERVER_LOCAL="192.168.1.26"
SERVER_ZEROTIER="10.244.132.148"
PORT="8000"

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Connection Diagnostic Tool${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Test 1: Check if ZeroTier is installed
echo -e "${YELLOW}[1/6] Checking ZeroTier installation...${NC}"
if command -v zerotier-cli &> /dev/null; then
    echo -e "${GREEN}  ✓ ZeroTier is installed${NC}"

    # Check ZeroTier status
    ZT_INFO=$(zerotier-cli info 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✓ ZeroTier service is running${NC}"
        echo -e "    $ZT_INFO"
    else
        echo -e "${RED}  ✗ ZeroTier service is not running${NC}"
        echo -e "    Try: sudo systemctl start zerotier-one"
    fi
else
    echo -e "${RED}  ✗ ZeroTier is not installed${NC}"
    echo -e "    Install from: https://www.zerotier.com/download/"
fi
echo ""

# Test 2: Check ZeroTier networks
echo -e "${YELLOW}[2/6] Checking ZeroTier networks...${NC}"
if command -v zerotier-cli &> /dev/null; then
    NETWORKS=$(zerotier-cli listnetworks 2>/dev/null | tail -n +2)
    if [ -n "$NETWORKS" ]; then
        echo -e "${GREEN}  ✓ ZeroTier networks found:${NC}"
        echo "$NETWORKS"

        # Check if we have 10.244.x.x IP
        HAS_10_244=$(echo "$NETWORKS" | grep "10.244")
        if [ -n "$HAS_10_244" ]; then
            echo -e "${GREEN}  ✓ Connected to same ZeroTier network (10.244.x.x)${NC}"
        else
            echo -e "${RED}  ✗ Not on the 10.244.x.x network${NC}"
            echo -e "    You need to join the same ZeroTier network as the server"
        fi
    else
        echo -e "${RED}  ✗ No ZeroTier networks found${NC}"
        echo -e "    Join a network: zerotier-cli join <network-id>"
    fi
else
    echo -e "${YELLOW}  ⊘ Skipped (ZeroTier not installed)${NC}"
fi
echo ""

# Test 3: Ping local IP
echo -e "${YELLOW}[3/6] Testing connectivity to Local IP ($SERVER_LOCAL)...${NC}"
if ping -c 2 -W 2 $SERVER_LOCAL &> /dev/null; then
    echo -e "${GREEN}  ✓ Server is reachable on local network${NC}"
else
    echo -e "${RED}  ✗ Cannot reach server on local network${NC}"
    echo -e "    Make sure you're on the same WiFi/LAN"
fi
echo ""

# Test 4: Ping ZeroTier IP
echo -e "${YELLOW}[4/6] Testing connectivity to ZeroTier IP ($SERVER_ZEROTIER)...${NC}"
if ping -c 2 -W 2 $SERVER_ZEROTIER &> /dev/null; then
    echo -e "${GREEN}  ✓ Server is reachable via ZeroTier${NC}"
else
    echo -e "${RED}  ✗ Cannot reach server via ZeroTier${NC}"
    echo -e "    Check if you're on the same ZeroTier network"
fi
echo ""

# Test 5: Test port access (Local)
echo -e "${YELLOW}[5/6] Testing port $PORT on Local IP...${NC}"
if command -v nc &> /dev/null; then
    if nc -zv -w 2 $SERVER_LOCAL $PORT &> /dev/null; then
        echo -e "${GREEN}  ✓ Port $PORT is accessible on local network${NC}"
    else
        echo -e "${RED}  ✗ Port $PORT is not accessible on local network${NC}"
        echo -e "    Server might not be running or firewall is blocking"
    fi
elif command -v telnet &> /dev/null; then
    (echo > /dev/tcp/$SERVER_LOCAL/$PORT) &>/dev/null && \
        echo -e "${GREEN}  ✓ Port $PORT is accessible on local network${NC}" || \
        echo -e "${RED}  ✗ Port $PORT is not accessible on local network${NC}"
else
    echo -e "${YELLOW}  ⊘ Skipped (nc/telnet not available)${NC}"
fi
echo ""

# Test 6: Test port access (ZeroTier)
echo -e "${YELLOW}[6/6] Testing port $PORT on ZeroTier IP...${NC}"
if command -v nc &> /dev/null; then
    if nc -zv -w 2 $SERVER_ZEROTIER $PORT &> /dev/null; then
        echo -e "${GREEN}  ✓ Port $PORT is accessible via ZeroTier${NC}"
    else
        echo -e "${RED}  ✗ Port $PORT is not accessible via ZeroTier${NC}"
        echo -e "    Server might not be running"
    fi
elif command -v telnet &> /dev/null; then
    (echo > /dev/tcp/$SERVER_ZEROTIER/$PORT) &>/dev/null && \
        echo -e "${GREEN}  ✓ Port $PORT is accessible via ZeroTier${NC}" || \
        echo -e "${RED}  ✗ Port $PORT is not accessible via ZeroTier${NC}"
else
    echo -e "${YELLOW}  ⊘ Skipped (nc/telnet not available)${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Recommended URLs:${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Local Network:${NC}  http://$SERVER_LOCAL:$PORT/player.html"
echo -e "${GREEN}ZeroTier VPN:${NC}   http://$SERVER_ZEROTIER:$PORT/player.html"
echo ""
echo -e "${YELLOW}Note:${NC} If tests failed, make sure:"
echo -e "  1. Server is running: ./start-server.sh"
echo -e "  2. You're on same network (WiFi or ZeroTier)"
echo -e "  3. Firewall allows port $PORT"
echo ""
