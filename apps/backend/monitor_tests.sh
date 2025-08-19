#!/bin/bash

# Test Performance Monitor
# Monitors test execution times and generates performance reports

set -e

echo "🔍 LaVidaLuca Test Performance Monitor"
echo "======================================"

# Configuration
BACKEND_DIR="apps/backend"
REPORT_DIR="test-reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create reports directory
mkdir -p $REPORT_DIR

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to run tests and capture metrics
run_test_with_metrics() {
    local test_type="$1"
    local test_command="$2"
    local output_file="$REPORT_DIR/${test_type}_${TIMESTAMP}.json"
    
    echo -e "\n${BLUE}📊 Running $test_type tests with performance metrics...${NC}"
    
    # Record start time
    start_time=$(date +%s.%N)
    
    # Run tests with JSON output
    cd $BACKEND_DIR
    eval $test_command --json-report --json-report-file=../../$output_file || true
    cd - > /dev/null
    
    # Record end time
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    echo -e "${GREEN}✅ $test_type completed in ${duration}s${NC}"
    
    # Extract metrics if JSON report exists
    if [ -f "$output_file" ]; then
        echo "📈 Test metrics saved to: $output_file"
        
        # Extract key metrics using jq if available
        if command -v jq &> /dev/null; then
            total_tests=$(jq '.summary.total' $output_file 2>/dev/null || echo "N/A")
            passed_tests=$(jq '.summary.passed' $output_file 2>/dev/null || echo "N/A")
            failed_tests=$(jq '.summary.failed' $output_file 2>/dev/null || echo "N/A")
            
            echo "  Total tests: $total_tests"
            echo "  Passed: $passed_tests"
            echo "  Failed: $failed_tests"
            echo "  Duration: ${duration}s"
        fi
    fi
    
    return 0
}

# Function to generate performance summary
generate_performance_summary() {
    echo -e "\n${YELLOW}📋 Generating performance summary...${NC}"
    
    summary_file="$REPORT_DIR/performance_summary_${TIMESTAMP}.txt"
    
    cat > $summary_file << EOF
LaVidaLuca Backend Test Performance Report
Generated: $(date)
==========================================

Test Execution Summary:
EOF

    # Process all JSON reports
    for report in $REPORT_DIR/*_${TIMESTAMP}.json; do
        if [ -f "$report" ]; then
            test_type=$(basename "$report" | cut -d'_' -f1)
            echo "" >> $summary_file
            echo "$test_type Tests:" >> $summary_file
            echo "  Report: $(basename $report)" >> $summary_file
            
            if command -v jq &> /dev/null; then
                echo "  Total: $(jq '.summary.total // "N/A"' $report)" >> $summary_file
                echo "  Passed: $(jq '.summary.passed // "N/A"' $report)" >> $summary_file
                echo "  Failed: $(jq '.summary.failed // "N/A"' $report)" >> $summary_file
                echo "  Duration: $(jq '.duration // "N/A"' $report)s" >> $summary_file
            fi
        fi
    done
    
    cat >> $summary_file << EOF

Coverage Information:
  HTML Report: htmlcov/index.html
  XML Report: coverage.xml

Performance Notes:
  - Unit tests should complete in < 30 seconds
  - Integration tests should complete in < 60 seconds
  - Security tests should complete in < 45 seconds
  - Individual tests should take < 5 seconds each

Recommendations:
  - Tests taking > 5s should be optimized or marked as slow
  - Failed tests should be investigated immediately
  - Coverage should be maintained above 80%
EOF

    echo -e "${GREEN}✅ Performance summary saved to: $summary_file${NC}"
}

# Function to check test health
check_test_health() {
    echo -e "\n${BLUE}🏥 Checking test suite health...${NC}"
    
    cd $BACKEND_DIR
    
    # Check for slow tests
    echo "Identifying slow tests..."
    pytest --durations=10 --collect-only -q 2>/dev/null | head -20
    
    # Check test discovery
    echo -e "\nTest discovery check..."
    total_tests=$(pytest --collect-only -q 2>/dev/null | grep -c "test session starts" || echo "0")
    echo "Total discoverable tests: $total_tests"
    
    # Check for test dependencies
    echo -e "\nChecking test dependencies..."
    python -c "
import sys
required_packages = ['pytest', 'pytest_asyncio', 'httpx', 'factory_boy']
missing = []
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing.append(package)

if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
else:
    print('All required test packages are available')
" 2>/dev/null || echo "Some test dependencies may be missing"
    
    cd - > /dev/null
}

# Main execution
main() {
    # Check if we're in the right directory
    if [ ! -d "$BACKEND_DIR" ]; then
        echo "Error: Backend directory not found. Please run from project root."
        exit 1
    fi
    
    # Check test health first
    check_test_health
    
    # Run different test suites with metrics
    run_test_with_metrics "unit" "pytest -m 'not integration and not security and not performance' --durations=10"
    run_test_with_metrics "integration" "pytest -m integration --durations=10"
    run_test_with_metrics "security" "pytest -m security --durations=10"
    
    # Generate coverage report
    echo -e "\n${BLUE}📊 Generating coverage report...${NC}"
    cd $BACKEND_DIR
    pytest --cov=app --cov-report=html --cov-report=xml -m "not performance" > /dev/null 2>&1 || true
    cd - > /dev/null
    
    # Generate performance summary
    generate_performance_summary
    
    echo -e "\n${GREEN}🎉 Performance monitoring complete!${NC}"
    echo "Reports available in: $REPORT_DIR"
}

# Handle command line arguments
case "${1:-}" in
    --help)
        echo "Usage: $0 [--health-only]"
        echo ""
        echo "Options:"
        echo "  --health-only    Only run health checks"
        echo "  --help          Show this help message"
        exit 0
        ;;
    --health-only)
        check_test_health
        exit 0
        ;;
    *)
        main
        ;;
esac