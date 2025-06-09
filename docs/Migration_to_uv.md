
### Migration to uv
To migrate your project to use `uv`, follow these steps:
1. **Install `uv`**: If you haven't already, install the `uv` package using pip.

```bash
pip install uv
```

2. **Activate the virtual environment

```bash
source venv/bin/activate
```

3.  **Run Script to delete unused dependencies**: Use the provided script to remove unused dependencies from your project.
    (click "y" to confirm deletion of all unused dependency), and replace by new `requirements.txt` file.
```bash
python scripts/delete_unused_dependencies.py
```









