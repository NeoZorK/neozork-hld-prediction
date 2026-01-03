# nbconvert CVE-2025-53000 Security Advisory

## Vulnerability Summary

**CVE**: CVE-2025-53000  
**Package**: nbconvert  
**Affected Versions**: <= 7.16.6  
**Patched Version**: None (as of current date)  
**Severity**: High  
**CWE**: CWE-427 (Uncontrolled Search Path Element)

## Description

An uncontrolled search path vulnerability in `nbconvert` versions 7.16.6 and below allows unauthorized code execution on Windows systems. When converting a Jupyter Notebook containing SVG output to PDF, `nbconvert` searches for the `inkscape` executable using `shutil.which()`, which includes the current working directory in the search path.

An attacker can create a malicious `inkscape.bat` file in the current working directory. When a user runs `jupyter nbconvert --to pdf` on a notebook containing SVG output, the malicious batch file will be executed instead of the legitimate `inkscape` executable, leading to arbitrary code execution with the user's privileges.

## Affected Usage

- **Platform**: Windows only
- **Command**: `jupyter nbconvert --to pdf`
- **Condition**: Notebook must contain SVG output
- **Trigger**: Malicious `inkscape.bat` file in current working directory

## Proof of Concept

1. Create a directory containing:
   - A hidden batch file called `inkscape.bat` containing: `msg * "You've been hacked!"`
   - A dummy `.ipynb` file called `Machine_Learning.ipynb` with SVG output

2. Run the command: `jupyter nbconvert --to pdf Machine_Learning.ipynb`

3. The malicious batch file will be executed, showing a popup message.

## Impact

- **All Windows users** using `nbconvert` to convert notebooks with SVG output to PDF
- **Arbitrary code execution** with the privileges of the user running `nbconvert`
- **No authentication required** - the attack can be performed by anyone who can place a file in the working directory

## Mitigation Strategies

### 1. Avoid Running nbconvert in Untrusted Directories

**CRITICAL**: Never run `jupyter nbconvert --to pdf` in directories that you do not control or trust.

- Always verify the contents of the current working directory before running `nbconvert`
- Use dedicated, controlled directories for notebook conversion
- Avoid running `nbconvert` in shared or public directories

### 2. Set Environment Variable (Windows)

Set the `NoDefaultCurrentDirectoryInExePath` environment variable to exclude the current working directory from the executable search path:

**PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("NoDefaultCurrentDirectoryInExePath", "1", "User")
```

**Command Prompt:**
```cmd
setx NoDefaultCurrentDirectoryInExePath 1
```

**Note**: This requires restarting the terminal/application for the change to take effect.

### 3. Use Full Path for inkscape

If you have `inkscape` installed, ensure it's in your system PATH and verify its location:

```powershell
# Verify inkscape location
where.exe inkscape

# Ensure it's in a trusted location (e.g., Program Files)
```

### 4. Monitor for Updates

Regularly check for updates to `nbconvert`:

```bash
pip index versions nbconvert
# or
pip install --upgrade nbconvert --dry-run
```

When a patched version (>= 7.16.7) becomes available, update immediately:

```bash
pip install --upgrade nbconvert
```

### 5. Alternative: Use Docker/Container

If possible, run `nbconvert` in a controlled container environment where the working directory is guaranteed to be clean:

```bash
docker run -v $(pwd):/workspace jupyter/scipy-notebook \
  jupyter nbconvert --to pdf /workspace/notebook.ipynb
```

## Detection

To check if you're vulnerable:

1. **Check installed version:**
   ```bash
   pip show nbconvert
   ```

2. **Check for suspicious files:**
   ```powershell
   # In your working directory
   Get-ChildItem -Force | Where-Object { $_.Name -like "*inkscape*" }
   ```

## Current Status

- **Current Version in Project**: 7.16.6 (vulnerable)
- **Patched Version**: Not yet available
- **Action Required**: Apply mitigation strategies above

## References

- [CVE-2025-53000](https://nvd.nist.gov/vuln/detail/CVE-2025-53000)
- [CWE-427: Uncontrolled Search Path Element](https://cwe.mitre.org/data/definitions/427.html)
- [nbconvert GitHub Repository](https://github.com/jupyter/nbconvert)
- [nbconvert Issue Tracker](https://github.com/jupyter/nbconvert/issues)

## Update Instructions

When a patched version becomes available:

1. Update `pyproject.toml`:
   ```toml
   "nbconvert>=7.16.7",
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

3. Verify the update:
   ```bash
   uv pip list | grep nbconvert
   ```

## Additional Security Recommendations

1. **Principle of Least Privilege**: Run `nbconvert` with minimal required privileges
2. **Directory Isolation**: Use separate directories for different tasks
3. **File Monitoring**: Monitor working directories for unexpected files
4. **User Education**: Educate users about the risks of running commands in untrusted directories

