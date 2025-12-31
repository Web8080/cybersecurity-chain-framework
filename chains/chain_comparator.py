#!/usr/bin/env python3
"""
Chain Comparator - Compare Attack Chains
Author: Victor Ibhafidon

WHAT IT DOES:
- Compares two attack chains side-by-side
- Highlights differences in steps, vulnerabilities, and structure
- Identifies common patterns and similarities
- Generates comparison reports
- Calculates similarity scores

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py's AttackChain and ChainStep classes
- Integrates with report_generator.py for formatted output
- Helps identify patterns across different attack scenarios
- Supports chain analysis and optimization

USAGE:
    from chains.chain_comparator import ChainComparator
    from chains.chain_analyzer import AttackChain
    
    comparator = ChainComparator()
    comparison = comparator.compare_chains(chain1, chain2)
    print(comparator.generate_report(comparison))
"""

import sys
import os
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chains.chain_analyzer import AttackChain, ChainStep, VulnerabilityType, ImpactLevel


@dataclass
class StepComparison:
    """Comparison result for a single step"""
    step_number: int
    chain1_step: Optional[ChainStep] = None
    chain2_step: Optional[ChainStep] = None
    similarity_score: float = 0.0
    differences: List[str] = field(default_factory=list)
    similarities: List[str] = field(default_factory=list)


@dataclass
class ChainComparison:
    """Complete comparison between two chains"""
    chain1: AttackChain
    chain2: AttackChain
    overall_similarity: float = 0.0
    step_comparisons: List[StepComparison] = field(default_factory=list)
    common_vulnerabilities: Set[VulnerabilityType] = field(default_factory=set)
    common_patterns: List[str] = field(default_factory=list)
    structural_differences: List[str] = field(default_factory=list)
    impact_difference: str = ""


