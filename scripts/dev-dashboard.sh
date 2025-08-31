#!/bin/bash

# LaVidaLuca Development Dashboard
# Real-time development status monitoring

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear_screen() {
    clear
}

print_header() {
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║               LaVidaLuca Development Dashboard                ║${NC}"
    echo -e "${CYAN}║                    100x Accelerated Development              ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_frontend_status() {
    echo -e "${BLUE}Frontend Status:${NC}"
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "  🟢 Web Server: ${GREEN}RUNNING${NC} (http://localhost:3000)"
    else
        echo -e "  🔴 Web Server: ${RED}NOT RUNNING${NC}"
    fi
    
    # Check if build works
    cd apps/web
    if npm run build > /dev/null 2>&1; then
        echo -e "  ✅ Build Status: ${GREEN}PASSING${NC}"
    else
        echo -e "  ❌ Build Status: ${RED}FAILING${NC}"
    fi
    
    # Check linting
    if npm run lint > /dev/null 2>&1; then
        echo -e "  ✅ Lint Status: ${GREEN}PASSING${NC}"
    else
        echo -e "  ⚠️  Lint Status: ${YELLOW}ISSUES${NC}"
    fi
    cd ../..
}

check_backend_status() {
    echo -e "${BLUE}Backend Status:${NC}"
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "  🟢 API Server: ${GREEN}RUNNING${NC} (http://localhost:8000)"
    elif curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo -e "  🟡 API Server: ${YELLOW}RUNNING${NC} (no health endpoint)"
    else
        echo -e "  🔴 API Server: ${RED}NOT RUNNING${NC}"
    fi
    
    # Check if tests pass
    cd apps/backend
    if python -m pytest --collect-only > /dev/null 2>&1; then
        if python -m pytest -x > /dev/null 2>&1; then
            echo -e "  ✅ Test Status: ${GREEN}PASSING${NC}"
        else
            echo -e "  ❌ Test Status: ${RED}FAILING${NC}"
        fi
    else
        echo -e "  ⚠️  Test Status: ${YELLOW}SYNTAX ERROR${NC}"
    fi
    cd ../..
}

check_development_tools() {
    echo -e "${BLUE}Development Tools:${NC}"
    
    # Check if concurrent processes are running
    if pgrep -f "concurrently" > /dev/null; then
        echo -e "  🟢 Concurrent Dev: ${GREEN}ACTIVE${NC}"
    else
        echo -e "  🔴 Concurrent Dev: ${RED}INACTIVE${NC}"
    fi
    
    # Check if pytest watch is running
    if pgrep -f "pytest.*looponfail" > /dev/null; then
        echo -e "  🟢 Test Watch: ${GREEN}ACTIVE${NC}"
    else
        echo -e "  🔴 Test Watch: ${RED}INACTIVE${NC}"
    fi
    
    # Check git status
    if git status --porcelain | grep -q .; then
        echo -e "  📝 Git Status: ${YELLOW}CHANGES${NC}"
    else
        echo -e "  ✅ Git Status: ${GREEN}CLEAN${NC}"
    fi
}

show_quick_commands() {
    echo -e "${PURPLE}Quick Commands:${NC}"
    echo -e "  ${GREEN}npm run dev:turbo${NC}    - Start full accelerated development"
    echo -e "  ${GREEN}npm run dev:full${NC}     - Start web + API + test watch"
    echo -e "  ${GREEN}npm run test:watch${NC}   - Start test watch mode"
    echo -e "  ${GREEN}npm run status${NC}       - Check all component status"
    echo -e "  ${GREEN}npm run validate${NC}     - Run full validation"
}

show_metrics() {
    echo -e "${YELLOW}Performance Metrics:${NC}"
    
    # Count lines of code
    if command -v cloc > /dev/null 2>&1; then
        total_lines=$(cloc --quiet --csv apps/ | tail -1 | cut -d',' -f5)
        echo -e "  📊 Total Lines: ${CYAN}${total_lines}${NC}"
    fi
    
    # Git commits today
    commits_today=$(git log --since="midnight" --oneline | wc -l)
    echo -e "  📈 Commits Today: ${CYAN}${commits_today}${NC}"
    
    # Last commit time
    last_commit=$(git log -1 --format="%cr")
    echo -e "  ⏰ Last Commit: ${CYAN}${last_commit}${NC}"
}

# Main loop
while true; do
    clear_screen
    print_header
    
    check_frontend_status
    echo ""
    
    check_backend_status
    echo ""
    
    check_development_tools
    echo ""
    
    show_metrics
    echo ""
    
    show_quick_commands
    echo ""
    
    echo -e "${CYAN}Dashboard refreshes every 10 seconds. Press Ctrl+C to exit.${NC}"
    echo -e "Last update: $(date '+%H:%M:%S')"
    
    sleep 10
done