#!/bin/bash

# Simple activation script for the project
if [ -f ".venv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo "Python: $(which python)"
    echo "Python version: $(python --version)"
    echo ""
    echo "Available commands:"
    echo "  make help          - Show all make targets"
    echo "  make run          - Run the Streamlit app"
    echo "  make test         - Run tests"
    echo "  make qa           - Run quality checks"
    echo "  ./qa.sh           - Run quality assurance"
    echo ""
else
    echo "❌ Virtual environment not found!"
    echo "Run ./setup-dev.sh first to set up the development environment."
fi