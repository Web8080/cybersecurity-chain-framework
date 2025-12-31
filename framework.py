#!/usr/bin/env python3
"""
Security Testing Framework - Core Framework Module
Author: Victor Ibhafidon

This is the foundational module that embodies the core philosophy of the framework:
- Automation finds bugs: Automated tools excel at discovering common vulnerabilities
- Humans find chains: Security researchers identify multi-step exploits
- Business logic requires context: Understanding workflows is essential for logic flaws

HOW IT CONNECTS TO THE FRAMEWORK:
This module provides the base classes and data structures used throughout the framework.
It defines the SecurityFinding class and SecurityFramework class that other modules
(chain_analyzer, target_manager, etc.) build upon. This is the foundation that enables
the entire attack chain analysis workflow.

USAGE:
    from framework import SecurityFramework, FindingType
    
    framework = SecurityFramework()
    framework.add_automated_bug("SQL Injection", "...", "High")
    framework.add_attack_chain("XSS to RCE", "...", "Critical", chain=[...])
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


class FindingType(Enum):
    """
    Types of security findings that can be discovered.
    
    This enum categorizes findings based on how they were discovered,
    which aligns with the framework's core philosophy.
    """
    AUTOMATED_BUG = "automated_bug"      # Found by automation tools
    ATTACK_CHAIN = "attack_chain"        # Found by human analysis (multi-step)
    BUSINESS_LOGIC = "business_logic"   # Requires context and domain knowledge


@dataclass
class SecurityFinding:
    """
    Represents a single security finding in the framework.
    
    This is the core data structure that stores all security findings,
    whether they're automated bugs, attack chains, or business logic flaws.
    All findings are stored as instances of this class.
    
    Attributes:
        title: Short descriptive title of the finding
        finding_type: Type of finding (automated, chain, or business logic)
        description: Detailed description of the vulnerability
        severity: Severity level (Critical, High, Medium, Low)
        context: Additional context about the finding
        attack_chain: List of steps if this is an attack chain finding
        business_workflow: Workflow description if this is a business logic flaw
        discovered_by: Who or what discovered this (automation/human)
        discovered_at: Timestamp of when the finding was discovered
    """
    title: str
    finding_type: FindingType
    description: str
    severity: str
    context: Optional[str] = None
    attack_chain: Optional[List[str]] = None
    business_workflow: Optional[str] = None
    discovered_by: Optional[str] = None
    discovered_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamp if not provided"""
        if self.discovered_at is None:
            self.discovered_at = datetime.now()


