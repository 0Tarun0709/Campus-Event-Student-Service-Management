# Getting Started

Welcome to the Campus Event Management System! This guide will help you get up and running quickly.

## Quick Setup

### Using Our Automated Setup

The fastest way to get started is using our automated setup script:

```bash
# Clone the repository
git clone <your-repo-url>
cd campus-event-management

# Run automated setup (creates virtual environment, installs dependencies, runs tests)
./setup-dev.sh
```

### Manual Setup

If you prefer manual setup or need more control:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with UV (recommended)
pip install uv
uv pip install --python .venv/bin/python -e ".[dev]"

# Or install with pip
pip install -e ".[dev]"

# Run tests to verify installation
pytest tests/ -v
```

## Running the Application

### Start the Streamlit App

```bash
# Using make command
make run

# Or directly
streamlit run app.py
```

The application will be available at http://localhost:8501

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Or use Docker directly
docker build -t campus-app .
docker run -p 8501:8501 campus-app
```

## Available Commands

We provide a comprehensive Makefile with common development tasks:

```bash
make help          # Show all available commands
make install-dev   # Install development dependencies
make test          # Run tests
make qa            # Run quality assurance checks
make format        # Format code with black and isort
make docs-serve    # Serve documentation locally
make clean         # Clean up build artifacts
```

## Project Structure

```
├── app.py              # Main Streamlit application
├── main.py             # Core system logic
├── models.py           # Data models
├── tabs/               # UI components
├── data/               # Data handling
├── tests/              # Test suite
├── docs/               # Documentation
└── .github/workflows/  # CI/CD pipelines
```

## Key Features

- **Student Management**: Add, update, and manage student records
- **Event Management**: Create and organize campus events
- **Registration System**: Handle event registrations
- **Analytics Dashboard**: View system analytics and reports
- **Request Management**: Handle student service requests

## Next Steps

- Explore the [CI/CD Migration Guide](ci-cd/migration-guide.md) to understand our modern development practices
- Check out the [Development Guide](development.md) for contributing guidelines
- Review the test suite in the `tests/` directory
- Try the different features in the web interface

## Need Help?

- Check our comprehensive documentation
- Run `make help` to see available commands
- Look at the test files for usage examples
- Review the CI/CD workflows for best practices