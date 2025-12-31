# Automation Module

Automated vulnerability discovery tools.

## OWASP ZAP Integration

The `zap_integration.py` module provides automated vulnerability scanning using OWASP ZAP.

### Setup

1. Install OWASP ZAP:
   ```bash
   # Using Docker (recommended)
   docker run -d -p 8080:8080 owasp/zap2docker-stable
   
   # Or download from https://www.zaproxy.org/
   ```

2. Install Python dependencies:
   ```bash
   pip install requests
   ```

### Usage

```python
from automation.zap_integration import ZAPScanner

# Initialize scanner
scanner = ZAPScanner("http://localhost:8080")

# Check connection
if scanner.check_connection():
    # Scan a target
    alerts = scanner.scan_target("http://target.com")
    
    # Generate report
    report = scanner.generate_findings_report(alerts)
    print(report)
    
    # Get chain suggestions
    suggestions = scanner.suggest_chains(alerts)
    for suggestion in suggestions:
        print(f"- {suggestion}")
```

### Features

- Spider scanning for page discovery
- Active vulnerability scanning
- Alert retrieval and categorization
- Automatic finding conversion to framework format
- Attack chain suggestions based on findings

### Integration

- Uses `framework.py` to store automated findings
- Integrates with `chain_analyzer.py` for chain suggestions
- Works with `target_manager.py` for target management


