#!/bin/bash

# Advanced Dead Code and Duplicate Code Analysis Runner
# ====================================================

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

echo -e "${BLUE}🔍 Advanced Dead Code and Duplicate Code Analysis${NC}"
echo "=================================================="
echo -e "Project root: ${CYAN}$PROJECT_ROOT${NC}"

# Detect environment
if [ -f /.dockerenv ]; then
    echo -e "${YELLOW}🐳 Running in Docker environment${NC}"
    PYTHON_CMD="python"
else
    echo -e "${GREEN}💻 Running in native environment${NC}"
    PYTHON_CMD="uv run python"
fi

# Function to show help
show_help() {
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dead-code          Analyze dead code (functions/classes never called)"
    echo "  --dead-libraries     Analyze dead libraries (unused dependencies)"
    echo "  --duplicate-code     Analyze duplicate code"
    echo "  --all                Run all analyses"
    echo "  --interactive        Use interactive menu"
    echo "  --output-dir DIR     Save results to directory"
    echo "  --verbose            Verbose output"
    echo "  --json               Output in JSON format"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --interactive"
    echo "  $0 --dead-code --verbose"
    echo "  $0 --all --output-dir ./results"
    echo "  $0 --duplicate-code --json --output-file results.json"
    echo ""
}

# Function to run analysis
run_analysis() {
    local analysis_type="$1"
    local output_dir="$2"
    local verbose="$3"
    local json_output="$4"
    
    echo ""
    echo -e "${BLUE}Running $analysis_type analysis...${NC}"
    
    # Build command
    local cmd="$PYTHON_CMD scripts/analysis/dead-code/advanced_dead_code_analyzer.py"
    
    case "$analysis_type" in
        "dead-code")
            cmd="$cmd --dead-code"
            ;;
        "dead-libraries")
            cmd="$cmd --dead-libraries"
            ;;
        "duplicate-code")
            cmd="$cmd --duplicate-code"
            ;;
        "all")
            cmd="$cmd --all"
            ;;
    esac
    
    if [ "$verbose" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    if [ "$json_output" = true ]; then
        cmd="$cmd --output-format json"
        if [ -n "$output_dir" ]; then
            cmd="$cmd --output-file $output_dir/advanced_analysis.json"
        fi
    fi
    
    # Run the analysis
    eval "$cmd"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $analysis_type analysis completed!${NC}"
        if [ -n "$output_dir" ] && [ "$json_output" = true ]; then
            echo -e "${GREEN}📁 Results saved to: $output_dir/advanced_analysis.json${NC}"
        fi
    else
        echo -e "${RED}❌ $analysis_type analysis failed!${NC}"
        return 1
    fi
}

