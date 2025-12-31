#!/usr/bin/env python3
"""
Report Generator - Automated Report Generation Module
Author: Victor Ibhafidon

Generates professional security reports from attack chains.

WHAT IT DOES:
- Creates executive summaries from attack chains
- Generates detailed technical reports
- Includes visualizations (Mermaid diagrams)
- Exports to multiple formats (Markdown, HTML)
- Provides recommendations and remediation guidance

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py for chain data
- Integrates with visualizer.py for diagrams
- Outputs reports to docs/ folder
- Used by target-specific modules for reporting

USAGE:
    from chains.report_generator import ReportGenerator
    
    generator = ReportGenerator()
    report = generator.generate_executive_summary(chain)
    full_report = generator.generate_full_report(chain)
    generator.export_to_markdown(chain, "report.md")
"""

import sys
import os
from datetime import datetime
from typing import List, Optional

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chains.chain_analyzer import AttackChain, ChainStep, ImpactLevel, VulnerabilityType
from chains.visualizer import generate_mermaid_diagram, generate_markdown_report


class ReportGenerator:
    """
    Generates professional security reports from attack chains.
    """
    
    def __init__(self):
        """Initialize the report generator"""
        self.report_date = datetime.now().strftime("%Y-%m-%d")
    
    def generate_executive_summary(self, chain: AttackChain) -> str:
        """
        Generate an executive summary of the attack chain.
        
        This is a high-level overview suitable for management and stakeholders.
        
        Args:
            chain: The AttackChain to summarize
            
        Returns:
            Executive summary as formatted string
        """
        summary = []
        summary.append("=" * 80)
        summary.append("EXECUTIVE SUMMARY")
        summary.append("=" * 80)
        summary.append("")
        
        summary.append(f"Title: {chain.title}")
        summary.append(f"Severity: {chain.severity}")
        summary.append(f"Impact Level: {chain.impact.value}")
        summary.append(f"Date: {self.report_date}")
        summary.append("")
        
        summary.append("Overview:")
        summary.append(f"  {chain.description}")
        summary.append("")
        
        summary.append("Attack Chain Summary:")
        summary.append(f"  This attack chain consists of {len(chain.steps)} steps that can be")
        summary.append(f"  chained together to achieve {chain.impact.value.lower()} impact.")
        summary.append("")
        
        summary.append("Key Steps:")
        for i, step in enumerate(chain.steps[:3], 1):  # Show first 3 steps
            summary.append(f"  {i}. {step.vulnerability_type.value}: {step.description[:60]}...")
        if len(chain.steps) > 3:
            summary.append(f"  ... and {len(chain.steps) - 3} more steps")
        summary.append("")
        
        summary.append("Business Impact:")
        impact_descriptions = {
            ImpactLevel.CRITICAL: "Critical impact - Complete system compromise possible",
            ImpactLevel.HIGH: "High impact - Significant data or system access possible",
            ImpactLevel.MEDIUM: "Medium impact - Limited access or data exposure possible",
            ImpactLevel.LOW: "Low impact - Minor information disclosure or limited access"
        }
        summary.append(f"  {impact_descriptions.get(chain.impact, 'Unknown impact')}")
        summary.append("")
        
        summary.append("Recommendation:")
        summary.append("  Immediate remediation is recommended. Please review the full technical")
        summary.append("  report for detailed steps and mitigation strategies.")
        summary.append("")
        summary.append("=" * 80)
        
        return "\n".join(summary)
    
    def generate_technical_report(self, chain: AttackChain) -> str:
        """
        Generate a detailed technical report.
        
        This includes all technical details, payloads, endpoints, and evidence.
        
        Args:
            chain: The AttackChain to document
            
        Returns:
            Technical report as formatted string
        """
        report = []
        report.append("=" * 80)
        report.append("TECHNICAL SECURITY REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Header Information
        report.append("Report Information:")
        report.append(f"  Title: {chain.title}")
        report.append(f"  Severity: {chain.severity}")
        report.append(f"  Impact: {chain.impact.value}")
        report.append(f"  Discovered: {chain.discovered_at.strftime('%Y-%m-%d') if chain.discovered_at else 'Unknown'}")
        report.append(f"  Discovered By: {chain.discovered_by or 'Unknown'}")
        report.append(f"  Report Date: {self.report_date}")
        report.append("")
        
        # Description
        report.append("Description:")
        report.append(f"  {chain.description}")
        report.append("")
        
        # Context
        if chain.context:
            report.append("Context:")
            report.append(f"  {chain.context}")
            report.append("")
        
        # Prerequisites
        if chain.prerequisites:
            report.append("Prerequisites:")
            for prereq in chain.prerequisites:
                report.append(f"  - {prereq}")
            report.append("")
        
        # Attack Chain Steps
        report.append("=" * 80)
        report.append("ATTACK CHAIN DETAILS")
        report.append("=" * 80)
        report.append("")
        
        for step in chain.steps:
            report.append(f"Step {step.step_number}: {step.vulnerability_type.value}")
            report.append("-" * 80)
            report.append(f"Description: {step.description}")
            report.append("")
            
            if step.endpoint:
                report.append(f"Endpoint: {step.endpoint}")
                report.append("")
            
            if step.payload:
                report.append("Payload:")
                report.append("```")
                report.append(step.payload)
                report.append("```")
                report.append("")
            
            if step.prerequisites:
                report.append("Prerequisites:")
                for prereq in step.prerequisites:
                    report.append(f"  - {prereq}")
                report.append("")
            
            if step.outcome:
                report.append(f"Outcome: {step.outcome}")
                report.append("")
            
            if step.evidence:
                report.append("Evidence:")
                report.append(f"  {step.evidence}")
                report.append("")
            
            report.append("")
        
        # Impact Assessment
        report.append("=" * 80)
        report.append("IMPACT ASSESSMENT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Overall Impact: {chain.impact.value}")
        report.append(f"Severity: {chain.severity}")
        report.append("")
        
        if chain.steps:
            last_step = chain.steps[-1]
            if last_step.outcome:
                report.append(f"Final Outcome: {last_step.outcome}")
                report.append("")
        
        # Tags
        if chain.tags:
            report.append("Tags:")
            report.append(f"  {', '.join(sorted(chain.tags))}")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_recommendations(self, chain: AttackChain) -> str:
        """
        Generate remediation recommendations based on the attack chain.
        
        Args:
            chain: The AttackChain to analyze
            
        Returns:
            Recommendations as formatted string
        """
        recommendations = []
        recommendations.append("=" * 80)
        recommendations.append("REMEDIATION RECOMMENDATIONS")
        recommendations.append("=" * 80)
        recommendations.append("")
        
        # General recommendations based on vulnerability types
        vuln_recommendations = {
            VulnerabilityType.XSS: [
                "Implement Content Security Policy (CSP)",
                "Sanitize all user input",
                "Use output encoding for user-generated content",
                "Implement XSS filters and validation"
            ],
            VulnerabilityType.SQL_INJECTION: [
                "Use parameterized queries or prepared statements",
                "Implement input validation and sanitization",
                "Apply principle of least privilege to database users",
                "Use Web Application Firewall (WAF) rules"
            ],
            VulnerabilityType.IDOR: [
                "Implement proper authorization checks",
                "Use indirect object references",
                "Validate user permissions for each resource access",
                "Implement access control lists (ACL)"
            ],
            VulnerabilityType.AUTH_BYPASS: [
                "Implement strong authentication mechanisms",
                "Use secure session management",
                "Validate tokens and session state",
                "Implement multi-factor authentication (MFA)"
            ],
            VulnerabilityType.SESSION_HIJACKING: [
                "Use secure, HttpOnly cookies",
                "Implement session timeout and rotation",
                "Use HTTPS for all session-related traffic",
                "Implement CSRF protection"
            ],
            VulnerabilityType.RCE: [
                "Sanitize all command inputs",
                "Use whitelisting for allowed commands",
                "Implement least privilege for system users",
                "Use sandboxing and isolation"
            ],
            VulnerabilityType.BUSINESS_LOGIC: [
                "Review business logic workflows",
                "Implement proper state validation",
                "Add transaction integrity checks",
                "Conduct security code reviews"
            ]
        }
        
        # Collect unique vulnerability types from chain
        vuln_types = set(step.vulnerability_type for step in chain.steps)
        
        recommendations.append("Priority Actions:")
        recommendations.append("")
        
        priority = 1
        for vuln_type in vuln_types:
            if vuln_type in vuln_recommendations:
                recommendations.append(f"{priority}. Address {vuln_type.value}:")
                for rec in vuln_recommendations[vuln_type]:
                    recommendations.append(f"   - {rec}")
                recommendations.append("")
                priority += 1
        
        # General recommendations
        recommendations.append("General Recommendations:")
        recommendations.append("  - Conduct regular security assessments")
        recommendations.append("  - Implement security monitoring and logging")
        recommendations.append("  - Keep all software and dependencies updated")
        recommendations.append("  - Follow secure coding practices")
        recommendations.append("  - Implement defense in depth strategies")
        recommendations.append("")
        
        recommendations.append("=" * 80)
        
        return "\n".join(recommendations)
    
    def generate_full_report(self, chain: AttackChain, include_diagram: bool = True) -> str:
        """
        Generate a complete report with all sections.
        
        Args:
            chain: The AttackChain to document
            include_diagram: Whether to include Mermaid diagram
            
        Returns:
            Complete report as formatted string
        """
        report = []
        
        # Title Page
        report.append("=" * 80)
        report.append("ATTACK CHAIN SECURITY REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Title: {chain.title}")
        report.append(f"Report Date: {self.report_date}")
        report.append(f"Severity: {chain.severity}")
        report.append(f"Impact: {chain.impact.value}")
        report.append("")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append(self.generate_executive_summary(chain))
        report.append("")
        report.append("")
        
        # Technical Report
        report.append(self.generate_technical_report(chain))
        report.append("")
        report.append("")
        
        # Visual Diagram
        if include_diagram:
            report.append("=" * 80)
            report.append("ATTACK CHAIN VISUALIZATION")
            report.append("=" * 80)
            report.append("")
            report.append(generate_mermaid_diagram(chain))
            report.append("")
            report.append("")
        
        # Recommendations
        report.append(self.generate_recommendations(chain))
        report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_to_markdown(self, chain: AttackChain, output_file: str, 
                          include_diagram: bool = True):
        """
        Export report to Markdown file.
        
        Args:
            chain: The AttackChain to export
            output_file: Path to output file
            include_diagram: Whether to include Mermaid diagram
        """
        report = self.generate_full_report(chain, include_diagram)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report exported to: {output_file}")
    
    def export_to_html(self, chain: AttackChain, output_file: str):
        """
        Export report to HTML file.
        
        Args:
            chain: The AttackChain to export
            output_file: Path to output file
        """
        # Convert markdown report to HTML
        markdown_report = generate_markdown_report(chain)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{chain.title} - Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #777; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .severity-critical {{ color: #d32f2f; font-weight: bold; }}
        .severity-high {{ color: #f57c00; font-weight: bold; }}
        .severity-medium {{ color: #fbc02d; font-weight: bold; }}
        .severity-low {{ color: #388e3c; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>{chain.title}</h1>
    <p><strong>Severity:</strong> <span class="severity-{chain.severity.lower()}">{chain.severity}</span></p>
    <p><strong>Impact:</strong> {chain.impact.value}</p>
    <p><strong>Report Date:</strong> {self.report_date}</p>
    <hr>
    <div id="content">
        {markdown_report.replace(chr(10), '<br>')}
    </div>
</body>
</html>"""
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML report exported to: {output_file}")


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
    
    # Create example chain
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Example Attack Chain",
        description="An example attack chain for testing report generation",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR in admin panel", 
                     prerequisites=["XSS stored"], outcome="Admin access")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    # Generate reports
    generator = ReportGenerator()
    
    print("=" * 80)
    print("EXECUTIVE SUMMARY")
    print("=" * 80)
    print(generator.generate_executive_summary(chain))
    print()
    
    print("=" * 80)
    print("FULL REPORT")
    print("=" * 80)
    print(generator.generate_full_report(chain))
    
    # Export
    generator.export_to_markdown(chain, "example_report.md")
    print("\nExample report exported to: example_report.md")

