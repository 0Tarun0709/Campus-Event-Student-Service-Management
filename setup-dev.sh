#!/bin/bash

# Development setup script for Campus Event Management System
set -e

echo "🚀 Setting up development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install --python .venv/bin/python -e ".[dev]"

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
.venv/bin/python -m pre_commit install

# Run initial tests to ensure everything works
echo "Running initial tests..."
.venv/bin/python -m pytest tests/ -v

echo "✅ Development environment setup complete!"
echo ""
echo "To activate the environment, run: source .venv/bin/activate"
echo "To run the app: .venv/bin/python -m streamlit run app.py"
echo "To run tests: .venv/bin/python -m pytest"
echo "To run quality checks: ./qa.sh"
echo "To use make commands: make help"