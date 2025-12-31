#!/usr/bin/env python3
"""
Robotics Attack Chain Examples
Author: Victor Ibhafidon

Demonstrates attack chains applicable to robotics platforms (ROS, Modbus, MQTT).

WHAT IT DOES:
- Creates example attack chains for robotics systems
- Demonstrates robot controller takeover chains
- Shows cloud API exploitation chains
- Provides ROS network exploitation examples

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py for chain creation
- Integrates with robotics discovery tools
- Used as templates for real robotics pentesting
- Chains saved as JSON for documentation

USAGE:
    python targets/robotics/example_chains.py
"""

import sys
import os

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'chains'))

from chain_analyzer import (
    ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)


def create_robot_controller_takeover_chain():
    """Example: Robot Controller Takeover Chain"""
    
    analyzer = ChainAnalyzer()
    
    chain = analyzer.create_chain(
        title="Robot Controller Network Takeover",
        description="Chained vulnerabilities leading to unauthorized robot control",
        impact=ImpactLevel.CRITICAL
    )
    
    chain.prerequisites = [
        "Network access to robot controller",
        "Robot controller on same network segment"
    ]
    chain.context = "Industrial robot with network-enabled controller"
    chain.tags = {"robotics", "network", "privilege-escalation", "hardware"}
    chain.severity = "Critical"
    
    # Step 1: Network Discovery
    step1 = ChainStep(
        step_number=1,
        vulnerability_type=VulnerabilityType.OTHER,
        description="Network scan discovers robot controller on port 502 (Modbus)",
        endpoint="Network scan: nmap -p 502 <network>",
        outcome="Robot controller IP and open ports identified"
    )
    
    # Step 2: Default Credentials
    step2 = ChainStep(
        step_number=2,
        vulnerability_type=VulnerabilityType.AUTH_BYPASS,
        description="Default credentials (admin/admin) allow access to controller web interface",
        endpoint="http://<robot-ip>/login",
        payload="admin:admin",
        prerequisites=["Robot controller IP and open ports identified"],
        outcome="Authenticated access to robot controller"
    )
    
    # Step 3: Command Injection
    step3 = ChainStep(
        step_number=3,
        vulnerability_type=VulnerabilityType.RCE,
        description="Command injection in robot control API allows system command execution",
        endpoint="/api/robot/command",
        payload='{"command": "move; cat /etc/passwd"}',
        prerequisites=["Authenticated access to robot controller"],
        outcome="System-level command execution achieved"
    )
    
    # Step 4: Robot Control Manipulation
    step4 = ChainStep(
        step_number=4,
        vulnerability_type=VulnerabilityType.BUSINESS_LOGIC,
        description="Modify robot control parameters to bypass safety limits",
        endpoint="/api/robot/config",
        prerequisites=["System-level command execution achieved"],
        outcome="Robot safety systems disabled, unauthorized control achieved"
    )
    
    chain.add_step(step1)
    chain.add_step(step2)
    chain.add_step(step3)
    chain.add_step(step4)
    
    return analyzer, chain


def create_cloud_robot_api_chain():
    """Example: Cloud Robot Service API Chain"""
    
    analyzer = ChainAnalyzer()
    
    chain = analyzer.create_chain(
        title="Cloud Robot Service API Exploitation",
        description="Chained API vulnerabilities leading to unauthorized robot control via cloud service",
        impact=ImpactLevel.HIGH
    )
    
    chain.prerequisites = [
        "Robot connected to cloud service",
        "Access to cloud service API"
    ]
    chain.context = "Cloud-connected service robot with mobile app control"
    chain.tags = {"robotics", "api", "cloud", "authentication"}
    chain.severity = "High"
    
    # Step 1: API Discovery
    step1 = ChainStep(
        step_number=1,
        vulnerability_type=VulnerabilityType.OTHER,
        description="Reverse engineer mobile app to discover cloud API endpoints",
        endpoint="api.robot-service.com/v1/",
        outcome="API endpoints and structure discovered"
    )
    
    # Step 2: Authentication Bypass
    step2 = ChainStep(
        step_number=2,
        vulnerability_type=VulnerabilityType.AUTH_BYPASS,
        description="JWT token validation bypass allows access without valid credentials",
        endpoint="/api/v1/auth/verify",
        payload='{"token": "eyJ0eXAiOiJKV1QiLCJhbGc..."}',
        prerequisites=["API endpoints and structure discovered"],
        outcome="Unauthenticated API access achieved"
    )
    
    # Step 3: IDOR to Robot Access
    step3 = ChainStep(
        step_number=3,
        vulnerability_type=VulnerabilityType.IDOR,
        description="Insecure direct object reference allows access to any robot by ID",
        endpoint="/api/v1/robots/{id}/control",
        prerequisites=["Unauthenticated API access achieved"],
        outcome="Access to unauthorized robot control endpoints"
    )
    
    # Step 4: Robot Command Injection
    step4 = ChainStep(
        step_number=4,
        vulnerability_type=VulnerabilityType.RCE,
        description="Command injection in robot control API allows arbitrary robot commands",
        endpoint="/api/v1/robots/{id}/execute",
        payload='{"command": "move_forward; speed=1000; disable_safety"}',
        prerequisites=["Access to unauthorized robot control endpoints"],
        outcome="Unauthorized robot control and manipulation"
    )
    
    chain.add_step(step1)
    chain.add_step(step2)
    chain.add_step(step3)
    chain.add_step(step4)
    
    return analyzer, chain


