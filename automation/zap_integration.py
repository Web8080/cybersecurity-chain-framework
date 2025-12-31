#!/usr/bin/env python3
"""
OWASP ZAP Integration - Automated Target Discovery
Author: Victor Ibhafidon

Integrates with OWASP ZAP for automated vulnerability discovery.

WHAT IT DOES:
- Connects to OWASP ZAP API
- Scans targets for vulnerabilities
- Generates vulnerability lists
- Converts findings to framework format
- Suggests potential attack chains

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses framework.py to store automated findings
- Integrates with chain_analyzer.py for chain suggestions
- Works with target_manager.py for target management
- Outputs findings compatible with attack chain creation

USAGE:
    from automation.zap_integration import ZAPScanner
    
    scanner = ZAPScanner("http://localhost:8080")
    vulnerabilities = scanner.scan_target("http://target.com")
    scanner.generate_findings_report(vulnerabilities)
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from framework import SecurityFramework, FindingType


class ZAPScanner:
    """
    OWASP ZAP API integration for automated vulnerability scanning.
    """
    
    def __init__(self, zap_url: str = "http://localhost:8080", api_key: Optional[str] = None):
        """
        Initialize ZAP scanner.
        
        Args:
            zap_url: ZAP API URL (default: http://localhost:8080)
            api_key: ZAP API key (optional, if ZAP requires authentication)
        """
        self.zap_url = zap_url.rstrip('/')
        self.api_key = api_key
        self.api_base = f"{self.zap_url}/JSON"
        self.framework = SecurityFramework()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a request to ZAP API.
        
        Args:
            endpoint: API endpoint (e.g., "core/view/version")
            params: Additional parameters
            
        Returns:
            API response as dictionary
        """
        url = f"{self.api_base}/{endpoint}/"
        
        request_params = {}
        if self.api_key:
            request_params['apikey'] = self.api_key
        if params:
            request_params.update(params)
        
        try:
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to ZAP: {e}")
            return {}
    
    def check_connection(self) -> bool:
        """
        Check if ZAP is accessible.
        
        Returns:
            True if ZAP is accessible, False otherwise
        """
        try:
            result = self._make_request("core/view/version")
            if result and 'version' in result:
                print(f"Connected to ZAP version: {result['version']}")
                return True
            return False
        except Exception as e:
            print(f"ZAP connection check failed: {e}")
            return False
    
    def spider_target(self, target_url: str, max_children: int = 10) -> str:
        """
        Spider a target URL to discover pages.
        
        Args:
            target_url: URL to spider
            max_children: Maximum number of children to crawl
            
        Returns:
            Spider scan ID
        """
        params = {
            'url': target_url,
            'maxChildren': max_children,
            'recurse': 'true'
        }
        
        result = self._make_request("spider/action/scan", params)
        if result and 'scan' in result:
            scan_id = result['scan']
            print(f"Spider scan started: {scan_id}")
            return scan_id
        return ""
    
    def wait_for_spider(self, scan_id: str, timeout: int = 300) -> bool:
        """
        Wait for spider scan to complete.
        
        Args:
            scan_id: Spider scan ID
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if scan completed, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self._make_request("spider/view/status", {'scanId': scan_id})
            if result and 'status' in result:
                status = int(result['status'])
                if status >= 100:
                    print("Spider scan completed")
                    return True
                print(f"Spider progress: {status}%")
            time.sleep(2)
        
        print("Spider scan timeout")
        return False
    
    def active_scan(self, target_url: str) -> str:
        """
        Start active scan on target URL.
        
        Args:
            target_url: URL to scan
            
        Returns:
            Active scan ID
        """
        params = {
            'url': target_url,
            'recurse': 'true'
        }
        
        result = self._make_request("ascan/action/scan", params)
        if result and 'scan' in result:
            scan_id = result['scan']
            print(f"Active scan started: {scan_id}")
            return scan_id
        return ""
    
    def wait_for_active_scan(self, scan_id: str, timeout: int = 600) -> bool:
        """
        Wait for active scan to complete.
        
        Args:
            scan_id: Active scan ID
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if scan completed, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self._make_request("ascan/view/status", {'scanId': scan_id})
            if result and 'status' in result:
                status = int(result['status'])
                if status >= 100:
                    print("Active scan completed")
                    return True
                print(f"Active scan progress: {status}%")
            time.sleep(5)
        
        print("Active scan timeout")
        return False
    
    def get_alerts(self, base_url: Optional[str] = None) -> List[Dict]:
        """
        Get alerts (vulnerabilities) from ZAP.
        
        Args:
            base_url: Filter alerts by base URL (optional)
            
        Returns:
            List of alert dictionaries
        """
        params = {}
        if base_url:
            params['baseurl'] = base_url
        
        result = self._make_request("core/view/alerts", params)
        if result and 'alerts' in result:
            return result['alerts']
        return []
    
    def scan_target(self, target_url: str, spider: bool = True, 
                   active_scan: bool = True) -> List[Dict]:
        """
        Complete scan workflow: spider + active scan.
        
        Args:
            target_url: URL to scan
            spider: Whether to run spider scan
            active_scan: Whether to run active scan
            
        Returns:
            List of discovered vulnerabilities
        """
        print(f"Starting scan of: {target_url}")
        
        # Step 1: Spider (if enabled)
        if spider:
            scan_id = self.spider_target(target_url)
            if scan_id:
                self.wait_for_spider(scan_id)
        
        # Step 2: Active Scan (if enabled)
        if active_scan:
            scan_id = self.active_scan(target_url)
            if scan_id:
                self.wait_for_active_scan(scan_id)
        
        # Step 3: Get alerts
        alerts = self.get_alerts(target_url)
        print(f"Found {len(alerts)} alerts")
        
        return alerts
    
    def convert_alert_to_finding(self, alert: Dict) -> None:
        """
        Convert ZAP alert to framework finding.
        
        Args:
            alert: ZAP alert dictionary
        """
        # Map ZAP risk levels to framework severity
        risk_map = {
            'High': 'High',
            'Medium': 'Medium',
            'Low': 'Low',
            'Informational': 'Low'
        }
        
        risk = alert.get('risk', 'Low')
        severity = risk_map.get(risk, 'Low')
        
        # Create finding
        self.framework.add_automated_bug(
            title=f"{alert.get('name', 'Unknown')} - {alert.get('url', '')}",
            description=alert.get('description', ''),
            severity=severity
        )
    
    def generate_findings_report(self, alerts: List[Dict]) -> str:
        """
        Generate a report of findings.
        
        Args:
            alerts: List of ZAP alerts
            
        Returns:
            Report as string
        """
        report = []
        report.append("=" * 80)
        report.append("AUTOMATED VULNERABILITY DISCOVERY REPORT")
        report.append("=" * 80)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Findings: {len(alerts)}")
        report.append("")
        
        # Group by risk level
        by_risk = {}
        for alert in alerts:
            risk = alert.get('risk', 'Unknown')
            if risk not in by_risk:
                by_risk[risk] = []
            by_risk[risk].append(alert)
        
        # Report by risk level
        for risk in ['High', 'Medium', 'Low', 'Informational']:
            if risk in by_risk:
                report.append(f"{risk} Risk Findings: {len(by_risk[risk])}")
                for alert in by_risk[risk][:5]:  # Show first 5
                    report.append(f"  - {alert.get('name', 'Unknown')}")
                    report.append(f"    URL: {alert.get('url', 'N/A')}")
                if len(by_risk[risk]) > 5:
                    report.append(f"  ... and {len(by_risk[risk]) - 5} more")
                report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def suggest_chains(self, alerts: List[Dict]) -> List[str]:
        """
        Suggest potential attack chains based on vulnerabilities.
        
        Args:
            alerts: List of ZAP alerts
            
        Returns:
            List of suggested chain descriptions
        """
        suggestions = []
        
        # Look for common chain patterns
        xss_alerts = [a for a in alerts if 'XSS' in a.get('name', '') or 'Cross-Site Scripting' in a.get('name', '')]
        sql_alerts = [a for a in alerts if 'SQL' in a.get('name', '') or 'Injection' in a.get('name', '')]
        auth_alerts = [a for a in alerts if 'Authentication' in a.get('name', '') or 'Session' in a.get('name', '')]
        
        if xss_alerts and auth_alerts:
            suggestions.append("XSS to Session Hijacking: XSS vulnerabilities could be chained with session management issues")
        
        if sql_alerts and xss_alerts:
            suggestions.append("SQL Injection to XSS: SQL injection could lead to stored XSS if data is reflected")
        
        if len(auth_alerts) > 1:
            suggestions.append("Multiple Auth Issues: Multiple authentication vulnerabilities could be chained for privilege escalation")
        
        return suggestions


if __name__ == "__main__":
    print("=" * 80)
    print("OWASP ZAP INTEGRATION - AUTOMATED TARGET DISCOVERY")
    print("=" * 80)
    print()
    
    # Example usage
    scanner = ZAPScanner()
    
    if scanner.check_connection():
        print("ZAP is accessible")
        print()
        print("Example usage:")
        print("  scanner = ZAPScanner('http://localhost:8080')")
        print("  alerts = scanner.scan_target('http://target.com')")
        print("  report = scanner.generate_findings_report(alerts)")
        print("  suggestions = scanner.suggest_chains(alerts)")
    else:
        print("ZAP is not accessible. Make sure ZAP is running on http://localhost:8080")
        print()
        print("To start ZAP:")
        print("  1. Download OWASP ZAP")
        print("  2. Start ZAP (it runs on port 8080 by default)")
        print("  3. Or use Docker: docker run -d -p 8080:8080 owasp/zap2docker-stable")

