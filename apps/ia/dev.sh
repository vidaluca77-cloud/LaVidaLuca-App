#!/bin/bash

# La Vida Luca API Development Helper Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_help() {
    echo "La Vida Luca API Development Helper"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup     - Initial setup (create venv, install deps)"
    echo "  install   - Install dependencies"
    echo "  dev       - Start development server"
    echo "  test      - Run test suite"
    echo "  init-db   - Initialize database with sample data"
    echo "  clean     - Clean up temporary files"
    echo "  help      - Show this help message"
}

setup() {
    echo -e "${YELLOW}Setting up La Vida Luca API...${NC}"
    
    # Create virtual environment
    echo "Creating virtual environment..."
    python -m venv .venv
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env with your actual configuration${NC}"
    fi
    
    echo -e "${GREEN}✅ Setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env with your database and API keys"
    echo "2. Run './dev.sh init-db' to initialize the database"
    echo "3. Run './dev.sh dev' to start the development server"
}

install() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    source .venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed!${NC}"
}

dev() {
    echo -e "${YELLOW}Starting development server...${NC}"
    source .venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

test() {
    echo -e "${YELLOW}Running tests...${NC}"
    source .venv/bin/activate
    python -m pytest tests/ -v
}

init_db() {
    echo -e "${YELLOW}Initializing database...${NC}"
    source .venv/bin/activate
    python init_db.py
}

clean() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf tests/__pycache__
    rm -rf app/__pycache__
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    rm -f test.db
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
}

# Main script logic
case $1 in
    setup)
        setup
        ;;
    install)
        install
        ;;
    dev)
        dev
        ;;
    test)
        test
        ;;
    init-db)
        init_db
        ;;
    clean)
        clean
        ;;
    help|--help|-h|"")
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac