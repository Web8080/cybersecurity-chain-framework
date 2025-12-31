#!/usr/bin/env python3
"""
IoTGoat - Attack Chain Templates
Author: Victor Ibhafidon

Pre-built attack chain templates for IoTGoat.
IoTGoat is a vulnerable IoT firmware for hardware security testing.

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Templates for IoT-specific attack scenarios
- Integrates with visualizer.py for diagram generation

USAGE:
 from chains.chain_templates.iotgoat_templates import get_iotgoat_templates
 
 templates = get_iotgoat_templates()
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_firmware_analysis_chain():
 """
 Template: Firmware Analysis to Device Compromise
 
 Firmware analysis reveals hardcoded credentials and backdoors.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="IoTGoat - Firmware Analysis to Device Compromise",
 description="Firmware analysis reveals hardcoded credentials leading to device compromise",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = [
 "Access to IoTGoat firmware image",
 "Firmware analysis tools (binwalk, strings, etc.)"
 ]
 chain.context = "IoTGoat vulnerable IoT firmware"
 chain.tags = {"firmware", "iot", "hardcoded-credentials", "iotgoat"}
 chain.severity = "Critical"
 
 # Step 1: Firmware Extraction
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Extract firmware filesystem using binwalk",
 endpoint="Firmware image file",
 payload="binwalk -e firmware.bin",
 outcome="Firmware filesystem extracted"
 )
 
 # Step 2: Credential Discovery
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.AUTH_BYPASS,
 description="Search for hardcoded credentials in extracted files",
 endpoint="Extracted filesystem",
 prerequisites=["Firmware filesystem extracted"],
 payload="strings filesystem/ | grep -i password",
 outcome="Hardcoded credentials discovered"
 )
 
 # Step 3: Device Compromise
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.RCE,
 description="Use discovered credentials to access device",
 endpoint="Device web interface or SSH",
 prerequisites=["Hardcoded credentials discovered"],
 payload="ssh root@device_ip (with discovered password)",
 outcome="Device compromised"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def create_network_exploitation_chain():
 """
 Template: Network Exploitation to Device Control
 
 Network scanning and exploitation leads to unauthorized device control.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="IoTGoat - Network Exploitation to Device Control",
 description="Network scanning reveals vulnerable services leading to device control",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "Network access to IoTGoat device",
 "Network scanning tools (nmap, etc.)"
 ]
 chain.context = "IoTGoat device on local network"
 chain.tags = {"network", "iot", "exploitation", "iotgoat"}
 chain.severity = "High"
 
 # Step 1: Network Discovery
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Scan network for IoTGoat device and open ports",
 endpoint="Network scan",
 payload="nmap -p- 192.168.1.100",
 outcome="Device and open ports identified"
 )
 
 # Step 2: Service Exploitation
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Exploit vulnerable service (e.g., Telnet with default credentials)",
 endpoint="Device service (port 23, 80, etc.)",
 prerequisites=["Device and open ports identified"],
 payload="telnet 192.168.1.100 (admin/admin)",
 outcome="Service access obtained"
 )
 
 # Step 3: Device Control
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.RCE,
 description="Execute commands to control device",
 endpoint="Device shell",
 prerequisites=["Service access obtained"],
 payload="Command execution via exploited service",
 outcome="Device control achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def get_iotgoat_templates():
 """Get all IoTGoat attack chain templates."""
 templates = []
 
 analyzer1, chain1 = create_firmware_analysis_chain()
 templates.append((analyzer1, chain1))
 
 analyzer2, chain2 = create_network_exploitation_chain()
 templates.append((analyzer2, chain2))
 
 return templates

if __name__ == "__main__":
 print("=" * 80)
 print("IoTGoat - ATTACK CHAIN TEMPLATES")
 print("=" * 80)
 
 templates = get_iotgoat_templates()
 for analyzer, chain in templates:
 print(f"\n {chain.title}")
 print(f" Steps: {len(chain.steps)}")
 is_valid, _ = chain.validate_chain()
 print(f" Status: {' Valid' if is_valid else ' Issues'}")
 
 print(f"\n Total: {len(templates)} templates")

