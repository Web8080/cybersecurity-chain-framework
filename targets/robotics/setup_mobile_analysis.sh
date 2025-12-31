#!/bin/bash
# Setup script for Mobile App Reverse Engineering

set -e

echo " Setting up Mobile App Reverse Engineering Environment..."
echo ""

# Check for Java (needed for apktool and jadx)
if command -v java &> /dev/null; then
 echo " Java found: $(java -version 2>&1 | head -1)"
else
 echo " Java not found"
 echo " Install: brew install openjdk (macOS) or apt-get install default-jdk (Linux)"
fi

# Check for Python
if command -v python3 &> /dev/null; then
 echo " Python found: $(python3 --version)"
else
 echo " Python 3 not found"
 exit 1
fi

echo ""
echo " Installing Tools..."
echo ""

# Create tools directory
mkdir -p tools/mobile-analysis
cd tools/mobile-analysis

# Check for apktool
if command -v apktool &> /dev/null; then
 echo " apktool already installed"
else
 echo " Installing apktool..."
 if [[ "$OSTYPE" == "darwin"* ]]; then
 # macOS
 if command -v brew &> /dev/null; then
 brew install apktool
 else
 echo " Please install Homebrew first: https://brew.sh/"
 echo " Or download from: https://ibotpeaches.github.io/Apktool/"
 fi
 else
 # Linux
 echo " Download from: https://ibotpeaches.github.io/Apktool/"
 echo " Or install via package manager"
 fi
fi

# Check for jadx
if command -v jadx &> /dev/null; then
 echo " jadx already installed"
else
 echo " Installing jadx..."
 if [[ "$OSTYPE" == "darwin"* ]]; then
 if command -v brew &> /dev/null; then
 brew install jadx
 else
 echo " Download from: https://github.com/skylot/jadx/releases"
 fi
 else
 echo " Download from: https://github.com/skylot/jadx/releases"
 fi
fi

# Check for adb (Android Debug Bridge)
if command -v adb &> /dev/null; then
 echo " adb (Android Debug Bridge) found"
else
 echo " adb not found (optional, for extracting APKs from devices)"
 if [[ "$OSTYPE" == "darwin"* ]]; then
 echo " Install: brew install android-platform-tools"
 else
 echo " Install: apt-get install android-tools-adb"
 fi
fi

cd ../..

echo ""
echo " Setup complete!"
echo ""
echo " Next Steps:"
echo " 1. Download a robot control app APK"
echo " 2. Extract: apktool d app.apk -o extracted/"
echo " 3. Decompile: jadx app.apk -d decompiled/"
echo " 4. Find APIs: grep -r 'https://' decompiled/"
echo " 5. Test with Burp Suite"
echo ""
echo " See: docs/mobile_analysis_guide.md for detailed instructions"

