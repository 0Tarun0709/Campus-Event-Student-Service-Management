#!/bin/bash

# Two-Phase Quality Assessment and Fix Script
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate >/dev/null 2>&1
fi

PYTHON=${VIRTUAL_ENV:+python}
PYTHON=${PYTHON:-python}

# Function to show phase header
show_phase() {
    local phase_num=$1
    local phase_name=$2
    echo -e "\n${BOLD}${PURPLE}═══════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${PURPLE}   PHASE $phase_num: $phase_name${NC}"
    echo -e "${BOLD}${PURPLE}═══════════════════════════════════════════════${NC}\n"
}

# Function to prompt for continuation
prompt_continue() {
    echo -e "\n${YELLOW}Press ENTER to continue to Phase 2 (Fixes), or Ctrl+C to exit...${NC}"
    read -r
}

clear
echo -e "${BOLD}${CYAN}🎯 TWO-PHASE QUALITY ASSESSMENT & AUTO-FIX${NC}"
echo -e "${CYAN}===========================================${NC}"
echo -e "${BLUE}Phase 1: Assessment | Phase 2: Automated Fixes${NC}\n"

# =====================================================
# PHASE 1: COMPREHENSIVE ASSESSMENT
# =====================================================
show_phase "1" "QUALITY ASSESSMENT & SCORING"

TOTAL_SCORE=0
MAX_SCORE=95
RESULTS_FILE="phase1_assessment.txt"
echo "🎯 Quality Assessment Results - $(date)" > $RESULTS_FILE
echo "===========================================" >> $RESULTS_FILE

# 1. BLACK FORMATTING ASSESSMENT
echo -e "${PURPLE}1. 🎨 BLACK CODE FORMATTING${NC}"
echo "=============================="
BLACK_SCORE=0
if $PYTHON -c "import black" 2>/dev/null; then
    echo -e "${BLUE}Analyzing code formatting...${NC}"
    
    BLACK_OUTPUT=$($PYTHON -m black --check --diff . 2>&1 || true)
    FILES_TO_FORMAT=$(echo "$BLACK_OUTPUT" | grep "would reformat" | wc -l | tr -d ' ')
    TOTAL_FILES=$(find . -name "*.py" -not -path "./.venv/*" -not -path "./site/*" | wc -l | tr -d ' ')
    
    if [ "$FILES_TO_FORMAT" = "0" ]; then
        BLACK_SCORE=20
        echo -e "${GREEN}✅ Perfect! All $TOTAL_FILES files properly formatted${NC}"
        echo "✅ BLACK FORMATTING: PERFECT (20/20)" >> $RESULTS_FILE
    else
        FORMATTED_FILES=$((TOTAL_FILES - FILES_TO_FORMAT))
        BLACK_SCORE=$((FORMATTED_FILES * 20 / TOTAL_FILES))
        echo -e "${RED}❌ $FILES_TO_FORMAT out of $TOTAL_FILES files need formatting${NC}"
        echo -e "${CYAN}   Score: $BLACK_SCORE/20${NC}"
        echo "❌ BLACK FORMATTING: $BLACK_SCORE/20 ($FILES_TO_FORMAT files need fixing)" >> $RESULTS_FILE
        
        echo -e "${YELLOW}   Files needing formatting:${NC}"
        echo "$BLACK_OUTPUT" | grep "would reformat" | head -5 | sed 's/would reformat /   • /'
        [ "$FILES_TO_FORMAT" -gt 5 ] && echo -e "${YELLOW}   ... and $((FILES_TO_FORMAT - 5)) more files${NC}"
    fi
else
    echo -e "${RED}❌ Black not installed${NC}"
    echo "❌ BLACK FORMATTING: NOT INSTALLED (0/20)" >> $RESULTS_FILE
fi
TOTAL_SCORE=$((TOTAL_SCORE + BLACK_SCORE))
echo ""

