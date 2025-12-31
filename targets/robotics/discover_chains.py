#!/usr/bin/env python3
"""
Robotics Chain Discovery Helper
Author: Victor Ibhafidon

Helps discover and document attack chains in robotics systems.

WHAT IT DOES:
- Scans for robot services (Modbus, ROS, MQTT)
- Tests default credentials on robot controllers
- Discovers network services and protocols
- Creates attack chains from discovered vulnerabilities

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create chains
- Integrates with mobile app analysis tools
- Works with ROS and Modbus testing tools
- Outputs chains for documentation

USAGE:
    from targets.robotics.discover_chains import RoboticsDiscoveryHelper
    
    helper = RoboticsDiscoveryHelper("192.168.1.100")
    results = helper.network_scan("192.168.1.100")
"""

import sys
import os
import subprocess
import socket
from typing import List, Dict, Optional

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'chains'))

from chain_analyzer import (
    ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)


class RoboticsDiscoveryHelper:
    """Helper for testing robotics systems"""
    
    def __init__(self, target_ip: Optional[str] = None):
        self.target_ip = target_ip
        self.analyzer = ChainAnalyzer()
        self.discovered_services = []
        self.discovered_vulnerabilities = []
    
    def network_scan(self, target_ip: str, ports: List[int] = None) -> Dict:
        """Scan target for common robot ports"""
        if ports is None:
            ports = [502, 11311, 80, 443, 8080, 1883]  # Modbus, ROS, HTTP, HTTPS, MQTT
        
        results = {
            "target": target_ip,
            "open_ports": [],
            "services": {}
        }
        
        print(f"🔍 Scanning {target_ip} for robot services...")
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                
                if result == 0:
                    results["open_ports"].append(port)
                    service = self._identify_service(port)
                    results["services"][port] = service
                    print(f"  ✅ Port {port} open - {service}")
            except Exception as e:
                pass
        
        return results
    
    def _identify_service(self, port: int) -> str:
        """Identify service by port"""
        service_map = {
            502: "Modbus (Industrial Protocol)",
            11311: "ROS Master",
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP (Alternative)",
            1883: "MQTT",
            22: "SSH",
            23: "Telnet"
        }
        return service_map.get(port, "Unknown")
    
    def check_default_credentials(self, target_ip: str, port: int = 80) -> List[str]:
        """Check for default credentials (example)"""
        common_credentials = [
            ("admin", "admin"),
            ("admin", "password"),
            ("root", "root"),
            ("user", "user"),
            ("guest", "guest")
        ]
        
        print(f"🔐 Checking default credentials on {target_ip}:{port}...")
        # This is a placeholder - implement actual credential checking
        return []
    
    def discover_vulnerabilities(self) -> List[Dict]:
        """Guide for discovering vulnerabilities"""
        checklist = [
            {
                "category": "Network Discovery",
                "tests": [
                    "Scan for robot controller ports (502, 11311, 80, 443)",
                    "Identify robot controller IP addresses",
                    "Map network topology",
                    "Identify protocols in use (Modbus, ROS, HTTP, MQTT)"
                ]
            },
            {
                "category": "Authentication",
                "tests": [
                    "Test default credentials (admin/admin, root/root)",
                    "Check for authentication bypass",
                    "Test JWT token validation",
                    "Check for session management issues"
                ]
            },
            {
                "category": "Network Protocols",
                "tests": [
                    "Test Modbus security (if port 502 open)",
                    "Test ROS master security (if port 11311 open)",
                    "Check for unencrypted communication",
                    "Test MQTT security (if port 1883 open)"
                ]
            },
            {
                "category": "Web Interfaces",
                "tests": [
                    "Test for command injection",
                    "Check for XSS vulnerabilities",
                    "Test for CSRF",
                    "Check for IDOR vulnerabilities",
                    "Test API endpoints"
                ]
            },
            {
                "category": "ROS Security (if applicable)",
                "tests": [
                    "Enumerate ROS topics",
                    "Test unauthenticated topic publishing",
                    "Check for service access",
                    "Test safety system bypass",
                    "Verify ROS master security"
                ]
            },
            {
                "category": "API Security",
                "tests": [
                    "Reverse engineer mobile apps for API discovery",
                    "Test API authentication",
                    "Check for IDOR in API endpoints",
                    "Test for command injection in APIs",
                    "Check rate limiting"
                ]
            },
            {
                "category": "Firmware/Hardware",
                "tests": [
                    "Extract firmware (if possible)",
                    "Analyze firmware for hardcoded credentials",
                    "Check for UART/JTAG access",
                    "Test physical security"
                ]
            }
        ]
        return checklist
    
    def create_chain_from_findings(self, title: str, description: str, 
                                   findings: List[Dict]) -> None:
        """Create an attack chain from discovered vulnerabilities"""
        chain = self.analyzer.create_chain(
            title=title,
            description=description,
            impact=ImpactLevel.HIGH
        )
        
        chain.context = "Robotics security testing"
        chain.tags = {"robotics", "pentest"}
        
        for finding in sorted(findings, key=lambda x: x.get("step", 0)):
            step = ChainStep(
                step_number=finding.get("step", 1),
                vulnerability_type=finding.get("type", VulnerabilityType.OTHER),
                description=finding.get("description", ""),
                endpoint=finding.get("endpoint"),
                payload=finding.get("payload"),
                outcome=finding.get("outcome")
            )
            chain.add_step(step)
        
        # Validate
        is_valid, issues = chain.validate_chain()
        
        if not is_valid:
            print("⚠️  Chain validation issues:")
            for issue in issues:
                print(f"  {issue}")
        
        self.analyzer.chains.append(chain)
        return chain
    
    def print_discovery_guide(self):
        """Print a guide for discovering vulnerabilities"""
        print("=" * 80)
        print("ROBOTICS SECURITY DISCOVERY GUIDE")
        print("=" * 80)
        print()
        
        if self.target_ip:
            print(f"🎯 Target: {self.target_ip}")
            print()
            scan_results = self.network_scan(self.target_ip)
            print()
            
            if scan_results["open_ports"]:
                print("📋 Discovered Services:")
                for port, service in scan_results["services"].items():
                    print(f"   Port {port}: {service}")
            else:
                print("⚠️  No common robot ports found")
                print("   Try scanning manually: nmap -p 502,11311,80,443 <target-ip>")
            print()
        else:
            print("💡 To scan a target, provide IP address:")
            print("   helper = RoboticsDiscoveryHelper(target_ip='192.168.1.100')")
            print()
        
        checklist = self.discover_vulnerabilities()
        
        for category in checklist:
            print(f"📋 {category['category']}")
            for test in category['tests']:
                print(f"   ☐ {test}")
            print()
        
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print()
        print("1. Run network scans to discover robot services")
        print("2. Test each item in the checklist")
        print("3. Document findings as you discover them")
        print("4. Look for relationships between vulnerabilities")
        print("5. Build attack chains using create_chain_from_findings()")
        print("6. Use chain_analyzer.py to document complete chains")
        print()


