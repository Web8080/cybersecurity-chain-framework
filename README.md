# Attack Chain Analyzer

> **Automation finds bugs, humans find chains, business logic requires context**

A security testing framework focused on **Attack Chain Analysis** - human-driven exploration of complex multi-step attack scenarios that automated tools miss.

**Author:** Victor Ibhafidon

## Core Philosophy

- **Automation finds bugs** - Automated tools excel at discovering common vulnerabilities
- **Humans find chains** - Security researchers identify multi-step exploits and complex attack vectors
- **Business logic requires context** - Understanding workflows is essential for finding logic flaws

## Primary Focus: Attack Chain Analysis

The framework provides interactive tools for building, validating, and visualizing attack chains:

- **Chain Builder** - `chains/chain_analyzer.py` for constructing multi-step attack scenarios
- **Visualization** - `chains/visualizer.py` for generating diagrams and reports
- **Validation** - Automatic validation of chain logic and prerequisites
- **Templates** - Common attack chain patterns and examples

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Create your first attack chain
python chains/chain_analyzer.py

# View documentation
cat docs/QUICK_START.md
```

## Documentation

All documentation is in the `docs/` folder:

- **Getting Started:** `docs/QUICK_START.md`
- **Chain Analysis Guide:** `docs/chains/README.md`
- **Target Setup:** `docs/targets/README.md`
- **Agile Workflow:** `docs/agile/WORKFLOW.md`
- **Full Index:** `docs/DOCUMENTATION_INDEX.md`

## Pentesting Targets

Ready-to-test targets for practicing attack chain analysis:

- **Web Apps:** OWASP Juice Shop, DVWA, bWAPP, WebGoat
- **IoT/Hardware:** IoTGoat, DVRF
- **Robotics:** Mobile app analysis, ROS security, Cloud APIs

See `docs/targets/README.md` for setup instructions.

## Project Structure

```
.
├── chains/          # Attack chain analysis tools
├── targets/         # Pentesting targets and setup scripts
├── automation/      # Automated testing tools
├── business-logic/  # Business logic analysis
├── agile/           # Agile methodology tools
└── docs/            # All documentation
```

## Contributing

This framework is designed for security researchers, pentesters, and bug bounty hunters who want to systematically document and analyze complex attack scenarios.

## License

MIT License - See LICENSE file for details

---

**Built for finding the chains that automation misses.**