class ChainComparator:
    """Compares attack chains and identifies patterns"""
    
    def compare_chains(self, chain1: AttackChain, chain2: AttackChain) -> ChainComparison:
        """Compare two attack chains"""
        comparison = ChainComparison(chain1=chain1, chain2=chain2)
        
        # Compare structure
        comparison.structural_differences = self._compare_structure(chain1, chain2)
        
        # Compare impact
        comparison.impact_difference = self._compare_impact(chain1, chain2)
        
        # Compare steps
        comparison.step_comparisons = self._compare_steps(chain1, chain2)
        
        # Find common vulnerabilities
        comparison.common_vulnerabilities = self._find_common_vulnerabilities(chain1, chain2)
        
        # Find common patterns
        comparison.common_patterns = self._find_common_patterns(chain1, chain2)
        
        # Calculate overall similarity
        comparison.overall_similarity = self._calculate_similarity(comparison)
        
        return comparison
    
    def _compare_structure(self, chain1: AttackChain, chain2: AttackChain) -> List[str]:
        """Compare structural differences"""
        differences = []
        
        if len(chain1.steps) != len(chain2.steps):
            differences.append(
                f"Step count: Chain 1 has {len(chain1.steps)} steps, "
                f"Chain 2 has {len(chain2.steps)} steps"
            )
        
        if chain1.impact != chain2.impact:
            differences.append(
                f"Impact level: Chain 1 is {chain1.impact.value}, "
                f"Chain 2 is {chain2.impact.value}"
            )
        
        chain1_tags = set(chain1.tags)
        chain2_tags = set(chain2.tags)
        if chain1_tags != chain2_tags:
            only_in_1 = chain1_tags - chain2_tags
            only_in_2 = chain2_tags - chain1_tags
            if only_in_1:
                differences.append(f"Tags only in Chain 1: {', '.join(only_in_1)}")
            if only_in_2:
                differences.append(f"Tags only in Chain 2: {', '.join(only_in_2)}")
        
        return differences
    
    def _compare_impact(self, chain1: AttackChain, chain2: AttackChain) -> str:
        """Compare impact levels"""
        if chain1.impact == chain2.impact:
            return f"Both chains have {chain1.impact.value} impact"
        else:
            return (
                f"Chain 1: {chain1.impact.value}, "
                f"Chain 2: {chain2.impact.value}"
            )
    
    def _compare_steps(self, chain1: AttackChain, chain2: AttackChain) -> List[StepComparison]:
        """Compare individual steps"""
        comparisons = []
        max_steps = max(len(chain1.steps), len(chain2.steps))
        
        for i in range(max_steps):
            step1 = chain1.steps[i] if i < len(chain1.steps) else None
            step2 = chain2.steps[i] if i < len(chain2.steps) else None
            
            comp = StepComparison(
                step_number=i + 1,
                chain1_step=step1,
                chain2_step=step2
            )
            
            if step1 and step2:
                # Both steps exist - compare them
                comp.similarity_score = self._compare_step_details(step1, step2, comp)
            elif step1:
                comp.differences.append(f"Step {i+1} only exists in Chain 1")
            elif step2:
                comp.differences.append(f"Step {i+1} only exists in Chain 2")
            
            comparisons.append(comp)
        
        return comparisons
    
    def _compare_step_details(
        self, 
        step1: ChainStep, 
        step2: ChainStep, 
        comp: StepComparison
    ) -> float:
        """Compare details of two steps and return similarity score"""
        similarities = []
        differences = []
        score = 0.0
        max_score = 0.0
        
        # Compare vulnerability type (weight: 40%)
        max_score += 0.4
        if step1.vulnerability_type == step2.vulnerability_type:
            score += 0.4
            similarities.append(f"Same vulnerability type: {step1.vulnerability_type.value}")
        else:
            differences.append(
                f"Vulnerability type: {step1.vulnerability_type.value} vs "
                f"{step2.vulnerability_type.value}"
            )
        
        # Compare description (weight: 30%)
        max_score += 0.3
        desc_sim = self._text_similarity(step1.description, step2.description)
        score += desc_sim * 0.3
        if desc_sim > 0.7:
            similarities.append("Similar descriptions")
        elif desc_sim < 0.3:
            differences.append("Different descriptions")
        
        # Compare endpoint (weight: 15%)
        max_score += 0.15
        if step1.endpoint and step2.endpoint:
            if step1.endpoint == step2.endpoint:
                score += 0.15
                similarities.append(f"Same endpoint: {step1.endpoint}")
            else:
                differences.append(f"Endpoints differ: {step1.endpoint} vs {step2.endpoint}")
        elif step1.endpoint or step2.endpoint:
            differences.append("One step missing endpoint")
        
        # Compare outcome (weight: 15%)
        max_score += 0.15
        if step1.outcome and step2.outcome:
            outcome_sim = self._text_similarity(step1.outcome, step2.outcome)
            score += outcome_sim * 0.15
            if outcome_sim > 0.7:
                similarities.append("Similar outcomes")
            elif outcome_sim < 0.3:
                differences.append("Different outcomes")
        elif step1.outcome or step2.outcome:
            differences.append("One step missing outcome")
        
        comp.similarities = similarities
        comp.differences = differences
        
        # Normalize score
        if max_score > 0:
            return score / max_score
        return 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity using word overlap"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _find_common_vulnerabilities(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> Set[VulnerabilityType]:
        """Find vulnerabilities present in both chains"""
        vulns1 = {step.vulnerability_type for step in chain1.steps}
        vulns2 = {step.vulnerability_type for step in chain2.steps}
        return vulns1 & vulns2
    
    def _find_common_patterns(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> List[str]:
        """Identify common attack patterns"""
        patterns = []
        
        # Check for same vulnerability sequence
        seq1 = [step.vulnerability_type for step in chain1.steps]
        seq2 = [step.vulnerability_type for step in chain2.steps]
        
        if seq1 == seq2:
            patterns.append("Identical vulnerability sequence")
        
        # Check for common starting vulnerability
        if chain1.steps and chain2.steps:
            if chain1.steps[0].vulnerability_type == chain2.steps[0].vulnerability_type:
                patterns.append(
                    f"Both start with {chain1.steps[0].vulnerability_type.value}"
                )
        
        # Check for common ending vulnerability
        if chain1.steps and chain2.steps:
            if chain1.steps[-1].vulnerability_type == chain2.steps[-1].vulnerability_type:
                patterns.append(
                    f"Both end with {chain1.steps[-1].vulnerability_type.value}"
                )
        
        # Check for privilege escalation pattern
        has_priv_esc1 = any(
            step.vulnerability_type == VulnerabilityType.PRIV_ESCALATION 
            for step in chain1.steps
        )
        has_priv_esc2 = any(
            step.vulnerability_type == VulnerabilityType.PRIV_ESCALATION 
            for step in chain2.steps
        )
        if has_priv_esc1 and has_priv_esc2:
            patterns.append("Both chains include privilege escalation")
        
        return patterns
    
    def _calculate_similarity(self, comparison: ChainComparison) -> float:
        """Calculate overall similarity score"""
        if not comparison.step_comparisons:
            return 0.0
        
        # Average step similarity
        step_scores = [
            comp.similarity_score 
            for comp in comparison.step_comparisons 
            if comp.chain1_step and comp.chain2_step
        ]
        
        if not step_scores:
            return 0.0
        
        avg_step_similarity = sum(step_scores) / len(step_scores)
        
        # Weight factors
        structure_weight = 0.2
        step_weight = 0.6
        pattern_weight = 0.2
        
        # Structure similarity (based on step count difference)
        step_count_diff = abs(
            len(comparison.chain1.steps) - len(comparison.chain2.steps)
        )
        max_steps = max(len(comparison.chain1.steps), len(comparison.chain2.steps))
        if max_steps > 0:
            structure_sim = 1.0 - (step_count_diff / max_steps)
        else:
            structure_sim = 1.0
        
        # Pattern similarity (based on common patterns)
        pattern_sim = min(len(comparison.common_patterns) / 3.0, 1.0)
        
        overall = (
            structure_sim * structure_weight +
            avg_step_similarity * step_weight +
            pattern_sim * pattern_weight
        )
        
        return overall
    
    def generate_report(self, comparison: ChainComparison) -> str:
        """Generate a formatted comparison report"""
        report = []
        report.append("=" * 80)
        report.append("ATTACK CHAIN COMPARISON REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Chain information
        report.append("Chain 1:")
        report.append(f"  Title: {comparison.chain1.title}")
        report.append(f"  Steps: {len(comparison.chain1.steps)}")
        report.append(f"  Impact: {comparison.chain1.impact.value}")
        report.append("")
        
        report.append("Chain 2:")
        report.append(f"  Title: {comparison.chain2.title}")
        report.append(f"  Steps: {len(comparison.chain2.steps)}")
        report.append(f"  Impact: {comparison.chain2.impact.value}")
        report.append("")
        
        # Overall similarity
        report.append("-" * 80)
        report.append(f"Overall Similarity: {comparison.overall_similarity * 100:.1f}%")
        report.append("-" * 80)
        report.append("")
        
        # Common vulnerabilities
        if comparison.common_vulnerabilities:
            report.append("Common Vulnerabilities:")
            for vuln in comparison.common_vulnerabilities:
                report.append(f"  - {vuln.value}")
            report.append("")
        
        # Common patterns
        if comparison.common_patterns:
            report.append("Common Patterns:")
            for pattern in comparison.common_patterns:
                report.append(f"  - {pattern}")
            report.append("")
        
        # Structural differences
        if comparison.structural_differences:
            report.append("Structural Differences:")
            for diff in comparison.structural_differences:
                report.append(f"  - {diff}")
            report.append("")
        
        # Step-by-step comparison
        report.append("-" * 80)
        report.append("STEP-BY-STEP COMPARISON")
        report.append("-" * 80)
        report.append("")
        
        for comp in comparison.step_comparisons:
            report.append(f"Step {comp.step_number}:")
            
            if comp.chain1_step:
                report.append(f"  Chain 1: [{comp.chain1_step.vulnerability_type.value}] "
                            f"{comp.chain1_step.description}")
            else:
                report.append("  Chain 1: (missing)")
            
            if comp.chain2_step:
                report.append(f"  Chain 2: [{comp.chain2_step.vulnerability_type.value}] "
                            f"{comp.chain2_step.description}")
            else:
                report.append("  Chain 2: (missing)")
            
            if comp.chain1_step and comp.chain2_step:
                report.append(f"  Similarity: {comp.similarity_score * 100:.1f}%")
                
                if comp.similarities:
                    report.append("  Similarities:")
                    for sim in comp.similarities:
                        report.append(f"    + {sim}")
                
                if comp.differences:
                    report.append("  Differences:")
                    for diff in comp.differences:
                        report.append(f"    - {diff}")
            
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def find_similar_chains(
        self, 
        target_chain: AttackChain, 
        chains: List[AttackChain],
        threshold: float = 0.5
    ) -> List[Tuple[AttackChain, float]]:
        """Find chains similar to the target chain"""
        similar = []
        
        for chain in chains:
            if chain == target_chain:
                continue
            
            comparison = self.compare_chains(target_chain, chain)
            if comparison.overall_similarity >= threshold:
                similar.append((chain, comparison.overall_similarity))
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return similar


if __name__ == "__main__":
    # Example usage
    from chains.chain_analyzer import ChainAnalyzer
    
    analyzer = ChainAnalyzer()
    
    # Create two example chains
    chain1 = analyzer.create_chain(
        "XSS to Admin Takeover",
        "XSS leading to admin access",
        ImpactLevel.CRITICAL
    )
    
    step1_1 = ChainStep(
        1, VulnerabilityType.XSS,
        "Stored XSS in user profile",
        outcome="XSS payload stored"
    )
    step1_2 = ChainStep(
        2, VulnerabilityType.SESSION_HIJACKING,
        "Admin views profile, session stolen",
        prerequisites=["XSS payload stored"],
        outcome="Admin session token obtained"
    )
    step1_3 = ChainStep(
        3, VulnerabilityType.PRIV_ESCALATION,
        "Use admin token to access admin panel",
        prerequisites=["Admin session token obtained"],
        outcome="Full admin access"
    )
    
    chain1.add_step(step1_1)
    chain1.add_step(step1_2)
    chain1.add_step(step1_3)
    
    chain2 = analyzer.create_chain(
        "XSS to Account Takeover",
        "XSS leading to user account takeover",
        ImpactLevel.HIGH
    )
    
    step2_1 = ChainStep(
        1, VulnerabilityType.XSS,
        "Reflected XSS in search field",
        outcome="XSS payload executed"
    )
    step2_2 = ChainStep(
        2, VulnerabilityType.SESSION_HIJACKING,
        "Steal user session cookie",
        prerequisites=["XSS payload executed"],
        outcome="User session token stolen"
    )
    step2_3 = ChainStep(
        3, VulnerabilityType.AUTH_BYPASS,
        "Use stolen session to access account",
        prerequisites=["User session token stolen"],
        outcome="Account compromised"
    )
    
    chain2.add_step(step2_1)
    chain2.add_step(step2_2)
    chain2.add_step(step2_3)
    
    # Compare chains
    comparator = ChainComparator()
    comparison = comparator.compare_chains(chain1, chain2)
    
    # Generate report
    print(comparator.generate_report(comparison))

