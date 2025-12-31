# Comprehensive Pentesting Targets Guide

This guide provides a complete overview of all available targets for practicing Attack Chain Analysis.

## Quick Reference

| Target | Type | Setup | Best For |
|--------|------|-------|----------|
| **OWASP Juice Shop** | Web | `bash targets/juice-shop/setup.sh` | Modern web apps, business logic, API chains |
| **DVWA** | Web | `bash targets/dvwa/setup.sh` | Learning fundamentals, OWASP Top 10 |
| **bWAPP** | Web | `bash targets/bwapp/setup.sh` | 100+ vulnerabilities, traditional web security |
| **WebGoat** | Web | `bash targets/webgoat/setup.sh` | Structured learning, guided lessons |
| **IoTGoat** | Hardware/IoT | See `targets/iotgoat/setup.sh` | Firmware analysis, embedded systems, hardware |
| **Robotics** | Hardware/Software | See `targets/robotics/README.md` | Robot security, ROS, cloud APIs |

## Web Applications

### 1. OWASP Juice Shop RECOMMENDED

**Why Start Here:**
- Modern, realistic e-commerce application
- 100+ vulnerabilities perfect for chaining
- Active development and community
- Built-in scoreboard for tracking progress

**Setup:**
```bash
cd targets/juice-shop
bash setup.sh
# Access at http://localhost:3000
```

**Perfect For:**
- Multi-step attack chains
- Business logic flaws
- API security testing
- Modern web application security

**Tools:**
- `discover_chains.py` - Vulnerability discovery checklist
- `example_chain.py` - Example attack chains

**Resources:**
- Official: https://owasp.org/www-project-juice-shop/
- Scoreboard: Built into the app (find it!)

---

### 2. DVWA (Damn Vulnerable Web Application)

**Why:**
- Classic, well-documented
- Adjustable difficulty levels
- Great for learning fundamentals
- Covers OWASP Top 10

**Setup:**
```bash
cd targets/dvwa
bash setup.sh
# Access at http://localhost:8080
# Default: admin/password
```

**Perfect For:**
- Learning web security basics
- Practicing common attack techniques
- Understanding vulnerability categories
- Building foundational knowledge

**Note:** Click "Create / Reset Database" on first visit

---

### 3. bWAPP (Buggy Web Application)

**Why:**
- 100+ vulnerabilities
- Great for comprehensive testing
- Covers wide range of vulnerabilities
- Educational focus

**Setup:**
```bash
cd targets/bwapp
bash setup.sh
# Access at http://localhost
# Default: bee/bug or admin/admin
```

**Perfect For:**
- Comprehensive vulnerability testing
- Traditional web vulnerabilities
- OWASP Top 10 practice
- Security awareness training

---

### 4. WebGoat

**Why:**
- OWASP-maintained
- Educational lessons with guidance
- Structured learning path
- Covers modern vulnerabilities

**Setup:**
```bash
cd targets/webgoat
bash setup.sh
# Access at http://localhost:8080/WebGoat
# Register a new account
```

**Perfect For:**
- Structured learning
- Guided scenarios
- Educational purposes
- Understanding attack techniques

---

## Hardware/IoT Targets

### 1. IoTGoat RECOMMENDED FOR HARDWARE

**Why:**
- OWASP project
- Intentionally vulnerable IoT firmware
- Real router firmware (not simulation)
- Perfect for hardware security

**Setup:**
```bash
cd targets/iotgoat
bash setup.sh
# Follow instructions for VM or build from source
```

**Perfect For:**
- Firmware analysis
- Hardware security
- IoT attack chains
- Embedded system security
- **Robotics** (similar architecture to robot controllers)

**Resources:**
- GitHub: https://github.com/OWASP/IoTGoat
- OWASP: https://owasp.org/www-project-iotgoat/

**Attack Chain Opportunities:**
- Firmware extraction → Credential discovery → Network access
- Default credentials → Command injection → Root access
- Weak encryption → Credential theft → API access

---

### 2. Damn Vulnerable Router Firmware (DVRF)

