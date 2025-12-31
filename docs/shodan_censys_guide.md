# Shodan/Censys Search Guide

## 🎯 Goal: Find Exposed Robot Services

### ⚠️ CRITICAL LEGAL WARNING

**ONLY search for and test devices you own or have explicit written permission to test!**

Unauthorized access to computer systems is illegal and can result in criminal charges.

## Step 1: Get API Access

### Shodan

1. **Sign up:** https://account.shodan.io/register
2. **Get API key:** https://account.shodan.io/
3. **Configure:**
   ```bash
   shodan init YOUR_API_KEY
   ```

### Censys

1. **Sign up:** https://search.censys.io/register
2. **Get credentials:** https://search.censys.io/account/api
3. **Configure:**
   ```bash
   export CENSYS_API_ID='your_id'
   export CENSYS_API_SECRET='your_secret'
   ```

## Step 2: Search for Robot Services

### Shodan Queries

```bash
# Robot controllers
shodan search "robot controller"

# Modbus (Industrial robots)
shodan search "modbus" port:502

# ROS master
shodan search "ros master" port:11311

# Robot web interfaces
shodan search "robot" "web interface"

# MQTT (IoT robots)
shodan search "mqtt" port:1883
```

### Censys Queries

```python
# Using Python
from censys.search import CensysHosts

h = CensysHosts()

# Search for Modbus
results = h.search("services.service_name:MODBUS")

# Search for ROS
results = h.search("services.service_name:ROS")

# Iterate results
for result in results:
    print(result)
```

## Step 3: Analyze Results

**What to look for:**
- IP addresses
- Open ports
- Service banners
- Geographic location
- Organization

**Important:** Only note devices you own or have permission to test!

## Step 4: Test (ONLY with Permission)

```bash
# Network scan
nmap -p 502,11311,80,443 <target-ip>

# Service enumeration
nmap -sV <target-ip>

# Test web interface
curl http://<target-ip>/
```

## Step 5: Document Findings

```python
from chains.chain_analyzer import *

analyzer = ChainAnalyzer()

chain = analyzer.create_chain(
    title="Exposed Robot Controller",
    description="Found via Shodan search (with permission)",
    impact=ImpactLevel.HIGH
)

# Add steps based on discovered vulnerabilities
# ...
```

## 🔍 Example Search Script

```python
#!/usr/bin/env python3
import shodan

# Initialize Shodan
api = shodan.Shodan('YOUR_API_KEY')

try:
    # Search for robot controllers
    results = api.search('robot controller')
    
    print(f"Found {results['total']} results")
    
    for result in results['matches']:
        print(f"IP: {result['ip_str']}")
        print(f"Port: {result['port']}")
        print(f"Banner: {result['data']}")
        print("---")
        
except shodan.APIError as e:
    print(f"Error: {e}")
```

## 📋 Search Queries Reference

### Shodan
- `"robot controller"` - Robot controllers
- `"modbus" port:502` - Modbus devices
- `"ros master" port:11311` - ROS masters
- `"robot" "web interface"` - Robot web UIs
- `"mqtt" port:1883` - MQTT brokers

### Censys
- `services.service_name:MODBUS`
- `services.service_name:ROS`
- `services.port:502`
- `services.port:11311`

## ⚠️ Legal Reminders

- ✅ **Legal:** Search for your own devices
- ✅ **Legal:** Search with permission
- ✅ **Legal:** Research and documentation
- ❌ **Illegal:** Access without permission
- ❌ **Illegal:** Test production systems
- ❌ **Illegal:** Cause damage or disruption

## 🛠️ Tools

- **Shodan CLI** - Command-line interface
- **Shodan Python** - Python library
- **Censys Python** - Censys library
- **nmap** - Network scanning
- **curl** - HTTP testing

## Next Steps

1. Run setup: `bash setup_shodan.sh`
2. Get API keys
3. Configure tools
4. Search (responsibly!)
5. Test (with permission only!)
6. Document findings


