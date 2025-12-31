#!/usr/bin/env python3
"""
OWASP Juice Shop - Chain Discovery Helper
Author: Victor Ibhafidon

Helps discover and document attack chains in OWASP Juice Shop.

WHAT IT DOES:
- Provides helper methods for testing Juice Shop
- Generates vulnerability discovery checklists
- Assists in finding potential attack chains
- Connects to running Juice Shop instance

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py to create chains from findings
- Integrates with target_manager.py for target status
- Provides discovery workflow for Juice Shop
- Outputs chains compatible with framework

USAGE:
 from targets.juice_shop.discover_chains import JuiceShopHelper
 
 helper = JuiceShopHelper("http://localhost:3000")
 if helper.check_connection():
 checklist = helper.discover_vulnerabilities()
"""

import sys
import os
import requests
from typing import List, Dict

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'chains'))

from chain_analyzer import (
 ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)

class JuiceShopHelper:
 """Helper for testing Juice Shop"""
 
 def __init__(self, base_url: str = "http://localhost:3000"):
 self.base_url = base_url
 self.session = requests.Session()
 self.analyzer = ChainAnalyzer()
 
 def check_connection(self) -> bool:
 """Check if Juice Shop is accessible"""
 try:
 response = self.session.get(self.base_url, timeout=2)
 return response.status_code == 200
 except:
 return False
 
 def discover_vulnerabilities(self) -> List[Dict]:
 """
 Guide for discovering vulnerabilities
 Returns a checklist of things to test
 """
 checklist = [
 {
 "category": "Authentication",
 "tests": [
 "Try default credentials",
 "Test password reset functionality",
 "Check for JWT vulnerabilities",
 "Test session management",
 "Look for privilege escalation"
 ]
 },
 {
 "category": "Injection",
 "tests": [
 "SQL Injection in search",
 "NoSQL Injection in login",
 "Command Injection in file upload",
 "LDAP Injection if applicable"
 ]
 },
 {
 "category": "XSS",
 "tests": [
 "Stored XSS in product reviews",
 "Reflected XSS in search",
 "DOM-based XSS",
 "XSS in user profile"
 ]
 },
 {
 "category": "Business Logic",
 "tests": [
 "Price manipulation via API",
 "Quantity manipulation",
 "Checkout bypass",
 "Coupon code manipulation",
 "Race conditions"
 ]
 },
 {
 "category": "API Security",
 "tests": [
 "Test REST API endpoints",
 "Check for broken authentication",
 "Look for excessive data exposure",
 "Test mass assignment",
 "Check rate limiting"
 ]
 },
 {
 "category": "Other",
 "tests": [
 "SSRF vulnerabilities",
 "XXE if XML parsing exists",
 "Path traversal",
 "Insecure deserialization"
 ]
 }
 ]
 return checklist
 
 def create_chain_from_findings(self, title: str, description: str, 
 findings: List[Dict]) -> None:
 """
 Create an attack chain from discovered vulnerabilities
 
 findings format:
 [
 {
 "step": 1,
 "type": VulnerabilityType.XSS,
 "description": "...",
 "endpoint": "...",
 "payload": "...",
 "outcome": "..."
 },
 ...
 ]
 """
 chain = self.analyzer.create_chain(
 title=title,
 description=description,
 impact=ImpactLevel.HIGH
 )
 
 chain.context = "OWASP Juice Shop"
 chain.tags = {"juice-shop", "web"}
 
 for finding in sorted(findings, key=lambda x: x["step"]):
 step = ChainStep(
 step_number=finding["step"],
 vulnerability_type=finding["type"],
 description=finding["description"],
 endpoint=finding.get("endpoint"),
 payload=finding.get("payload"),
 outcome=finding.get("outcome")
 )
 chain.add_step(step)
 
 # Validate
 is_valid, issues = chain.validate_chain()
 
 if not is_valid:
 print(" Chain validation issues:")
 for issue in issues:
 print(f" - {issue}")
 
 self.analyzer.chains.append(chain)
 return chain
 
 def print_discovery_guide(self):
 """Print a guide for discovering vulnerabilities"""
 print("=" * 80)
 print("JUICE SHOP VULNERABILITY DISCOVERY GUIDE")
 print("=" * 80)
 print()
 
 if not self.check_connection():
 print(" Cannot connect to Juice Shop at", self.base_url)
 print(" Make sure it's running: bash targets/juice-shop/setup.sh")
 return
 
 print(" Connected to Juice Shop")
 print()
 
 checklist = self.discover_vulnerabilities()
 
 for category in checklist:
 print(f" {category['category']}")
 for test in category['tests']:
 print(f" {test}")
 print()
 
 print("=" * 80)
 print("NEXT STEPS")
 print("=" * 80)
 print()
 print("1. Test each item in the checklist")
 print("2. Document findings as you discover them")
 print("3. Look for relationships between vulnerabilities")
 print("4. Build attack chains using create_chain_from_findings()")
 print("5. Use chain_analyzer.py to document complete chains")
 print()

def example_price_manipulation_chain():
 """Example: Price manipulation attack chain"""
 helper = JuiceShopHelper()
 
 findings = [
 {
 "step": 1,
 "type": VulnerabilityType.BUSINESS_LOGIC,
 "description": "Price manipulation via API - modify product price in cart",
 "endpoint": "/api/BasketItems/{id}",
 "payload": '{"quantity": 1, "ProductId": 1, "BasketId": "...", "price": 0}',
 "outcome": "Product price set to $0"
 },
 {
 "step": 2,
 "type": VulnerabilityType.BUSINESS_LOGIC,
 "description": "Add multiple items with manipulated price",
 "endpoint": "/api/BasketItems",
 "prerequisites": ["Product price set to $0"],
 "outcome": "Cart contains free items"
 },
 {
 "step": 3,
 "type": VulnerabilityType.BUSINESS_LOGIC,
 "description": "Complete checkout with free items",
 "endpoint": "/api/Orders",
 "prerequisites": ["Cart contains free items"],
 "outcome": "Order completed without payment"
 }
 ]
 
 chain = helper.create_chain_from_findings(
 title="Juice Shop - Price Manipulation to Free Purchase",
 description="Chained business logic flaws allowing free product purchase",
 findings=findings
 )
 
 chain.impact = ImpactLevel.HIGH
 chain.severity = "High"
 
 print(chain.get_chain_summary())
 return chain

if __name__ == "__main__":
 helper = JuiceShopHelper()
 helper.print_discovery_guide()
 
 print("\n" + "=" * 80)
 print("EXAMPLE CHAIN")
 print("=" * 80)
 print()
 example_price_manipulation_chain()

