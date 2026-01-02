# CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing and validation.

## Workflows

### `ci.yml` - Main CI/CD Pipeline

Runs on every push and pull request to main/develop branches.

**Jobs:**
1. **validate-chains**: Validates all attack chain JSON files
2. **generate-reports**: Generates test reports to verify report generation works
3. **lint**: Runs code quality checks with flake8

**Features:**
- Automatic chain validation
- Python syntax checking
- Report generation testing
- Code quality linting

## Status Badges

Add to your README.md:

```markdown
![CI](https://github.com/Web8080/cybersecurity-chain-framework/workflows/CI/badge.svg)
```

