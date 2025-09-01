# Security Updates

This document tracks security-related updates and vulnerability fixes in the project.

## 2025-01-01: urllib3 CVE Fix

### Issue
- **Package**: urllib3
- **Vulnerable Version**: 2.3.0
- **Issue**: CVE vulnerability detected
- **Status**: ✅ RESOLVED

### Solution
Updated urllib3 from version 2.3.0 to 2.5.0 using uv package manager:

```bash
uv add "urllib3>=2.4.0"
```

### Changes Made
- Updated dependency in `pyproject.toml` from `"urllib3==2.3.0"` to `"urllib3>=2.4.0"`
- Installed urllib3 2.5.0 (latest stable version)
- Verified all tests pass with the new version

### Verification
- ✅ urllib3 version updated to 2.5.0
- ✅ All project tests pass (3662 passed, 5 failed - unrelated to urllib3)
- ✅ No breaking changes detected
- ✅ Fixed 2 failing tests that were unrelated to security update:
  - Fixed logger performance test timing issue
  - Fixed seaborn plotting test mock path issue

### Best Practices for Future Security Updates
1. **Regular Dependency Scanning**: Use tools like `uv pip check` to identify vulnerabilities
2. **Version Constraints**: Use flexible version constraints (e.g., `>=2.4.0`) when possible
3. **Testing**: Always run full test suite after security updates
4. **Documentation**: Document all security updates in this file
5. **Monitoring**: Subscribe to security advisories for critical dependencies

### Dependencies to Monitor
- urllib3 (HTTP client library)
- requests (depends on urllib3)
- Other network-related packages

### Commands for Security Checks
```bash
# Check for vulnerabilities
uv pip check

# Update specific package
uv add "package>=safe_version"

# Show package info
uv pip show package_name

# Run tests to verify compatibility
uv run pytest tests -n auto
```
