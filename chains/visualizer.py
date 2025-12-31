#!/usr/bin/env python3
"""
Attack Chain Visualizer - Visualization and Reporting Module
Author: Victor Ibhafidon

Generates visual representations and reports of attack chains in multiple formats.

WHAT IT DOES:
- Creates Mermaid diagrams for visual chain representation
- Generates text-based diagrams for terminal output
- Creates Markdown reports with full chain details
- Exports chains to JSON format
- Integrates with chain_analyzer.py to visualize AttackChain objects

HOW IT CONNECTS TO THE FRAMEWORK:
- Takes AttackChain objects from chain_analyzer.py
- Generates reports for documentation (docs/ folder)
- Creates diagrams for presentations and reports
- Used by target-specific modules to visualize their chains
- Output formats support integration with documentation tools

USAGE:
    from chains.visualizer import generate_mermaid_diagram, generate_markdown_report
    from chains.chain_analyzer import ChainAnalyzer
    
    analyzer = ChainAnalyzer()
    chain = analyzer.load_chain("my_chain.json")
    diagram = generate_mermaid_diagram(chain)
    report = generate_markdown_report(chain)
"""

from typing import List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chains.chain_analyzer import AttackChain, ChainStep
import json


def generate_mermaid_diagram(chain: AttackChain) -> str:
    """Generate a Mermaid diagram for the attack chain"""
    diagram = []
    diagram.append("```mermaid")
    diagram.append("graph TD")
    
    # Add prerequisites
    if chain.prerequisites:
        diagram.append("    Prerequisites[Prerequisites]")
        for i, prereq in enumerate(chain.prerequisites):
            prereq_id = f"Prereq{i+1}"
            diagram.append(f"    Prerequisites --> {prereq_id}[{prereq}]")
            if i == 0:
                first_step = f"Step{chain.steps[0].step_number}"
                diagram.append(f"    {prereq_id} --> {first_step}")
            elif i < len(chain.prerequisites) - 1:
                next_prereq = f"Prereq{i+2}"
                diagram.append(f"    {prereq_id} --> {next_prereq}")
    
    # Add steps
    for i, step in enumerate(chain.steps):
        step_id = f"Step{step.step_number}"
        step_label = f"{step.step_number}. {step.vulnerability_type.value}"
        diagram.append(f"    {step_id}[{step_label}]")
        
        # Connect to next step
        if i < len(chain.steps) - 1:
            next_step_id = f"Step{chain.steps[i+1].step_number}"
            diagram.append(f"    {step_id} --> {next_step_id}")
        
        # Connect prerequisites
        if step.prerequisites:
            for prereq in step.prerequisites:
                # Try to find if this prereq is from a previous step
                for prev_step in chain.steps[:i]:
                    if prev_step.outcome and prereq in prev_step.outcome:
                        prev_id = f"Step{prev_step.step_number}"
                        diagram.append(f"    {prev_id} -.-> {step_id}")
    
    # Add final outcome
    if chain.steps:
        last_step = chain.steps[-1]
        last_id = f"Step{last_step.step_number}"
        diagram.append(f"    {last_id} --> Outcome[{chain.impact.value} Impact]")
    
    diagram.append("```")
    return "\n".join(diagram)


def generate_text_diagram(chain: AttackChain) -> str:
    """Generate a simple text-based diagram"""
    diagram = []
    diagram.append("=" * 80)
    diagram.append(f"ATTACK CHAIN: {chain.title}")
    diagram.append("=" * 80)
    diagram.append(f"\nImpact: {chain.impact.value}")
    diagram.append(f"Severity: {chain.severity}")
    
    if chain.prerequisites:
        diagram.append("\nPrerequisites:")
        for prereq in chain.prerequisites:
            diagram.append(f"  • {prereq}")
    
    diagram.append("\nChain Flow:")
    diagram.append("─" * 80)
    
    for i, step in enumerate(chain.steps):
        connector = "└─►" if i == len(chain.steps) - 1 else "├─►"
        diagram.append(f"{connector} Step {step.step_number}: {step.vulnerability_type.value}")
        diagram.append(f"   Description: {step.description}")
        if step.endpoint:
            diagram.append(f"   Endpoint: {step.endpoint}")
        if step.outcome:
            diagram.append(f"   Outcome: {step.outcome}")
        
        if i < len(chain.steps) - 1:
            diagram.append("   │")
            diagram.append("   ▼")
    
    if chain.steps:
        last_step = chain.steps[-1]
        diagram.append(f"\nFinal Impact: {chain.impact.value}")
        if last_step.outcome:
            diagram.append(f"Result: {last_step.outcome}")
    
    diagram.append("─" * 80)
    return "\n".join(diagram)


def generate_json_export(chain: AttackChain) -> str:
    """Generate JSON export of the chain"""
    return json.dumps(chain.to_dict(), indent=2)


def generate_markdown_report(chain: AttackChain) -> str:
    """Generate a markdown report of the chain"""
    report = []
    report.append(f"# {chain.title}\n")
    report.append(f"**Severity:** {chain.severity}  \n")
    report.append(f"**Impact:** {chain.impact.value}  \n")
    report.append(f"**Discovered:** {chain.discovered_at.strftime('%Y-%m-%d') if chain.discovered_at else 'Unknown'}  \n")
    
    if chain.description:
        report.append(f"\n## Description\n\n{chain.description}\n")
    
    if chain.context:
        report.append(f"\n## Context\n\n{chain.context}\n")
    
    if chain.prerequisites:
        report.append("\n## Prerequisites\n")
        for prereq in chain.prerequisites:
            report.append(f"- {prereq}")
        report.append("")
    
    report.append("\n## Attack Chain Steps\n")
    
    for step in chain.steps:
        report.append(f"### Step {step.step_number}: {step.vulnerability_type.value}\n")
        report.append(f"**Description:** {step.description}\n")
        
        if step.endpoint:
            report.append(f"**Endpoint:** `{step.endpoint}`\n")
        
        if step.payload:
            report.append(f"**Payload:**\n```\n{step.payload}\n```\n")
        
        if step.prerequisites:
            report.append("**Prerequisites:**\n")
            for prereq in step.prerequisites:
                report.append(f"- {prereq}\n")
        
        if step.outcome:
            report.append(f"**Outcome:** {step.outcome}\n")
        
        if step.evidence:
            report.append(f"**Evidence:** {step.evidence}\n")
        
        report.append("")
    
    # Add Mermaid diagram
    report.append("## Chain Visualization\n")
    report.append(generate_mermaid_diagram(chain))
    report.append("")
    
    if chain.tags:
        report.append("\n## Tags\n")
        for tag in sorted(chain.tags):
            report.append(f"`{tag}` ")
        report.append("")
    
    return "\n".join(report)


if __name__ == "__main__":
    # Example usage
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Example Chain",
        description="An example attack chain",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR in admin panel", 
                     prerequisites=["XSS stored"], outcome="Admin access")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    print(generate_text_diagram(chain))
    print("\n" + "="*80 + "\n")
    print(generate_markdown_report(chain))

