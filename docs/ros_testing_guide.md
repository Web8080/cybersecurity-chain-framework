# ROS Security Testing Guide

## Goal: Test ROS Security Locally

### Step 1: Install ROS

**macOS:**
```bash
# Option 1: Homebrew
brew install ros-noetic-desktop

# Option 2: Docker (Recommended)
docker run -it --rm osrf/ros:noetic-desktop
```

**Linux (Ubuntu/Debian):**
```bash
# Follow official guide:
# http://wiki.ros.org/Installation/Ubuntu

# Quick install:
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt update
sudo apt install ros-noetic-desktop-full
```

### Step 2: Start ROS Master

```bash
# Source ROS setup
source /opt/ros/noetic/setup.bash

# Start ROS master
roscore

# This starts ROS master on port 11311
```

### Step 3: Test ROS Security

**Network Scan:**
```bash
# Scan for ROS master
nmap -p 11311 localhost

# Should show port 11311 open
```

**ROS Commands:**
```bash
# In another terminal (after sourcing ROS)

# List topics
rostopic list

# List nodes
rosnode list

# List services
rosservice list

# Get topic info
rostopic info /topic_name

# Echo topic data
rostopic echo /topic_name
```

### Step 4: Test Unauthenticated Access

**ROS 1 Security Issues:**
- No authentication by default
- All nodes trusted
- Topics/services accessible without auth

**Test:**
```bash
# Publish to any topic (if no auth)
rostopic pub /robot/cmd_vel geometry_msgs/Twist ...

# Call any service
rosservice call /service_name ...
```

### Step 5: Document Findings

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

chain = analyzer.create_chain(
 title="ROS Unauthenticated Topic Publishing",
 description="ROS master allows unauthenticated topic publishing",
 impact=ImpactLevel.HIGH
)

# Add steps...
# See example_chains.py for ROS chain example
```

## ROS Security Testing Checklist

- [ ] ROS master running (port 11311)
- [ ] Network scan confirms port open
- [ ] Topics enumerated
- [ ] Services enumerated
- [ ] Unauthenticated publishing tested
- [ ] Safety system bypass tested
- [ ] Findings documented

## ROS Tools

- **roscore** - Start ROS master
- **rostopic** - Topic management
- **rosnode** - Node management
- **rosservice** - Service management
- **rosbag** - Record/playback
- **nmap** - Network scanning

## Common ROS Security Issues

1. **No Authentication** - ROS 1 has no built-in auth
2. **Unencrypted Communication** - Default ROS communication unencrypted
3. **Open Topics** - All topics accessible
4. **No Access Control** - No permission system
5. **Network Exposure** - ROS master often exposed on network

## Testing Scenarios

### Scenario 1: Local ROS Testing
```bash
# 1. Start ROS master
roscore

# 2. Scan for ROS master
nmap -p 11311 localhost

# 3. Enumerate topics
rostopic list

# 4. Test unauthenticated publishing
rostopic pub /test_topic std_msgs/String "data: 'test'"
```

### Scenario 2: Network ROS Testing
```bash
# 1. Find ROS master on network
nmap -p 11311 <target-network>

# 2. Set ROS_MASTER_URI
export ROS_MASTER_URI=http://<target-ip>:11311

# 3. Test access
rostopic list
```

## Legal Note

 **Legal:** Test your own ROS setup
 **Legal:** Test with permission
 **Illegal:** Access ROS masters without permission

## Next Steps

1. Run setup: `bash setup_ros.sh`
2. Install ROS
3. Start ROS master
4. Test security
5. Document findings

