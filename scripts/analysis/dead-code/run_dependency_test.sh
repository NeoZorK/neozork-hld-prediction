#!/bin/bash

# Dependency Test Analyzer Runner
# ===============================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

echo -e "${BLUE}🧪 Dependency Test Analyzer${NC}"
echo "=============================="
echo -e "Project root: ${CYAN}$PROJECT_ROOT${NC}"

# Detect environment
if [ -f /.dockerenv ]; then
    echo -e "${YELLOW}🐳 Running in Docker environment${NC}"
    ENVIRONMENT="docker"
    PYTHON_CMD="python"
elif [ -f /.container ]; then
    echo -e "${YELLOW}📦 Running in Container environment${NC}"
    ENVIRONMENT="container"
    PYTHON_CMD="python"
else
    echo -e "${GREEN}💻 Running in native environment${NC}"
    ENVIRONMENT="native"
    PYTHON_CMD="uv run python"
fi

# Function to show help
show_help() {
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "This tool tests dependencies by temporarily disabling them and running tests"
    echo "to determine which packages are actually needed."
    echo ""
    echo "Options:"
    echo "  --environment ENV     Test environment (native, docker, container)"
    echo "  --test-type TYPE      Type of tests (pytest, mcp, all)"
    echo "  --packages PKG1 PKG2  Specific packages to test"
    echo "  --dry-run             Show what would be tested without running"
    echo "  --verbose             Verbose output"
    echo "  --json                Output in JSON format"
    echo "  --output-file FILE    Output file path"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --dry-run"
    echo "  $0 --test-type pytest --verbose"
    echo "  $0 --environment docker --test-type all"
    echo "  $0 --packages numpy pandas --json --output-file results.json"
    echo ""
    echo "Test Types:"
    echo "  pytest    - Run pytest tests only"
    echo "  mcp       - Run MCP server tests only"
    echo "  all       - Run both pytest and MCP tests (default)"
    echo ""
    echo "Environments:"
    echo "  native    - Local environment with uv"
    echo "  docker    - Docker container"
    echo "  container - Podman container"
    echo ""
}

