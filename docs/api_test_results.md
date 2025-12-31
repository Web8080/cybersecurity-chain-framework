# API Endpoint Testing Results

## 🧪 Test Results Summary

### ✅ SUCCESS: iRobot Discovery API

**Endpoint:** `https://disc-int-test.iot.irobotapi.com/v1/robot/discover?robot_id=TEST&country_code=US`

**Response:**
```json
{
  "discoveryTTL": 84662,
  "httpBase": "https://unauth1.int-test.iot.irobotapi.com",
  "iotTopics": "$aws",
  "irbtTopics": "v027-irbthbu",
  "mqtt": "agrxftka9i3qm.iot.us-east-1.amazonaws.com",
  "svcDeplId": "v027"
}
```

**Critical Findings:**
- ✅ **API is accessible** without authentication!
- ✅ **MQTT endpoint discovered:** `agrxftka9i3qm.iot.us-east-1.amazonaws.com`
- ✅ **Base URL provided:** `https://unauth1.int-test.iot.irobotapi.com`
- ✅ **IoT Topics:** `$aws` and `v027-irbthbu`

**Security Implications:**
- Discovery API exposes infrastructure details
- MQTT broker endpoint revealed
- Base URLs for API access provided

---

### ⚠️ Unauthenticated Endpoints (403 Forbidden)

**Endpoints Tested:**
- `https://unauth1.int-test.iot.irobotapi.com` → **403 Forbidden**
- `https://unauth2.int-test.iot.irobotapi.com` → **403 Forbidden**
- `https://unauth3.int-test.iot.irobotapi.com` → **403 Forbidden**

**Analysis:**
- Endpoints exist but require authentication
- 403 indicates access control is in place
- May be vulnerable to authentication bypass

---

## 🔍 Java Code Analysis Results

### Critical API Endpoints Found

#### iRobot Production APIs
1. **IFTTT Integration:**
   - Int-test: `https://integrate-int-test.iot.irobotapi.com/account-linking/ifttt`
   - Production: `https://integrate-prod.iot.irobotapi.com/account-linking/ifttt`
   - China: `https://integrate-prod-cn.iot.irobot.cn/account-linking/ifttt`

2. **Content Services:**
   - Main: `https://www.irobot.com/services/content/`
   - China: `https://appcontent.irobot.cn`
   - Global: `https://global.irobot.com`

3. **Web API:**
   - `https://webapi.irobot.com/legal/documents/...`

4. **Axeda Integration:**
   - Sandbox: `https://irobot-sandbox.axeda.com/services/v1/rest/Scripto/execute/`

#### Third-Party APIs
- **IFTTT:** `https://connectapi.ifttt.com`
- **Pushy:** `https://api.pushy.me`
- **iRobot Pushy:** `https://irobot.pushy.me`
- **Bit.ly:** `https://bit.ly/api/click`
- **Gigya:** `https://www.gigya.com`

#### AWS Services
- **Kinesis Video:** `https://kinesisvideo.us-west-2.amazonaws.com`
- **MQTT Broker:** `agrxftka9i3qm.iot.us-east-1.amazonaws.com` (from discovery API)

#### Firebase Services
- Remote Config: `https://firebaseremoteconfig.googleapis.com/...`
- Real-time Config: `https://firebaseremoteconfigrealtime.googleapis.com/...`

#### Google APIs
- Multiple Google OAuth endpoints
- Google Play Store URLs

---

## 🎯 Key Discoveries

### 1. Discovery API Vulnerability ⚠️
- **Endpoint:** Discovery API accessible without auth
- **Exposes:** MQTT broker, base URLs, deployment info
- **Risk:** Information disclosure, infrastructure mapping

### 2. Multiple Environment Endpoints
- **Int-test:** `int-test.iot.irobotapi.com`
- **Production:** `prod.iot.irobotapi.com`
- **China:** `prod-cn.iot.irobot.cn`

### 3. MQTT Broker Discovery
- **Broker:** `agrxftka9i3qm.iot.us-east-1.amazonaws.com`
- **Topics:** `$aws`, `v027-irbthbu`
- **Risk:** Potential MQTT security issues

### 4. API Gateway Endpoints
- Multiple AWS Lambda endpoints
- Unauthenticated base URLs
- Authentication endpoints

---

## 📋 Testing Recommendations

### High Priority
1. **Test MQTT Broker**
   ```bash
   # Test MQTT connection
   # Use MQTT client to connect
   # Test topic access
   ```

2. **Test IFTTT Integration**
   ```bash
   curl "https://integrate-int-test.iot.irobotapi.com/account-linking/ifttt"
   ```

3. **Test Content Services**
   ```bash
   curl "https://www.irobot.com/services/content/"
   ```

### Medium Priority
4. **Test Axeda Sandbox**
   ```bash
   curl "https://irobot-sandbox.axeda.com/services/v1/rest/Scripto/execute/"
   ```

5. **Test Web API**
   ```bash
   curl "https://webapi.irobot.com/..."
   ```

---

## 🚨 Security Concerns

1. **Discovery API** - Exposes infrastructure without authentication
2. **MQTT Broker** - Endpoint and topics exposed
3. **Multiple Environments** - Test endpoints in production code
4. **Third-Party Integrations** - Multiple external services

---

## 📝 Next Steps

1. ✅ Test MQTT broker connection
2. ✅ Test IFTTT integration endpoints
3. ✅ Analyze authentication mechanisms
4. ✅ Test for IDOR vulnerabilities
5. ✅ Document new attack chains

---

**Status:** Testing in progress. Multiple endpoints discovered and ready for further analysis.