class SecurityFramework:
    """
    Main framework class for organizing and managing security testing findings.
    
    This is the central orchestrator of the framework. It maintains a collection
    of all security findings and provides methods to add different types of findings.
    Other modules (like chain_analyzer) can use this to store their findings in
    a unified format.
    
    HOW IT CONNECTS:
    - Used by chain_analyzer.py to store attack chain findings
    - Used by target_manager.py to track findings per target
    - Used by automation tools to store automated bug discoveries
    - Provides unified reporting across all finding types
    """
    
    def __init__(self):
        """Initialize the framework with an empty findings list"""
        self.findings: List[SecurityFinding] = []
    
    def add_automated_bug(self, title: str, description: str, severity: str):
        """
        Add a finding discovered by automated tools.
        
        This method is used when automated scanners (like OWASP ZAP, Burp Suite)
        discover vulnerabilities. These are typically single-step, well-known bugs.
        
        Args:
            title: Short title of the bug
            description: Detailed description
            severity: Severity level
            
        Returns:
            The created SecurityFinding object
        """
        finding = SecurityFinding(
            title=title,
            finding_type=FindingType.AUTOMATED_BUG,
            description=description,
            severity=severity,
            discovered_by="automation"
        )
        self.findings.append(finding)
        return finding
    
    def add_attack_chain(self, title: str, description: str, severity: str, 
                        chain: List[str], context: Optional[str] = None):
        """
        Add a finding representing a multi-step attack chain.
        
        This is the core method for storing attack chains discovered through
        human analysis. Attack chains are sequences of vulnerabilities that
        can be chained together for greater impact.
        
        Args:
            title: Title of the attack chain
            description: Overall description
            severity: Overall severity
            chain: List of steps in the chain (strings)
            context: Additional context about the attack
            
        Returns:
            The created SecurityFinding object
        """
        finding = SecurityFinding(
            title=title,
            finding_type=FindingType.ATTACK_CHAIN,
            description=description,
            severity=severity,
            attack_chain=chain,
            context=context,
            discovered_by="human"
        )
        self.findings.append(finding)
        return finding
    
    def add_business_logic_flaw(self, title: str, description: str, severity: str,
                               workflow: str, context: str):
        """
        Add a business logic vulnerability finding.
        
        Business logic flaws require understanding of the application's
        business rules and workflows. These are typically discovered through
        manual analysis and domain knowledge.
        
        Args:
            title: Title of the flaw
            description: Description of the vulnerability
            severity: Severity level
            workflow: Description of the affected workflow
            context: Business context and rules
            
        Returns:
            The created SecurityFinding object
        """
        finding = SecurityFinding(
            title=title,
            finding_type=FindingType.BUSINESS_LOGIC,
            description=description,
            severity=severity,
            business_workflow=workflow,
            context=context,
            discovered_by="human"
        )
        self.findings.append(finding)
        return finding
    
    def get_findings_by_type(self, finding_type: FindingType) -> List[SecurityFinding]:
        """
        Filter findings by type.
        
        Useful for generating reports focused on specific types of findings,
        or for analyzing patterns in how vulnerabilities are discovered.
        
        Args:
            finding_type: The type of findings to filter
            
        Returns:
            List of findings matching the type
        """
        return [f for f in self.findings if f.finding_type == finding_type]
    
    def generate_report(self) -> str:
        """
        Generate a summary report of all findings.
        
        Creates a text-based report showing the total findings and breakdown
        by type. This is useful for quick overviews and sprint reviews.
        
        Returns:
            Formatted string report
        """
        report = []
        report.append("=" * 60)
        report.append("Security Testing Report")
        report.append("=" * 60)
        report.append(f"\nTotal Findings: {len(self.findings)}")
        report.append(f"\nBy Type:")
        # Count each type of finding
        report.append(f"  Automated Bugs: {len(self.get_findings_by_type(FindingType.AUTOMATED_BUG))}")
        report.append(f"  Attack Chains: {len(self.get_findings_by_type(FindingType.ATTACK_CHAIN))}")
        report.append(f"  Business Logic: {len(self.get_findings_by_type(FindingType.BUSINESS_LOGIC))}")
        report.append("\n" + "=" * 60)
        return "\n".join(report)


if __name__ == "__main__":
    """
    Example usage demonstrating the three types of findings:
    1. Automated bugs - found by tools
    2. Attack chains - found by humans (multi-step)
    3. Business logic - requires context understanding
    """
    framework = SecurityFramework()
    
    # Example 1: Automation finds bugs
    # This represents a single vulnerability discovered by automated scanners
    framework.add_automated_bug(
        "SQL Injection in Login",
        "User input not properly sanitized in login query",
        "High"
    )
    
    # Example 2: Humans find chains
    # This represents a multi-step attack that requires human analysis to discover
    # Each step in the chain builds on the previous step's outcome
    framework.add_attack_chain(
        "Privilege Escalation Chain",
        "Chained vulnerabilities leading to admin access",
        "Critical",
        chain=[
            "1. XSS in user profile",           # Step 1: Initial vulnerability
            "2. Session hijacking via XSS",     # Step 2: Uses Step 1's outcome
            "3. IDOR in admin panel",           # Step 3: Uses Step 2's outcome
            "4. Privilege escalation"          # Step 4: Final goal achieved
        ],
        context="Multi-step attack requiring user interaction"
    )
    
    # Example 3: Business logic requires context
    # This represents a flaw that requires understanding the application's
    # business rules and workflows - something automated tools can't detect
    framework.add_business_logic_flaw(
        "Payment Bypass via Workflow Manipulation",
        "Users can skip payment step by manipulating workflow state",
        "High",
        workflow="Checkout -> Payment -> Confirmation",
        context="Payment validation only checks if step exists, not if payment was actually processed"
    )
    
    # Generate and display a summary report
    print(framework.generate_report())


