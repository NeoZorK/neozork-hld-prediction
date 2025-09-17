#!/bin/bash

# NeoZork Pocket Hedge Fund - Database Setup Script
# This script sets up PostgreSQL database for the Pocket Hedge Fund system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="neozork_fund"
DB_USER="neozork_user"
DB_PASSWORD="neozork_password"
DB_HOST="localhost"
DB_PORT="5432"

echo -e "${BLUE}🚀 NeoZork Pocket Hedge Fund - Database Setup${NC}"
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

# Check if PostgreSQL is installed
check_postgresql() {
    print_info "Checking PostgreSQL installation..."
    
    if command -v psql &> /dev/null; then
        print_status "PostgreSQL is installed"
        psql --version
    else
        print_error "PostgreSQL is not installed"
        echo ""
        echo "Please install PostgreSQL:"
        echo "  macOS: brew install postgresql"
        echo "  Ubuntu: sudo apt-get install postgresql postgresql-contrib"
        echo "  CentOS: sudo yum install postgresql postgresql-server"
        exit 1
    fi
}

# Check if PostgreSQL service is running
check_postgresql_service() {
    print_info "Checking PostgreSQL service..."
    
    if pg_isready -h $DB_HOST -p $DB_PORT &> /dev/null; then
        print_status "PostgreSQL service is running"
    else
        print_warning "PostgreSQL service is not running"
        echo ""
        echo "Please start PostgreSQL service:"
        echo "  macOS: brew services start postgresql"
        echo "  Ubuntu: sudo systemctl start postgresql"
        echo "  CentOS: sudo systemctl start postgresql"
        exit 1
    fi
}

# Create database and user
create_database() {
    print_info "Creating database and user..."
    
    # Create user if it doesn't exist
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || print_warning "User $DB_USER already exists"
    
    # Create database if it doesn't exist
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || print_warning "Database $DB_NAME already exists"
    
    # Grant privileges
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    
    print_status "Database and user created successfully"
}

# Run database schema
run_schema() {
    print_info "Running database schema..."
    
    if [ -f "src/pocket_hedge_fund/database/schema.sql" ]; then
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f src/pocket_hedge_fund/database/schema.sql
        print_status "Database schema applied successfully"
    else
        print_error "Schema file not found: src/pocket_hedge_fund/database/schema.sql"
        exit 1
    fi
}

# Test database connection
test_connection() {
    print_info "Testing database connection..."
    
    if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" &> /dev/null; then
        print_status "Database connection successful"
    else
        print_error "Database connection failed"
        exit 1
    fi
}

# Show database info
show_database_info() {
    print_info "Database Information:"
    echo "  Host: $DB_HOST"
    echo "  Port: $DB_PORT"
    echo "  Database: $DB_NAME"
    echo "  User: $DB_USER"
    echo "  Password: $DB_PASSWORD"
    echo ""
    
    print_info "Connection string:"
    echo "  postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    echo ""
}

# Main execution
main() {
    echo "Starting database setup..."
    echo ""
    
    check_postgresql
    echo ""
    
    check_postgresql_service
    echo ""
    
    create_database
    echo ""
    
    run_schema
    echo ""
    
    test_connection
    echo ""
    
    show_database_info
    
    print_status "Database setup completed successfully!"
    echo ""
    echo "🎉 You can now run the Pocket Hedge Fund application:"
    echo "   uv run python run_pocket_hedge_fund.py"
    echo ""
    echo "📚 API Documentation will be available at:"
    echo "   http://localhost:8080/docs"
    echo ""
}

# Run main function
main "$@"