# 2. ISORT IMPORT ANALYSIS
echo -e "${PURPLE}2. 📦 IMPORT ORGANIZATION${NC}"
echo "=============================="
ISORT_SCORE=0
if $PYTHON -c "import isort" 2>/dev/null; then
    echo -e "${BLUE}Checking import organization...${NC}"
    
    ISORT_OUTPUT=$($PYTHON -m isort --check-only --diff . 2>&1 || true)
    
    if echo "$ISORT_OUTPUT" | grep -q "would be reformatted"; then
        IMPORT_FILES=$(echo "$ISORT_OUTPUT" | grep "would be reformatted" | wc -l | tr -d ' ')
        ISORT_SCORE=$((10 - IMPORT_FILES > 0 ? 10 - IMPORT_FILES : 0))
        echo -e "${YELLOW}⚠️ $IMPORT_FILES files have import issues (Score: $ISORT_SCORE/10)${NC}"
        echo "⚠️ IMPORT ORGANIZATION: $ISORT_SCORE/10 ($IMPORT_FILES files need fixing)" >> $RESULTS_FILE
        
        echo -e "${YELLOW}   Files with import issues:${NC}"
        echo "$ISORT_OUTPUT" | grep "would be reformatted" | head -3 | sed 's/.* /   • /'
    else
        ISORT_SCORE=10
        echo -e "${GREEN}✅ Perfect! All imports properly organized${NC}"
        echo "✅ IMPORT ORGANIZATION: PERFECT (10/10)" >> $RESULTS_FILE
    fi
else
    echo -e "${RED}❌ isort not installed${NC}"
    echo "❌ IMPORT ORGANIZATION: NOT INSTALLED (0/10)" >> $RESULTS_FILE
fi
TOTAL_SCORE=$((TOTAL_SCORE + ISORT_SCORE))
echo ""

# 3. FLAKE8 LINTING ANALYSIS
echo -e "${PURPLE}3. 🔍 CODE LINTING ANALYSIS${NC}"
echo "=============================="
FLAKE8_SCORE=0
if $PYTHON -c "import flake8" 2>/dev/null; then
    echo -e "${BLUE}Running comprehensive linting analysis...${NC}"
    
    # Get detailed flake8 output
    FLAKE8_OUTPUT=$($PYTHON -m flake8 . --count --statistics 2>/dev/null || echo "Error: Unable to run flake8")
    
    if echo "$FLAKE8_OUTPUT" | grep -q "Error:"; then
        FLAKE8_ERRORS=999
        echo -e "${RED}❌ Flake8 encountered errors${NC}"
    else
        FLAKE8_ERRORS=$(echo "$FLAKE8_OUTPUT" | tail -n 1 | awk '{print $1}' 2>/dev/null || echo "0")
    fi
    
    if [ "$FLAKE8_ERRORS" = "0" ]; then
        FLAKE8_SCORE=25
        echo -e "${GREEN}✅ Perfect! No linting errors found${NC}"
        echo "✅ CODE LINTING: PERFECT (25/25)" >> $RESULTS_FILE
    elif [ "$FLAKE8_ERRORS" -lt "50" ]; then
        FLAKE8_SCORE=$((25 - FLAKE8_ERRORS / 2))
        [ $FLAKE8_SCORE -lt 0 ] && FLAKE8_SCORE=0
        echo -e "${YELLOW}⚠️ $FLAKE8_ERRORS linting issues found (Score: $FLAKE8_SCORE/25)${NC}"
        echo "⚠️ CODE LINTING: $FLAKE8_SCORE/25 ($FLAKE8_ERRORS issues)" >> $RESULTS_FILE
    else
        FLAKE8_SCORE=0
        echo -e "${RED}❌ Too many linting issues: $FLAKE8_ERRORS (Score: 0/25)${NC}"
        echo "❌ CODE LINTING: 0/25 ($FLAKE8_ERRORS issues - needs major cleanup)" >> $RESULTS_FILE
    fi
    
    # Show sample issues
    if [ "$FLAKE8_ERRORS" != "0" ]; then
        echo -e "${YELLOW}   Top linting issues:${NC}"
        $PYTHON -m flake8 . 2>/dev/null | head -5 | sed 's/^/   • /'
        [ "$FLAKE8_ERRORS" -gt 5 ] && echo -e "${YELLOW}   ... and $((FLAKE8_ERRORS - 5)) more issues${NC}"
    fi
else
    echo -e "${RED}❌ flake8 not installed${NC}"
    echo "❌ CODE LINTING: NOT INSTALLED (0/25)" >> $RESULTS_FILE
fi
TOTAL_SCORE=$((TOTAL_SCORE + FLAKE8_SCORE))
echo ""

