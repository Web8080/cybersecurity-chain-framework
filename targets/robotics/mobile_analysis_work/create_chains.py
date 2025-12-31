#!/usr/bin/env python3
"""
Create Attack Chains from Mobile App Analysis Findings
Author: Victor Ibhafidon

Creates attack chains based on findings from mobile app reverse engineering.

WHAT IT DOES:
- Creates attack chains for DJI GO 4 and iRobot Home apps
- Documents discovered endpoints and vulnerabilities
- Structures findings into multi-step attack chains
- Exports chains to JSON for documentation

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Processes findings from mobile app analysis workflow
- Integrates with endpoint_discovery.py results
- Chains document real-world mobile app vulnerabilities

USAGE:
 python targets/robotics/mobile_analysis_work/create_chains.py
"""

import sys
import os

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chains'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_dji_chain():
 """Create attack chain for DJI GO findings"""
 
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="DJI GO 4 - Firebase Database to Drone Control",
 description="Chained vulnerabilities discovered via mobile app reverse engineering",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "DJI GO 4 mobile app",
 "Access to decompiled app code"
 ]
 chain.context = "DJI GO 4 drone control application"
 chain.tags = {"dji", "drone", "mobile-app", "firebase", "api"}
 chain.severity = "High"
 
 # Step 1: Reverse Engineering
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Reverse engineered DJI GO 4 mobile app to discover Firebase database URL",
 endpoint="Mobile app analysis: apktool + jadx",
 payload="Extracted: https://djigo4-f53cb.firebaseio.com",
 outcome="Firebase database endpoint discovered"
 )
 
 # Step 2: Firebase Access
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Test Firebase database for unauthenticated access",
 endpoint="https://djigo4-f53cb.firebaseio.com/.json",
 prerequisites=["Firebase database endpoint discovered"],
 outcome="Firebase database access status determined"
 )
 
 # Step 3: Data Extraction
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Extract drone information, user data, or flight records from Firebase",
 endpoint="https://djigo4-f53cb.firebaseio.com/",
 prerequisites=["Firebase database access status determined"],
 outcome="Sensitive drone/user data accessed"
 )
 
 # Step 4: Flight Control API Discovery
 step4 = ChainStep(
 step_number=4,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Discover flight control API endpoints from app code (auto takeoff, landing, return home)",
 endpoint="Java code analysis",
 prerequisites=["Sensitive drone/user data accessed"],
 outcome="Flight control API endpoints identified"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 chain.add_step(step4)
 
 return analyzer, chain

def create_irobot_chain():
 """Create attack chain for iRobot findings"""
 
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="iRobot Home - Cloud API to Robot Control",
 description="Chained vulnerabilities discovered via mobile app reverse engineering",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "iRobot Home mobile app",
 "Access to decompiled app code"
 ]
 chain.context = "iRobot Home robot vacuum control application"
 chain.tags = {"irobot", "roomba", "mobile-app", "cloud-api", "iot"}
 chain.severity = "High"
 
 # Step 1: Reverse Engineering
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Reverse engineered iRobot Home app to discover cloud API endpoints",
 endpoint="Mobile app analysis: apktool + jadx",
 payload="Discovered: App/Cloud-api references, status.irobot.com",
 outcome="Cloud API endpoints and status endpoint discovered"
 )
 
 # Step 2: Status Endpoint Testing
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Test status endpoint for information disclosure",
 endpoint="https://status.irobot.com",
 prerequisites=["Cloud API endpoints and status endpoint discovered"],
 outcome="Status endpoint information gathered"
 )
 
 # Step 3: Cloud API Discovery
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Discover cloud API base URL and endpoints from Java code",
 endpoint="Java code analysis",
 prerequisites=["Status endpoint information gathered"],
 outcome="Cloud API base URL and endpoints identified"
 )
 
 # Step 4: Authentication Bypass
 step4 = ChainStep(
 step_number=4,
 vulnerability_type=VulnerabilityType.AUTH_BYPASS,
 description="Test cloud API for authentication bypass or weak authentication",
 endpoint="Cloud API endpoints",
 prerequisites=["Cloud API base URL and endpoints identified"],
 outcome="Unauthorized access to robot control API achieved"
 )
 
 # Step 5: Robot Control
 step5 = ChainStep(
 step_number=5,
 vulnerability_type=VulnerabilityType.BUSINESS_LOGIC,
 description="Execute unauthorized robot commands (start, stop, schedule)",
 endpoint="Robot control API",
 prerequisites=["Unauthorized access to robot control API achieved"],
 outcome="Unauthorized robot control achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 chain.add_step(step4)
 chain.add_step(step5)
 
 return analyzer, chain

if __name__ == "__main__":
 print("=" * 80)
 print("CREATING ATTACK CHAINS FROM MOBILE APP ANALYSIS")
 print("=" * 80)
 print()
 
 # DJI Chain
 print("\n" + "=" * 80)
 print("DJI GO 4 Attack Chain")
 print("=" * 80)
 analyzer1, chain1 = create_dji_chain()
 is_valid, issues = chain1.validate_chain()
 print(chain1.get_chain_summary())
 if not is_valid:
 print("\n Validation Issues:")
 for issue in issues:
 print(f" {issue}")
 analyzer1.chains.append(chain1)
 
 # Export DJI chain
 output_file1 = "dji_attack_chain.json"
 analyzer1.export_chain(chain1, output_file1)
 print(f"\n DJI chain exported to: {output_file1}")
 
 # iRobot Chain
 print("\n" + "=" * 80)
 print("iRobot Home Attack Chain")
 print("=" * 80)
 analyzer2, chain2 = create_irobot_chain()
 is_valid, issues = chain2.validate_chain()
 print(chain2.get_chain_summary())
 if not is_valid:
 print("\n Validation Issues:")
 for issue in issues:
 print(f" {issue}")
 analyzer2.chains.append(chain2)
 
 # Export iRobot chain
 output_file2 = "irobot_attack_chain.json"
 analyzer2.export_chain(chain2, output_file2)
 print(f"\n iRobot chain exported to: {output_file2}")
 
 print("\n" + "=" * 80)
 print("SUMMARY")
 print("=" * 80)
 print(f"DJI Chain: {len(chain1.steps)} steps, Impact: {chain1.impact.value}")
 print(f"iRobot Chain: {len(chain2.steps)} steps, Impact: {chain2.impact.value}")
 print("\n Both chains created and exported!")
 print("\nNext steps:")
 print(" 1. Test discovered endpoints")
 print(" 2. Validate chain feasibility")
 print(" 3. Generate reports with visualizer.py")

