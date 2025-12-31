# Complete Mobile App Analysis Guide

## 🎯 Goal: Find Robot APIs and Build Attack Chains

### Step 1: Get an APK File

**Easiest Method: Download from APKPure**
1. Go to: https://apkpure.com/
2. Search for: "irobot", "roomba", "robot"
3. Download APK file
4. Save to: `/Users/user/Cybersecurity/targets/robotics/`

**Recommended Apps:**
- **iRobot Home** - Roomba control (most popular)
- **DJI GO** - Drone control
- **Sphero** - Robot toy control

### Step 2: Run Analysis Workflow

```bash
cd /Users/user/Cybersecurity/targets/robotics

# Run the workflow
bash mobile_app_workflow.sh <path-to-apk>

# Example:
bash mobile_app_workflow.sh ~/Downloads/irobot.apk
```

**What it does:**
1. Extracts APK with apktool
2. Decompiles with jadx
3. Searches for API endpoints
4. Finds authentication mechanisms
5. Saves results to files

### Step 3: Review Findings

```bash
cd mobile_analysis_work

# View found endpoints
cat api_endpoints.txt

# View API keywords
cat api_keywords.txt

# View authentication
cat auth_references.txt
```

### Step 4: Test APIs

**Using curl:**
```bash
# Test discovered endpoint
curl -X GET https://api.robot-service.com/v1/status

# Test with authentication
curl -X GET https://api.robot-service.com/v1/robots \
  -H "Authorization: Bearer TOKEN"
```

**Using Burp Suite:**
1. Configure proxy (127.0.0.1:8080)
2. Configure Android device to use proxy
3. Run the app
4. Intercept API calls
5. Analyze requests/responses

### Step 5: Document Findings

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

# Create chain based on discovered vulnerabilities
chain = analyzer.create_chain(
    title="Robot API Authentication Bypass",
    description="Discovered via mobile app reverse engineering",
    impact=ImpactLevel.HIGH
)

# Add steps
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.OTHER,
    description="Reverse engineered mobile app to discover API endpoints",
    endpoint="Mobile app analysis",
    outcome="API endpoints and authentication mechanisms discovered"
)

step2 = ChainStep(
    step_number=2,
    vulnerability_type=VulnerabilityType.AUTH_BYPASS,
    description="JWT token validation bypass allows unauthorized access",
    endpoint="https://api.robot-service.com/v1/robots",
    prerequisites=["API endpoints and authentication mechanisms discovered"],
    outcome="Unauthorized API access achieved"
)

chain.add_step(step1)
chain.add_step(step2)

# Validate and export
is_valid, issues = chain.validate_chain()
if is_valid:
    analyzer.export_chain(chain, "mobile_app_finding.json")
    print("✅ Chain exported!")
else:
    print("⚠️  Validation issues:")
    for issue in issues:
        print(f"  {issue}")
```

## 🔍 Analysis Checklist

### Extraction
- [ ] APK extracted with apktool
- [ ] Resources extracted
- [ ] AndroidManifest.xml analyzed

### Decompilation
- [ ] APK decompiled with jadx
- [ ] Java code readable
- [ ] Dependencies identified

### API Discovery
- [ ] HTTPS URLs found
- [ ] API base URLs identified
- [ ] Endpoint paths discovered
- [ ] Request/response formats analyzed

### Authentication
- [ ] Authentication mechanisms identified
- [ ] API keys found
- [ ] Tokens discovered
- [ ] OAuth flows analyzed

### Testing
- [ ] APIs tested with curl
- [ ] Burp Suite configured
- [ ] Traffic intercepted
- [ ] Vulnerabilities identified

### Documentation
- [ ] Findings documented
- [ ] Attack chains created
- [ ] Reports generated

## 🛠️ Tools Reference

### apktool
```bash
# Extract APK
apktool d app.apk -o extracted/

# Rebuild APK (if needed)
apktool b extracted/ -o rebuilt.apk
```

### jadx
```bash
# Decompile APK
jadx app.apk -d decompiled/

# Decompile with GUI
jadx-gui app.apk
```

### grep
```bash
# Find HTTPS URLs
grep -r "https://" decompiled/

# Find API keywords
grep -ri "api\|endpoint" decompiled/

# Find authentication
grep -ri "token\|auth\|bearer" decompiled/
```

## 📋 Common Findings

### API Endpoints
- Base URLs in config files
- Endpoints in API client classes
- Hardcoded URLs in code

### Authentication
- API keys in strings.xml
- Tokens in SharedPreferences
- OAuth client IDs
- JWT tokens

### Vulnerabilities
- Hardcoded credentials
- Weak authentication
- Missing SSL pinning
- Insecure storage

## 🎯 Example Workflow

```bash
# 1. Get APK
# Download from APKPure or extract from device

# 2. Analyze
cd /Users/user/Cybersecurity/targets/robotics
bash mobile_app_workflow.sh irobot.apk

# 3. Review findings
cd mobile_analysis_work
cat api_endpoints.txt

# 4. Test APIs
curl -X GET https://api.irobot.com/v1/status

# 5. Document
python3
# ... use chain_analyzer.py ...
```

## Next Steps

1. ✅ Get an APK file
2. ✅ Run analysis workflow
3. ✅ Review findings
4. ✅ Test APIs
5. ✅ Document with chain_analyzer.py

## Need Help?

- **Finding APKs:** See `find_robot_apps.md`
- **Workflow:** Run `mobile_app_workflow.sh`
- **Documentation:** Use `chain_analyzer.py`


