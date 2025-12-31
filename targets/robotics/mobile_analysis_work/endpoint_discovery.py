#!/usr/bin/env python3
"""
Endpoint Discovery Script - Mobile App Analysis Tool
Author: Victor Ibhafidon

Searches decompiled Java code for API endpoints, URLs, and service configurations.

WHAT IT DOES:
- Scans decompiled Java code for API endpoints
- Finds base URLs, Firebase URLs, AWS endpoints
- Identifies API client classes
- Generates comprehensive endpoint discovery reports

HOW IT CONNECTS TO THE FRAMEWORK:
- Used during mobile app reverse engineering workflow
- Discovers endpoints for attack chain creation
- Outputs findings used by create_chains.py
- Integrates with mobile_app_workflow.sh

USAGE:
    python targets/robotics/mobile_analysis_work/endpoint_discovery.py decompiled/
"""

import os
import re
from pathlib import Path

def find_api_endpoints(decompiled_dir):
    """Find API endpoints in decompiled Java code"""
    endpoints = {
        "base_urls": [],
        "api_endpoints": [],
        "firebase_urls": [],
        "service_urls": [],
        "api_classes": []
    }
    
    decompiled_path = Path(decompiled_dir)
    
    if not decompiled_path.exists():
        print(f"❌ Decompiled directory not found: {decompiled_dir}")
        return endpoints
    
    # Patterns to search for
    patterns = {
        "base_urls": [
            r'BASE_URL\s*=\s*["\']([^"\']+)["\']',
            r'baseUrl\s*=\s*["\']([^"\']+)["\']',
            r'base_url\s*=\s*["\']([^"\']+)["\']',
            r'API_BASE\s*=\s*["\']([^"\']+)["\']',
        ],
        "api_endpoints": [
            r'https://[^"\'\s]+api[^"\'\s]*',
            r'https://[^"\'\s]+\.irobot[^"\'\s]*',
            r'https://[^"\'\s]+iot\.irobotapi[^"\'\s]*',
        ],
        "firebase_urls": [
            r'https://[^"\'\s]+firebaseio\.com[^"\'\s]*',
        ],
        "service_urls": [
            r'https://[^"\'\s]+execute-api[^"\'\s]*',
            r'https://[^"\'\s]+\.amazonaws\.com[^"\'\s]*',
        ]
    }
    
    # Search Java files
    java_files = list(decompiled_path.rglob("*.java"))
    print(f"📁 Searching {len(java_files)} Java files...")
    
    for java_file in java_files:
        try:
            with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Search for patterns
                for category, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[0] if match else ""
                            if match and match not in endpoints[category]:
                                endpoints[category].append(match)
                                print(f"  ✅ Found {category}: {match}")
                
                # Find API classes
                if re.search(r'class\s+\w*Api\w*|class\s+\w*API\w*|class\s+\w*Client\w*', content, re.IGNORECASE):
                    rel_path = str(java_file.relative_to(decompiled_path))
                    if rel_path not in endpoints["api_classes"]:
                        endpoints["api_classes"].append(rel_path)
                        
        except Exception as e:
            continue
    
    return endpoints


def generate_report(endpoints):
    """Generate a report of discovered endpoints"""
    report = []
    report.append("=" * 80)
    report.append("API ENDPOINT DISCOVERY REPORT")
    report.append("=" * 80)
    report.append("")
    
    if endpoints["base_urls"]:
        report.append("📡 Base URLs:")
        for url in endpoints["base_urls"]:
            report.append(f"  - {url}")
        report.append("")
    
    if endpoints["api_endpoints"]:
        report.append("🔌 API Endpoints:")
        for url in endpoints["api_endpoints"]:
            report.append(f"  - {url}")
        report.append("")
    
    if endpoints["firebase_urls"]:
        report.append("🔥 Firebase URLs:")
        for url in endpoints["firebase_urls"]:
            report.append(f"  - {url}")
        report.append("")
    
    if endpoints["service_urls"]:
        report.append("☁️  Service URLs:")
        for url in endpoints["service_urls"]:
            report.append(f"  - {url}")
        report.append("")
    
    if endpoints["api_classes"]:
        report.append("📦 API Classes Found:")
        for cls in endpoints["api_classes"][:20]:  # Limit to first 20
            report.append(f"  - {cls}")
        if len(endpoints["api_classes"]) > 20:
            report.append(f"  ... and {len(endpoints["api_classes"]) - 20} more")
        report.append("")
    
    return "\n".join(report)


if __name__ == "__main__":
    import sys
    
    decompiled_dir = "decompiled"
    if len(sys.argv) > 1:
        decompiled_dir = sys.argv[1]
    
    print("🔍 Starting API Endpoint Discovery...")
    print("")
    
    endpoints = find_api_endpoints(decompiled_dir)
    
    print("")
    print(generate_report(endpoints))
    
    # Save to file
    output_file = "java_endpoint_discovery.txt"
    with open(output_file, 'w') as f:
        f.write(generate_report(endpoints))
    
    print(f"✅ Report saved to: {output_file}")


