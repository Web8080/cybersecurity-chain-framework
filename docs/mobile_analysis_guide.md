# Mobile App Reverse Engineering Guide

## Goal: Find Robot APIs by Analyzing Mobile Apps

### Step 1: Get an APK File

**Option A: Download from Google Play**
```bash
# Use online tools like:
# - APKPure.com
# - APKMirror.com
# Search for: "robot", "roomba", "drone", etc.
```

**Option B: Extract from Android Device**
```bash
# Connect Android device via USB
# Enable USB debugging
adb devices

# List installed packages
adb shell pm list packages | grep robot

# Extract APK
adb pull /data/app/com.example.robotapp/base.apk robot-app.apk
```

**Option C: Use APK Downloader**
- Chrome extension: "APK Downloader"
- Or online services

### Step 2: Extract APK

```bash
# Using apktool
apktool d robot-app.apk -o extracted/

# This extracts:
# - AndroidManifest.xml
# - Resources
# - Smali code
```

### Step 3: Decompile APK

```bash
# Using jadx (better for Java code)
jadx robot-app.apk -d decompiled/

# This creates readable Java code
```

### Step 4: Find API Endpoints

```bash
cd decompiled/

# Search for HTTPS URLs
grep -r "https://" .

# Search for API keywords
grep -r "api" .
grep -r "endpoint" .
grep -r "baseUrl" .

# Search for authentication
grep -r "token" .
grep -r "auth" .
grep -r "bearer" .
```

### Step 5: Analyze Findings

**Common API Patterns:**
- `https://api.robot-service.com/v1/...`
- `https://robot.example.com/api/...`
- Base URLs in config files
- Hardcoded API keys

**Look for:**
- API base URLs
- Authentication tokens
- API keys
- Endpoint paths
- Request/response formats

### Step 6: Test APIs

**Using Burp Suite:**
1. Configure proxy (127.0.0.1:8080)
2. Configure Android device to use proxy
3. Intercept traffic from app
4. Analyze API calls
5. Test for vulnerabilities

**Using curl:**
```bash
# Test discovered endpoints
curl -X GET https://api.robot-service.com/v1/status

# Test with authentication
curl -X GET https://api.robot-service.com/v1/status \
 -H "Authorization: Bearer TOKEN"
```

### Step 7: Document Findings

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

chain = analyzer.create_chain(
 title="Robot API Authentication Bypass",
 description="Discovered via mobile app reverse engineering",
 impact=ImpactLevel.HIGH
)

# Add steps based on discovered vulnerabilities
# ...

analyzer.export_chain(chain, "mobile_app_finding.json")
```

## Example: Roomba App Analysis

```bash
# 1. Download Roomba app APK
# 2. Extract
apktool d roomba-app.apk -o roomba-extracted/

# 3. Decompile
jadx roomba-app.apk -d roomba-decompiled/

# 4. Search for APIs
cd roomba-decompiled/
grep -r "https://" . | grep -i api

# 5. Find authentication
grep -r "token" . | grep -i auth
```

## Tools

- **apktool** - APK extraction
- **jadx** - Java decompilation
- **Burp Suite** - Traffic interception
- **adb** - Android Debug Bridge
- **grep** - Text search

## Checklist

- [ ] APK file obtained
- [ ] APK extracted with apktool
- [ ] APK decompiled with jadx
- [ ] API endpoints found
- [ ] Authentication mechanisms identified
- [ ] APIs tested with Burp Suite
- [ ] Vulnerabilities documented
- [ ] Attack chains created

## Legal Note

 **Legal:** Reverse engineer apps you own or have permission
 **Legal:** Analyze for security research
 **Illegal:** Use findings to access unauthorized systems

## Next Steps

1. Run setup: `bash setup_mobile_analysis.sh`
2. Get an APK file
3. Extract and decompile
4. Find APIs
5. Test with Burp Suite
6. Document findings

