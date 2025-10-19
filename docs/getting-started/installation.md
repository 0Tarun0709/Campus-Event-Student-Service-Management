# Installation Guide

## Prerequisites

Before installing the Campus Event & Student Service Management System, ensure you have:

- Python 3.11 or higher
- Git
- UV package manager (recommended) or pip

## System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.11+
- **Memory**: 512MB minimum, 1GB recommended
- **Storage**: 100MB for application + dependencies

## Installation Methods

### Method 1: Automated Setup (Recommended)

The easiest way to get started is using our automated setup script:

```bash
# Clone the repository
git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management

# Run automated setup
./setup-dev.sh
```

This script will:

- Install UV if not present
- Create a virtual environment
- Install all dependencies
- Set up pre-commit hooks
- Run initial tests

### Method 2: Manual Installation with UV

If you prefer manual control:

```bash
# Clone repository
git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management

# Create virtual environment
uv venv .venv

# Install dependencies
uv pip install --python .venv/bin/python -e ".[dev]"

# Activate environment
source .venv/bin/activate
```

### Method 3: Using pip

For traditional pip users:

```bash
# Clone repository
git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Method 4: Docker Installation

For containerized deployment:

```bash
# Clone repository
git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management

# Build and run with Docker Compose
docker-compose up --build
```

## Verification

After installation, verify everything works:

### 1. Check Installation
```bash
# Activate environment
source .venv/bin/activate

# Check Python version
python --version

# Check installed packages
pip list | grep -E "(streamlit|pandas|plotly)"
```

### 2. Run Tests
```bash
# Run test suite
make test
# or
python -m pytest tests/ -v
```

### 3. Start Application
```bash
# Start Streamlit app
make run
# or
python -m streamlit run app.py
```

The application should open in your browser at `http://localhost:8501`.

## Troubleshooting

### Common Issues

#### UV Installation Issues
```bash
# Install UV manually
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

#### Python Version Issues
```bash
# Check Python version
python --version

# Install Python 3.11+ if needed (macOS with Homebrew)
brew install python@3.11
```

#### Permission Issues (Linux/macOS)
```bash
# Make scripts executable
chmod +x setup-dev.sh activate.sh qa.sh
```

#### Windows-specific Issues
```powershell
# Use PowerShell equivalent for activation
.venv\Scripts\Activate.ps1

# Or Command Prompt
.venv\Scripts\activate.bat
```

### Environment Issues

If you encounter environment-related issues:

```bash
# Clean environment
rm -rf .venv
rm -rf __pycache__
rm -rf *.egg-info

# Reinstall
./setup-dev.sh
```

## Development Dependencies

The development installation includes:

- **Testing**: pytest, pytest-cov, pytest-html
- **Code Quality**: black, isort, flake8, mypy, pylint  
- **Security**: bandit, safety
- **Documentation**: mkdocs, mkdocs-material
- **Performance**: locust, memory-profiler

## Production Installation

For production deployment, install only core dependencies:

```bash
uv pip install --python .venv/bin/python -e .
```

This installs only:
- streamlit
- pandas
- plotly
- psutil
- python-dotenv
- requests

## Next Steps

After successful installation:

1. [Quick Start Guide](../getting-started/quick-start.md)
2. [Configuration](../getting-started/configuration.md)
3. [Development Setup](../development/setup.md)