# Quick Start Guide

Get started with the Attack Chain Analysis framework in 5 minutes!

## Step 1: Choose a Target (30 seconds)

**Recommended:** OWASP Juice Shop (best for beginners)

```bash
cd targets/juice-shop
bash setup.sh
```

Access at: http://localhost:3000

**Other Options:**
- DVWA: `bash targets/dvwa/setup.sh` → http://localhost:8080
- bWAPP: `bash targets/bwapp/setup.sh` → http://localhost
- WebGoat: `bash targets/webgoat/setup.sh` → http://localhost:8080/WebGoat

## Step 2: Discover Vulnerabilities (2 minutes)

```bash
# For Juice Shop
python3 targets/juice-shop/discover_chains.py
```

This gives you a checklist of things to test.

## Step 3: Build Your First Chain (2 minutes)

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

# Create a chain
chain = analyzer.create_chain(
    title="My First Chain",
    description="What I discovered",
    impact=ImpactLevel.HIGH
)

# Add a step
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="Found XSS in search field",
    endpoint="/api/search",
    outcome="XSS payload executed"
)

chain.add_step(step1)

# Validate
is_valid, issues = chain.validate_chain()
print(chain.get_chain_summary())
```

## Step 4: Generate a Report (30 seconds)

```python
# Text report
print(analyzer.generate_report())

# Markdown with diagrams
from chains.visualizer import generate_markdown_report
print(generate_markdown_report(chain))

# Export to JSON
analyzer.export_chain(chain, "my_finding.json")
```

## That's It! 🎉

You've created your first attack chain. Now:

1. **Find more vulnerabilities** - Build longer chains
2. **Review examples** - Check `targets/*/example_chain.py`
3. **Use templates** - See `chains/chain_templates/`
4. **Read the workflow** - `chains/workflow.md` for methodology

## Next Steps

- **Learn the methodology:** `chains/workflow.md`
- **See all targets:** `targets/COMPREHENSIVE_GUIDE.md`
- **Full documentation:** `DOCUMENTATION_INDEX.md`

## Need Help?

- Quick Start: `chains/QUICKSTART.md`
- Getting Started: `targets/GETTING_STARTED.md`
- Examples: `targets/juice-shop/example_chain.py`

Happy hunting! 🎯


