# Attack Chain Analysis Workflow

## Step-by-Step Process for Discovering and Documenting Attack Chains

### Phase 1: Discovery & Reconnaissance

1. **Map the Attack Surface**
   - Identify all entry points (endpoints, APIs, user inputs)
   - Document authentication and authorization mechanisms
   - Map data flows through the application
   - Identify user roles and privilege levels

2. **Find Individual Vulnerabilities**
   - Use automated tools to find common bugs
   - Manual testing for edge cases
   - Review code for security issues
   - Test business logic flaws

3. **Document Findings**
   - Create a vulnerability inventory
   - Note prerequisites for each vulnerability
   - Document what each vulnerability enables

---

### Phase 2: Chain Building

1. **Identify Relationships**
   - Look for vulnerabilities that enable others
   - Find vulnerabilities that share prerequisites
   - Identify data flows between vulnerabilities
   - Map privilege boundaries

2. **Build Hypothetical Chains**
   - Start with high-impact goals (admin access, data exfiltration)
   - Work backwards: what vulnerabilities enable this?
   - Connect vulnerabilities in logical sequence
   - Consider multiple paths to the same goal

3. **Test Chain Feasibility**
   - Verify prerequisites can be met
   - Test if vulnerabilities can be chained
   - Check timing and ordering requirements
   - Validate dependencies

---

### Phase 3: Validation & Testing

1. **End-to-End Testing**
   - Execute the complete chain in a test environment
   - Document each step with evidence
   - Note any variations or alternative paths
   - Test edge cases and failure scenarios

2. **Impact Assessment**
   - Determine what an attacker can achieve
   - Assess business impact
   - Evaluate data exposure
   - Consider regulatory/compliance implications

3. **Reproducibility**
   - Document exact steps to reproduce
   - Note required conditions
   - Create proof of concept
   - Test in different environments

---

### Phase 4: Documentation

1. **Use Chain Analyzer Tool**
   - Create chain in `chain_analyzer.py`
   - Add all steps with details
   - Set prerequisites and outcomes
   - Validate chain logic

2. **Generate Documentation**
   - Use `chain_documentation.md` template
   - Include all technical details
   - Add visualizations using `visualizer.py`
   - Document mitigation strategies

3. **Create Visualizations**
   - Generate Mermaid diagrams
   - Create text-based flowcharts
   - Export to markdown/JSON
   - Include in reports

---

### Phase 5: Reporting & Remediation

1. **Prioritize Chains**
   - Rank by impact and severity
   - Consider exploitability
   - Assess business risk
   - Plan remediation order

2. **Recommend Mitigations**
   - Address each step in the chain
   - Recommend defense-in-depth
   - Suggest monitoring/detection
   - Provide code examples

3. **Track Remediation**
   - Monitor fix progress
   - Re-test after fixes
   - Validate chain is broken
   - Document lessons learned

---

## Tips for Effective Chain Analysis

### Think Like an Attacker
- What is the ultimate goal?
- What are the obstacles?
- How can vulnerabilities be combined?
- What creative techniques can bypass controls?

### Look for Patterns
- Review `chain_templates/` for common patterns
- Learn from real-world examples
- Adapt known chains to your application
- Document new patterns you discover

### Use Tools Effectively
- `chain_analyzer.py` for building and validating chains
- `visualizer.py` for creating diagrams
- Templates for consistent documentation
- Version control for tracking chain evolution

### Collaborate
- Share chains with team
- Get feedback on feasibility
- Brainstorm alternative paths
- Review together for completeness

---

## Common Pitfalls to Avoid

1. **Assuming Linear Chains**
   - Chains can branch and merge
   - Multiple paths to same goal
   - Parallel exploitation possible

2. **Ignoring Prerequisites**
   - Not all chains are immediately exploitable
   - Some require specific conditions
   - Timing may be critical

3. **Overlooking Context**
   - Business logic matters
   - User behavior affects feasibility
   - System architecture influences chains

4. **Incomplete Validation**
   - Test the full chain, not just parts
   - Verify in realistic conditions
   - Don't assume steps will work together


