# Quick Setup: All Three Approaches

## Setup All Three Methods

### Option 1: Run All Setups

```bash
cd /Users/user/Cybersecurity/targets/robotics

# Setup mobile app analysis
bash setup_mobile_analysis.sh

# Setup ROS environment
bash setup_ros.sh

# Setup Shodan/Censys
bash setup_shodan.sh
```

### Option 2: Setup Individually

#### 1⃣ Mobile App Reverse Engineering

```bash
bash setup_mobile_analysis.sh
```

**What it installs:**
- apktool (APK extraction)
- jadx (Java decompilation)
- adb (Android Debug Bridge, optional)

**Next steps:**
- See: `mobile_analysis_guide.md`
- Get an APK file
- Extract and analyze

#### 2⃣ Local ROS Setup

```bash
bash setup_ros.sh
```

**What it does:**
- Checks for ROS installation
- Provides installation instructions
- Sets up ROS environment

**Next steps:**
- See: `ros_testing_guide.md`
- Install ROS (if not installed)
- Start ROS master
- Test ROS security

#### 3⃣ Shodan/Censys Setup

```bash
bash setup_shodan.sh
```

**What it installs:**
- Shodan CLI
- Censys Python library

**Next steps:**
- See: `shodan_censys_guide.md`
- Get API keys
- Configure tools
- Search responsibly!

## Quick Start Checklist

### Mobile App Analysis
- [ ] Run `setup_mobile_analysis.sh`
- [ ] Get robot app APK
- [ ] Extract with apktool
- [ ] Decompile with jadx
- [ ] Find API endpoints
- [ ] Test with Burp Suite

### ROS Testing
- [ ] Run `setup_ros.sh`
- [ ] Install ROS
- [ ] Start ROS master
- [ ] Scan port 11311
- [ ] Test ROS commands
- [ ] Document findings

### Shodan/Censys
- [ ] Run `setup_shodan.sh`
- [ ] Get Shodan API key
- [ ] Get Censys credentials
- [ ] Configure tools
- [ ] Search (with permission!)
- [ ] Test (with permission!)

## Recommended Order

1. **Start with Mobile App Analysis** (Easiest, no setup needed)
2. **Then ROS Setup** (Good for learning)
3. **Finally Shodan/Censys** (Requires API keys)

## Documentation

- **Mobile Analysis:** `mobile_analysis_guide.md`
- **ROS Testing:** `ros_testing_guide.md`
- **Shodan/Censys:** `shodan_censys_guide.md`
- **Discovery Tool:** `discover_chains.py`

## Need Help?

Run the setup scripts and follow the guides. Each approach has detailed documentation.

