# IDOR to Privilege Escalation Chain

## Overview

**Pattern:** IDOR → Information Disclosure → Privilege Escalation

**Severity:** High to Critical

**Common in:** Applications with role-based access control and direct object references

---

## Chain Steps

### Step 1: IDOR Discovery

**Type:** Insecure Direct Object Reference

**Description:**
Attacker discovers they can access resources belonging to other users by manipulating object identifiers (IDs, UUIDs, etc.).

**Common Endpoints:**
```
GET /api/users/{id}
GET /api/orders/{order_id}
GET /api/documents/{doc_id}
```

**Technique:**
- Enumerate sequential IDs: `/api/users/1`, `/api/users/2`, etc.
- Test with different user IDs
- Check for predictable identifiers

**Outcome:** Access to unauthorized resources

---

### Step 2: Information Disclosure

**Type:** Information Leakage

**Description:**
Through IDOR, attacker gathers sensitive information about other users or the system.

**Information Gathered:**
- User email addresses
- Internal user IDs
- Account details
- System architecture hints
- Admin user IDs

**Prerequisites:**
- IDOR vulnerability exists
- Resources contain sensitive information

**Outcome:** Sufficient information to plan privilege escalation

---

### Step 3: Privilege Escalation

**Type:** Authorization Bypass

**Description:**
Using gathered information, attacker identifies admin accounts or privileged endpoints and attempts to escalate privileges.

**Techniques:**
- Modify user profile to change role
- Access admin endpoints with discovered admin IDs
- Exploit missing authorization checks
- Chain with other vulnerabilities (e.g., CSRF)

**Prerequisites:**
- Knowledge of admin user IDs or endpoints
- Missing or weak authorization checks

**Outcome:** Elevated privileges, admin access

---

## Variations

### Variation 1: IDOR → Password Reset → Account Takeover
- IDOR reveals password reset tokens
- Attacker uses tokens to reset passwords

### Variation 2: IDOR → API Key Discovery → System Access
- IDOR exposes API keys in user profiles
- Attacker uses keys to access other systems

### Variation 3: IDOR → SSRF → Internal Network Access
- IDOR allows accessing internal endpoints
- Internal endpoint vulnerable to SSRF
- Attacker gains internal network access

---

## Mitigation

1. **Authorization Checks**
   - Verify user has permission for every resource access
   - Use indirect object references (mapping)
   - Implement role-based access control (RBAC)

2. **Object References**
   - Use unpredictable identifiers (UUIDs)
   - Implement access control lists (ACLs)
   - Log and monitor access attempts

3. **Information Disclosure**
   - Minimize data in API responses
   - Sanitize error messages
   - Don't expose internal IDs or structure

---

## Real-World Examples

- Common in REST APIs
- Frequently found in admin panels
- Often combined with other vulnerabilities


