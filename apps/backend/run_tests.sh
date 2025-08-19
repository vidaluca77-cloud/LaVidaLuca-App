#!/bin/bash

# LaVidaLuca Backend Test Runner
# Comprehensive test suite execution script

set -e  # Exit on any error

echo "🚀 LaVidaLuca Backend Test Suite"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
RUN_UNIT=true
RUN_INTEGRATION=true
RUN_SECURITY=true
RUN_PERFORMANCE=false
RUN_COVERAGE=true
FAIL_FAST=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit-only)
            RUN_UNIT=true
            RUN_INTEGRATION=false
            RUN_SECURITY=false
            shift
            ;;
        --integration-only)
            RUN_UNIT=false
            RUN_INTEGRATION=true
            RUN_SECURITY=false
            shift
            ;;
        --security-only)
            RUN_UNIT=false
            RUN_INTEGRATION=false
            RUN_SECURITY=true
            shift
            ;;
        --performance)
            RUN_PERFORMANCE=true
            shift
            ;;
        --no-coverage)
            RUN_COVERAGE=false
            shift
            ;;
        --fail-fast)
            FAIL_FAST=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --unit-only      Run only unit tests"
            echo "  --integration-only Run only integration tests"
            echo "  --security-only   Run only security tests"
            echo "  --performance     Include performance tests"
            echo "  --no-coverage     Skip coverage reporting"
            echo "  --fail-fast       Stop on first failure"
            echo "  --verbose         Verbose output"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to run tests with proper error handling
run_test_suite() {
    local test_name="$1"
    local test_command="$2"
    local color="$3"
    
    echo -e "\n${color}📋 Running $test_name...${NC}"
    echo "Command: $test_command"
    
    if $VERBOSE; then
        eval $test_command
    else
        eval $test_command > /tmp/test_output.log 2>&1
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $test_name passed${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name failed${NC}"
        if ! $VERBOSE; then
            echo "Error output:"
            cat /tmp/test_output.log
        fi
        return 1
    fi
}

# Function to check dependencies
check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"
    
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}❌ pytest not found. Please install: pip install pytest${NC}"
        exit 1
    fi
    
    if $RUN_COVERAGE && ! python -c "import pytest_cov" &> /dev/null; then
        echo -e "${YELLOW}⚠️  pytest-cov not found. Coverage reporting will be skipped.${NC}"
        RUN_COVERAGE=false
    fi
    
    if $RUN_PERFORMANCE && ! python -c "import locust" &> /dev/null; then
        echo -e "${YELLOW}⚠️  locust not found. Performance tests will be skipped.${NC}"
        RUN_PERFORMANCE=false
    fi
    
    echo -e "${GREEN}✅ Dependencies checked${NC}"
}

# Function to setup test environment
setup_test_env() {
    echo -e "${BLUE}🔧 Setting up test environment...${NC}"
    
    # Create test database if needed
    export ENVIRONMENT=testing
    export DATABASE_URL="sqlite:///./test.db"
    
    # Clean up previous test artifacts
    rm -rf htmlcov/
    rm -f coverage.xml
    rm -f .coverage
    rm -f test.db
    
    echo -e "${GREEN}✅ Test environment ready${NC}"
}

# Main test execution
main() {
    echo "Test Configuration:"
    echo "- Unit Tests: $RUN_UNIT"
    echo "- Integration Tests: $RUN_INTEGRATION"
    echo "- Security Tests: $RUN_SECURITY"
    echo "- Performance Tests: $RUN_PERFORMANCE"
    echo "- Coverage: $RUN_COVERAGE"
    echo "- Fail Fast: $FAIL_FAST"
    echo ""
    
    check_dependencies
    setup_test_env
    
    # Build pytest command
    PYTEST_ARGS="-v"
    
    if $FAIL_FAST; then
        PYTEST_ARGS="$PYTEST_ARGS -x"
    fi
    
    if $RUN_COVERAGE; then
        PYTEST_ARGS="$PYTEST_ARGS --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml"
    fi
    
    # Track test results
    FAILED_TESTS=()
    
    # Run test suites
    if $RUN_UNIT; then
        if ! run_test_suite "Unit Tests" "pytest $PYTEST_ARGS -m 'not integration and not security and not performance'" "$BLUE"; then
            FAILED_TESTS+=("Unit Tests")
            if $FAIL_FAST; then exit 1; fi
        fi
    fi
    
    if $RUN_INTEGRATION; then
        if ! run_test_suite "Integration Tests" "pytest $PYTEST_ARGS -m 'integration'" "$YELLOW"; then
            FAILED_TESTS+=("Integration Tests")
            if $FAIL_FAST; then exit 1; fi
        fi
    fi
    
    if $RUN_SECURITY; then
        if ! run_test_suite "Security Tests" "pytest $PYTEST_ARGS -m 'security' app/tests/test_security.py" "$RED"; then
            FAILED_TESTS+=("Security Tests")
            if $FAIL_FAST; then exit 1; fi
        fi
    fi
    
    # Run all remaining tests if no specific markers
    if $RUN_UNIT && $RUN_INTEGRATION && $RUN_SECURITY; then
        if ! run_test_suite "All Tests" "pytest $PYTEST_ARGS" "$GREEN"; then
            FAILED_TESTS+=("All Tests")
            if $FAIL_FAST; then exit 1; fi
        fi
    fi
    
    # Performance tests (separate because they're resource intensive)
    if $RUN_PERFORMANCE; then
        echo -e "\n${YELLOW}⚡ Performance tests should be run separately with Locust${NC}"
        echo "To run performance tests:"
        echo "  locust -f app/tests/test_performance.py --host=http://localhost:8000"
    fi
    
    # Generate reports
    if $RUN_COVERAGE; then
        echo -e "\n${BLUE}📊 Generating coverage reports...${NC}"
        if [ -f "htmlcov/index.html" ]; then
            echo -e "${GREEN}✅ HTML coverage report: htmlcov/index.html${NC}"
        fi
        if [ -f "coverage.xml" ]; then
            echo -e "${GREEN}✅ XML coverage report: coverage.xml${NC}"
        fi
    fi
    
    # Summary
    echo -e "\n${BLUE}📈 Test Summary${NC}"
    echo "==============="
    
    if [ ${#FAILED_TESTS[@]} -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}❌ Failed test suites:${NC}"
        for test in "${FAILED_TESTS[@]}"; do
            echo -e "${RED}  - $test${NC}"
        done
        exit 1
    fi
}

# Security scan function
security_scan() {
    echo -e "\n${RED}🔒 Running security scans...${NC}"
    
    # Bandit security scan
    if command -v bandit &> /dev/null; then
        echo "Running Bandit security scan..."
        bandit -r app/ -f json -o bandit-report.json || true
        bandit -r app/ || true
    else
        echo "Bandit not found. Install with: pip install bandit"
    fi
    
    # Safety check for known vulnerabilities
    if command -v safety &> /dev/null; then
        echo "Running Safety vulnerability check..."
        safety check --json --output safety-report.json || true
        safety check || true
    else
        echo "Safety not found. Install with: pip install safety"
    fi
}

# Run security scan if requested
if [[ "${1:-}" == "--security-scan" ]]; then
    security_scan
    exit 0
fi

# Run main test suite
main