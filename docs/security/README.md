# Security Documentation

This directory contains security-related documentation for the NeoZork HLD Prediction project.

## Documentation Index

### Post-CVE Fix Process

- **[Post-CVE Fix Checklist](post_cve_fix_checklist.md)** - Comprehensive checklist for steps to follow after fixing CVE vulnerabilities on GitHub

### Known Vulnerabilities

- **[nbconvert CVE-2025-53000](nbconvert_cve_2025_53000.md)** - Security advisory for nbconvert uncontrolled search path vulnerability
- **[Ray Security Guidelines](ray_security.md)** - Security guidelines for using Ray in the project

## Quick Start

### After Fixing CVE Vulnerabilities

1. **Run verification script:**
   ```bash
   ./scripts/security/verify_cve_fixes.sh --verbose
   ```

2. **Follow the checklist:**
   - See [Post-CVE Fix Checklist](post_cve_fix_checklist.md) for detailed steps

3. **Update documentation:**
   - Update relevant CVE documentation files
   - Mark vulnerabilities as fixed

### Security Tools

The project uses several security tools:

- **safety** - Check for known vulnerabilities in dependencies
- **bandit** - Security linter for Python code
- **pip-audit** - Audit dependencies for known vulnerabilities
- **Trivy** - Container and filesystem vulnerability scanner (in CI/CD)

### Running Security Scans

```bash
# Install security tools
uv pip install safety bandit pip-audit

# Check dependencies for vulnerabilities
safety check

# Run security linter
bandit -r src/

# Audit dependencies
pip-audit --desc
```

## Security Best Practices

1. **Keep dependencies updated** - Regularly update packages to latest secure versions
2. **Monitor security alerts** - Check GitHub Security tab regularly
3. **Run security scans** - Include security checks in CI/CD pipeline
4. **Document vulnerabilities** - Keep detailed records of all security issues
5. **Test after fixes** - Always run tests after applying security fixes

## Related Resources

- [GitHub Security Advisories](https://github.com/advisories)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

