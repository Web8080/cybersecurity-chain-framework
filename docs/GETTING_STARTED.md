# Getting Started with Real Targets

This guide will help you set up and start pentesting real targets using the Attack Chain Analysis framework.

## Quick Start: OWASP Juice Shop (Recommended)

### Step 1: Start the Target

```bash
# Navigate to targets directory
cd targets/juice-shop

# Run setup script
bash setup.sh
```

Or manually with Docker:
```bash
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
```

### Step 2: Verify It's Running

```bash
# Check status
python3 ../target_manager.py

# Or visit in browser
open http://localhost:3000
```

### Step 3: Start Discovering Vulnerabilities

```bash
# Run discovery helper
python3 juice-shop/discover_chains.py
```

This will give you a checklist of things to test.

### Step 4: Document Your Findings

As you discover vulnerabilities, use the chain analyzer:

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

# Create your chain
chain = analyzer.create_chain(
 title="My Discovered Chain",
 description="What I found",
 impact=ImpactLevel.HIGH
)

# Add steps as you discover them
# ... (see examples)
```

### Step 5: Generate Reports

```python
# Generate report
print(analyzer.generate_report())

# Export to JSON
analyzer.export_chain(chain, "my_finding.json")

# Generate markdown
from chains.visualizer import generate_markdown_report
print(generate_markdown_report(chain))
```

## Other Targets

### DVWA (Damn Vulnerable Web Application)

```bash
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
# Access at http://localhost:8080
# Default: admin/password
```

### bWAPP

```bash
docker run -d --name bwapp -p 80:80 raesene/bwapp
# Access at http://localhost
```

## Hardware/IoT Targets

### IoTGoat

1. Download from: https://github.com/OWASP/IoTGoat
2. Follow setup instructions
3. Apply same chain analysis methodology

## Workflow

1. **Start Target** → Use setup scripts or Docker
2. **Reconnaissance** → Map the application, find endpoints
3. **Discover Bugs** → Use automated tools + manual testing
4. **Find Relationships** → Identify how bugs can chain
5. **Build Chains** → Use `chain_analyzer.py` to document
6. **Validate** → Test the complete chain end-to-end
7. **Document** → Generate reports and visualizations

## Tips

- **Start Simple** → Find individual bugs first
- **Think Chains** → Always ask "what can this enable?"
- **Document Early** → Use the framework as you discover
- **Test End-to-End** → Validate complete chains
- **Review Examples** → Check `juice-shop/example_chain.py`

## Resources

- **Juice Shop Docs:** https://pwning.owasp-juice.shop/
- **Juice Shop Scoreboard:** Find it in the app!
- **Chain Templates:** `chains/chain_templates/`
- **Workflow Guide:** `chains/workflow.md`

## Next Steps

1. Set up Juice Shop
2. Run discovery helper
3. Start finding vulnerabilities
4. Build your first attack chain
5. Document and share findings

Happy hunting! 
