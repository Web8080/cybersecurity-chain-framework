# Attack Chain Analysis - Quick Start Guide

## Getting Started

### 1. Basic Usage

```python
from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel

# Create analyzer
analyzer = ChainAnalyzer()

# Create a new chain
chain = analyzer.create_chain(
    title="My Attack Chain",
    description="Description of the attack",
    impact=ImpactLevel.HIGH
)

# Add steps
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="XSS vulnerability in user input",
    endpoint="/api/user/profile",
    outcome="XSS payload stored"
)

step2 = ChainStep(
    step_number=2,
    vulnerability_type=VulnerabilityType.SESSION_HIJACKING,
    description="Session stolen via XSS",
    prerequisites=["XSS payload stored"],  # Must match step1.outcome
    outcome="Session credentials obtained"
)

chain.add_step(step1)
chain.add_step(step2)

# Validate
is_valid, issues = chain.validate_chain()
print(chain.get_chain_summary())
```

### 2. Generate Reports

```python
# Generate text report
report = analyzer.generate_report()
print(report)

# Export to JSON
analyzer.export_chain(chain, "my_chain.json")

# Import from JSON
imported_chain = analyzer.import_chain("my_chain.json")
```

### 3. Visualize Chains

```python
from chains.visualizer import generate_text_diagram, generate_markdown_report

# Text diagram
print(generate_text_diagram(chain))

# Markdown report with Mermaid diagram
print(generate_markdown_report(chain))
```

### 4. Search and Filter

```python
# Find chains by vulnerability type
xss_chains = analyzer.find_chains_by_vulnerability(VulnerabilityType.XSS)

# Find chains by tag
web_chains = analyzer.find_chains_by_tag("web")

# Validate all chains
validation_results = analyzer.validate_all_chains()
```

## Command Line Usage

### Run Example

```bash
cd /Users/user/Cybersecurity
python3 chains/chain_analyzer.py
```

### Interactive Analysis

Create a Python script:

```python
#!/usr/bin/env python3
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

# Build your chain here
# ... (see examples above)

# Generate report
print(analyzer.generate_report())
```

## Workflow

1. **Discover vulnerabilities** - Use automated tools and manual testing
2. **Identify relationships** - Find how vulnerabilities can chain together
3. **Build the chain** - Use `chain_analyzer.py` to document the chain
4. **Validate** - Ensure prerequisites are met and chain is logical
5. **Visualize** - Generate diagrams and reports
6. **Document** - Use `chain_documentation.md` template for detailed write-up

## Tips

- **Prerequisites must match outcomes** - Step 2's prerequisites should match Step 1's outcome text exactly
- **Use tags** - Tag chains for easy filtering (e.g., "web", "api", "auth")
- **Document context** - Always include context about the application/environment
- **Test end-to-end** - Validate the complete chain, not just individual steps
- **Review templates** - Check `chain_templates/` for common patterns

## Next Steps

- Read `workflow.md` for detailed methodology
- Review `chain_templates/` for example patterns
- Use `chain_documentation.md` template for formal documentation
- Explore `visualizer.py` for advanced visualization options


