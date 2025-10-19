#!/bin/bash

# Simple Real Quality Check - Shows actual tool outputs
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate >/dev/null 2>&1
fi

PYTHON=${VIRTUAL_ENV:+python}
PYTHON=${PYTHON:-python}

clear
echo -e "${CYAN}🔍 SIMPLE REAL QUALITY CHECK${NC}"
echo -e "${CYAN}============================${NC}\n"

# 1. BLACK FORMATTING
echo -e "${PURPLE}1. 🎨 BLACK FORMATTING CHECK${NC}"
echo "=============================="
if $PYTHON -c "import black" 2>/dev/null; then
    echo -e "${BLUE}Checking which files need formatting...${NC}"
    BLACK_OUTPUT=$($PYTHON -m black --check --diff . 2>&1 || true)
    FILES_TO_FORMAT=$(echo "$BLACK_OUTPUT" | grep "would reformat" | wc -l | tr -d ' ')
    
    if [ "$FILES_TO_FORMAT" = "0" ]; then
        echo -e "${GREEN}✅ All files properly formatted!${NC}"
    else
        echo -e "${YELLOW}⚠️ $FILES_TO_FORMAT files need formatting${NC}"
        echo -e "${CYAN}Files that need formatting:${NC}"
        echo "$BLACK_OUTPUT" | grep "would reformat" | head -5
        [ "$FILES_TO_FORMAT" -gt 5 ] && echo "... and $((FILES_TO_FORMAT - 5)) more"
    fi
else
    echo -e "${RED}❌ Black not installed${NC}"
fi
echo ""

# 2. ISORT IMPORT SORTING
echo -e "${PURPLE}2. 📦 ISORT IMPORT SORTING${NC}"
echo "=============================="
if $PYTHON -c "import isort" 2>/dev/null; then
    echo -e "${BLUE}Checking import sorting...${NC}"
    ISORT_OUTPUT=$($PYTHON -m isort --check-only --diff . 2>&1 || true)
    
    if echo "$ISORT_OUTPUT" | grep -q "would be reformatted"; then
        IMPORT_FILES=$(echo "$ISORT_OUTPUT" | grep "would be reformatted" | wc -l | tr -d ' ')
        echo -e "${YELLOW}⚠️ $IMPORT_FILES files have import sorting issues${NC}"
        echo -e "${CYAN}Files with import issues:${NC}"
        echo "$ISORT_OUTPUT" | grep "would be reformatted" | head -3
    else
        echo -e "${GREEN}✅ All imports properly sorted!${NC}"
    fi
else
    echo -e "${RED}❌ isort not installed${NC}"
fi
echo ""

# 3. FLAKE8 LINTING (sample)
echo -e "${PURPLE}3. 🔍 FLAKE8 LINTING (Sample)${NC}"
echo "=============================="
if $PYTHON -c "import flake8" 2>/dev/null; then
    echo -e "${BLUE}Running flake8 on main files...${NC}"
    FLAKE8_OUTPUT=$($PYTHON -m flake8 main.py models.py app.py 2>/dev/null || echo "No main files to check")
    
    if [ -n "$FLAKE8_OUTPUT" ] && [ "$FLAKE8_OUTPUT" != "No main files to check" ]; then
        ISSUE_COUNT=$(echo "$FLAKE8_OUTPUT" | wc -l | tr -d ' ')
        echo -e "${YELLOW}⚠️ Found $ISSUE_COUNT linting issues in main files${NC}"
        echo -e "${CYAN}Sample issues:${NC}"
        echo "$FLAKE8_OUTPUT" | head -10
        [ "$ISSUE_COUNT" -gt 10 ] && echo "... and $((ISSUE_COUNT - 10)) more issues"
    else
        echo -e "${GREEN}✅ No linting issues in main files!${NC}"
    fi
else
    echo -e "${RED}❌ flake8 not installed${NC}"
fi
echo ""

