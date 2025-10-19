# CI/CD Pipeline Documentation

## 📋 Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Campus Event & Student Service Management System.

## 🏗️ Pipeline Architecture

### Workflows

1. **Main CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
   - Runs on push to `main` and `develop` branches
   - Includes code quality, testing, building, and deployment

2. **Code Quality** (`.github/workflows/code-quality.yml`)
   - Code formatting checks (Black, isort)
   - Linting (flake8, pylint)
   - Type checking (mypy)

3. **Security Scanning** (`.github/workflows/security.yml`)
   - Vulnerability scanning (Bandit, Safety)
   - Dependency analysis (CodeQL, Trivy)
   - SARIF report generation

4. **Performance Testing** (`.github/workflows/performance.yml`)
   - Benchmark testing
   - Memory profiling
   - Load testing

5. **Deployment** (`.github/workflows/deploy.yml`)
   - Streamlit Cloud deployment
   - Health checks
   - Rollback capabilities

## 🚀 Getting Started

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/0Tarun0709/Campus-Event-Student-Service-Management.git
   cd Campus-Event-Student-Service-Management
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv pip install -e ".[dev]"
   
   # Or using pip
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Environment Configuration

Create environment-specific configuration files:

- `.env.development` - Development settings
- `.env.production` - Production settings

## 🧪 Testing

### Running Tests Locally

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Only integration tests
```

### Test Structure

```
tests/
├── test_system.py       # Unit tests for core system
├── test_integration.py  # Integration tests for Streamlit app
└── conftest.py         # Test configuration and fixtures
```

## 🔍 Code Quality

### Tools Used

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Static type checking
- **pylint**: Advanced linting
- **bandit**: Security linting
- **safety**: Vulnerability scanning

### Running Code Quality Checks

```bash
# Using Makefile (recommended)
make qa                 # Run all quality checks
make format            # Format code only
make lint              # Lint code only
make security          # Security checks only

# Or manually
black .               # Format code
isort .              # Sort imports
flake8 .             # Lint code
mypy .               # Type checking
pylint **/*.py       # Advanced linting
bandit -r .          # Security scanning
safety check         # Vulnerability checking
```

## 🐳 Docker

### Building Docker Image

```bash
docker build -t campus-management .
```

### Running with Docker Compose

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml up
```

## 🚀 Deployment

### Streamlit Cloud Deployment

The application automatically deploys to Streamlit Cloud when:
1. Code is pushed to the `main` branch
2. All tests pass
3. Security scans are clean

### Environment Variables

Required secrets for deployment:

```
DOCKERHUB_USERNAME      # Docker Hub username
DOCKERHUB_TOKEN         # Docker Hub access token
STREAMLIT_APP_URL       # URL of deployed Streamlit app
SLACK_WEBHOOK_URL       # Slack notifications (optional)
SONAR_TOKEN            # SonarCloud token (optional)
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint

The application includes a health check endpoint accessible at `/healthz` that monitors:

- System resources (CPU, memory, disk)
- Application state
- Component health

### Monitoring Dashboards

- **GitHub Actions**: Pipeline status and history
- **SonarCloud**: Code quality metrics
- **Streamlit Cloud**: Application metrics

## 🔄 Branching Strategy

### Git Flow

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development
- `hotfix/*`: Production hotfixes
- `release/*`: Release preparation

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Ensure all CI checks pass
4. Request review from team members
5. Merge to `develop` after approval
6. Deploy to staging for testing
7. Merge to `main` for production deployment

## 🚨 Troubleshooting

### Common Issues

#### Pipeline Failures

1. **Test Failures**
   - Check test logs in GitHub Actions
   - Run tests locally to reproduce
   - Fix failing tests and push changes

2. **Security Scan Failures**
   - Review security report artifacts
   - Update vulnerable dependencies
   - Add security exceptions if needed

3. **Deployment Failures**
   - Check deployment logs
   - Verify environment variables
   - Test health check endpoint

#### Local Development Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Pre-commit Hook Failures**
   ```bash
   pre-commit run --all-files
   ```

3. **Docker Build Issues**
   ```bash
   docker system prune
   docker build --no-cache -t campus-management .
   ```

## 📈 Performance Optimization

### Benchmarking

Performance benchmarks are automatically run in CI/CD:
- Function execution time
- Memory usage
- Load testing results

### Optimization Guidelines

1. **Code Performance**
   - Use pandas vectorized operations
   - Implement caching where appropriate
   - Optimize database queries

2. **Streamlit Performance**
   - Use `@st.cache_data` for expensive computations
   - Minimize re-runs with proper session state
   - Optimize data loading

## 🔐 Security

### Security Measures

1. **Static Analysis**
   - Bandit security linting
   - Safety vulnerability checking
   - CodeQL analysis

2. **Dependency Security**
   - Automated dependency updates
   - Vulnerability scanning
   - License compliance checking

3. **Container Security**
   - Non-root user execution
   - Minimal base images
   - Security scanning with Trivy

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Testing Best Practices](https://docs.pytest.org/en/stable/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all CI checks pass
6. Submit a pull request

## 📞 Support

For questions or issues with the CI/CD pipeline:

1. Check the [Issues](https://github.com/0Tarun0709/Campus-Event-Student-Service-Management/issues) page
2. Review pipeline logs in GitHub Actions
3. Contact the development team

---

**Last Updated**: October 2025
**Pipeline Version**: 1.0.0