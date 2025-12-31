#!/bin/bash
# Setup script for Local ROS Environment

set -e

echo " Setting up Local ROS Environment..."
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
 echo " macOS detected"
 echo ""
 
 # Check for Homebrew
 if command -v brew &> /dev/null; then
 echo " Homebrew found"
 echo ""
 echo " ROS Installation Options for macOS:"
 echo ""
 echo "Option 1: ROS Noetic (via Homebrew)"
 echo " brew install ros-noetic-desktop"
 echo ""
 echo "Option 2: Docker ROS (Recommended for macOS)"
 echo " docker run -it --rm osrf/ros:noetic-desktop"
 echo ""
 echo "Option 3: Manual Installation"
 echo " See: http://wiki.ros.org/Installation/macOS"
 echo ""
 
 read -p "Install ROS via Homebrew? (y/n) " -n 1 -r
 echo
 if [[ $REPLY =~ ^[Yy]$ ]]; then
 echo "Installing ROS Noetic..."
 brew install ros-noetic-desktop
 echo ""
 echo " ROS installed!"
 echo ""
 echo "To use ROS:"
 echo " source /opt/ros/noetic/setup.bash"
 echo " roscore"
 fi
 else
 echo " Homebrew not found"
 echo " Install from: https://brew.sh/"
 echo ""
 echo "Alternative: Use Docker"
 echo " docker run -it --rm osrf/ros:noetic-desktop"
 fi
 
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
 echo " Linux detected"
 echo ""
 echo " ROS Installation for Linux:"
 echo ""
 echo "Follow official installation guide:"
 echo " http://wiki.ros.org/Installation/Ubuntu"
 echo ""
 echo "Quick install (Ubuntu/Debian):"
 echo " sudo sh -c 'echo \"deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main\" > /etc/apt/sources.list.d/ros-latest.list'"
 echo " sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654"
 echo " sudo apt update"
 echo " sudo apt install ros-noetic-desktop-full"
 echo ""
 
else
 echo " Unsupported OS: $OSTYPE"
 echo " See: http://wiki.ros.org/Installation"
fi

echo ""
echo " Checking for ROS..."
if command -v roscore &> /dev/null; then
 echo " ROS is installed!"
 echo ""
 echo "To start ROS master:"
 echo " roscore"
 echo ""
 echo "This will start ROS master on port 11311"
 echo "You can then test ROS security locally"
else
 echo " ROS not found in PATH"
 echo ""
 echo "After installation, source ROS setup:"
 echo " source /opt/ros/noetic/setup.bash"
 echo " roscore"
fi

echo ""
echo " ROS Security Testing:"
echo " - ROS master runs on port 11311"
echo " - Test with: rostopic list"
echo " - Test with: rosnode list"
echo " - Network scan: nmap -p 11311 localhost"
echo ""
echo " See: docs/ros_testing_guide.md for detailed instructions"

