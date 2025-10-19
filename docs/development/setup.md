# Development Setup

This guide covers how to set up the Campus Event & Student Service Management System for local development.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** (Python 3.13 recommended)
- **Git** for version control
- **Make** (optional, but recommended for convenience)
- **Virtual environment** support

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management
```

### 2. Set Up Development Environment

We provide an automated setup script:

```bash
./setup-dev.sh
```

This script will:
- Create a Python virtual environment (`.venv`)
- Install all dependencies from `requirements.txt`
- Install development dependencies from `requirements-dev.txt`
- Set up pre-commit hooks (if configured)

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e ".[dev]"
```

## Running the Application

### Using Make

```bash
# Run the Streamlit app
make run

# Run tests
make test

# Run code quality checks
make qa

# View all available commands
make help
```

### Direct Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the app
streamlit run app.py

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Development Tools

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy . --ignore-missing-imports

# Security scanning with bandit
bandit -r .
```

### Running All Quality Checks

```bash
# Using the provided script
./qa-simple-real.sh

# Or using make
make qa
```

## Project Structure

```
Campus-Event-Student-Service-Management/
├── app.py                 # Main Streamlit application
├── models.py             # Data models and business logic
├── data/                 # Data management
│   └── data.py
├── tabs/                 # UI components for each tab
│   ├── students.py
│   ├── events.py
│   ├── requests.py
│   ├── analytics.py
│   └── dashboard.py
├── tests/                # Test suite
│   ├── test_system.py
│   ├── test_integration.py
│   └── conftest.py
├── docs/                 # Documentation
└── .github/              # CI/CD workflows
    └── workflows/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_system.py -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Test Categories

- **Unit Tests**: Test individual components (`test_system.py`)
- **Integration Tests**: Test Streamlit app integration (`test_integration.py`)
- **Main System Tests**: Test core functionality (`test_main_system.py`)

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Open http://127.0.0.1:8000 in your browser
```

### Documentation Structure

- `docs/index.md` - Home page
- `docs/getting-started/` - Installation and quick start
- `docs/user-guide/` - Feature documentation
- `docs/development/` - Developer guides
- `docs/ci-cd/` - CI/CD documentation
- `mkdocs.yml` - MkDocs configuration

## Troubleshooting

### Common Issues

**Virtual Environment Not Activating**
```bash
# Make sure you're in the project root
pwd

# Try creating a fresh venv
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
```

**Import Errors**
```bash
# Reinstall in editable mode
pip install -e ".[dev]"
```

**Port Already in Use**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

**Tests Failing**
```bash
# Clear pytest cache
pytest --cache-clear

# Reinstall test dependencies
pip install -r requirements-dev.txt
```

## Contributing

Before submitting a pull request:

1. ✅ Run all tests: `make test`
2. ✅ Run quality checks: `make qa`
3. ✅ Format code: `black .` and `isort .`
4. ✅ Update documentation if needed
5. ✅ Add tests for new features

See [Contributing Guide](contributing.md) for detailed guidelines.

## Environment Variables

Create a `.env` file for local configuration:

```bash
# Application Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_EXPORT=true
```

## Next Steps

- 📖 [User Guide](../user-guide/students.md) - Learn how to use the system
- 🔧 [Configuration Guide](../getting-started/configuration.md) - Customize settings
- 🚀 [CI/CD Guide](../ci-cd/overview.md) - Learn about our automation
- 🤝 [Contributing Guide](contributing.md) - How to contribute

## Getting Help

- 📚 [Documentation](../index.md)
- 🐛 [Issue Tracker](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/issues)
- 💬 [Discussions](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/discussions)
