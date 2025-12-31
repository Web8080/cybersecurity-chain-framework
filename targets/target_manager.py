#!/usr/bin/env python3
"""
Target Manager - Pentesting Target Management Module
Author: Victor Ibhafidon

Manages pentesting targets (vulnerable applications) and their lifecycle.

WHAT IT DOES:
- Tracks multiple pentesting targets (Juice Shop, DVWA, bWAPP, etc.)
- Checks target status (running/stopped/unknown)
- Starts/stops Docker containers for targets
- Provides status reports for all targets
- Integrates with chain_analyzer for target-specific chains

HOW IT CONNECTS TO THE FRAMEWORK:
- Provides targets for attack chain analysis
- Used by setup scripts (targets/*/setup.sh) to manage targets
- Status information used by chain discovery tools
- Each target can have associated attack chains
- Works with Docker to manage containerized targets

USAGE:
    from targets.target_manager import TargetManager
    
    manager = TargetManager()
    status = manager.check_all_status()
    manager.start_target("juice-shop")
    report = manager.generate_status_report()
"""

import subprocess
import requests
import json
import os
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class TargetStatus(Enum):
    """Status of a target"""
    RUNNING = "running"
    STOPPED = "stopped"
    UNKNOWN = "unknown"
    NOT_INSTALLED = "not_installed"


@dataclass
class Target:
    """Represents a pentesting target"""
    name: str
    target_type: str  # "web", "hardware", "iot", "robotics"
    url: Optional[str] = None
    port: Optional[int] = None
    docker_image: Optional[str] = None
    docker_container: Optional[str] = None
    description: str = ""
    setup_command: Optional[str] = None
    
    def check_status(self) -> TargetStatus:
        """Check if target is running"""
        if self.docker_container:
            try:
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if self.docker_container in result.stdout:
                    # Check if it's actually responding
                    if self.url:
                        try:
                            response = requests.get(self.url, timeout=2)
                            if response.status_code < 500:
                                return TargetStatus.RUNNING
                        except:
                            pass
                    return TargetStatus.RUNNING
                return TargetStatus.STOPPED
            except:
                return TargetStatus.UNKNOWN
        
        if self.url:
            try:
                response = requests.get(self.url, timeout=2)
                if response.status_code < 500:
                    return TargetStatus.RUNNING
            except:
                pass
        
        return TargetStatus.UNKNOWN
    
    def start(self) -> bool:
        """Start the target"""
        if self.docker_container:
            try:
                # Check if container exists
                result = subprocess.run(
                    ["docker", "ps", "-a", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True
                )
                
                if self.docker_container in result.stdout:
                    # Start existing container
                    subprocess.run(
                        ["docker", "start", self.docker_container],
                        check=True,
                        capture_output=True
                    )
                elif self.docker_image:
                    # Create and start new container
                    cmd = [
                        "docker", "run", "-d",
                        "--name", self.docker_container,
                        "-p", f"{self.port}:{self.port}",
                        self.docker_image
                    ]
                    subprocess.run(cmd, check=True, capture_output=True)
                else:
                    return False
                
                return True
            except subprocess.CalledProcessError:
                return False
        
        return False
    
    def stop(self) -> bool:
        """Stop the target"""
        if self.docker_container:
            try:
                subprocess.run(
                    ["docker", "stop", self.docker_container],
                    check=True,
                    capture_output=True
                )
                return True
            except subprocess.CalledProcessError:
                return False
        return False


class TargetManager:
    """Manages multiple pentesting targets"""
    
    def __init__(self):
        self.targets: Dict[str, Target] = {}
        self._load_default_targets()
    
    def _load_default_targets(self):
        """Load default targets"""
        # OWASP Juice Shop
        self.targets["juice-shop"] = Target(
            name="OWASP Juice Shop",
            target_type="web",
            url="http://localhost:3000",
            port=3000,
            docker_image="bkimminich/juice-shop",
            docker_container="juice-shop",
            description="Modern vulnerable web application with 100+ vulnerabilities"
        )
        
        # DVWA
        self.targets["dvwa"] = Target(
            name="Damn Vulnerable Web Application",
            target_type="web",
            url="http://localhost:8080",
            port=8080,
            docker_image="vulnerables/web-dvwa",
            docker_container="dvwa",
            description="Classic vulnerable web application for learning"
        )
        
        # bWAPP
        self.targets["bwapp"] = Target(
            name="bWAPP (Buggy Web Application)",
            target_type="web",
            url="http://localhost:80",
            port=80,
            docker_image="raesene/bwapp",
            docker_container="bwapp",
            description="100+ vulnerabilities for practicing"
        )
        
        # WebGoat
        self.targets["webgoat"] = Target(
            name="OWASP WebGoat",
            target_type="web",
            url="http://localhost:8080/WebGoat",
            port=8080,
            docker_image="webgoat/goatandwolf",
            docker_container="webgoat",
            description="OWASP-maintained educational platform with guided lessons"
        )
    
    def add_target(self, target: Target):
        """Add a custom target"""
        self.targets[target.name.lower().replace(" ", "-")] = target
    
    def get_target(self, name: str) -> Optional[Target]:
        """Get a target by name"""
        return self.targets.get(name.lower())
    
    def list_targets(self) -> List[Target]:
        """List all targets"""
        return list(self.targets.values())
    
    def check_all_status(self) -> Dict[str, TargetStatus]:
        """Check status of all targets"""
        statuses = {}
        for name, target in self.targets.items():
            statuses[name] = target.check_status()
        return statuses
    
    def start_target(self, name: str) -> bool:
        """Start a target"""
        target = self.get_target(name)
        if target:
            return target.start()
        return False
    
    def stop_target(self, name: str) -> bool:
        """Stop a target"""
        target = self.get_target(name)
        if target:
            return target.stop()
        return False
    
    def generate_status_report(self) -> str:
        """Generate a status report"""
        report = []
        report.append("=" * 80)
        report.append("PENTESTING TARGETS STATUS")
        report.append("=" * 80)
        report.append("")
        
        statuses = self.check_all_status()
        
        for name, target in self.targets.items():
            status = statuses[name]
            status_icon = {
                TargetStatus.RUNNING: "✅",
                TargetStatus.STOPPED: "⏸️",
                TargetStatus.UNKNOWN: "❓",
                TargetStatus.NOT_INSTALLED: "❌"
            }.get(status, "❓")
            
            report.append(f"{status_icon} {target.name}")
            report.append(f"   Type: {target.target_type}")
            report.append(f"   Status: {status.value}")
            if target.url:
                report.append(f"   URL: {target.url}")
            report.append(f"   Description: {target.description}")
            report.append("")
        
        return "\n".join(report)


if __name__ == "__main__":
    manager = TargetManager()
    
    print(manager.generate_status_report())
    
    # Example: Start Juice Shop
    print("\n" + "=" * 80)
    print("QUICK START EXAMPLE")
    print("=" * 80)
    print("\nTo start Juice Shop:")
    print("  python3 target_manager.py --start juice-shop")
    print("\nOr use the setup script:")
    print("  bash targets/juice-shop/setup.sh")

