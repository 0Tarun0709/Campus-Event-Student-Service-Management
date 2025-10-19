# 🎯 UV Command Cheat Sheet

## The Issue You Encountered

When you ran `uv sync`, it was looking for a different project structure because:
- `uv sync` is for projects with `uv.lock` files (fully uv-managed projects)
- Your project uses traditional `pyproject.toml` with pip-style dependency management

## ✅ Correct Commands for Your Setup

### Virtual Environment
```bash
# Create venv (if needed)
uv venv .venv

# Activate manually (optional)
source .venv/bin/activate
```

### Installing Dependencies
```bash
# Production dependencies
uv pip install --python .venv/bin/python -e .

# Development dependencies (recommended)
uv pip install --python .venv/bin/python -e ".[dev]"

# Specific groups
uv pip install --python .venv/bin/python -e ".[test]"
uv pip install --python .venv/bin/python -e ".[security]"
```

### Running Commands
```bash
# Run Streamlit app
uv run --python .venv/bin/python streamlit run app.py

# Run tests
uv run --python .venv/bin/python pytest

# Run with specific dependencies
uv run --python .venv/bin/python --with pytest pytest tests/
```

### Using Make (Recommended)
```bash
make install-dev    # Install dev dependencies
make run           # Run the app
make test          # Run tests
make uv-run        # Run app with uv
make uv-test       # Run tests with uv
```

## 🔄 Alternative: Full UV Project

If you want to use `uv sync`, convert to full uv management:

```bash
# Initialize uv project (creates uv.lock)
uv init --python 3.12

# Then you can use
uv sync           # Install dependencies from lock file
uv run app.py     # Run commands
uv add package    # Add dependencies
```

## 🎯 Your Current Workflow

**Recommended approach for your project:**
1. Use `make install-dev` (easiest)
2. Use `make run` to start the app
3. Use `make test` for testing
4. Use `./setup-dev.sh` for first-time setup

The key insight: **Always specify `--python .venv/bin/python`** when using `uv pip` commands to ensure it uses your local virtual environment!