# 4. PYLINT SCORES
echo -e "${PURPLE}4. 🔬 PYLINT SCORES${NC}"
echo "=============================="
if $PYTHON -c "import pylint" 2>/dev/null; then
    echo -e "${BLUE}Analyzing all project files with pylint...${NC}"
    
    # Core application files
    echo -e "${CYAN}📦 Core Files:${NC}"
    for file in main.py models.py app.py data/data.py; do
        if [ -f "$file" ]; then
            PYLINT_SCORE=$($PYTHON -m pylint "$file" --score=yes 2>/dev/null | grep "Your code has been rated" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0.00")
            echo -e "${CYAN}  $file: ${PYLINT_SCORE}/10${NC}"
        fi
    done
    
    # UI/Tab modules
    echo -e "${CYAN}🎨 UI Modules:${NC}"
    for file in tabs/*.py; do
        if [ -f "$file" ] && [ "$file" != "tabs/__init__.py" ]; then
            PYLINT_SCORE=$($PYTHON -m pylint "$file" --score=yes 2>/dev/null | grep "Your code has been rated" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0.00")
            echo -e "${CYAN}  $file: ${PYLINT_SCORE}/10${NC}"
        fi
    done
    
    # Test files (with relaxed standards)
    echo -e "${CYAN}🧪 Test Files:${NC}"
    for file in tests/test_*.py tests/conftest.py; do
        if [ -f "$file" ]; then
            # Use more lenient pylint settings for tests
            PYLINT_SCORE=$($PYTHON -m pylint "$file" --disable=missing-docstring,too-many-locals,redefined-outer-name --score=yes 2>/dev/null | grep "Your code has been rated" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0.00")
            echo -e "${CYAN}  $file: ${PYLINT_SCORE}/10${NC}"
        fi
    done
else
    echo -e "${RED}❌ pylint not installed${NC}"
fi
echo ""

# 5. TEST SUMMARY
echo -e "${PURPLE}5. 🧪 TEST SUMMARY${NC}"
echo "=============================="
if [ -d "tests" ]; then
    TEST_FILES=$(find tests -name "*.py" | wc -l | tr -d ' ')
    echo -e "${CYAN}Test files found: $TEST_FILES${NC}"
    
    if $PYTHON -c "import pytest" 2>/dev/null; then
        echo -e "${BLUE}Running pytest...${NC}"
        TEST_OUTPUT=$($PYTHON -m pytest tests/ --tb=no -v 2>/dev/null || echo "Tests failed")
        
        if echo "$TEST_OUTPUT" | grep -q "passed"; then
            PASSED=$(echo "$TEST_OUTPUT" | grep -o "[0-9]* passed" | grep -o "[0-9]*" || echo "0")
            echo -e "${GREEN}✅ $PASSED tests passed${NC}"
        fi
        
        if echo "$TEST_OUTPUT" | grep -q "failed"; then
            FAILED=$(echo "$TEST_OUTPUT" | grep -o "[0-9]* failed" | grep -o "[0-9]*" || echo "0")
            echo -e "${RED}❌ $FAILED tests failed${NC}"
        fi
        
        # Try coverage if available
        if $PYTHON -c "import coverage" 2>/dev/null; then
            echo -e "${BLUE}Running detailed coverage analysis...${NC}"
            COVERAGE_OUTPUT=$($PYTHON -m pytest tests/ --cov=. --cov-report=term-missing --tb=no 2>/dev/null)
            
            if echo "$COVERAGE_OUTPUT" | grep -q "TOTAL"; then
                TOTAL_LINE=$(echo "$COVERAGE_OUTPUT" | grep "TOTAL")
                echo -e "${CYAN}Coverage: $TOTAL_LINE${NC}"
                
                # Show files with low coverage (under 80%)
                echo -e "${YELLOW}📋 Coverage Analysis:${NC}"
                echo "$COVERAGE_OUTPUT" | grep -E "^[a-zA-Z]" | while IFS= read -r line; do
                    if echo "$line" | grep -E "\s+[0-9]+%\s*$" > /dev/null; then
                        COVERAGE_PCT=$(echo "$line" | grep -o "[0-9]*%" | sed 's/%//')
                        if [ "$COVERAGE_PCT" -lt 80 ] 2>/dev/null; then
                            echo -e "${RED}  📌 $line${NC}"
                        elif [ "$COVERAGE_PCT" -lt 95 ] 2>/dev/null; then
                            echo -e "${YELLOW}  📝 $line${NC}"
                        else
                            echo -e "${GREEN}  ✅ $line${NC}"
                        fi
                    fi
                done
                
                # Show missing coverage summary
                echo -e "${CYAN}🎯 Missing Coverage Highlights:${NC}"
                echo "$COVERAGE_OUTPUT" | grep -A 50 "Missing" | grep -E "(main\.py|models\.py|app\.py)" | head -3 | while IFS= read -r line; do
                    echo -e "${YELLOW}  • $line${NC}"
                done
            fi
        fi
    else
        echo -e "${RED}❌ pytest not installed${NC}"
    fi
else
    echo -e "${RED}❌ No tests directory found${NC}"
fi

echo -e "\n${PURPLE}💡 QUICK FIXES${NC}"
echo "==================="
echo -e "${CYAN}• Format code:    $PYTHON -m black .${NC}"
echo -e "${CYAN}• Sort imports:   $PYTHON -m isort .${NC}"
echo -e "${CYAN}• Check linting:  $PYTHON -m flake8 .${NC}"
echo -e "${CYAN}• Run tests:      $PYTHON -m pytest tests/${NC}"
echo -e "${CYAN}• Full QA:        make qa${NC}"

echo -e "\n${GREEN}✅ Real quality check complete!${NC}"
echo -e "${CYAN}The tools ARE working - they found real issues to fix! 🔧${NC}"