def example_robotics_chain():
    """Example: Robotics attack chain"""
    helper = RoboticsDiscoveryHelper()
    
    findings = [
        {
            "step": 1,
            "type": VulnerabilityType.OTHER,
            "description": "Network scan discovers robot controller on port 502 (Modbus)",
            "endpoint": "Network scan: nmap -p 502 <network>",
            "outcome": "Robot controller IP and open ports identified"
        },
        {
            "step": 2,
            "type": VulnerabilityType.AUTH_BYPASS,
            "description": "Default credentials (admin/admin) allow access to controller",
            "endpoint": "http://<robot-ip>/login",
            "payload": "admin:admin",
            "outcome": "Authenticated access to robot controller"
        },
        {
            "step": 3,
            "type": VulnerabilityType.RCE,
            "description": "Command injection in robot control API",
            "endpoint": "/api/robot/command",
            "payload": '{"command": "move; cat /etc/passwd"}',
            "outcome": "System-level command execution achieved"
        }
    ]
    
    chain = helper.create_chain_from_findings(
        title="Robot Controller Network Takeover",
        description="Chained vulnerabilities leading to unauthorized robot control",
        findings=findings
    )
    
    chain.impact = ImpactLevel.CRITICAL
    chain.severity = "Critical"
    
    print(chain.get_chain_summary())
    return chain


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Robotics Security Discovery Helper")
    parser.add_argument("--target", "-t", help="Target IP address to scan")
    parser.add_argument("--example", "-e", action="store_true", help="Show example chain")
    
    args = parser.parse_args()
    
    if args.example:
        print("\n" + "=" * 80)
        print("EXAMPLE ROBOTICS ATTACK CHAIN")
        print("=" * 80)
        print()
        example_robotics_chain()
    else:
        helper = RoboticsDiscoveryHelper(target_ip=args.target)
        helper.print_discovery_guide()
        
        if args.target:
            print("\n" + "=" * 80)
            print("EXAMPLE CHAIN")
            print("=" * 80)
            print()
            example_robotics_chain()


