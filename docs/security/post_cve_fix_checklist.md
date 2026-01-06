# Post-CVE Fix Checklist

This document provides a comprehensive checklist of steps to follow after fixing all CVE vulnerabilities on GitHub.

## Overview

After addressing CVE vulnerabilities identified by GitHub's security scanning, follow these steps to ensure all fixes are properly applied, tested, and documented.

## Prerequisites

- All CVE vulnerabilities have been addressed in code or dependencies
- Dependencies have been updated in `pyproject.toml` or `requirements.txt`
- You have access to the repository and can create commits/PRs

## Step-by-Step Checklist

### 1. Verify Dependency Updates

**Check that all vulnerable packages are updated:**

```bash
# Check current installed versions
uv pip list | grep -E "(package1|package2|package3)"

# Verify versions match updated requirements
uv pip list --format=json | jq '.[] | select(.name == "vulnerable-package")'
```

**Verify `pyproject.toml` contains updated versions:**

```bash
# Check pyproject.toml for updated package versions
grep -E "package.*>=" pyproject.toml
```

### 2. Synchronize Dependencies

**Sync dependencies using UV:**

```bash
# Sync all dependencies
uv sync

# Verify sync was successful
uv pip list
```

**If using requirements.txt:**

```bash
# Install updated dependencies
uv pip install -r requirements.txt --upgrade

# Verify installation
uv pip list
```

### 3. Run Security Scans

**Run automated security checks:**

```bash
# Install security tools if not already installed
uv pip install safety bandit

# Check for known vulnerabilities in dependencies
safety check

# Run Bandit security linter
bandit -r src/ -f json -o bandit-report.json

# Check for CVE vulnerabilities (if using pip-audit)
uv pip install pip-audit
pip-audit --desc
```

**Verify GitHub Security tab:**

1. Go to GitHub repository → Security tab
2. Check "Dependabot alerts" section
3. Verify all alerts are resolved or dismissed with proper justification
4. Check "Code scanning alerts" for any remaining issues

### 4. Run All Tests

**Run comprehensive test suite:**

```bash
# Run all tests with UV (multithreaded)
uv run pytest tests -n auto

# Run with coverage
uv run pytest tests --cov=src --cov-report=html -n auto

# Run specific security-related tests if they exist
uv run pytest tests/security/ -n auto
```

**Verify test results:**

- All tests should pass
- No new test failures introduced by dependency updates
- Coverage should remain at acceptable levels

### 5. Update Security Documentation

**Update security documentation files:**

1. **Update CVE-specific documentation:**
   - Update `docs/security/nbconvert_cve_2025_53000.md` (or relevant CVE docs)
   - Change status from "vulnerable" to "patched"
   - Update version information
   - Add fix date and verification steps

2. **Create or update security changelog:**
   ```bash
   # Create security changelog entry
   cat >> docs/security/CHANGELOG.md << EOF
   ## $(date +%Y-%m-%d) - CVE Fixes
   
   - Fixed CVE-XXXX-XXXX: [Package Name] updated to version X.X.X
   - Fixed CVE-YYYY-YYYY: [Package Name] updated to version Y.Y.Y
   EOF
   ```

3. **Update main security documentation:**
   - Update `docs/security/` index if it exists
   - Document mitigation strategies that were applied

### 6. Verify Fixes in Different Environments

**Test in different environments:**

```bash
# Test in Docker environment
docker-compose build
docker-compose up -d
docker-compose exec neozork uv run pytest tests -n auto

# Test in native container (if applicable)
./scripts/native-container/run.sh
# Run tests inside container

# Test locally
uv run pytest tests -n auto
```

### 7. Update Lock Files

**Update dependency lock files:**

```bash
# Update uv.lock if using UV
uv lock --upgrade

# Verify lock file is updated
git diff uv.lock
```

### 8. Create Commit and Pull Request

**Create a comprehensive commit:**

```bash
# Stage all changes
git add pyproject.toml uv.lock requirements.txt
git add docs/security/
git add tests/

# Create commit with descriptive message
git commit -m "security: Fix CVE vulnerabilities

- Updated [Package1] to version X.X.X (fixes CVE-XXXX-XXXX)
- Updated [Package2] to version Y.Y.Y (fixes CVE-YYYY-YYYY)
- Updated security documentation
- Verified all tests pass
- Ran security scans (safety, bandit)

Closes #[issue-number]"
```

**Create Pull Request:**

1. Push to feature branch
2. Create PR with:
   - Clear title: "Security: Fix CVE vulnerabilities"
   - Description listing all fixed CVEs
   - Link to GitHub Security alerts
   - Test results
   - Security scan results

### 9. Verify GitHub Security Tab

**After PR is merged, verify:**

1. Go to Security tab → Dependabot alerts
2. All alerts should show as "Dismissed" or "Fixed"
3. Code scanning alerts should be resolved
4. No new vulnerabilities introduced

### 10. Run Final Verification

**Final security verification:**

```bash
# Run comprehensive security check
safety check --full-report

# Verify no critical vulnerabilities remain
pip-audit --desc | grep -i "critical\|high"

# Check GitHub Security tab one more time
# Verify all alerts are resolved
```

### 11. Update Release Notes (if applicable)

**If preparing a release:**

1. Update `docs/release-notes/` with security fixes
2. Document all CVE fixes in release notes
3. Include upgrade instructions if needed

### 12. Monitor for New Vulnerabilities

**Set up ongoing monitoring:**

1. Ensure Dependabot is enabled in GitHub settings
2. Configure security alerts notifications
3. Set up automated security scanning in CI/CD
4. Schedule regular security audits

## Verification Commands Summary

```bash
# Quick verification script
#!/bin/bash

echo "=== Verifying CVE Fixes ==="

echo "1. Checking dependency versions..."
uv pip list | grep -E "(vulnerable-package1|vulnerable-package2)"

echo "2. Running security scan..."
safety check

echo "3. Running tests..."
uv run pytest tests -n auto

echo "4. Checking for remaining vulnerabilities..."
pip-audit --desc | grep -i "critical\|high" || echo "No critical/high vulnerabilities found"

echo "=== Verification Complete ==="
```

## Common Issues and Solutions

### Issue: Tests fail after dependency update

**Solution:**
- Review test failures carefully
- Check if API changes in updated packages require test updates
- Verify compatibility of updated packages with existing code
- Update tests to match new package behavior

### Issue: Security scan still shows vulnerabilities

**Solution:**
- Verify package versions are correctly updated
- Check if vulnerabilities are in transitive dependencies
- Update parent packages that depend on vulnerable packages
- Use `pip-audit --desc` to see full dependency tree

### Issue: GitHub Security tab still shows alerts

**Solution:**
- Wait a few minutes for GitHub to refresh
- Manually dismiss alerts if fixes are verified
- Add justification when dismissing alerts
- Check if alerts are for different branches

## Best Practices

1. **Always test before merging:** Never merge security fixes without running tests
2. **Document all fixes:** Keep detailed records of what was fixed and how
3. **Monitor continuously:** Set up automated security scanning
4. **Review regularly:** Schedule regular security audits
5. **Keep dependencies updated:** Don't wait for CVEs to update dependencies

## Related Documentation

- [nbconvert CVE-2025-53000](nbconvert_cve_2025_53000.md)
- [Ray Security Guidelines](ray_security.md)
- [Security Monitoring](../development/security-monitoring.md)

## Additional Resources

- [GitHub Security Advisories](https://github.com/advisories)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