# Function to show interactive menu
show_interactive_menu() {
    echo ""
    echo -e "${PURPLE}🔍 Advanced Dead Code Analysis Menu${NC}"
    echo "=========================================="
    echo "Choose what to analyze:"
    echo "1. Dead Code (functions/classes never called)"
    echo "2. Dead Libraries (unused dependencies)"
    echo "3. Duplicate Code (code duplication)"
    echo "4. All analyses"
    echo "5. Exit"
    echo ""
    
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}Selected: Dead Code Analysis${NC}"
            read -p "Verbose output? (y/n): " verbose_choice
            read -p "Save to directory? (leave empty for no): " output_dir
            read -p "JSON output? (y/n): " json_choice
            
            verbose=false
            if [[ $verbose_choice =~ ^[Yy]$ ]]; then
                verbose=true
            fi
            
            json_output=false
            if [[ $json_choice =~ ^[Yy]$ ]]; then
                json_output=true
            fi
            
            if [ -n "$output_dir" ]; then
                mkdir -p "$output_dir"
            fi
            
            run_analysis "dead-code" "$output_dir" "$verbose" "$json_output"
            ;;
        2)
            echo -e "${BLUE}Selected: Dead Libraries Analysis${NC}"
            read -p "Verbose output? (y/n): " verbose_choice
            read -p "Save to directory? (leave empty for no): " output_dir
            read -p "JSON output? (y/n): " json_choice
            
            verbose=false
            if [[ $verbose_choice =~ ^[Yy]$ ]]; then
                verbose=true
            fi
            
            json_output=false
            if [[ $json_choice =~ ^[Yy]$ ]]; then
                json_output=true
            fi
            
            if [ -n "$output_dir" ]; then
                mkdir -p "$output_dir"
            fi
            
            run_analysis "dead-libraries" "$output_dir" "$verbose" "$json_output"
            ;;
        3)
            echo -e "${BLUE}Selected: Duplicate Code Analysis${NC}"
            read -p "Verbose output? (y/n): " verbose_choice
            read -p "Save to directory? (leave empty for no): " output_dir
            read -p "JSON output? (y/n): " json_choice
            
            verbose=false
            if [[ $verbose_choice =~ ^[Yy]$ ]]; then
                verbose=true
            fi
            
            json_output=false
            if [[ $json_choice =~ ^[Yy]$ ]]; then
                json_output=true
            fi
            
            if [ -n "$output_dir" ]; then
                mkdir -p "$output_dir"
            fi
            
            run_analysis "duplicate-code" "$output_dir" "$verbose" "$json_output"
            ;;
        4)
            echo -e "${BLUE}Selected: All Analyses${NC}"
            read -p "Verbose output? (y/n): " verbose_choice
            read -p "Save to directory? (leave empty for no): " output_dir
            read -p "JSON output? (y/n): " json_choice
            
            verbose=false
            if [[ $verbose_choice =~ ^[Yy]$ ]]; then
                verbose=true
            fi
            
            json_output=false
            if [[ $json_choice =~ ^[Yy]$ ]]; then
                json_output=true
            fi
            
            if [ -n "$output_dir" ]; then
                mkdir -p "$output_dir"
            fi
            
            run_analysis "all" "$output_dir" "$verbose" "$json_output"
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
DEAD_CODE=false
DEAD_LIBRARIES=false
DUPLICATE_CODE=false
ALL=false
VERBOSE=false
JSON_OUTPUT=false
OUTPUT_DIR=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dead-code)
            DEAD_CODE=true
            shift
            ;;
        --dead-libraries)
            DEAD_LIBRARIES=true
            shift
            ;;
        --duplicate-code)
            DUPLICATE_CODE=true
            shift
            ;;
        --all)
            ALL=true
            shift
            ;;
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --output-file)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
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

# Create output directory if specified
if [ -n "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo -e "${GREEN}Output directory: ${CYAN}$OUTPUT_DIR${NC}"
fi

# Run interactive menu if requested
if [ "$INTERACTIVE" = true ]; then
    show_interactive_menu
    exit 0
fi

# Determine analysis type
ANALYSIS_TYPE=""
if [ "$ALL" = true ]; then
    ANALYSIS_TYPE="all"
elif [ "$DEAD_CODE" = true ]; then
    ANALYSIS_TYPE="dead-code"
elif [ "$DEAD_LIBRARIES" = true ]; then
    ANALYSIS_TYPE="dead-libraries"
elif [ "$DUPLICATE_CODE" = true ]; then
    ANALYSIS_TYPE="duplicate-code"
else
    # Default to interactive if no analysis type specified
    echo -e "${YELLOW}No analysis type specified. Starting interactive menu...${NC}"
    show_interactive_menu
    exit 0
fi

# Run the analysis
run_analysis "$ANALYSIS_TYPE" "$OUTPUT_DIR" "$VERBOSE" "$JSON_OUTPUT"

echo ""
echo -e "${GREEN}💡 Next steps:${NC}"
echo "1. Review the analysis results carefully"
echo "2. Check high-confidence items first"
echo "3. Verify public API functions before removal"
echo "4. Consider refactoring duplicate code"
echo "5. Run tests after any changes"
echo ""
echo -e "For more information, see the documentation in ${CYAN}docs/development/${NC}"