def create_ros_security_chain():
    """Example: ROS (Robot Operating System) Security Chain"""
    
    analyzer = ChainAnalyzer()
    
    chain = analyzer.create_chain(
        title="ROS Network Security Exploitation",
        description="Exploiting ROS network security vulnerabilities to control robot",
        impact=ImpactLevel.HIGH
    )
    
    chain.prerequisites = [
        "Network access to robot network",
        "ROS master node discoverable"
    ]
    chain.context = "Robot using ROS for control, ROS master exposed on network"
    chain.tags = {"robotics", "ros", "network", "protocol"}
    chain.severity = "High"
    
    # Step 1: ROS Master Discovery
    step1 = ChainStep(
        step_number=1,
        vulnerability_type=VulnerabilityType.OTHER,
        description="Network scan discovers ROS master on default port 11311",
        endpoint="Network: <robot-ip>:11311",
        outcome="ROS master node identified"
    )
    
    # Step 2: ROS Topic Discovery
    step2 = ChainStep(
        step_number=2,
        vulnerability_type=VulnerabilityType.OTHER,
        description="Query ROS master to discover available topics and services",
        endpoint="ROS master API: rostopic list",
        prerequisites=["ROS master node identified"],
        outcome="Robot control topics and services discovered"
    )
    
    # Step 3: Unauthenticated Topic Publishing
    step3 = ChainStep(
        step_number=3,
        vulnerability_type=VulnerabilityType.BUSINESS_LOGIC,
        description="Publish commands to robot control topics without authentication",
        endpoint="ROS topic: /robot/cmd_vel",
        payload='{"linear": {"x": 1.0}, "angular": {"z": 0.5}}',
        prerequisites=["Robot control topics and services discovered"],
        outcome="Unauthorized robot movement commands sent"
    )
    
    # Step 4: Safety System Bypass
    step4 = ChainStep(
        step_number=4,
        vulnerability_type=VulnerabilityType.BUSINESS_LOGIC,
        description="Publish to safety override topic to disable safety systems",
        endpoint="ROS topic: /robot/safety/override",
        payload='{"override": true, "reason": "maintenance"}',
        prerequisites=["Unauthorized robot movement commands sent"],
        outcome="Robot safety systems disabled, full control achieved"
    )
    
    chain.add_step(step1)
    chain.add_step(step2)
    chain.add_step(step3)
    chain.add_step(step4)
    
    return analyzer, chain


if __name__ == "__main__":
    print("=" * 80)
    print("ROBOTICS ATTACK CHAIN EXAMPLES")
    print("=" * 80)
    print()
    
    # Example 1
    print("\n" + "=" * 80)
    print("Example 1: Robot Controller Network Takeover")
    print("=" * 80)
    analyzer1, chain1 = create_robot_controller_takeover_chain()
    is_valid, issues = chain1.validate_chain()
    print(chain1.get_chain_summary())
    analyzer1.chains.append(chain1)
    
    # Example 2
    print("\n" + "=" * 80)
    print("Example 2: Cloud Robot Service API Exploitation")
    print("=" * 80)
    analyzer2, chain2 = create_cloud_robot_api_chain()
    is_valid, issues = chain2.validate_chain()
    print(chain2.get_chain_summary())
    analyzer2.chains.append(chain2)
    
    # Example 3
    print("\n" + "=" * 80)
    print("Example 3: ROS Network Security Exploitation")
    print("=" * 80)
    analyzer3, chain3 = create_ros_security_chain()
    is_valid, issues = chain3.validate_chain()
    print(chain3.get_chain_summary())
    analyzer3.chains.append(chain3)
    
    print("\n" + "=" * 80)
    print("All chains created successfully!")
    print("=" * 80)
    print("\nTo export chains:")
    print("  analyzer.export_chain(chain, 'robot_chain.json')")
    print("\nTo generate reports:")
    print("  from chains.visualizer import generate_markdown_report")
    print("  print(generate_markdown_report(chain))")


