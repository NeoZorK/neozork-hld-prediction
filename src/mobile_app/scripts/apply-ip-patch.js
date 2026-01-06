#!/usr/bin/env node

/**
 * Script to apply security patch for ip package SSRF vulnerability.
 * 
 * This script applies a fix for CVE-2024-29415 / CVE-2023-42282
 * by replacing the vulnerable isPublic() function with a secure implementation.
 */

const fs = require('fs');
const path = require('path');

const IP_PACKAGE_PATH = path.join(__dirname, '../node_modules/ip/lib/ip.js');
const BACKUP_PATH = IP_PACKAGE_PATH + '.backup';

// Secure implementation of isPublic function
const SECURE_IS_PUBLIC = `
ip.isPublic = function (addr) {
  if (typeof addr !== 'string') {
    return false;
  }
  
  var normalized = addr.trim();
  
  // Handle IPv4 addresses with octal notation and edge cases
  if (normalized.indexOf('.') !== -1) {
    // Check for octal notation (e.g., 012.1.2.3)
    if (/^0\\d+\\./.test(normalized)) {
      return false; // Octal notation likely indicates private address
    }
    
    // Normalize IPv4: handle cases like 127.1 -> 127.0.0.1
    var parts = normalized.split('.');
    if (parts.length >= 1 && parts.length <= 4) {
      // Expand shortened IPv4 addresses
      while (parts.length < 4) {
        parts.push('0');
      }
      
      // Normalize each part: remove leading zeros, handle octal
      var normalizedParts = [];
      for (var i = 0; i < 4; i++) {
        var part = parts[i] || '0';
        // Handle octal notation
        if (/^0+[0-9]+$/.test(part) && part.length > 1) {
          try {
            part = parseInt(part, 8).toString();
          } catch (e) {
            return false;
          }
        } else {
          part = part.replace(/^0+/, '') || '0';
        }
        var num = parseInt(part, 10);
        if (isNaN(num) || num < 0 || num > 255) {
          return false;
        }
        normalizedParts.push(num.toString());
      }
      normalized = normalizedParts.join('.');
    }
  }
  
  // Handle IPv6 addresses with embedded IPv4 (e.g., ::ffff:127.0.0.1)
  if (normalized.indexOf(':') !== -1) {
    // Check for IPv6 with embedded IPv4
    var ipv4Match = normalized.match(/(.*:)(\\d+\\.\\d+\\.\\d+\\.\\d+)$/);
    if (ipv4Match) {
      // Check the embedded IPv4 part using isPrivate (to avoid recursion)
      var ipv4Part = ipv4Match[2];
      // Normalize the IPv4 part first
      var ipv4Parts = ipv4Part.split('.');
      if (ipv4Parts.length === 4) {
        var normalizedIpv4Parts = [];
        for (var j = 0; j < 4; j++) {
          var p = ipv4Parts[j] || '0';
          if (/^0+[0-9]+$/.test(p) && p.length > 1) {
            try {
              p = parseInt(p, 8).toString();
            } catch (e) {
              return false;
            }
          } else {
            p = p.replace(/^0+/, '') || '0';
          }
          var num = parseInt(p, 10);
          if (isNaN(num) || num < 0 || num > 255) {
            return false;
          }
          normalizedIpv4Parts.push(num.toString());
        }
        var normalizedIpv4 = normalizedIpv4Parts.join('.');
        if (ip.isPrivate(normalizedIpv4)) {
          return false; // If embedded IPv4 is private, whole address is not public
        }
      }
    }
    
    // Normalize IPv6: convert to lowercase, handle leading zeros
    normalized = normalized.toLowerCase();
    // Check for loopback variations
    if (normalized === '::1' || 
        normalized === '0:0:0:0:0:0:0:1' ||
        /^::ffff:127\\./.test(normalized) ||
        /^::ffff:0:127\\./.test(normalized) ||
        /^::ffff:0*:?127\\./.test(normalized)) {
      return false;
    }
  }
  
  // Check if normalized address is private
  if (ip.isPrivate(normalized)) {
    return false;
  }
  
  // Also check original address to catch edge cases
  if (ip.isPrivate(addr)) {
    return false;
  }
  
  return true;
};
`;

function applyPatch() {
  try {
    // Check if file exists
    if (!fs.existsSync(IP_PACKAGE_PATH)) {
      console.log('ip package not found, skipping patch application');
      return;
    }

    // Read the original file
    let content = fs.readFileSync(IP_PACKAGE_PATH, 'utf8');

    // Check if already patched
    if (content.includes('// Handle octal notation (e.g., 012.1.2.3)')) {
      console.log('ip package already patched');
      return;
    }

    // Create backup
    if (!fs.existsSync(BACKUP_PATH)) {
      fs.copyFileSync(IP_PACKAGE_PATH, BACKUP_PATH);
      console.log('Created backup of original ip.js');
    }

    // Find and replace the isPublic function
    const isPublicRegex = /ip\.isPublic\s*=\s*function\s*\([^)]*\)\s*\{[^}]*return\s*!ip\.isPrivate\([^)]*\);[^}]*\};/s;
    
    if (isPublicRegex.test(content)) {
      content = content.replace(isPublicRegex, SECURE_IS_PUBLIC.trim());
      fs.writeFileSync(IP_PACKAGE_PATH, content, 'utf8');
      console.log('Successfully applied security patch to ip package');
    } else {
      // Try alternative pattern
      const altRegex = /ip\.isPublic\s*=\s*function\s*\([^)]*\)\s*\{[^}]*\};/s;
      if (altRegex.test(content)) {
        content = content.replace(altRegex, SECURE_IS_PUBLIC.trim());
        fs.writeFileSync(IP_PACKAGE_PATH, content, 'utf8');
        console.log('Successfully applied security patch to ip package (alternative method)');
      } else {
        console.error('Could not find isPublic function to patch');
        process.exit(1);
      }
    }
  } catch (error) {
    console.error('Error applying patch:', error.message);
    process.exit(1);
  }
}

// Run the patch
applyPatch();

