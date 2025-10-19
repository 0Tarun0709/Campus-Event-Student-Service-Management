# Contributing Guide

We love contributions! This guide will help you get started with contributing to the Campus Event & Student Service Management System.

## 🚀 Quick Start for Contributors

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/Campus-Event-Student-Service-Management.git
cd Campus-Event-Student-Service-Management

# Add upstream remote
git remote add upstream https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
```

### 2. Set Up Development Environment
```bash
# Run our automated setup
./setup-dev.sh

# Or manual setup
uv venv .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -e ".[dev]"
pre-commit install
```

### 3. Create Feature Branch
```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

## 📋 Types of Contributions

### 🐛 Bug Reports
Found a bug? Please help us fix it!

1. Check [existing issues](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/issues)
2. Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
3. Include:
   - Steps to reproduce
   - Expected vs actual behavior  
   - Screenshots if applicable
   - Environment details

### ✨ Feature Requests
Have an idea for improvement?

1. Check [existing feature requests](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
3. Describe:
   - The problem you're solving
   - Proposed solution
   - Alternative solutions considered

### 🔧 Code Contributions
Ready to write some code?

#### Areas We Need Help
- **Frontend Improvements**: Streamlit UI/UX enhancements
- **Data Visualization**: New chart types and analytics
- **Performance**: Optimization and caching
- **Testing**: More comprehensive test coverage
- **Documentation**: Examples, tutorials, API docs
- **Accessibility**: Making the app more accessible
- **Internationalization**: Multi-language support

## 🛠️ Development Workflow

### 1. Code Quality Standards
We maintain high code quality standards:

```bash
# Format code
make format

# Run linting
make lint  

# Run security checks
make security

# Run all quality checks
make qa
```

### 2. Testing Requirements
All contributions must include tests:

```bash
# Run tests
make test

# Run with coverage
make test-cov

# Add new tests in tests/ directory
# - tests/test_your_feature.py for unit tests
# - tests/test_integration_your_feature.py for integration tests
```

### 3. Commit Guidelines
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Examples
git commit -m "feat: add student batch import functionality"
git commit -m "fix: resolve event conflict detection bug"
git commit -m "docs: update installation guide"
git commit -m "test: add tests for service request validation"
```

**Commit Types:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

### 4. Pull Request Process

#### Before Submitting
```bash
# Ensure your branch is up to date
git fetch upstream
git rebase upstream/main

# Run full quality checks
make ci-local

# Push to your fork
git push origin feature/your-feature-name
```

#### Pull Request Template
When creating a PR, use our template and include:

- **Description**: What does this PR do?
- **Issue Link**: Fixes #123
- **Type of Change**: Bug fix, feature, docs, etc.
- **Testing**: How was this tested?
- **Screenshots**: For UI changes
- **Breaking Changes**: Any breaking changes?

#### Review Process
1. Automated checks must pass (CI/CD pipeline)
2. At least one maintainer review required
3. Code quality standards met
4. Tests pass and coverage maintained
5. Documentation updated if needed

## 🎯 Development Guidelines

### Code Style
- **Python**: Follow PEP 8, enforced by Black and flake8
- **Line Length**: 88 characters (Black default)
- **Imports**: Sorted with isort
- **Type Hints**: Use type hints where beneficial
- **Docstrings**: Follow Google style for public APIs

### Architecture Patterns
- **Separation of Concerns**: Keep UI, logic, and data separate
- **Single Responsibility**: Each function/class has one job
- **DRY Principle**: Don't repeat yourself
- **Error Handling**: Use proper exception handling
- **Logging**: Use appropriate logging levels

### Streamlit Best Practices
- **Session State**: Use for data persistence
- **Caching**: Use `@st.cache_data` for expensive operations
- **Performance**: Minimize re-runs with proper state management
- **User Experience**: Clear error messages and loading states

## 📚 Documentation Standards

### Code Documentation
```python
def add_student(student_id: str, name: str, email: str, major: str) -> str:
    """Add a new student to the system.
    
    Args:
        student_id: Unique identifier for the student
        name: Full name of the student
        email: Contact email address
        major: Student's field of study
        
    Returns:
        Success message or error description
        
    Raises:
        ValueError: If student_id already exists
        
    Example:
        >>> result = add_student("STU001", "John Doe", "john@edu", "CS")
        >>> print(result)
        "Student added successfully!"
    """
```

### Documentation Files
- Keep docs up to date with code changes
- Use Markdown with MkDocs Material extensions
- Include code examples and screenshots
- Test documentation locally: `make docs-serve`

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── test_models.py          # Unit tests for data models
├── test_system.py          # Unit tests for core system
├── test_integration.py     # Integration tests
├── test_performance.py     # Performance benchmarks
└── conftest.py            # Test configuration
```

### Writing Tests
```python
import pytest
from main import CampusEventManagementSystem

class TestStudentManagement:
    def test_add_student_success(self, system):
        """Test successful student addition."""
        result = system.add_student("STU001", "John Doe", "john@edu", "CS")
        assert result == "Student added successfully!"
        assert len(system.students) == 1
        
    def test_add_duplicate_student_fails(self, system):
        """Test that adding duplicate student fails."""
        system.add_student("STU001", "John Doe", "john@edu", "CS")
        result = system.add_student("STU001", "Jane Doe", "jane@edu", "Math")
        assert "already exists" in result.lower()
```

## 🚦 CI/CD Pipeline

Our automated pipeline runs on every PR:

1. **Code Quality**: Black, isort, flake8, mypy, pylint
2. **Security**: Bandit, Safety, CodeQL
3. **Testing**: pytest with coverage reporting
4. **Performance**: Benchmark tests
5. **Documentation**: MkDocs build verification

### Local CI Simulation
```bash
# Run the same checks as CI
make ci-local

# Individual checks
make format lint security test-cov
```

## 🎯 Getting Help

### Communication Channels
- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **PR Comments**: For code review discussions

### Maintainer Response Times
- **Issues**: Within 2-3 business days
- **PRs**: Within 1-2 business days for initial review
- **Security Issues**: Within 24 hours

### Code of Conduct
- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow our community guidelines

## 🏆 Recognition

Contributors are recognized in:
- README contributors section
- Release notes for significant contributions
- Special recognition for first-time contributors
- Maintainer status for long-term contributors

## 📋 Checklist for Contributors

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] PR description is complete
- [ ] No merge conflicts with main branch
- [ ] CI/CD pipeline passes

## 🚀 Release Process

For maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. GitHub Actions handles deployment

Thank you for contributing! Every contribution, no matter how small, helps make this project better. 🙏