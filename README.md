# Attack Chain Analyzer Framework

**Author:** Victor Ibhafidon

A comprehensive framework for analyzing, documenting, and visualizing multi-step cybersecurity attack chains. This framework helps security researchers and pentesters identify, validate, and report on complex attack scenarios across various targets.

## Overview

The Attack Chain Analyzer Framework provides tools for:
- **Chain Creation**: Build multi-step attack chains with validation
- **Chain Comparison**: Compare similar chains to identify patterns
- **Target Analysis**: Pre-built templates for common pentesting targets
- **Automated Discovery**: Integration with OWASP ZAP for vulnerability scanning
- **Report Generation**: Export chains to PDF, HTML, Word, and interactive diagrams
- **Visualization**: Interactive web-based chain diagrams with expand/collapse

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Web8080/cybersecurity-chain-framework.git
cd cybersecurity-chain-framework

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel

# Create an analyzer
analyzer = ChainAnalyzer()

# Create a chain
chain = analyzer.create_chain(
    title="XSS to Admin Takeover",
    description="Multi-step attack chain",
    impact=ImpactLevel.CRITICAL
)

# Add steps
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="Stored XSS in user profile",
    endpoint="/profile",
    payload="<script>alert('XSS')</script>",
    outcome="XSS payload stored"
)

chain.add_step(step1)

# Validate
is_valid, issues = chain.validate_chain()
if is_valid:
    print("Chain is valid!")
    
# Export
analyzer.export_chain(chain, "my_chain.json")
```

## Features

### Core Features

- **Chain Validation**: Comprehensive validation with detailed error messages
- **Chain Comparison**: Side-by-side comparison with similarity scoring
- **Target Templates**: Pre-built chains for Juice Shop, DVWA, bWAPP, IoTGoat, and Robotics
- **Multi-Format Export**: PDF, HTML, Word/DOCX, and JSON
- **Interactive Diagrams**: Web-based viewer with expand/collapse functionality
- **Automated Discovery**: OWASP ZAP integration for vulnerability scanning

### Target Support

- **Web Applications**: OWASP Juice Shop, DVWA, bWAPP, WebGoat
- **IoT/Hardware**: IoTGoat, DVRF
- **Robotics**: DJI GO 4, iRobot Home, ROS testing

## Project Structure

```
.
├── chains/              # Core framework modules
│   ├── chain_analyzer.py      # Main chain analysis engine
│   ├── chain_comparator.py    # Chain comparison tool
│   ├── export_formats.py      # Multi-format export
│   ├── interactive_diagram.py # Interactive diagram viewer
│   ├── report_generator.py    # Report generation
│   └── visualizer.py          # Visualization tools
├── targets/             # Target-specific analysis
│   ├── juice-shop/      # OWASP Juice Shop chains
│   ├── dvwa/           # DVWA chains
│   ├── bwapp/          # bWAPP chains
│   ├── iotgoat/        # IoTGoat chains
│   └── robotics/        # Robotics security chains
├── automation/          # Automated discovery tools
│   └── zap_integration.py    # OWASP ZAP integration
├── docs/               # Documentation
│   ├── GETTING_STARTED.md
│   ├── PENTEST_GUIDE.md
│   └── exports/        # Generated reports and diagrams
└── agile/              # Agile project management
    └── sprints/        # Sprint tracking
```

## Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Quick start guide
- **[Pentest Guide](docs/PENTEST_GUIDE.md)** - Comprehensive pentesting guide
- **[Documentation Index](docs/DOCUMENTATION_INDEX.md)** - Full documentation index

## Examples

### Compare Two Chains

```python
from chains.chain_comparator import ChainComparator

comparator = ChainComparator()
comparison = comparator.compare_chains(chain1, chain2)
print(comparator.generate_report(comparison))
```

### Export to Multiple Formats

```python
from chains.export_formats import MultiFormatExporter

exporter = MultiFormatExporter()
results = exporter.export_all_formats(chain)
# Exports to PDF, HTML, and Word
```

### Generate Interactive Diagram

```python
from chains.interactive_diagram import InteractiveDiagram

diagram = InteractiveDiagram()
html_file = diagram.generate_interactive_viewer(chain)
# Opens in web browser
```

## Requirements

- Python 3.9+
- See `requirements.txt` for full dependency list

### Optional Dependencies

- `reportlab` - For PDF export
- `python-docx` - For Word export
- `python-owasp-zap-v2.4` - For ZAP integration

## Contributing

This is a research and educational framework. Contributions welcome!

## License

See [LICENSE](LICENSE) file for details.

## Author

**Victor Ibhafidon**

## Status

- **Sprint 1**: ✅ Complete (21/21 points)
- **Sprint 2**: ✅ Complete (21/21 points)

## Repository

https://github.com/Web8080/cybersecurity-chain-framework
