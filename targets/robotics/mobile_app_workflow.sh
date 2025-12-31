#!/bin/bash
# Mobile App Analysis Workflow
# Step-by-step guide for analyzing robot apps

set -e

echo "📱 Mobile App Reverse Engineering Workflow"
echo "=========================================="
echo ""

# Check if tools are installed
if ! command -v apktool &> /dev/null; then
    echo "❌ apktool not found. Run: bash setup_mobile_analysis.sh"
    exit 1
fi

if ! command -v jadx &> /dev/null; then
    echo "❌ jadx not found. Run: bash setup_mobile_analysis.sh"
    exit 1
fi

echo "✅ Tools ready: apktool, jadx"
echo ""

# Create working directory
WORK_DIR="mobile_analysis_work"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "📁 Working directory: $(pwd)"
echo ""

# Check if APK provided
if [ -z "$1" ]; then
    echo "📋 Step 1: Get an APK File"
    echo "=========================="
    echo ""
    echo "You need a robot app APK file. Options:"
    echo ""
    echo "Option A: Download from APK sites"
    echo "  - APKPure.com"
    echo "  - APKMirror.com"
    echo "  - Search for: 'roomba', 'robot', 'drone', etc."
    echo ""
    echo "Option B: Extract from Android device"
    echo "  adb shell pm list packages | grep robot"
    echo "  adb pull /data/app/com.example.robotapp/base.apk"
    echo ""
    echo "Option C: Use example/test APK"
    echo "  Download a sample robot app for testing"
    echo ""
    echo "Once you have an APK, run:"
    echo "  bash mobile_app_workflow.sh <path-to-apk>"
    echo ""
    exit 0
fi

APK_FILE="$1"

if [ ! -f "$APK_FILE" ]; then
    echo "❌ APK file not found: $APK_FILE"
    exit 1
fi

echo "📦 APK File: $APK_FILE"
echo ""

# Step 2: Extract APK
echo "📋 Step 2: Extracting APK..."
echo "============================="
echo ""

EXTRACTED_DIR="extracted"
if [ -d "$EXTRACTED_DIR" ]; then
    echo "⚠️  Extracted directory exists. Removing..."
    rm -rf "$EXTRACTED_DIR"
fi

echo "Running: apktool d \"$APK_FILE\" -o $EXTRACTED_DIR"
apktool d "$APK_FILE" -o "$EXTRACTED_DIR" 2>&1 | tail -5

if [ -d "$EXTRACTED_DIR" ]; then
    echo "✅ APK extracted to: $EXTRACTED_DIR"
else
    echo "❌ Extraction failed"
    exit 1
fi

echo ""

# Step 3: Decompile APK
echo "📋 Step 3: Decompiling APK..."
echo "=============================="
echo ""

DECOMPILED_DIR="decompiled"
if [ -d "$DECOMPILED_DIR" ]; then
    echo "⚠️  Decompiled directory exists. Removing..."
    rm -rf "$DECOMPILED_DIR"
fi

echo "Running: jadx \"$APK_FILE\" -d $DECOMPILED_DIR"
jadx "$APK_FILE" -d "$DECOMPILED_DIR" 2>&1 | tail -5

if [ -d "$DECOMPILED_DIR" ]; then
    echo "✅ APK decompiled to: $DECOMPILED_DIR"
else
    echo "❌ Decompilation failed"
    exit 1
fi

echo ""

# Step 4: Find API endpoints
echo "📋 Step 4: Finding API Endpoints..."
echo "===================================="
echo ""

cd "$DECOMPILED_DIR"

echo "Searching for HTTPS URLs..."
echo "---------------------------"
HTTPS_RESULTS=$(grep -r "https://" . 2>/dev/null | head -20)
if [ -n "$HTTPS_RESULTS" ]; then
    echo "$HTTPS_RESULTS"
    echo ""
    echo "💡 Found API endpoints! Saving to api_endpoints.txt"
    grep -r "https://" . 2>/dev/null > ../api_endpoints.txt
else
    echo "⚠️  No HTTPS URLs found"
fi

echo ""
echo "Searching for API keywords..."
echo "-----------------------------"
API_KEYWORDS=$(grep -ri "api\|endpoint\|baseurl\|base_url" . 2>/dev/null | head -20)
if [ -n "$API_KEYWORDS" ]; then
    echo "$API_KEYWORDS"
    echo ""
    echo "💡 Found API references! Saving to api_keywords.txt"
    grep -ri "api\|endpoint\|baseurl\|base_url" . 2>/dev/null > ../api_keywords.txt
else
    echo "⚠️  No API keywords found"
fi

echo ""
echo "Searching for authentication..."
echo "-------------------------------"
AUTH_RESULTS=$(grep -ri "token\|auth\|bearer\|jwt\|apikey" . 2>/dev/null | head -20)
if [ -n "$AUTH_RESULTS" ]; then
    echo "$AUTH_RESULTS"
    echo ""
    echo "💡 Found authentication references! Saving to auth_references.txt"
    grep -ri "token\|auth\|bearer\|jwt\|apikey" . 2>/dev/null > ../auth_references.txt
else
    echo "⚠️  No authentication references found"
fi

cd ..

echo ""
echo "✅ Analysis complete!"
echo ""
echo "📁 Results saved in: $(pwd)"
echo "   - api_endpoints.txt"
echo "   - api_keywords.txt"
echo "   - auth_references.txt"
echo ""
echo "📋 Next Steps:"
echo "   1. Review the found endpoints"
echo "   2. Test APIs with Burp Suite or curl"
echo "   3. Document findings with chain_analyzer.py"
echo ""


