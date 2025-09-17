#!/bin/bash

# NeoZork Pocket Hedge Fund - Start Script
# This script starts the Pocket Hedge Fund application with proper setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="NeoZork Pocket Hedge Fund"
APP_PORT=8080
DB_PORT=5432

echo -e "${PURPLE}🚀 $APP_NAME - Starting Up${NC}"
echo "=================================================="
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔄 $1${NC}"
}

# Check if .env file exists
check_env_file() {
    print_step "Checking environment configuration..."
    
    if [ -f ".env" ]; then
        print_status "Environment file found"
    else
        print_warning "Environment file not found, creating from example..."
        if [ -f "env.example" ]; then
            cp env.example .env
            print_status "Environment file created from example"
            print_warning "Please review and update .env file with your settings"
        else
            print_error "No environment example file found"
            exit 1
        fi
    fi
}

# Check if UV is installed
check_uv() {
    print_step "Checking UV installation..."
    
    if command -v uv &> /dev/null; then
        print_status "UV is installed"
        uv --version
    else
        print_error "UV is not installed"
        echo ""
        echo "Please install UV:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
}

# Check if PostgreSQL is running
check_postgresql() {
    print_step "Checking PostgreSQL connection..."
    
    if pg_isready -h localhost -p $DB_PORT &> /dev/null; then
        print_status "PostgreSQL is running"
    else
        print_warning "PostgreSQL is not running"
        echo ""
        echo "Starting PostgreSQL with Docker..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f docker-compose.db.yml up -d
            print_status "PostgreSQL started with Docker"
        else
            print_error "Docker Compose not found"
            echo "Please start PostgreSQL manually or install Docker Compose"
            exit 1
        fi
    fi
}

# Install dependencies
install_dependencies() {
    print_step "Installing dependencies..."
    
    uv pip install -r requirements.txt 2>/dev/null || {
        print_warning "requirements.txt not found, installing core dependencies..."
        uv pip install scikit-learn bcrypt pyotp "qrcode[pil]" fastapi uvicorn asyncpg psycopg2-binary sqlalchemy PyJWT
    }
    
    print_status "Dependencies installed"
}

# Run database setup
setup_database() {
    print_step "Setting up database..."
    
    if [ -f "scripts/setup_database.sh" ]; then
        chmod +x scripts/setup_database.sh
        ./scripts/setup_database.sh
        print_status "Database setup completed"
    else
        print_warning "Database setup script not found, skipping..."
    fi
}

# Run tests
run_tests() {
    print_step "Running tests..."
    
    if [ -f "test_pocket_hedge_fund_basic.py" ]; then
        uv run python test_pocket_hedge_fund_basic.py
        print_status "Tests passed"
    else
        print_warning "Test file not found, skipping tests..."
    fi
}

# Start application
start_application() {
    print_step "Starting application..."
    
    echo ""
    echo -e "${PURPLE}🎯 Application Information:${NC}"
    echo "  Name: $APP_NAME"
    echo "  Port: $APP_PORT"
    echo "  Environment: ${ENVIRONMENT:-development}"
    echo ""
    echo -e "${PURPLE}📚 API Documentation:${NC}"
    echo "  Swagger UI: http://localhost:$APP_PORT/docs"
    echo "  ReDoc: http://localhost:$APP_PORT/redoc"
    echo "  Health Check: http://localhost:$APP_PORT/health"
    echo ""
    echo -e "${PURPLE}🗄️ Database Management:${NC}"
    echo "  PgAdmin: http://localhost:5050"
    echo "  Username: admin@neozork.com"
    echo "  Password: admin123"
    echo ""
    echo -e "${GREEN}🚀 Starting application...${NC}"
    echo ""
    
    # Start the application
    uv run python run_pocket_hedge_fund.py
}

# Main execution
main() {
    echo "Starting $APP_NAME setup and launch..."
    echo ""
    
    check_env_file
    echo ""
    
    check_uv
    echo ""
    
    check_postgresql
    echo ""
    
    install_dependencies
    echo ""
    
    setup_database
    echo ""
    
    run_tests
    echo ""
    
    start_application
}

# Handle Ctrl+C
trap 'echo -e "\n${YELLOW}👋 Shutting down $APP_NAME...${NC}"; exit 0' INT

# Run main function
main "$@"
