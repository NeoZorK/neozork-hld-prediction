# Smart Container Logic

## Overview

The interactive native container script now includes smart logic to handle different container states automatically, preventing errors when trying to start an already running container.

## Problem Solved

Previously, when users selected "Start Container" while a container was already running, the script would:
1. Try to remove the existing container
2. Fail with errors like "delete failed for one or more containers"
3. Require manual intervention

## New Smart Logic

The script now checks the container state and acts accordingly:

### 1. Container Already Running
```
[WARNING] Container is already running!
[INFO] Skipping setup and start steps...
[INFO] Opening interactive shell directly...
```
- Skips setup and start steps
- Opens shell directly
- No errors or manual intervention needed

### 2. Container Exists But Stopped
```
[WARNING] Container exists but is stopped
[INFO] Starting existing container...
```
- Starts the existing container
- Then opens shell
- No setup needed

### 3. Container Doesn't Exist
```
[INFO] Step 1: Running setup...
[INFO] Step 2: Starting container...
```
- Runs full setup sequence
- Creates new container
- Starts container
- Opens shell

## Benefits

1. **No More Errors**: Eliminates "delete failed" errors
2. **Faster Access**: Already running containers open shell immediately
3. **User-Friendly**: No manual intervention required
4. **Consistent Experience**: Same menu option works in all states

## Implementation

The logic is implemented in the `start_container_sequence()` function:

```bash
# Check if container already exists and is running
if check_container_exists && check_container_running; then
    # Skip setup, open shell directly
elif check_container_exists && ! check_container_running; then
    # Start existing container, then open shell
else
    # Run full setup sequence
fi
```

## Testing

Use the test script to verify the logic:
```bash
./scripts/native-container/test_smart_logic.sh
```

This script shows the current container state and what logic would be applied. 