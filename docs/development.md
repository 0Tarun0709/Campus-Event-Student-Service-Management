# Development Guide

This guide covers development practices, contributing guidelines, and technical details for the Campus Event Management System.

## Development Environment

### Prerequisites

- Python 3.11+ 
- Git
- UV package manager (recommended) or pip
- Docker (optional)
- VS Code (recommended)

### Setup Development Environment

```bash
# Quick setup with automated script
./setup-dev.sh

# Manual setup
python -m venv .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
pre-commit install
```

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow code style guidelines
   - Write tests for new functionality
   - Update documentation as needed

3. **Quality Checks**
   ```bash
   make qa  # Runs formatting, linting, type checking, security scans
   ```

4. **Run Tests**
   ```bash
   make test  # Run full test suite with coverage
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Quality Standards

### Code Formatting

We use **Black** for consistent code formatting:

```bash
black .  # Format all Python files
```

Configuration in `pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py311']
```

### Import Sorting

We use **isort** for consistent import organization:

```bash
isort .  # Sort all imports
```

### Linting

We use **flake8** for code linting:

```bash
flake8 .  # Check code quality
```

### Type Checking

We use **mypy** for static type checking:

```bash
mypy .  # Type check all files
```

### Security Scanning

We use **bandit** for security analysis:

```bash
bandit -r .  # Scan for security issues
```

## Testing Guidelines

### Test Structure

```
tests/
├── test_system.py      # Unit tests for main system
├── test_integration.py # Integration tests
├── test_models.py      # Model tests
└── conftest.py         # Test configuration and fixtures
```

### Writing Tests

#### Unit Tests
```python
import pytest
from main import CampusEventManagementSystem

@pytest.fixture
def system():
    return CampusEventManagementSystem()

def test_add_student_success(system):
    result = system.add_student("S001", "John", "john@edu", "CS")
    assert result == "Student added successfully!"
```

#### Integration Tests
```python
@pytest.mark.integration
def test_student_registration_workflow(system):
    # Add student
    system.add_student("S001", "John", "john@edu", "CS")
    
    # Add event
    system.add_event("E001", "Workshop", "Tech", "2025-12-01", 
                    "10:00", "12:00", "Room A", 50)
    
    # Register student for event
    result = system.register_student("S001", "E001")
    assert result == "Student registered successfully!"
```

### Test Commands

```bash
# Run all tests
make test

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_system.py -v

# Run tests matching pattern
pytest -k "test_student" -v
```

## Architecture Overview

### Core Components

1. **Main System** (`main.py`)
   - Central business logic
   - Student and event management
   - Registration handling

2. **Models** (`models.py`)
   - Data structures
   - Student and Event classes
   - Validation logic

3. **Streamlit App** (`app.py`)
   - Web interface
   - User interactions
   - Tab-based navigation

4. **Tab Components** (`tabs/`)
   - Modular UI components
   - Separate concerns
   - Reusable widgets

5. **Data Layer** (`data/`)
   - Data persistence
   - File I/O operations
   - Data validation

### Design Patterns

- **Singleton**: CampusEventManagementSystem
- **Factory**: Event and Student creation
- **Observer**: UI updates on data changes
- **Strategy**: Different registration strategies

## CI/CD Pipeline

### Workflow Overview

Our CI/CD pipeline includes:

1. **Code Quality** - Formatting, linting, type checking
2. **Testing** - Unit, integration, and performance tests
3. **Security** - Vulnerability scanning and code analysis
4. **Building** - Package and Docker image creation
5. **Deployment** - Automated deployment to staging/production

### Workflow Files

- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `.github/workflows/code-quality.yml` - Code quality checks
- `.github/workflows/security.yml` - Security scanning
- `.github/workflows/performance.yml` - Performance testing
- `.github/workflows/docs.yml` - Documentation deployment

### Quality Gates

All PRs must pass:
- ✅ Code formatting (Black, isort)
- ✅ Linting (flake8)
- ✅ Type checking (mypy)
- ✅ Security scanning (bandit, safety)
- ✅ Test coverage (85%+ required)
- ✅ All tests passing
- ✅ Documentation builds

## Performance Guidelines

### Benchmarking

We use `pytest-benchmark` for performance testing:

```python
def test_student_addition_performance(benchmark, system):
    result = benchmark(system.add_student, "S001", "John", "john@edu", "CS")
    assert result == "Student added successfully!"
```

### Memory Profiling

```python
@pytest.mark.memory
def test_memory_usage():
    system = CampusEventManagementSystem()
    # Add many students and check memory
    for i in range(1000):
        system.add_student(f"S{i:03d}", f"Student{i}", f"s{i}@edu", "CS")
```

### Performance Monitoring

- **Streamlit Performance**: Page load times, memory usage
- **Backend Performance**: Function execution times
- **Database Performance**: Query optimization (when applicable)

## Documentation

### Writing Documentation

- Use clear, concise language
- Include code examples
- Update docstrings for all functions
- Keep README.md current

### Building Documentation

```bash
# Serve documentation locally
make docs-serve

# Build documentation
make docs-build

# Deploy documentation (automated in CI)
mkdocs gh-deploy
```

### Documentation Structure

```
docs/
├── index.md                    # Project overview
├── getting-started.md          # Quick start guide
├── ci-cd/
│   └── migration-guide.md      # This comprehensive guide
└── development.md              # This development guide
```

## Troubleshooting

### Common Issues

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

#### UV Installation Issues
```bash
# Install UV
pip install uv

# Use explicit Python path
uv pip install --python .venv/bin/python -e ".[dev]"
```

#### Test Failures
```bash
# Run tests with verbose output
pytest -v -s

# Run specific failing test
pytest tests/test_system.py::test_specific_function -v -s
```

#### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Getting Help

1. Check this documentation first
2. Review CI/CD workflow logs
3. Run diagnostic commands:
   ```bash
   make help
   make test
   make qa
   ```
4. Check GitHub Issues for similar problems

## Contributing

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Run quality checks (`make qa`)
5. Submit PR with clear description
6. Address review feedback
7. Merge after approval

### Commit Message Format

Follow conventional commits:

```
feat: add new student validation
fix: resolve event registration bug
docs: update installation guide
test: add integration tests for events
chore: update dependencies
```

### Code Review Guidelines

- Review for functionality, performance, security
- Check test coverage and quality
- Verify documentation updates
- Ensure CI/CD pipeline passes
- Provide constructive feedback

This development guide ensures consistent, high-quality contributions to our modernized codebase! 🚀