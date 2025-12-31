#!/usr/bin/env python3
"""
Interactive Chain Diagram Viewer
Author: Victor Ibhafidon

WHAT IT DOES:
- Creates interactive web-based chain diagrams
- Supports expand/collapse functionality for steps
- Provides hover details for each step
- Exports diagrams as images (PNG/SVG)
- Generates standalone HTML viewer

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py for chain data
- Integrates with visualizer.py for Mermaid diagrams
- Outputs interactive HTML files to docs/exports/
- Can be embedded in reports or viewed standalone

USAGE:
    from chains.interactive_diagram import InteractiveDiagram
    
    diagram = InteractiveDiagram()
    html_file = diagram.generate_interactive_viewer(chain, "diagram.html")
    diagram.export_as_image(chain, "diagram.png")
"""

import sys
import os
import json
from typing import Optional, List
from datetime import datetime

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chains.chain_analyzer import AttackChain, ChainStep, VulnerabilityType, ImpactLevel
from chains.visualizer import generate_mermaid_diagram


class InteractiveDiagram:
    """Creates interactive chain diagrams"""
    
    def __init__(self):
        """Initialize the diagram generator"""
        self.output_dir = os.path.join(
            os.path.dirname(__file__), '..', 'docs', 'exports'
        )
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_interactive_viewer(
        self, 
        chain: AttackChain, 
        output_file: Optional[str] = None
    ) -> str:
        """
        Generate interactive HTML viewer for attack chain
        
        Args:
            chain: AttackChain to visualize
            output_file: Output HTML file path (optional)
        
        Returns:
            Path to generated HTML file
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in chain.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = os.path.join(
                self.output_dir, 
                f"{safe_title}_interactive_{timestamp}.html"
            )
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Prepare step data for JavaScript
        steps_data = []
        for step in chain.steps:
            step_data = {
                "number": step.step_number,
                "vulnerability": step.vulnerability_type.value,
                "description": step.description,
                "endpoint": step.endpoint or "",
                "payload": step.payload or "",
                "prerequisites": step.prerequisites,
                "outcome": step.outcome or "",
                "evidence": step.evidence or ""
            }
            steps_data.append(step_data)
        
        # Generate Mermaid diagram
        mermaid_diagram = generate_mermaid_diagram(chain)
        
        # Create HTML with interactive features
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chain.title} - Interactive Chain Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .metadata {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .header .badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 0;
        }}
        
        .diagram-section {{
            padding: 30px;
            background: #f8f9fa;
            min-height: 600px;
        }}
        
        .diagram-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}
        
        .steps-panel {{
            background: white;
            padding: 30px;
            overflow-y: auto;
            max-height: calc(100vh - 200px);
        }}
        
        .step-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .step-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .step-card.expanded {{
            background: #e9ecef;
        }}
        
        .step-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .step-number {{
            background: #667eea;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .step-vulnerability {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.1em;
        }}
        
        .step-description {{
            color: #555;
            margin: 10px 0;
            line-height: 1.6;
        }}
        
        .step-details {{
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }}
        
        .step-details.expanded {{
            display: block;
        }}
        
        .detail-item {{
            margin: 10px 0;
        }}
        
        .detail-label {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .detail-value {{
            color: #666;
            font-family: 'Courier New', monospace;
            background: #f1f3f5;
            padding: 8px;
            border-radius: 4px;
            word-break: break-all;
        }}
        
        .prerequisites-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .prerequisites-list li {{
            padding: 5px 0;
            color: #666;
        }}
        
        .prerequisites-list li:before {{
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
            margin-right: 5px;
        }}
        
        .toggle-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }}
        
        .toggle-btn:hover {{
            background: #5568d3;
        }}
        
        .impact-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .impact-critical {{ background: #dc3545; color: white; }}
        .impact-high {{ background: #fd7e14; color: white; }}
        .impact-medium {{ background: #ffc107; color: #333; }}
        .impact-low {{ background: #28a745; color: white; }}
        
        @media (max-width: 1024px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{chain.title}</h1>
            <div class="metadata">
                <span class="badge">Impact: <span class="impact-{chain.impact.value.lower()}">{chain.impact.value}</span></span>
                <span class="badge">Severity: {chain.severity}</span>
                <span class="badge">Steps: {len(chain.steps)}</span>
            </div>
        </div>
        
        <div class="content">
            <div class="diagram-section">
                <h2 style="margin-bottom: 20px; color: #333;">Attack Chain Flow</h2>
                <div class="diagram-container">
                    <div class="mermaid">
{mermaid_diagram}
                    </div>
                </div>
            </div>
            
            <div class="steps-panel">
                <h2 style="margin-bottom: 20px; color: #333;">Chain Steps</h2>
                <div id="steps-container">
                    {self._generate_step_cards_html(steps_data)}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Initialize Mermaid
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        
        // Step data for tooltips and interactions
        const stepsData = {json.dumps(steps_data)};
        
        // Toggle step expansion
        document.querySelectorAll('.step-card').forEach((card, index) => {{
            card.addEventListener('click', function() {{
                const details = this.querySelector('.step-details');
                const isExpanded = this.classList.contains('expanded');
                
                if (isExpanded) {{
                    this.classList.remove('expanded');
                    details.classList.remove('expanded');
                }} else {{
                    this.classList.add('expanded');
                    details.classList.add('expanded');
                }}
            }});
        }});
        
        // Highlight step on diagram hover (if Mermaid supports it)
        document.querySelectorAll('.step-card').forEach((card, index) => {{
            card.addEventListener('mouseenter', function() {{
                this.style.borderLeftColor = '#764ba2';
            }});
            
            card.addEventListener('mouseleave', function() {{
                this.style.borderLeftColor = '#667eea';
            }});
        }});
    </script>
</body>
</html>"""
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Interactive diagram exported to: {output_file}")
        return output_file
    
    def _generate_step_cards_html(self, steps_data: List[dict]) -> str:
        """Generate HTML for step cards"""
        cards_html = []
        
        for step in steps_data:
            card_html = f"""
            <div class="step-card">
                <div class="step-header">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div class="step-number">{step['number']}</div>
                        <div class="step-vulnerability">{step['vulnerability']}</div>
                    </div>
                    <button class="toggle-btn" onclick="event.stopPropagation(); this.parentElement.parentElement.click();">
                        Details
                    </button>
                </div>
                <div class="step-description">{step['description']}</div>
                <div class="step-details">
                    {self._generate_step_details_html(step)}
                </div>
            </div>
            """
            cards_html.append(card_html)
        
        return "\n".join(cards_html)
    
    def _generate_step_details_html(self, step: dict) -> str:
        """Generate HTML for step details"""
        details = []
        
        if step['endpoint']:
            details.append(f"""
            <div class="detail-item">
                <div class="detail-label">Endpoint:</div>
                <div class="detail-value">{step['endpoint']}</div>
            </div>
            """)
        
        if step['payload']:
            details.append(f"""
            <div class="detail-item">
                <div class="detail-label">Payload:</div>
                <div class="detail-value">{step['payload']}</div>
            </div>
            """)
        
        if step['prerequisites']:
            prereqs_html = "".join([f"<li>{prereq}</li>" for prereq in step['prerequisites']])
            details.append(f"""
            <div class="detail-item">
                <div class="detail-label">Prerequisites:</div>
                <ul class="prerequisites-list">{prereqs_html}</ul>
            </div>
            """)
        
        if step['outcome']:
            details.append(f"""
            <div class="detail-item">
                <div class="detail-label">Outcome:</div>
                <div class="detail-value">{step['outcome']}</div>
            </div>
            """)
        
        if step['evidence']:
            details.append(f"""
            <div class="detail-item">
                <div class="detail-label">Evidence:</div>
                <div class="detail-value">{step['evidence']}</div>
            </div>
            """)
        
        return "\n".join(details)
    
    def export_as_image(
        self, 
        chain: AttackChain, 
        output_file: Optional[str] = None,
        format: str = "png"
    ) -> str:
        """
        Export diagram as image (PNG or SVG)
        
        Note: This requires additional setup (headless browser or image library)
        For now, generates HTML that can be manually converted to image
        
        Args:
            chain: AttackChain to export
            output_file: Output file path (optional)
            format: Image format ("png" or "svg")
        
        Returns:
            Path to exported image or HTML file
        """
        # For now, generate HTML that can be converted to image
        # In production, could use playwright/selenium to render and screenshot
        html_file = self.generate_interactive_viewer(chain)
        
        print(f"Note: Image export requires manual conversion or headless browser setup.")
        print(f"HTML file generated: {html_file}")
        print(f"To convert to image, use a tool like:")
        print(f"  - wkhtmltopdf (for PDF)")
        print(f"  - Playwright (for PNG)")
        print(f"  - Puppeteer (for PNG)")
        
        return html_file


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
    
    # Create example chain
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="XSS to Admin Takeover",
        description="A multi-step attack chain demonstrating XSS leading to admin access",
        impact=ImpactLevel.CRITICAL
    )
    
    step1 = ChainStep(
        1, VulnerabilityType.XSS,
        "Stored XSS in user profile bio field",
        endpoint="/profile",
        payload="<script>alert('XSS')</script>",
        outcome="XSS payload stored"
    )
    step2 = ChainStep(
        2, VulnerabilityType.SESSION_HIJACKING,
        "Admin views user profile, XSS executes in admin context",
        endpoint="/admin/users",
        prerequisites=["XSS payload stored"],
        outcome="Admin session token stolen"
    )
    step3 = ChainStep(
        3, VulnerabilityType.PRIV_ESCALATION,
        "Use stolen admin session token to access admin panel",
        endpoint="/admin/dashboard",
        prerequisites=["Admin session token stolen"],
        outcome="Full admin access"
    )
    
    chain.add_step(step1)
    chain.add_step(step2)
    chain.add_step(step3)
    
    # Generate interactive diagram
    diagram = InteractiveDiagram()
    print("=" * 80)
    print("GENERATING INTERACTIVE DIAGRAM")
    print("=" * 80)
    print()
    
    html_file = diagram.generate_interactive_viewer(chain)
    print(f"\nOpen {html_file} in a web browser to view the interactive diagram.")