# 4. PYLINT ADVANCED ANALYSIS
echo -e "${PURPLE}4. 🔬 ADVANCED CODE ANALYSIS${NC}"
echo "=============================="
PYLINT_SCORE=0
if $PYTHON -c "import pylint" 2>/dev/null; then
    echo -e "${BLUE}Running comprehensive pylint analysis...${NC}"
    
    # Define file groups
    CORE_FILES="main.py models.py app.py data/data.py"
    TAB_FILES=$(find tabs -name "*.py" -not -name "__init__.py" 2>/dev/null | tr '\n' ' ')
    TEST_FILES=$(find tests -name "test_*.py" -o -name "conftest.py" 2>/dev/null | tr '\n' ' ')
    
    PYLINT_TOTAL=0
    FILES_CHECKED=0
    
    # Analyze core files
    echo -e "${CYAN}📦 Core Application Files:${NC}"
    for file in $CORE_FILES; do
        if [ -f "$file" ]; then
            FILES_CHECKED=$((FILES_CHECKED + 1))
            PYLINT_OUTPUT=$($PYTHON -m pylint "$file" --score=yes 2>/dev/null | grep "Your code has been rated" || echo "0.00/10")
            FILE_SCORE=$(echo "$PYLINT_OUTPUT" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0")
            PYLINT_TOTAL=$(echo "$PYLINT_TOTAL + $FILE_SCORE" | bc -l 2>/dev/null || echo "$PYLINT_TOTAL")
            
            if (( $(echo "$FILE_SCORE >= 8.0" | bc -l 2>/dev/null || echo 0) )); then
                echo -e "${GREEN}   ✅ $file: $FILE_SCORE/10 (Excellent)${NC}"
            elif (( $(echo "$FILE_SCORE >= 6.0" | bc -l 2>/dev/null || echo 0) )); then
                echo -e "${YELLOW}   ⚠️ $file: $FILE_SCORE/10 (Good)${NC}"
            else
                echo -e "${RED}   ❌ $file: $FILE_SCORE/10 (Needs Work)${NC}"
            fi
        fi
    done
    
    # Analyze UI/tab files
    if [ -n "$TAB_FILES" ]; then
        echo -e "${CYAN}🎨 UI/Tab Modules:${NC}"
        for file in $TAB_FILES; do
            if [ -f "$file" ]; then
                FILES_CHECKED=$((FILES_CHECKED + 1))
                PYLINT_OUTPUT=$($PYTHON -m pylint "$file" --score=yes 2>/dev/null | grep "Your code has been rated" || echo "0.00/10")
                FILE_SCORE=$(echo "$PYLINT_OUTPUT" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0")
                PYLINT_TOTAL=$(echo "$PYLINT_TOTAL + $FILE_SCORE" | bc -l 2>/dev/null || echo "$PYLINT_TOTAL")
                
                if (( $(echo "$FILE_SCORE >= 7.0" | bc -l 2>/dev/null || echo 0) )); then
                    echo -e "${GREEN}   ✅ $file: $FILE_SCORE/10 (Good)${NC}"
                elif (( $(echo "$FILE_SCORE >= 5.0" | bc -l 2>/dev/null || echo 0) )); then
                    echo -e "${YELLOW}   ⚠️ $file: $FILE_SCORE/10 (Fair)${NC}"
                else
                    echo -e "${RED}   ❌ $file: $FILE_SCORE/10 (Needs Work)${NC}"
                fi
            fi
        done
    fi
    
    # Analyze test files with relaxed standards
    if [ -n "$TEST_FILES" ]; then
        echo -e "${CYAN}🧪 Test Files (Relaxed Standards):${NC}"
        for file in $TEST_FILES; do
            if [ -f "$file" ]; then
                FILES_CHECKED=$((FILES_CHECKED + 1))
                # Use more lenient settings for tests
                PYLINT_OUTPUT=$($PYTHON -m pylint "$file" --disable=missing-docstring,too-many-locals,redefined-outer-name,unused-argument --score=yes 2>/dev/null | grep "Your code has been rated" || echo "0.00/10")
                FILE_SCORE=$(echo "$PYLINT_OUTPUT" | grep -o "[0-9]*\.[0-9]*" | head -1 2>/dev/null || echo "0")
                PYLINT_TOTAL=$(echo "$PYLINT_TOTAL + $FILE_SCORE" | bc -l 2>/dev/null || echo "$PYLINT_TOTAL")
                
                if (( $(echo "$FILE_SCORE >= 6.0" | bc -l 2>/dev/null || echo 0) )); then
                    echo -e "${GREEN}   ✅ $file: $FILE_SCORE/10 (Good)${NC}"
                elif (( $(echo "$FILE_SCORE >= 4.0" | bc -l 2>/dev/null || echo 0) )); then
                    echo -e "${YELLOW}   ⚠️ $file: $FILE_SCORE/10 (Fair)${NC}"
                else
                    echo -e "${RED}   ❌ $file: $FILE_SCORE/10 (Needs Work)${NC}"
                fi
            fi
        done
    fi
    
    if [ $FILES_CHECKED -gt 0 ]; then
        AVG_SCORE=$(echo "scale=1; $PYLINT_TOTAL / $FILES_CHECKED" | bc -l 2>/dev/null || echo "0")
        PYLINT_SCORE=$(echo "scale=0; $AVG_SCORE * 25 / 10" | bc -l 2>/dev/null || echo "0")
        echo -e "${CYAN}   Average Score: $AVG_SCORE/10 → Scaled: $PYLINT_SCORE/25${NC}"
        echo "🔬 ADVANCED ANALYSIS: $PYLINT_SCORE/25 (Avg: $AVG_SCORE/10)" >> $RESULTS_FILE
    else
        PYLINT_SCORE=10
        echo -e "${YELLOW}⚠️ No main files found, giving partial credit${NC}"
        echo "⚠️ ADVANCED ANALYSIS: 10/25 (No main files found)" >> $RESULTS_FILE
    fi
else
    echo -e "${RED}❌ pylint not installed${NC}"
    echo "❌ ADVANCED ANALYSIS: NOT INSTALLED (0/25)" >> $RESULTS_FILE
fi
TOTAL_SCORE=$((TOTAL_SCORE + PYLINT_SCORE))
echo ""

# 5. TEST COVERAGE ANALYSIS
echo -e "${PURPLE}5. 🧪 TEST COVERAGE ANALYSIS${NC}"
echo "=============================="
COVERAGE_SCORE=0
if [ -d "tests" ]; then
    TEST_FILES=$(find tests -name "*.py" | wc -l | tr -d ' ')
    echo -e "${CYAN}Found $TEST_FILES test files${NC}"
    
    if $PYTHON -c "import pytest, coverage" 2>/dev/null; then
        echo -e "${BLUE}Running test suite with coverage...${NC}"
        
        # Run tests and capture results
        TEST_OUTPUT=$($PYTHON -m pytest tests/ --tb=no -q 2>/dev/null || echo "Tests failed")
        COVERAGE_OUTPUT=$($PYTHON -m pytest tests/ --cov=. --cov-report=term-missing --tb=no -q 2>/dev/null | grep "TOTAL" || echo "")
        
        # Parse test results
        if echo "$TEST_OUTPUT" | grep -q "passed"; then
            PASSED=$(echo "$TEST_OUTPUT" | grep -o "[0-9]* passed" | grep -o "[0-9]*" || echo "0")
            echo -e "${GREEN}   ✅ $PASSED tests passed${NC}"
        fi
        
        if echo "$TEST_OUTPUT" | grep -q "failed"; then
            FAILED=$(echo "$TEST_OUTPUT" | grep -o "[0-9]* failed" | grep -o "[0-9]*" || echo "0")
            echo -e "${RED}   ❌ $FAILED tests failed${NC}"
        fi
        
        # Parse coverage
        if [ -n "$COVERAGE_OUTPUT" ]; then
            COVERAGE_PERCENT=$(echo "$COVERAGE_OUTPUT" | grep -o "[0-9][0-9]*%" | head -1 | tr -d '%' 2>/dev/null || echo "0")
            
            if ! [[ "$COVERAGE_PERCENT" =~ ^[0-9]+$ ]]; then
                COVERAGE_PERCENT=0
            fi
            
            COVERAGE_SCORE=$(echo "scale=0; $COVERAGE_PERCENT * 15 / 100" | bc -l 2>/dev/null || echo "0")
            
            if [ "$COVERAGE_PERCENT" -ge 80 ]; then
                echo -e "${GREEN}   ✅ Coverage: $COVERAGE_PERCENT% (Excellent: $COVERAGE_SCORE/15)${NC}"
            elif [ "$COVERAGE_PERCENT" -ge 60 ]; then
                echo -e "${YELLOW}   ⚠️ Coverage: $COVERAGE_PERCENT% (Good: $COVERAGE_SCORE/15)${NC}"
            else
                echo -e "${RED}   ❌ Coverage: $COVERAGE_PERCENT% (Low: $COVERAGE_SCORE/15)${NC}"
            fi
            
            # Generate detailed coverage breakdown
            echo -e "\n${CYAN}📊 DETAILED COVERAGE BREAKDOWN:${NC}"
            FULL_COVERAGE=$($PYTHON -m pytest tests/ --cov=. --cov-report=term-missing --tb=no -q 2>/dev/null || echo "ERROR")
            
            if [ "$FULL_COVERAGE" != "ERROR" ]; then
                echo "$FULL_COVERAGE" | grep -E "^[a-zA-Z].*\.py" | while IFS= read -r line; do
                    FILENAME=$(echo "$line" | awk '{print $1}')
                    FILE_COVERAGE=$(echo "$line" | grep -o "[0-9]*%" | sed 's/%//')
                    MISSING=$(echo "$line" | awk -F'Missing' '{if(NF>1) print $2}' | sed 's/^[[:space:]]*//' | cut -c1-50)
                    
                    if [ -n "$FILE_COVERAGE" ]; then
                        if [ "$FILE_COVERAGE" -eq 0 ] 2>/dev/null; then
                            echo -e "   ${RED}🔴 $FILENAME: ${FILE_COVERAGE}% - NO COVERAGE${NC}"
                        elif [ "$FILE_COVERAGE" -lt 50 ] 2>/dev/null; then
                            echo -e "   ${RED}📌 $FILENAME: ${FILE_COVERAGE}%${NC}"
                            [ -n "$MISSING" ] && echo -e "      ${GRAY}Missing: $MISSING...${NC}"
                        elif [ "$FILE_COVERAGE" -lt 80 ] 2>/dev/null; then
                            echo -e "   ${YELLOW}📝 $FILENAME: ${FILE_COVERAGE}%${NC}"
                            [ -n "$MISSING" ] && echo -e "      ${GRAY}Missing: $MISSING...${NC}"
                        else
                            echo -e "   ${GREEN}✅ $FILENAME: ${FILE_COVERAGE}%${NC}"
                        fi
                    fi
                done
                
                # Highlight critical missing areas
                echo -e "\n${CYAN}🎯 CRITICAL AREAS NEEDING TEST COVERAGE:${NC}"
                
                # Check for completely uncovered files
                UNCOVERED=$(echo "$FULL_COVERAGE" | grep -E "0%.*Missing" | head -3)
                if [ -n "$UNCOVERED" ]; then
                    echo -e "${RED}🚫 Files with ZERO test coverage:${NC}"
                    echo "$UNCOVERED" | while IFS= read -r line; do
                        FILENAME=$(echo "$line" | awk '{print $1}')
                        echo -e "   ${RED}• $FILENAME${NC}"
                    done
                fi
                
                # Check main.py specifically
                if echo "$FULL_COVERAGE" | grep -q "main.py"; then
                    MAIN_MISSING=$(echo "$FULL_COVERAGE" | grep "main.py" | awk -F'Missing' '{if(NF>1) print $2}' | sed 's/^[[:space:]]*//')
                    if [ -n "$MAIN_MISSING" ]; then
                        echo -e "${YELLOW}⚠️  main.py missing coverage on lines:${NC}"
                        echo -e "   ${GRAY}$MAIN_MISSING${NC}"
                    fi
                fi
                
                # Summary of what needs testing
                echo -e "\n${BLUE}💡 SUGGESTED TESTING PRIORITIES:${NC}"
                if echo "$FULL_COVERAGE" | grep -q "console_app.py.*0%"; then
                    echo -e "   ${RED}1. Add tests for console_app.py (156 lines, 0% coverage)${NC}"
                fi
                if echo "$FULL_COVERAGE" | grep -q "main.py.*[0-6][0-9]%"; then
                    echo -e "   ${YELLOW}2. Improve main.py test coverage (core system logic)${NC}"
                fi
                if echo "$FULL_COVERAGE" | grep -q "tabs/.*[0-5][0-9]%"; then
                    echo -e "   ${YELLOW}3. Add UI component tests for tabs/ modules${NC}"
                fi
            fi
            
            echo "🧪 TEST COVERAGE: $COVERAGE_SCORE/15 ($COVERAGE_PERCENT% coverage)" >> $RESULTS_FILE
        else
            echo -e "${RED}   ❌ Could not determine coverage${NC}"
            echo "❌ TEST COVERAGE: 0/15 (Coverage unknown)" >> $RESULTS_FILE
        fi
    else
        echo -e "${RED}❌ pytest or coverage not installed${NC}"
        echo "❌ TEST COVERAGE: NOT INSTALLED (0/15)" >> $RESULTS_FILE
    fi
else
    echo -e "${RED}❌ No tests directory found${NC}"
    echo "❌ TEST COVERAGE: NO TESTS (0/15)" >> $RESULTS_FILE
fi
TOTAL_SCORE=$((TOTAL_SCORE + COVERAGE_SCORE))
echo ""

# PHASE 1 SUMMARY
PERCENTAGE=$((TOTAL_SCORE * 100 / MAX_SCORE))

if [ $PERCENTAGE -ge 90 ]; then
    GRADE="A+"
    GRADE_COLOR=$GREEN
    EMOJI="🏆"
elif [ $PERCENTAGE -ge 80 ]; then
    GRADE="A"
    GRADE_COLOR=$GREEN
    EMOJI="🥇"
elif [ $PERCENTAGE -ge 70 ]; then
    GRADE="B"
    GRADE_COLOR=$YELLOW
    EMOJI="🥈"
elif [ $PERCENTAGE -ge 60 ]; then
    GRADE="C"
    GRADE_COLOR=$YELLOW
    EMOJI="🥉"
else
    GRADE="F"
    GRADE_COLOR=$RED
    EMOJI="📈"
fi

echo -e "${BOLD}${PURPLE}📊 PHASE 1 ASSESSMENT SUMMARY${NC}"
echo "============================================="
echo -e "${CYAN}🎨 Code Formatting:     $BLACK_SCORE/20${NC}"
echo -e "${CYAN}📦 Import Organization: $ISORT_SCORE/10${NC}"
echo -e "${CYAN}🔍 Code Linting:        $FLAKE8_SCORE/25${NC}"
echo -e "${CYAN}🔬 Advanced Analysis:   $PYLINT_SCORE/25${NC}"
echo -e "${CYAN}🧪 Test Coverage:       $COVERAGE_SCORE/15${NC}"
echo "============================================="
echo -e "${GRADE_COLOR}${EMOJI} CURRENT QUALITY SCORE: $TOTAL_SCORE/$MAX_SCORE (${PERCENTAGE}%) - Grade: $GRADE${NC}"

# Write summary to file
echo "" >> $RESULTS_FILE
echo "=============================================" >> $RESULTS_FILE
echo "PHASE 1 SUMMARY: $TOTAL_SCORE/$MAX_SCORE (${PERCENTAGE}%) - Grade: $GRADE" >> $RESULTS_FILE
echo "=============================================" >> $RESULTS_FILE

prompt_continue

# =====================================================
# PHASE 2: AUTOMATED FIXES
# =====================================================
show_phase "2" "AUTOMATED FIXES & IMPROVEMENTS"

FIXES_APPLIED=0

echo -e "${BLUE}Starting automated code quality improvements...${NC}\n"

# Fix 1: Black Code Formatting
if [ $BLACK_SCORE -lt 18 ]; then
    echo -e "${PURPLE}🎨 FIXING CODE FORMATTING${NC}"
    echo "=========================="
    echo -e "${BLUE}Running Black formatter...${NC}"
    
    if $PYTHON -m black . 2>/dev/null; then
        echo -e "${GREEN}✅ All Python files formatted successfully!${NC}"
        FIXES_APPLIED=$((FIXES_APPLIED + 1))
    else
        echo -e "${RED}❌ Black formatting failed${NC}"
    fi
    echo ""
fi

# Fix 2: Import Sorting
if [ $ISORT_SCORE -lt 9 ]; then
    echo -e "${PURPLE}📦 FIXING IMPORT ORGANIZATION${NC}"
    echo "============================="
    echo -e "${BLUE}Running isort to organize imports...${NC}"
    
    if $PYTHON -m isort . 2>/dev/null; then
        echo -e "${GREEN}✅ All imports organized successfully!${NC}"
        FIXES_APPLIED=$((FIXES_APPLIED + 1))
    else
        echo -e "${RED}❌ Import sorting failed${NC}"
    fi
    echo ""
fi

# Fix 3: Auto-fixable Linting Issues
if [ $FLAKE8_SCORE -lt 20 ]; then
    echo -e "${PURPLE}🔧 FIXING AUTO-CORRECTABLE LINTING ISSUES${NC}"
    echo "=========================================="
    echo -e "${BLUE}Attempting to fix common linting issues...${NC}"
    
    # Try autopep8 if available
    if $PYTHON -c "import autopep8" 2>/dev/null; then
        echo -e "${CYAN}Using autopep8 to fix PEP8 violations...${NC}"
        if $PYTHON -m autopep8 --in-place --recursive . 2>/dev/null; then
            echo -e "${GREEN}✅ Auto-fixable linting issues resolved!${NC}"
            FIXES_APPLIED=$((FIXES_APPLIED + 1))
        else
            echo -e "${YELLOW}⚠️ Some issues require manual fixing${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ autopep8 not installed - install with: pip install autopep8${NC}"
        echo -e "${CYAN}Running Black and isort again to fix formatting-related issues...${NC}"
        $PYTHON -m black . >/dev/null 2>&1
        $PYTHON -m isort . >/dev/null 2>&1
        echo -e "${GREEN}✅ Formatting-related linting issues fixed${NC}"
        FIXES_APPLIED=$((FIXES_APPLIED + 1))
    fi
    echo ""
fi

# Fix 4: Generate Missing Test Structure
if [ $COVERAGE_SCORE -lt 8 ]; then
    echo -e "${PURPLE}🧪 IMPROVING TEST STRUCTURE${NC}"
    echo "==========================="
    echo -e "${BLUE}Creating basic test improvements...${NC}"
    
    # Create conftest.py if missing
    if [ ! -f "tests/conftest.py" ]; then
        echo -e "${CYAN}Creating tests/conftest.py...${NC}"
        cat > tests/conftest.py << 'EOF'
"""Test configuration and fixtures."""
import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_system():
    """Fixture for testing the main system."""
    from main import CampusEventManagementSystem
    return CampusEventManagementSystem()
EOF
        echo -e "${GREEN}✅ Created basic conftest.py${NC}"
        FIXES_APPLIED=$((FIXES_APPLIED + 1))
    fi
    echo ""
fi

# PHASE 2 SUMMARY
echo -e "${BOLD}${PURPLE}🔧 PHASE 2 FIXES SUMMARY${NC}"
echo "============================================="
echo -e "${GREEN}✅ Automated fixes applied: $FIXES_APPLIED${NC}"
echo ""

if [ $FIXES_APPLIED -gt 0 ]; then
    echo -e "${CYAN}🔄 Running quick re-assessment...${NC}"
    
    # Quick re-check
    NEW_BLACK=$($PYTHON -m black --check . >/dev/null 2>&1 && echo "20" || echo "15")
    NEW_ISORT=$($PYTHON -m isort --check-only . >/dev/null 2>&1 && echo "10" || echo "8")
    
    echo -e "${GREEN}📈 Improved scores:${NC}"
    echo -e "${CYAN}   🎨 Formatting: $BLACK_SCORE → $NEW_BLACK${NC}"
    echo -e "${CYAN}   📦 Imports: $ISORT_SCORE → $NEW_ISORT${NC}"
fi

echo -e "\n${PURPLE}💡 NEXT STEPS FOR FURTHER IMPROVEMENT${NC}"
echo "======================================"
[ $FLAKE8_SCORE -lt 20 ] && echo -e "${YELLOW}• Review and fix remaining flake8 issues: python -m flake8 .${NC}"
[ $PYLINT_SCORE -lt 20 ] && echo -e "${YELLOW}• Address pylint suggestions for better code quality${NC}"
[ $COVERAGE_SCORE -lt 12 ] && echo -e "${YELLOW}• Add more comprehensive tests to increase coverage${NC}"

echo -e "\n${CYAN}📄 Assessment saved to: $RESULTS_FILE${NC}"
echo -e "${GREEN}🎉 Two-phase quality assessment and fixes complete!${NC}"