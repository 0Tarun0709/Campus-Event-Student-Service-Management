#!/bin/bash

# UV Project Management Guide
echo "🔧 UV Usage Guide for this project"
echo "=================================="

echo ""
echo "📋 Current Setup:"
echo "  This project uses pyproject.toml with optional dependencies"
echo "  Virtual environment: .venv/"
echo ""

echo "✅ Correct Commands:"
echo ""
echo "1. 🏗️  Create virtual environment:"
echo "   uv venv .venv"
echo ""
echo "2. 📦 Install production dependencies:"
echo "   uv pip install --python .venv/bin/python -e ."
echo ""
echo "3. 🔧 Install development dependencies:"
echo "   uv pip install --python .venv/bin/python -e \".[dev]\""
echo ""
echo "4. 🧪 Install only test dependencies:"
echo "   uv pip install --python .venv/bin/python -e \".[test]\""
echo ""
echo "5. 🔒 Install security tools:"
echo "   uv pip install --python .venv/bin/python -e \".[security]\""
echo ""
echo "6. ⚡ Run commands with uv:"
echo "   uv run --python .venv/bin/python streamlit run app.py"
echo "   uv run --python .venv/bin/python pytest"
echo ""

echo "❌ Why 'uv sync' doesn't work here:"
echo "   - 'uv sync' is for projects with uv.lock files"
echo "   - It's used when uv fully manages the project"
echo "   - Our project uses traditional pyproject.toml approach"
echo ""

echo "🎯 Recommended Workflow:"
echo "   1. Use './setup-dev.sh' for initial setup"
echo "   2. Use 'make install-dev' for installing deps"
echo "   3. Use 'make run' to run the application"
echo "   4. Use 'source .venv/bin/activate' to activate manually"
echo ""

echo "🔄 To convert to full uv project management:"
echo "   1. Run: uv init --python 3.12"
echo "   2. This will create uv.lock and manage dependencies differently"
echo "   3. Then you can use 'uv sync' and 'uv run' commands"
echo ""

echo "📊 Current Virtual Environment Status:"
if [ -d ".venv" ]; then
    echo "   ✅ .venv directory exists"
    if [ -f ".venv/bin/python" ]; then
        echo "   ✅ Python executable found: $(.venv/bin/python --version)"
        echo "   📍 Location: $(pwd)/.venv/bin/python"
    else
        echo "   ❌ Python executable not found in .venv"
    fi
else
    echo "   ❌ .venv directory not found"
fi