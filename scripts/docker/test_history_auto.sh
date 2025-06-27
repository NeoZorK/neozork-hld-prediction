#!/bin/bash

# Get the project root directory (two levels up from scripts/docker/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "=== Automatic Docker History Test ==="

# Test history initialization in Docker
docker run --rm \
  -v "$PROJECT_ROOT/data:/app/data" \
  -v "$PROJECT_ROOT/logs:/app/logs" \
  -v "$PROJECT_ROOT/results:/app/results" \
  --user root \
  neozork-hld-prediction bash -c "
echo '=== Running container initialization ==='
/app/container-entrypoint.sh init

echo '=== Checking history setup ==='
echo 'HISTFILE: '\$HISTFILE
echo 'HISTSIZE: '\$HISTSIZE
echo 'HISTCONTROL: '\$HISTCONTROL

echo '=== Checking history file ==='
ls -la /tmp/bash_history/ 2>/dev/null || echo 'History directory not found'
cat /tmp/bash_history/.bash_history 2>/dev/null || echo 'History file not found'

echo '=== Testing history command ==='
history | head -10

echo '=== Testing history file content ==='
if [ -f /tmp/bash_history/.bash_history ]; then
    echo 'History file exists with content:'
    cat /tmp/bash_history/.bash_history
else
    echo 'History file does not exist'
fi
" 