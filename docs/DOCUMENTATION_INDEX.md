# Complete Documentation Index

This document provides a comprehensive index of all documentation in the Cybersecurity framework.

## Core Framework

### Main Documentation
- **README.md** - Framework overview and philosophy
- **DOCUMENTATION_INDEX.md** (this file) - Complete documentation index
- **QUICK_START.md** - 5-minute getting started guide

### Agile Methodology
- **agile/README.md** - Agile framework overview
- **agile/WORKFLOW.md** - Complete Agile workflow guide
- **agile/QUICK_START.md** - Agile quick start
- **agile/product_backlog.md** - All features and stories
- **agile/sprints/sprint_001.md** - Current sprint
- **agile/tools/** - Sprint and backlog management tools

### Attack Chain Analysis (Primary Focus)
- **chains/README.md** - Attack chain analysis overview
- **chains/QUICKSTART.md** - Quick start guide for chain analysis
- **chains/workflow.md** - Step-by-step methodology
- **chains/chain_documentation.md** - Template for documenting chains
- **chains/chain_templates/** - Common attack chain patterns
  - `xss_to_account_takeover.md` - XSS chain example
  - `idor_privilege_escalation.md` - IDOR chain example

### Tools
- **chains/chain_analyzer.py** - Main chain analysis tool
- **chains/visualizer.py** - Visualization and reporting
- **framework.py** - Core framework classes

---

## Pentesting Targets

### Overview
- **targets/README.md** - Targets overview and recommendations
- **targets/GETTING_STARTED.md** - Quick start guide
- **targets/COMPREHENSIVE_GUIDE.md** - Complete targets guide
- **targets/target_manager.py** - Target management tool

### Web Applications

#### OWASP Juice Shop ⭐ RECOMMENDED
- **targets/juice-shop/README.md** - Juice Shop documentation
- **targets/juice-shop/setup.sh** - Quick setup script
- **targets/juice-shop/discover_chains.py** - Discovery helper
- **targets/juice-shop/example_chain.py** - Example chains

#### DVWA
- **targets/dvwa/setup.sh** - Setup script
- Access: http://localhost:8080 (admin/password)

#### bWAPP
- **targets/bwapp/setup.sh** - Setup script
- Access: http://localhost (bee/bug)

#### WebGoat
- **targets/webgoat/setup.sh** - Setup script
- Access: http://localhost:8080/WebGoat

### Hardware/IoT

#### IoTGoat ⭐ RECOMMENDED FOR HARDWARE
- **targets/iotgoat/README.md** - IoTGoat documentation
- **targets/iotgoat/setup.sh** - Setup guide
- GitHub: https://github.com/OWASP/IoTGoat

### Robotics

#### Robotics Security Research
- **targets/robotics/README.md** - Robotics security methodology
- **targets/robotics/example_chains.py** - Example robot attack chains
- Includes: ROS security, cloud APIs, controller exploitation

---

## Quick Reference

### Getting Started
1. **New to the framework?** → `chains/QUICKSTART.md`
2. **Want to start pentesting?** → `targets/GETTING_STARTED.md`
3. **Need methodology?** → `chains/workflow.md`

### Common Tasks

#### Setting Up a Target
```bash
# Juice Shop (recommended)
bash targets/juice-shop/setup.sh

# DVWA
bash targets/dvwa/setup.sh

# bWAPP
bash targets/bwapp/setup.sh

# WebGoat
bash targets/webgoat/setup.sh
```

#### Creating an Attack Chain
```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()
chain = analyzer.create_chain(
    title="My Chain",
    description="Description",
    impact=ImpactLevel.HIGH
)
# Add steps...
```

#### Generating Reports
```python
# Text report
print(analyzer.generate_report())

# Markdown with diagrams
from chains.visualizer import generate_markdown_report
print(generate_markdown_report(chain))
```

#### Managing Targets
```bash
# Check status
python3 targets/target_manager.py

# Start target
python3 targets/target_manager.py --start juice-shop
```

---

## Framework Philosophy

### Core Principles
1. **Automation finds bugs** - Tools discover individual vulnerabilities
2. **Humans find chains** - Researchers identify multi-step attacks
3. **Business logic requires context** - Understanding workflows is essential

### Focus Area
- **Attack Chain Analysis** - Primary focus of this framework
- Human-driven exploration of complex attack scenarios
- Multi-step vulnerability chaining
- Context-aware security testing

---

## Directory Structure

```
Cybersecurity/
├── README.md                    # Main overview
├── DOCUMENTATION_INDEX.md       # This file
├── framework.py                 # Core framework
│
├── chains/                      # Attack Chain Analysis
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── workflow.md
│   ├── chain_analyzer.py       # Main tool
│   ├── visualizer.py           # Visualization
│   ├── chain_documentation.md  # Template
│   └── chain_templates/        # Examples
│
├── targets/                     # Pentesting Targets
│   ├── README.md
│   ├── GETTING_STARTED.md
│   ├── COMPREHENSIVE_GUIDE.md
│   ├── target_manager.py
│   │
│   ├── juice-shop/             # ⭐ Recommended
│   ├── dvwa/
│   ├── bwapp/
│   ├── webgoat/
│   ├── iotgoat/                # Hardware/IoT
│   └── robotics/               # Robotics research
│
├── automation/                  # Automated testing
└── business-logic/              # Business logic review
```

---

## Examples and Templates

### Chain Templates
- XSS to Account Takeover
- IDOR to Privilege Escalation
- (Add more in `chains/chain_templates/`)

### Target Examples
- Juice Shop: Price manipulation chain
- Juice Shop: XSS to admin takeover
- Robotics: Controller takeover
- Robotics: Cloud API exploitation
- Robotics: ROS security chain

---

## Tools Reference

### Chain Analyzer (`chains/chain_analyzer.py`)
- Create and manage attack chains
- Validate chain logic
- Search and filter chains
- Export/import JSON
- Generate reports

### Visualizer (`chains/visualizer.py`)
- Text diagrams
- Mermaid diagrams
- Markdown reports
- JSON export

### Target Manager (`targets/target_manager.py`)
- Check target status
- Start/stop targets
- List available targets
- Docker integration

---

## Learning Path

### Beginner
1. Read `chains/QUICKSTART.md`
2. Set up Juice Shop
3. Run `discover_chains.py`
4. Build your first chain
5. Review example chains

### Intermediate
1. Test multiple targets
2. Build complex chains
3. Use visualization tools
4. Document findings
5. Review templates

### Advanced
1. Hardware/IoT testing (IoTGoat)
2. Robotics research
3. Custom target analysis
4. Create new templates
5. Contribute findings

---

## Resources

### External
- **OWASP Juice Shop:** https://owasp.org/www-project-juice-shop/
- **OWASP IoTGoat:** https://github.com/OWASP/IoTGoat
- **DVWA:** https://github.com/digininja/DVWA
- **bWAPP:** http://www.itsecgames.com/
- **WebGoat:** https://owasp.org/www-project-webgoat/

### Internal
- Chain templates: `chains/chain_templates/`
- Example chains: `targets/*/example_chain.py`
- Discovery helpers: `targets/*/discover_chains.py`

---

## Support

### Questions?
1. Check `QUICKSTART.md` for basics
2. Review `workflow.md` for methodology
3. See examples in target directories
4. Review chain templates

### Contributing
- Document new chains
- Add new templates
- Create target examples
- Improve documentation

---

**Last Updated:** Framework v1.0 - Attack Chain Analysis Focus

