import os
import sys
from pathlib import Path

REQUIREMENTS = Path(__file__).parent.parent / "requirements.txt"
PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def parse_requirements(req_path):
    """Parse requirements.txt and return a list of dependencies."""
    deps = []
    with open(req_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Remove inline comments
            if "#" in line:
                line = line.split("#", 1)[0].strip()
            if line:
                deps.append(line)
    return deps


def write_pyproject(pyproject_path, deps):
    """Write a minimal pyproject.toml with the given dependencies."""
    content = [
        "[project]",
        'name = "neozork-hld-prediction"',
        'dynamic = ["version"]',
        'description = "Machine Learning enhancement of proprietary trading indicators using Python"',
        'requires-python = ">=3.11"',
        "dependencies = ["
    ]
    for dep in deps:
        content.append(f'    "{dep}",')
    content.extend([
        "]",
        "",
        "[build-system]",
        'requires = ["setuptools>=45", "wheel"]',
        'build-backend = "setuptools.build_meta"',
        "",
        "[tool.setuptools.dynamic]",
        'version = {attr = "src.__version__"}',
        ""
    ])
    pyproject_path.write_text("\n".join(content), encoding="utf-8")


def main():
    if not REQUIREMENTS.exists():
        print(f"requirements.txt not found at {REQUIREMENTS}")
        sys.exit(1)
    deps = parse_requirements(REQUIREMENTS)
    if not deps:
        print("No dependencies found in requirements.txt")
        sys.exit(1)
    if not PYPROJECT.exists():
        print(f"Creating {PYPROJECT}")
        write_pyproject(PYPROJECT, deps)
    else:
        print(f"{PYPROJECT} already exists. No changes made.")


if __name__ == "__main__":
    main()

