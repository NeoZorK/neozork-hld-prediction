#!/bin/bash
# Script to verify CVE fixes after addressing security vulnerabilities
# Usage: ./scripts/security/verify_cve_fixes.sh [--verbose] [--package PACKAGE_NAME]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
VERBOSE=false
PACKAGE_FILTER=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --package|-p)
            PACKAGE_FILTER="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--verbose] [--package PACKAGE_NAME]"
            exit 1
            ;;
    esac
done

echo "=== CVE Fix Verification Script ==="
echo ""

# Function to print status
print_status() {
    if [ "$1" = "OK" ]; then
        echo -e "${GREEN}✓${NC} $2"
    elif [ "$1" = "WARN" ]; then
        echo -e "${YELLOW}⚠${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# Check if UV is available
if ! command -v uv &> /dev/null; then
    print_status "ERROR" "UV is not installed. Please install UV first."
    exit 1
fi

print_status "OK" "UV is available"

# 1. Check dependency versions
echo ""
echo "1. Checking dependency versions..."
if [ -n "$PACKAGE_FILTER" ]; then
    if [ "$VERBOSE" = true ]; then
        uv pip list | grep -i "$PACKAGE_FILTER" || print_status "WARN" "Package $PACKAGE_FILTER not found"
    else
        uv pip list | grep -i "$PACKAGE_FILTER" > /dev/null && print_status "OK" "Package $PACKAGE_FILTER found" || print_status "WARN" "Package $PACKAGE_FILTER not found"
    fi
else
    if [ "$VERBOSE" = true ]; then
        uv pip list
    else
        print_status "OK" "Dependencies listed (use --verbose to see details)"
    fi
fi

# 2. Sync dependencies
echo ""
echo "2. Synchronizing dependencies..."
if uv sync > /dev/null 2>&1; then
    print_status "OK" "Dependencies synchronized"
else
    print_status "ERROR" "Failed to sync dependencies"
    exit 1
fi

# 3. Run security scan with safety
echo ""
echo "3. Running security scan (safety)..."
if uv pip list | grep -q "^safety "; then
    if uv run safety check > /tmp/safety_output.txt 2>&1; then
        print_status "OK" "No known vulnerabilities found (safety)"
    else
        print_status "WARN" "Safety found some issues:"
        if [ "$VERBOSE" = true ]; then
            cat /tmp/safety_output.txt
        else
            grep -i "vulnerability\|cve" /tmp/safety_output.txt | head -5
        fi
    fi
else
    print_status "WARN" "Safety is not installed. Install with: uv pip install safety"
fi

# 4. Run pip-audit if available
echo ""
echo "4. Running pip-audit..."
if uv pip list | grep -q "^pip-audit "; then
    if uv run pip-audit --desc > /tmp/pip_audit_output.txt 2>&1; then
        CRITICAL_COUNT=$(grep -i "critical\|high" /tmp/pip_audit_output.txt | wc -l | tr -d ' ')
        if [ "$CRITICAL_COUNT" -eq 0 ]; then
            print_status "OK" "No critical/high vulnerabilities found (pip-audit)"
        else
            print_status "WARN" "Found $CRITICAL_COUNT critical/high vulnerabilities"
            if [ "$VERBOSE" = true ]; then
                grep -i "critical\|high" /tmp/pip_audit_output.txt
            fi
        fi
    else
        print_status "WARN" "pip-audit found issues"
        if [ "$VERBOSE" = true ]; then
            cat /tmp/pip_audit_output.txt
        fi
    fi
else
    print_status "WARN" "pip-audit is not installed. Install with: uv pip install pip-audit"
fi

# 5. Run Bandit security linter
echo ""
echo "5. Running Bandit security linter..."
if uv pip list | grep -q "^bandit "; then
    if uv run bandit -r src/ -f json -o /tmp/bandit_report.json > /dev/null 2>&1; then
        HIGH_ISSUES=$(jq -r '.metrics._totals | .SEVERITY.HIGH // 0' /tmp/bandit_report.json 2>/dev/null || echo "0")
        if [ "$HIGH_ISSUES" -eq 0 ]; then
            print_status "OK" "No high severity issues found (bandit)"
        else
            print_status "WARN" "Found $HIGH_ISSUES high severity issues (bandit)"
            if [ "$VERBOSE" = true ]; then
                jq '.results[] | select(.issue_severity == "HIGH")' /tmp/bandit_report.json
            fi
        fi
    else
        print_status "WARN" "Bandit scan completed with issues"
        if [ "$VERBOSE" = true ]; then
            cat /tmp/bandit_report.json
        fi
    fi
else
    print_status "WARN" "Bandit is not installed. Install with: uv pip install bandit"
fi

# 6. Run tests
echo ""
echo "6. Running tests..."
if uv run pytest tests -n auto --tb=short > /tmp/pytest_output.txt 2>&1; then
    print_status "OK" "All tests passed"
else
    print_status "ERROR" "Some tests failed"
    if [ "$VERBOSE" = true ]; then
        tail -50 /tmp/pytest_output.txt
    else
        echo "Run with --verbose to see test failures"
    fi
    exit 1
fi

# 7. Check pyproject.toml for updated versions
echo ""
echo "7. Checking pyproject.toml for version constraints..."
if [ -f "pyproject.toml" ]; then
    VERSION_CONSTRAINTS=$(grep -E ">=|==|~=" pyproject.toml | wc -l | tr -d ' ')
    print_status "OK" "Found $VERSION_CONSTRAINTS version constraints in pyproject.toml"
    if [ "$VERBOSE" = true ] && [ -n "$PACKAGE_FILTER" ]; then
        grep -i "$PACKAGE_FILTER" pyproject.toml
    fi
else
    print_status "WARN" "pyproject.toml not found"
fi

# 8. Check uv.lock file
echo ""
echo "8. Checking uv.lock file..."
if [ -f "uv.lock" ]; then
    print_status "OK" "uv.lock file exists"
    if [ "$VERBOSE" = true ]; then
        echo "Lock file last modified: $(stat -f "%Sm" uv.lock 2>/dev/null || stat -c "%y" uv.lock 2>/dev/null || echo "unknown")"
    fi
else
    print_status "WARN" "uv.lock file not found"
fi

# Summary
echo ""
echo "=== Verification Summary ==="
echo ""
echo "Next steps:"
echo "1. Review GitHub Security tab for remaining alerts"
echo "2. Update security documentation in docs/security/"
echo "3. Create commit with all changes"
echo "4. Create Pull Request with security fixes"
echo "5. Verify all alerts are resolved after merge"
echo ""
echo "For detailed instructions, see: docs/security/post_cve_fix_checklist.md"
echo ""

# Cleanup
rm -f /tmp/safety_output.txt /tmp/pip_audit_output.txt /tmp/bandit_report.json /tmp/pytest_output.txt

print_status "OK" "Verification complete"