# Function to run dependency test
run_dependency_test() {
    local environment="$1"
    local test_type="$2"
    local packages="$3"
    local dry_run="$4"
    local verbose="$5"
    local json_output="$6"
    local output_file="$7"
    
    echo ""
    echo -e "${BLUE}Running dependency test analysis...${NC}"
    
    # Build command
    local cmd="$PYTHON_CMD scripts/analysis/dead-code/dependency_test_analyzer.py"
    
    if [ -n "$environment" ]; then
        cmd="$cmd --environment $environment"
    fi
    
    if [ -n "$test_type" ]; then
        cmd="$cmd --test-type $test_type"
    fi
    
    if [ -n "$packages" ]; then
        cmd="$cmd --packages $packages"
    fi
    
    if [ "$dry_run" = true ]; then
        cmd="$cmd --dry-run"
    fi
    
    if [ "$verbose" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    if [ "$json_output" = true ]; then
        cmd="$cmd --output-format json"
        if [ -n "$output_file" ]; then
            cmd="$cmd --output-file $output_file"
        fi
    fi
    
    # Run the analysis
    eval "$cmd"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependency test analysis completed!${NC}"
        if [ -n "$output_file" ] && [ "$json_output" = true ]; then
            echo -e "${GREEN}📁 Results saved to: $output_file${NC}"
        fi
    else
        echo -e "${RED}❌ Dependency test analysis failed!${NC}"
        return 1
    fi
}

# Function to show interactive menu
show_interactive_menu() {
    echo ""
    echo -e "${PURPLE}🧪 Dependency Test Analyzer Menu${NC}"
    echo "====================================="
    echo "Choose test configuration:"
    echo "1. Quick test (pytest only, dry run)"
    echo "2. Full test (all tests, dry run)"
    echo "3. Real test (all tests, actual execution)"
    echo "4. Custom configuration"
    echo "5. Exit"
    echo ""
    
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}Selected: Quick test (pytest only, dry run)${NC}"
            run_dependency_test "$ENVIRONMENT" "pytest" "" true false false ""
            ;;
        2)
            echo -e "${BLUE}Selected: Full test (all tests, dry run)${NC}"
            run_dependency_test "$ENVIRONMENT" "all" "" true false false ""
            ;;
        3)
            echo -e "${BLUE}Selected: Real test (all tests, actual execution)${NC}"
            echo -e "${YELLOW}⚠️  This will actually disable packages and run tests!${NC}"
            read -p "Are you sure? (y/n): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                run_dependency_test "$ENVIRONMENT" "all" "" false false false ""
            else
                echo -e "${GREEN}Cancelled.${NC}"
            fi
            ;;
        4)
            echo -e "${BLUE}Selected: Custom configuration${NC}"
            
            # Environment selection
            echo "Available environments:"
            echo "1. native (local)"
            echo "2. docker"
            echo "3. container"
            echo "4. auto-detect (current: $ENVIRONMENT)"
            read -p "Choose environment (1-4): " env_choice
            
            case $env_choice in
                1) custom_env="native" ;;
                2) custom_env="docker" ;;
                3) custom_env="container" ;;
                4) custom_env="" ;;
                *) custom_env="" ;;
            esac
            
            # Test type selection
            echo "Available test types:"
            echo "1. pytest"
            echo "2. mcp"
            echo "3. all"
            read -p "Choose test type (1-3): " test_choice
            
            case $test_choice in
                1) custom_test="pytest" ;;
                2) custom_test="mcp" ;;
                3) custom_test="all" ;;
                *) custom_test="all" ;;
            esac
            
            # Dry run selection
            read -p "Dry run? (y/n): " dry_choice
            custom_dry=false
            if [[ $dry_choice =~ ^[Yy]$ ]]; then
                custom_dry=true
            fi
            
            # Verbose selection
            read -p "Verbose output? (y/n): " verbose_choice
            custom_verbose=false
            if [[ $verbose_choice =~ ^[Yy]$ ]]; then
                custom_verbose=true
            fi
            
            # Output file
            read -p "Output file (leave empty for stdout): " output_file
            
            # JSON output
            custom_json=false
            if [ -n "$output_file" ]; then
                read -p "JSON output? (y/n): " json_choice
                if [[ $json_choice =~ ^[Yy]$ ]]; then
                    custom_json=true
                fi
            fi
            
            run_dependency_test "$custom_env" "$custom_test" "" "$custom_dry" "$custom_verbose" "$custom_json" "$output_file"
            ;;
        5)
            echo -e "${GREEN}Exiting...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please enter 1-5.${NC}"
            show_interactive_menu
            ;;
    esac
}

# Parse command line arguments
INTERACTIVE=false
ENVIRONMENT=""
TEST_TYPE=""
PACKAGES=""
DRY_RUN=false
VERBOSE=false
JSON_OUTPUT=false
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --test-type)
            TEST_TYPE="$2"
            shift 2
            ;;
        --packages)
            PACKAGES="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --output-file)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Show warning for real execution
if [ "$DRY_RUN" = false ] && [ "$INTERACTIVE" = false ]; then
    echo -e "${YELLOW}⚠️  WARNING: This will actually disable packages and run tests!${NC}"
    echo -e "${YELLOW}   Use --dry-run to see what would be tested without execution.${NC}"
    echo ""
    read -p "Continue? (y/n): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Cancelled.${NC}"
        exit 0
    fi
fi

# Run interactive menu if requested
if [ "$INTERACTIVE" = true ]; then
    show_interactive_menu
    exit 0
fi

# Use auto-detected environment if not specified
if [ -z "$ENVIRONMENT" ]; then
    ENVIRONMENT="$ENVIRONMENT"
fi

# Run the dependency test
run_dependency_test "$ENVIRONMENT" "$TEST_TYPE" "$PACKAGES" "$DRY_RUN" "$VERBOSE" "$JSON_OUTPUT" "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}💡 Next steps:${NC}"
echo "1. Review the dependency test results"
echo "2. Check which packages are truly unused"
echo "3. Consider removing unused packages"
echo "4. Test thoroughly after removing packages"
echo "5. Update requirements.txt if needed"
echo ""
echo -e "For more information, see the documentation in ${CYAN}docs/development/${NC}"
