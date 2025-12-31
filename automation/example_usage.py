#!/usr/bin/env python3
"""
Example Usage of ZAP Integration
Author: Victor Ibhafidon

Demonstrates how to use the ZAP integration for automated scanning.
"""

from automation.zap_integration import ZAPScanner


def example_scan():
    """Example of scanning a target with ZAP"""
    
    # Initialize scanner
    scanner = ZAPScanner("http://localhost:8080")
    
    # Check if ZAP is running
    if not scanner.check_connection():
        print("ZAP is not running. Please start ZAP first.")
        print("Docker: docker run -d -p 8080:8080 owasp/zap2docker-stable")
        return
    
    # Scan a target
    target_url = "http://localhost:3000"  # Example: Juice Shop
    
    print(f"Scanning {target_url}...")
    alerts = scanner.scan_target(target_url, spider=True, active_scan=True)
    
    # Generate report
    report = scanner.generate_findings_report(alerts)
    print("\n" + report)
    
    # Get chain suggestions
    suggestions = scanner.suggest_chains(alerts)
    if suggestions:
        print("\nSuggested Attack Chains:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
    
    # Convert alerts to framework findings
    for alert in alerts[:5]:  # Convert first 5
        scanner.convert_alert_to_finding(alert)
    
    # Show framework findings
    print(f"\nTotal findings in framework: {len(scanner.framework.findings)}")


if __name__ == "__main__":
    example_scan()