**Why:**
- Custom router firmware with vulnerabilities
- Good for firmware analysis practice
- Similar to real-world router security

**Setup:**
- Download from: https://github.com/praetorian-inc/DVRF
- Use QEMU or physical hardware

**Perfect For:**
- Router security
- Embedded systems
- Firmware analysis

---

## Robotics Platforms

### Overview

While real AI humanoid robots are expensive and typically not available for public pentesting, you can:

1. **Research Known Vulnerabilities**
 - CVE databases for robotics platforms
 - Security research papers
 - Manufacturer security advisories

2. **Analyze Robot Software/Firmware**
 - Robot Operating System (ROS) security
 - Robot control APIs
 - Cloud-based robot services
 - Mobile app security

3. **Apply IoT Methodologies**
 - Many robots use similar embedded systems
 - Use IoTGoat approaches
 - Firmware analysis techniques

**See:** `targets/robotics/README.md` for detailed methodology

**Example Chains:** `targets/robotics/example_chains.py`

---

## Using the Framework with Targets

### Workflow

1. **Choose a Target**
 ```bash
 # Check available targets
 python3 targets/target_manager.py
 ```

2. **Start the Target**
 ```bash
 # Use setup script
 bash targets/<target>/setup.sh
 
 # Or use target manager
 python3 targets/target_manager.py --start <target>
 ```

3. **Discover Vulnerabilities**
 - Automated tools (Burp Suite, OWASP ZAP)
 - Manual testing
 - Use discovery helpers (e.g., `juice-shop/discover_chains.py`)

4. **Build Attack Chains**
 ```python
 from chains.chain_analyzer import *
 
 analyzer = ChainAnalyzer()
 chain = analyzer.create_chain(...)
 # Add steps...
 ```

5. **Document and Report**
 ```python
 # Validate
 is_valid, issues = chain.validate_chain()
 
 # Export
 analyzer.export_chain(chain, "finding.json")
 
 # Generate report
 from chains.visualizer import generate_markdown_report
 print(generate_markdown_report(chain))
 ```

---

## Target Selection Guide

### For Beginners
1. **Start with:** OWASP Juice Shop
 - Modern, well-documented
 - Built-in hints and scoreboard
 - Great examples available

2. **Then try:** DVWA
 - Adjustable difficulty
 - Clear vulnerability categories
 - Good for fundamentals

### For Intermediate
1. **bWAPP** - Comprehensive testing
2. **WebGoat** - Structured learning
3. **Multiple targets** - Compare approaches

### For Advanced
1. **IoTGoat** - Hardware/firmware analysis
2. **Robotics research** - Complex systems
3. **Custom targets** - Real-world applications

---

## Integration with Chain Analyzer

All targets integrate with the Attack Chain Analysis framework:

```python
# Example: Juice Shop chain
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

chain = analyzer.create_chain(
 title="Price Manipulation Chain",
 description="Business logic flaws in Juice Shop",
 impact=ImpactLevel.HIGH
)

# Add steps...
chain.add_step(...)

# Validate and export
is_valid, issues = chain.validate_chain()
analyzer.export_chain(chain, "juice_shop_chain.json")
```

---

## Tips for Success

1. **Start Simple** - Find individual bugs first
2. **Think Chains** - Always ask "what can this enable?"
3. **Document Early** - Use the framework as you discover
4. **Test End-to-End** - Validate complete chains
5. **Review Examples** - Check example chains in each target directory
6. **Use Templates** - See `chains/chain_templates/` for patterns

---

## Resources

- **Chain Analyzer:** `chains/chain_analyzer.py`
- **Visualization:** `chains/visualizer.py`
- **Templates:** `chains/chain_templates/`
- **Workflow:** `chains/workflow.md`
- **Quick Start:** `targets/GETTING_STARTED.md`

---

## Next Steps

1. Choose a target
2. Set it up using the setup script
3. Start discovering vulnerabilities
4. Build your first attack chain
5. Document and share findings

Happy hunting! 

