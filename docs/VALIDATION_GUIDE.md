# Chain Validation Guide

## Overview

The chain validation system ensures that attack chains are logically sound and properly structured. This guide explains how validation works and how to fix common issues.

## Validation Checks

### 1. Chain Structure
- **Empty Chain:** Chain must have at least one step
- **Step Numbering:** Steps must be numbered sequentially (1, 2, 3, ...)
- **No Duplicates:** Each step number should appear only once

### 2. Prerequisites
- **Prerequisite Matching:** Each step's prerequisites must be met by:
  - Outcomes from previous steps, OR
  - Chain-level prerequisites
- **Fuzzy Matching:** Similar outcomes are detected and suggested

### 3. Outcomes
- **Missing Outcomes:** Steps that are prerequisites for later steps should have outcomes
- **Outcome Clarity:** Outcomes should clearly describe what was achieved

### 4. Descriptions
- **Empty Descriptions:** All steps should have descriptions

## Error Messages

### ❌ Critical Issues (Chain Invalid)
- **"Chain has no steps"** - Add at least one step
- **"Step numbers are missing"** - Fix step numbering
- **"Prerequisite 'X' is not met"** - Fix prerequisite matching

### ⚠️ Warnings (Chain Valid but Issues Found)
- **"Prerequisite not found exactly, but similar outcomes exist"** - Consider using suggested outcome
- **"Missing description"** - Add description to step

### 💡 Suggestions (Helpful Hints)
- **"Consider using one of these outcomes"** - Use suggested outcome text
- **"Add outcome field"** - Add outcome if step is prerequisite for later steps

## How to Fix Common Issues

### Issue: Prerequisite Not Met

**Problem:**
```
❌ Step 2: Prerequisite 'Session stolen' is not met
```

**Solution 1:** Match the exact outcome text
```python
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="XSS in profile",
    outcome="Session stolen"  # Match exactly
)

step2 = ChainStep(
    step_number=2,
    vulnerability_type=VulnerabilityType.IDOR,
    description="IDOR access",
    prerequisites=["Session stolen"],  # Now matches
    outcome="Data accessed"
)
```

**Solution 2:** Use chain-level prerequisites
```python
chain.prerequisites = ["Session stolen"]

step2 = ChainStep(
    step_number=2,
    vulnerability_type=VulnerabilityType.IDOR,
    description="IDOR access",
    prerequisites=["Session stolen"],  # Now available from chain
    outcome="Data accessed"
)
```

### Issue: Similar Outcomes Detected

**Problem:**
```
⚠️ Step 2: Prerequisite 'XSS stored' not found exactly, but similar outcomes exist: ['XSS payload stored in profile']
```

**Solution:** Use the suggested outcome text
```python
# Option 1: Change prerequisite to match
step2.prerequisites = ["XSS payload stored in profile"]

# Option 2: Change step1 outcome to match
step1.outcome = "XSS stored"
```

### Issue: Missing Step Numbers

**Problem:**
```
❌ Step numbers are missing: [2]
```

**Solution:** Ensure sequential numbering
```python
step1 = ChainStep(step_number=1, ...)
step2 = ChainStep(step_number=2, ...)  # Don't skip to 3
step3 = ChainStep(step_number=3, ...)
```

### Issue: Missing Outcome

**Problem:**
```
💡 Step 1: Consider adding an 'outcome' field, as Step 2 may depend on it
```

**Solution:** Add outcome to step
```python
step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="XSS in profile",
    outcome="XSS payload stored"  # Add this
)
```

## Best Practices

1. **Be Consistent:** Use consistent outcome text throughout
2. **Be Specific:** Outcomes should clearly describe what was achieved
3. **Match Exactly:** Prerequisites should match outcomes exactly (or use fuzzy matching suggestions)
4. **Document Prerequisites:** Add chain-level prerequisites for external requirements
5. **Test Validation:** Run validation after creating chains

## Examples

### Valid Chain
```python
chain = analyzer.create_chain(
    title="Valid Chain",
    description="A properly structured chain",
    impact=ImpactLevel.HIGH
)

step1 = ChainStep(
    step_number=1,
    vulnerability_type=VulnerabilityType.XSS,
    description="XSS in profile",
    outcome="XSS payload stored"
)

step2 = ChainStep(
    step_number=2,
    vulnerability_type=VulnerabilityType.IDOR,
    description="IDOR access",
    prerequisites=["XSS payload stored"],  # Matches step1.outcome
    outcome="Data accessed"
)

chain.add_step(step1)
chain.add_step(step2)

is_valid, issues = chain.validate_chain()
# Returns: (True, [])
```

### Invalid Chain (Fixed)
```python
# Before (Invalid)
step1 = ChainStep(1, VulnerabilityType.XSS, "XSS", outcome="XSS done")
step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR", prerequisites=["XSS stored"])

# After (Valid)
step1 = ChainStep(1, VulnerabilityType.XSS, "XSS", outcome="XSS stored")  # Changed outcome
step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR", prerequisites=["XSS stored"])  # Now matches
```

## Testing

Run the validation test suite:
```bash
python3 chains/test_validation.py
```

This will test various validation scenarios and show how errors are reported.

## Integration

Validation is automatically called when:
- Creating chains with `chain_analyzer.py`
- Generating reports
- Exporting chains

You can also validate manually:
```python
is_valid, issues = chain.validate_chain()
if not is_valid:
    for issue in issues:
        print(issue)
```


