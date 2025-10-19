# 🚀 CI/CD Pipeline Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Campus Event & Student Service Management System.

## 📋 Pipeline Overview

Our CI/CD pipeline consists of several automated workflows that ensure code quality, security, and reliable deployments:

### 🔄 Main CI/CD Workflow (`ci-cd.yml`)
- **Triggers**: Push to `main`/`develop`, Pull Requests
- **Stages**:
  1. **Code Quality & Security** - Formatting, linting, type checking, security scans
  2. **Testing** - Unit tests across Python 3.11-3.13
  3. **Build** - Package creation and validation
  4. **Docker Build** - Container image creation
  5. **Deploy** - Staging and Production deployments
  6. **Release** - Automated releases with `[release]` commit message

### 🔍 Code Quality Workflow (`code-quality.yml`)
- **Purpose**: Comprehensive code analysis
- **Tools**: Black, isort, flake8, pylint, mypy, bandit, safety
- **Features**: PR comments with quality reports, SonarCloud integration

### 🛡️ Security Scanning (`security.yml`)
- **Tools**: Bandit, Safety, Semgrep, CodeQL, Trivy
- **Features**: SARIF uploads to GitHub Security tab, dependency reviews
- **Schedule**: Weekly automated scans

### ⚡ Performance Testing (`performance.yml`)
- **Tools**: pytest-benchmark, memory-profiler
- **Features**: Performance regression detection, PR comments

### 🚀 Deployment (`deploy.yml`)
- **Target**: Streamlit Cloud
- **Features**: Health checks, rollback capabilities, Slack notifications

## 🛠️ Setup Instructions

### 1. Required Repository Secrets

Set these secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

```bash
# Docker Hub (for container registry)
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_TOKEN=your_dockerhub_token

# SonarCloud (for code analysis)
SONAR_TOKEN=your_sonarcloud_token

# Slack (for notifications)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Streamlit Cloud (for deployment)
STREAMLIT_APP_URL=https://your-app.streamlit.app

# Optional: Semgrep
SEMGREP_APP_TOKEN=your_semgrep_token
```

### 2. Enable GitHub Features

1. **Security Tab**: Enable security advisories and dependency graph
2. **Code Scanning**: Will be automatically configured by CodeQL workflow
3. **Dependabot**: Enable for automated dependency updates

### 3. SonarCloud Setup

1. Go to [SonarCloud.io](https://sonarcloud.io)
2. Import your GitHub repository
3. Get your project key and organization from SonarCloud
4. Update `sonar-project.properties` with your details

### 4. Local Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests locally
pytest tests/ -v

# Run code quality checks
black .
isort .
flake8 .
mypy .
bandit -r .
```

## 📊 Quality Gates

### Code Quality Metrics
- **Code Coverage**: Minimum 80%
- **Code Formatting**: 100% Black compliant
- **Import Sorting**: 100% isort compliant
- **Linting**: Zero critical flake8 violations
- **Security**: Zero high-severity bandit issues

### Testing Requirements
- **Unit Tests**: Must pass on Python 3.11, 3.12, 3.13
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: No regression beyond 10%

### Security Requirements
- **Dependency Scanning**: No high/critical vulnerabilities
- **Code Scanning**: No security hotspots
- **Secret Detection**: No exposed secrets

## 🔄 Workflow Triggers

### Automatic Triggers
- **Push to main/develop**: Full CI/CD pipeline
- **Pull Requests**: Code quality + tests
- **Schedule**: Weekly security scans (Monday 2 AM)
- **Schedule**: Weekly performance tests (Tuesday 4 AM)

### Manual Triggers
- **Deployment**: Manual deployment to staging/production
- **Release**: Add `[release]` to commit message

## 🚀 Deployment Process

### Staging Deployment
```bash
git push origin develop
# Automatically deploys to staging environment
```

### Production Deployment
```bash
git push origin main
# Automatically deploys to production environment
```

### Manual Deployment
```bash
# Go to Actions tab in GitHub
# Select "Deploy to Streamlit Cloud"
# Click "Run workflow"
# Choose environment (staging/production)
```

## 📈 Monitoring & Observability

### GitHub Actions
- View workflow runs in the "Actions" tab
- Check artifact downloads for reports
- Monitor workflow duration and success rates

### SonarCloud Dashboard
- Code quality metrics and trends
- Security hotspots and vulnerabilities
- Technical debt analysis

### Streamlit App Health
- Health check endpoint: `/_stcore/health`
- Application metrics in Streamlit Cloud dashboard

## 🐛 Troubleshooting

### Common Issues

#### Tests Failing Locally
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run specific test
pytest tests/test_specific.py -v

# Debug with verbose output
pytest tests/ -v -s
```

#### Code Quality Issues
```bash
# Auto-fix formatting
black .
isort .

# Check specific issues
flake8 . --show-source
mypy . --show-error-codes
```

#### Docker Build Issues
```bash
# Test local build
docker build -t campus-management .
docker run -p 8501:8501 campus-management

# Check logs
docker logs <container_id>
```

#### Deployment Issues
```bash
# Check Streamlit Cloud logs
# Verify environment variables
# Check application health endpoint
```

### Getting Help

1. **GitHub Issues**: Report bugs and feature requests
2. **Discussions**: Ask questions and share ideas
3. **Wiki**: Extended documentation and guides
4. **Code Review**: Request reviews for complex changes

## 📝 Contributing to CI/CD

### Adding New Workflows
1. Create workflow file in `.github/workflows/`
2. Follow existing naming conventions
3. Add comprehensive documentation
4. Test thoroughly before merging

### Modifying Quality Gates
1. Update thresholds in workflow files
2. Update documentation
3. Communicate changes to team
4. Monitor impact after deployment

### Adding New Tools
1. Update `requirements.txt`
2. Add tool configuration files
3. Update workflows to include new tool
4. Add documentation

## 🔒 Security Best Practices

1. **Secrets Management**: Never commit secrets to code
2. **Dependency Updates**: Regular updates via Dependabot
3. **Access Control**: Limit who can modify workflows
4. **Audit Logs**: Regular review of workflow changes
5. **Branch Protection**: Require status checks before merge

## 📊 Performance Optimization

### Workflow Performance
- Use cache for dependencies
- Parallel job execution where possible
- Conditional job execution
- Artifact management

### Build Performance
- Multi-stage Docker builds
- Layer caching
- Minimal base images
- Dependency optimization

---

For more information, see the [GitHub Actions Documentation](https://docs.github.com/en/actions) and [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app).