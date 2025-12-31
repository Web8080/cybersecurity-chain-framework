# Attack Chain Documentation Template

Use this template to document discovered attack chains.

## Chain Overview

**Title:** [Descriptive title of the attack chain]

**Severity:** [Critical/High/Medium/Low]

**Impact:** [What can be achieved with this chain]

**Discovered By:** [Name/Team]

**Date:** [Discovery date]

**Status:** [Validated/Unvalidated/In Progress]

---

## Executive Summary

[2-3 sentence summary of the attack chain and its impact]

---

## Prerequisites

- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]
- [ ] [Prerequisite 3]

---

## Attack Chain Steps

### Step 1: [Vulnerability/Technique Name]

**Type:** [XSS/SQL Injection/IDOR/etc.]

**Description:**
[Detailed description of this step]

**Endpoint/Component:**
```
[Specific endpoint, API, or component]
```

**Payload/Technique:**
```
[Code, payload, or technique used]
```

**Prerequisites:**
- [What must be true before this step can execute]

**Outcome:**
[What is achieved after this step]

**Evidence:**
[Proof of concept, screenshots, logs, etc.]

---

### Step 2: [Vulnerability/Technique Name]

[Repeat structure from Step 1]

---

### Step 3: [Vulnerability/Technique Name]

[Repeat structure from Step 1]

---

## Context & Environment

**Application/System:** [Name and version]

**Architecture:** [Brief description of system architecture]

**Affected Components:** [List of affected components]

**User Roles Involved:** [Which user roles are involved in the chain]

---

## Impact Analysis

**What can an attacker achieve?**
- [Impact 1]
- [Impact 2]
- [Impact 3]

**Affected Data:**
- [Type of data that can be accessed/modified]

**Business Impact:**
[How this affects the business]

---

## Validation

**Tested:** [Yes/No]

**Reproducible:** [Yes/No]

**Test Environment:**
[Details about where/how it was tested]

**Proof of Concept:**
[Link to PoC or detailed steps]

---

## Mitigation Recommendations

1. [Mitigation for Step 1]
2. [Mitigation for Step 2]
3. [Mitigation for Step 3]
4. [General recommendations]

---

## Related Findings

- [Link to related vulnerabilities]
- [Link to related attack chains]

---

## Tags

[#tag1] [#tag2] [#tag3]

---

## Notes

[Additional notes, observations, or thoughts]

