#!/bin/bash
# Setup guide for OWASP IoTGoat

set -e

echo "🔌 OWASP IoTGoat Setup Guide"
echo ""
echo "IoTGoat is intentionally vulnerable IoT firmware for security testing."
echo ""

# Check for required tools
echo "Checking prerequisites..."

if command -v qemu-system-arm &> /dev/null; then
    echo "✅ QEMU found"
else
    echo "⚠️  QEMU not found (needed for emulation)"
fi

if command -v binwalk &> /dev/null; then
    echo "✅ Binwalk found (firmware analysis)"
else
    echo "⚠️  Binwalk not found (useful for firmware analysis)"
fi

echo ""
echo "📦 Setup Options:"
echo ""
echo "Option 1: Pre-built VM (Easiest)"
echo "  1. Download from: https://github.com/OWASP/IoTGoat/releases"
echo "  2. Import into VirtualBox or VMware"
echo "  3. Boot the VM"
echo ""
echo "Option 2: Build from Source"
echo "  1. git clone https://github.com/OWASP/IoTGoat.git"
echo "  2. cd IoTGoat"
echo "  3. Follow build instructions in README.md"
echo ""
echo "Option 3: Use QEMU Emulation"
echo "  1. Download firmware image"
echo "  2. Run: qemu-system-arm -M versatilepb -kernel <firmware>"
echo ""

echo "📚 Resources:"
echo "  - GitHub: https://github.com/OWASP/IoTGoat"
echo "  - OWASP Page: https://owasp.org/www-project-iotgoat/"
echo ""

echo "🎯 After Setup:"
echo "  1. Access the device (usually via web interface)"
echo "  2. Start firmware analysis"
echo "  3. Use chain_analyzer.py to document attack chains"
echo "  4. See iotgoat/README.md for attack chain examples"
echo ""

echo "💡 Tip: IoTGoat methodologies apply to:"
echo "  - Router security"
echo "  - IoT device firmware"
echo "  - Embedded systems"
echo "  - Robot controllers (similar architecture)"
echo ""


