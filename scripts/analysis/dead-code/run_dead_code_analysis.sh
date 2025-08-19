#!/bin/bash

# Dead Code and Libraries Analysis Runner
# This script runs comprehensive analysis to find dead code and unused libraries

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

echo -e "${BLUE}🔍 Dead Code and Libraries Analysis${NC}"
echo -e "${BLUE}=====================================${NC}"
echo "Project root: $PROJECT_ROOT"
echo ""

# Check if we're in a Docker container or native environment
if [ -f /.dockerenv ] || [ -f /run/.containerenv ]; then
    echo -e "${YELLOW}🐳 Running in Docker container${NC}"
    PYTHON_CMD="python"
else
    echo -e "${GREEN}💻 Running in native environment${NC}"
    PYTHON_CMD="uv run python"
fi

# Function to run analysis
run_analysis() {
    local analysis_type="$1"
    local output_file="$2"
    
    echo -e "${BLUE}Running $analysis_type analysis...${NC}"
    
    if [ -n "$output_file" ]; then
        $PYTHON_CMD scripts/analysis/dead-code/dead_code_analyzer.py --$analysis_type --output-file "$output_file"
        echo -e "${GREEN}Results saved to: $output_file${NC}"
    else
        $PYTHON_CMD scripts/analysis/dead-code/dead_code_analyzer.py --$analysis_type
    fi
}

# Parse command line arguments
ANALYZE_DEAD_CODE=false
ANALYZE_DEAD_LIBRARIES=false
ANALYZE_DEAD_FILES=false
RUN_ALL=false
OUTPUT_DIR=""
VERBOSE=false
FIX_ISSUES=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dead-code)
            ANALYZE_DEAD_CODE=true
            shift
            ;;
        --dead-libraries)
            ANALYZE_DEAD_LIBRARIES=true
            shift
            ;;
        --dead-files)
            ANALYZE_DEAD_FILES=true
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --fix)
            FIX_ISSUES=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dead-code          Analyze dead code (functions, classes, variables)"
            echo "  --dead-libraries     Analyze dead libraries (unused dependencies)"
            echo "  --dead-files         Analyze dead files (unused modules)"
            echo "  --all                Run all analyses"
            echo "  --output-dir DIR     Save results to directory"
            echo "  --verbose            Verbose output"
            echo "  --fix                Apply fixes after analysis"
            echo "  --dry-run            Show what would be fixed without applying"
            echo "  --help               Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --all"
            echo "  $0 --dead-libraries --output-dir ./results"
            echo "  $0 --dead-code --dead-files --verbose"
            echo "  $0 --all --fix --dry-run"
            echo "  $0 --all --fix"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Default to all analyses if none specified
if [ "$ANALYZE_DEAD_CODE" = false ] && [ "$ANALYZE_DEAD_LIBRARIES" = false ] && [ "$ANALYZE_DEAD_FILES" = false ] && [ "$RUN_ALL" = false ]; then
    RUN_ALL=true
fi

if [ "$RUN_ALL" = true ]; then
    ANALYZE_DEAD_CODE=true
    ANALYZE_DEAD_LIBRARIES=true
    ANALYZE_DEAD_FILES=true
fi

# Create output directory if specified
if [ -n "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo -e "${GREEN}Output directory: $OUTPUT_DIR${NC}"
fi

# Run analyses
echo ""
echo -e "${BLUE}Starting analysis...${NC}"
echo ""

# Run comprehensive analysis
ANALYSIS_ARGS=""
if [ "$ANALYZE_DEAD_CODE" = true ]; then
    ANALYSIS_ARGS="$ANALYSIS_ARGS --dead-code"
fi
if [ "$ANALYZE_DEAD_LIBRARIES" = true ]; then
    ANALYSIS_ARGS="$ANALYSIS_ARGS --dead-libraries"
fi
if [ "$ANALYZE_DEAD_FILES" = true ]; then
    ANALYSIS_ARGS="$ANALYSIS_ARGS --dead-files"
fi
if [ "$VERBOSE" = true ]; then
    ANALYSIS_ARGS="$ANALYSIS_ARGS --verbose"
fi

if [ -n "$OUTPUT_DIR" ]; then
    OUTPUT_FILE="$OUTPUT_DIR/dead_code_analysis.json"
    ANALYSIS_ARGS="$ANALYSIS_ARGS --output-format json --output-file $OUTPUT_FILE"
fi

echo -e "${BLUE}Running comprehensive analysis...${NC}"
$PYTHON_CMD scripts/analysis/dead-code/dead_code_analyzer.py $ANALYSIS_ARGS

echo ""
echo -e "${GREEN}✅ Analysis completed!${NC}"

if [ -n "$OUTPUT_DIR" ]; then
    echo -e "${GREEN}📁 Results saved to: $OUTPUT_FILE${NC}"
    
    # Create summary report
    SUMMARY_FILE="$OUTPUT_DIR/analysis_summary.txt"
    echo "Dead Code Analysis Summary" > "$SUMMARY_FILE"
    echo "Generated: $(date)" >> "$SUMMARY_FILE"
    echo "Project: $(basename "$PROJECT_ROOT")" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    
    if [ -f "$OUTPUT_FILE" ]; then
        echo "Detailed results: $OUTPUT_FILE" >> "$SUMMARY_FILE"
    fi
    
    echo -e "${GREEN}📋 Summary saved to: $SUMMARY_FILE${NC}"
fi

# Apply fixes if requested
if [ "$FIX_ISSUES" = true ] && [ -n "$OUTPUT_FILE" ] && [ -f "$OUTPUT_FILE" ]; then
    echo ""
    echo -e "${YELLOW}🔧 Applying fixes...${NC}"
    
    FIX_ARGS="--analysis-file $OUTPUT_FILE"
    if [ "$DRY_RUN" = true ]; then
        FIX_ARGS="$FIX_ARGS --dry-run"
    fi
    
    $PYTHON_CMD scripts/analysis/dead-code/fix_dead_code.py $FIX_ARGS
    
    if [ "$DRY_RUN" = false ]; then
        echo -e "${GREEN}✅ Fixes applied!${NC}"
    else
        echo -e "${YELLOW}🔍 Dry run completed - no changes made${NC}"
    fi
fi

echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "1. Review the analysis results"
echo "2. Consider removing unused code and libraries"
echo "3. Run tests to ensure nothing breaks"
echo "4. Use the fixer script to automatically apply fixes:"
echo "   $PYTHON_CMD scripts/analysis/dead-code/fix_dead_code.py --help"
echo ""
echo "For more information, see the documentation in docs/development/"
