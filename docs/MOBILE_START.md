# 🚀 Mobile App Analysis - Quick Start

## ✅ Tools Ready!

- ✅ apktool - Installed
- ✅ jadx - Installed
- ✅ Java - Installed

## 🎯 Quick Start (3 Steps)

### Step 1: Get an APK File

**Easiest: Download from APKPure**
1. Go to: https://apkpure.com/
2. Search: "irobot" or "roomba"
3. Download APK
4. Save to: `/Users/user/Cybersecurity/targets/robotics/`

**Or use any robot app:**
- Roomba apps
- Drone apps
- Robot toy apps

### Step 2: Run Analysis

```bash
cd /Users/user/Cybersecurity/targets/robotics

# Run workflow (replace with your APK path)
bash mobile_app_workflow.sh ~/Downloads/irobot.apk
```

**What happens:**
- Extracts APK
- Decompiles to Java
- Finds API endpoints
- Finds authentication
- Saves results

### Step 3: Review & Test

```bash
cd mobile_analysis_work

# View found endpoints
cat api_endpoints.txt

# Test APIs
curl -X GET <discovered-endpoint>
```

## 📋 Complete Workflow

1. **Get APK** → Download from APKPure
2. **Analyze** → Run `mobile_app_workflow.sh`
3. **Review** → Check `api_endpoints.txt`
4. **Test** → Use curl or Burp Suite
5. **Document** → Use `chain_analyzer.py`

## 🎯 Recommended First App

**iRobot Home (Roomba)**
- Most popular robot app
- Well-structured APIs
- Good for learning
- Download: https://apkpure.com/irobot-home/com.irobot.home

## 📚 Guides Available

- **Complete Guide:** `mobile_analysis_complete_guide.md`
- **Finding Apps:** `find_robot_apps.md`
- **Workflow Script:** `mobile_app_workflow.sh`

## 🛠️ Ready to Start?

```bash
# 1. Download an APK (or use one you have)
# 2. Run:
cd /Users/user/Cybersecurity/targets/robotics
bash mobile_app_workflow.sh <your-apk-file>

# 3. Review results in mobile_analysis_work/
```

**That's it!** The workflow will do everything automatically.


