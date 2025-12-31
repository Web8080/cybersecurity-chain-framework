# Targets Quick Reference

## 🎯 Primary Focus: OWASP Juice Shop ⭐

**Recommended for Sprint 1** - Best for attack chain analysis

### Access Information
- **URL:** http://localhost:3000
- **IP:** 127.0.0.1 (localhost)
- **Port:** 3000
- **Type:** Web Application (Node.js/Angular)

### Quick Start
```bash
cd targets/juice-shop
bash setup.sh
```

### Why Juice Shop?
- ✅ 100+ vulnerabilities perfect for chaining
- ✅ Modern, realistic e-commerce application
- ✅ Built-in scoreboard for tracking progress
- ✅ Great for multi-step attack chains
- ✅ Business logic flaws
- ✅ API security testing

---

## All Available Targets

### Web Applications

#### 1. OWASP Juice Shop ⭐ RECOMMENDED
- **URL:** http://localhost:3000
- **IP:** 127.0.0.1
- **Port:** 3000
- **Setup:** `bash targets/juice-shop/setup.sh`
- **Best for:** Attack chains, business logic, API security

#### 2. DVWA (Damn Vulnerable Web Application)
- **URL:** http://localhost:8080
- **IP:** 127.0.0.1
- **Port:** 8080
- **Default Credentials:** admin/password
- **Setup:** `bash targets/dvwa/setup.sh`
- **Best for:** Learning fundamentals, OWASP Top 10

#### 3. bWAPP (Buggy Web Application)
- **URL:** http://localhost
- **IP:** 127.0.0.1
- **Port:** 80
- **Default Credentials:** bee/bug or admin/admin
- **Setup:** `bash targets/bwapp/setup.sh`
- **Best for:** 100+ vulnerabilities, comprehensive testing

#### 4. WebGoat
- **URL:** http://localhost:8080/WebGoat
- **IP:** 127.0.0.1
- **Port:** 8080
- **Setup:** `bash targets/webgoat/setup.sh`
- **Best for:** Structured learning, guided lessons

### Hardware/IoT

#### 5. IoTGoat
- **Type:** Router firmware (VM or QEMU)
- **Setup:** See `targets/iotgoat/setup.sh`
- **Best for:** Firmware analysis, hardware security
- **Note:** Requires VM or emulation setup

### Robotics
- **Type:** Research and methodology
- **Examples:** See `targets/robotics/example_chains.py`
- **Best for:** Robot security research, ROS security

---

## Getting IP Addresses

### Local Targets (Running on Your Machine)
All web targets run on **localhost (127.0.0.1)** with different ports:

| Target | IP Address | Port | Full URL |
|--------|-----------|------|----------|
| Juice Shop | 127.0.0.1 | 3000 | http://127.0.0.1:3000 |
| DVWA | 127.0.0.1 | 8080 | http://127.0.0.1:8080 |
| bWAPP | 127.0.0.1 | 80 | http://127.0.0.1 |
| WebGoat | 127.0.0.1 | 8080 | http://127.0.0.1:8080/WebGoat |

### Finding Your Machine's IP (for network access)
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Or
ip addr show | grep "inet " | grep -v 127.0.0.1

# Quick check
hostname -I
```

### Docker Container IPs
```bash
# Get container IP
docker inspect <container-name> | grep IPAddress

# Example for Juice Shop
docker inspect juice-shop | grep IPAddress
```

---

## Current Status

Check which targets are running:
```bash
python3 targets/target_manager.py
```

Or check Docker:
```bash
docker ps
```

---

## Recommended Workflow for Sprint 1

1. **Start Juice Shop** (Primary target)
   ```bash
   cd targets/juice-shop
   bash setup.sh
   ```

2. **Access the target**
   - Browser: http://localhost:3000
   - Or: http://127.0.0.1:3000

3. **Start discovering**
   ```bash
   python3 targets/juice-shop/discover_chains.py
   ```

4. **Document findings**
   - Use `chains/chain_analyzer.py`
   - Follow Sprint 1 goals

---

## Need Help?

- **Quick Start:** `targets/GETTING_STARTED.md`
- **Full Guide:** `targets/COMPREHENSIVE_GUIDE.md`
- **Target Manager:** `python3 targets/target_manager.py`


