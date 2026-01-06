# Security Patches

This directory contains security patches for npm packages with known vulnerabilities.

## ip package SSRF vulnerability fix

**Issue**: CVE-2024-29415 / CVE-2023-42282  
**Package**: ip@1.1.9  
**Vulnerability**: SSRF (Server-Side Request Forgery) due to improper categorization of IP addresses in `isPublic()` function

### Problem

The `isPublic()` function in the `ip` package incorrectly categorizes certain IP addresses as globally routable when they are actually private or loopback addresses:

- `127.1` (should be loopback)
- `01200034567` (octal notation)
- `012.1.2.3` (octal notation, should be private)
- `000:0:0000::01` (IPv6 with leading zeros)
- `::fFFf:127.0.0.1` (IPv6 with embedded IPv4 loopback)

### Solution

This patch fixes the `isPublic()` function to:

1. Normalize IP addresses before validation
2. Handle octal notation in IPv4 addresses
3. Properly detect loopback addresses in various formats
4. Handle IPv6 addresses with embedded IPv4
5. Expand shortened IPv4 addresses (e.g., `127.1` → `127.0.0.1`)

### Application

The patch is automatically applied after `npm install` via the `postinstall` script in `package.json`, which:
1. Applies the patch using `patch-package`
2. Runs a fallback script `scripts/apply-ip-patch.js` to ensure the fix is applied even if patch-package fails

To manually apply the patch:

```bash
npx patch-package
# Or run the fallback script directly
node scripts/apply-ip-patch.js
```

### Testing

To verify the patch works correctly, test with the problematic IP addresses:

```javascript
const ip = require('ip');

// These should all return false (not public)
console.log(ip.isPublic('127.1')); // false
console.log(ip.isPublic('012.1.2.3')); // false
console.log(ip.isPublic('::ffff:127.0.0.1')); // false
console.log(ip.isPublic('000:0:0000::01')); // false
```

