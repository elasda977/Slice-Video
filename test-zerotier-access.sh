#!/bin/bash
# ZeroTier Access Test Script
# Run this script to diagnose connectivity issues

echo "=========================================="
echo "ZeroTier Network Diagnostic"
echo "=========================================="
echo ""

echo "1. Server ZeroTier IP:"
echo "   10.244.132.148"
echo ""

echo "2. ZeroTier Interface Status:"
ip addr show ztfp6i6ewq | grep -E "inet |state"
echo ""

echo "3. ZeroTier Interface Zone:"
firewall-cmd --get-zone-of-interface=ztfp6i6ewq 2>/dev/null || echo "   Error: Need sudo to check"
echo ""

echo "4. Listening Ports:"
ss -tlnp | grep -E ":(8000|8001|3000)"
echo ""

echo "5. Testing Local Access via ZeroTier IP:"
echo "   Testing port 8001..."
curl -s -m 5 http://10.244.132.148:8001/health && echo "   ✓ Port 8001 accessible" || echo "   ✗ Port 8001 NOT accessible"
echo ""
echo "   Testing port 8000..."
curl -s -m 5 http://10.244.132.148:8000 -I | head -1 && echo "   ✓ Port 8000 accessible" || echo "   ✗ Port 8000 NOT accessible"
echo ""

echo "6. Firewall Status:"
systemctl is-active firewalld 2>/dev/null || echo "   firewalld not running"
echo ""

echo "7. ZeroTier Service Status:"
systemctl is-active zerotier-one 2>/dev/null || echo "   zerotier-one not running"
echo ""

echo "=========================================="
echo "Instructions for Mac:"
echo "=========================================="
echo ""
echo "On your Mac, run these tests:"
echo ""
echo "1. Check if Mac can reach this server's ZeroTier IP:"
echo "   ping 10.244.132.148"
echo ""
echo "2. Test port connectivity from Mac:"
echo "   curl http://10.244.132.148:8001/health"
echo "   curl http://10.244.132.148:8000"
echo ""
echo "3. Check Mac's ZeroTier IP (should be in 10.244.x.x range):"
echo "   ifconfig | grep 10.244"
echo "   # or on newer Macs:"
echo "   ip addr | grep 10.244"
echo ""
echo "4. Check ZeroTier network membership on Mac:"
echo "   sudo zerotier-cli listnetworks"
echo ""
echo "=========================================="
