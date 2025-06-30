# Force Restart Container Service

This document describes the force restart functionality for the NeoZork HLD Prediction native container system.

## Overview

The force restart feature is designed to handle situations where the normal container stop process fails or hangs. It provides an automated way to restart the container service and retry the stop operation.

## Problem Statement

Sometimes when trying to stop a container using the normal `./scripts/native-container/native-container.sh` and selecting "Stop Container", the operation may fail or hang. This can happen due to:

1. Stuck container processes
2. Container service issues
3. Resource conflicts
4. Network connectivity problems

## Solution

The force restart functionality provides a comprehensive solution:

### Automatic Detection

The system automatically detects when a container stop operation fails by:
- Checking if the container is still running after a stop attempt
- Monitoring the exit status of the stop command
- Providing user feedback about the failure

### Interactive Recovery

When a stop failure is detected, the system:

1. **Shows an interactive prompt**: "Do you want to force restart container service then try delete container again?"
2. **If user confirms (y)**: Executes the force restart sequence
3. **If user declines (N)**: Continues with normal cleanup

### Force Restart Sequence

The force restart process follows these steps:

1. **Stop container service**: `container system stop`
2. **Wait for service to stop**: 3-second delay
3. **Start container service**: `container system start`
4. **Wait for service to start**: 5-second delay
5. **Verify service status**: `container system status`
6. **Retry container stop**: `./scripts/native-container/stop.sh`

## Usage

### Automatic Usage

The force restart is automatically triggered when:

1. Running `./scripts/native-container/native-container.sh`
2. Selecting "Stop Container"
3. The normal stop operation fails
4. User confirms the force restart prompt

### Manual Usage

You can also use the force restart script directly:

```bash
# Check container service status
./scripts/native-container/force_restart.sh --check

# Force restart with confirmation prompt
./scripts/native-container/force_restart.sh

# Force restart without confirmation
./scripts/native-container/force_restart.sh --force

# Show help
./scripts/native-container/force_restart.sh --help
```

## Script Location

- **Main script**: `./scripts/native-container/force_restart.sh`
- **Integration**: Integrated into `./scripts/native-container/native-container.sh`
- **Tests**: `./tests/native-container/test_force_restart.sh`

## Features

### Enhanced Shell with Ctrl+D Handling

The container shell now properly handles Ctrl+D (EOF) signals:

- **Graceful exit**: Ctrl+D is handled gracefully without hanging
- **Custom bashrc**: Prevents accidental Ctrl+D exits
- **Signal handlers**: Proper trap setup for EXIT, INT, TERM signals
- **Custom prompt**: Shows "(neozork-container)" prefix
- **User feedback**: Clear messages about exit methods

### Error Recovery

The system provides comprehensive error recovery:

- **Automatic detection**: Detects stuck containers automatically
- **User choice**: Interactive prompts for recovery actions
- **Service restart**: Automatic container service restart
- **Retry mechanism**: Automatic retry after service restart
- **Status verification**: Confirms service status after restart

## Testing

Run the force restart tests:

```bash
# Run force restart tests
./tests/native-container/test_force_restart.sh

# Run all native container tests
uv run pytest tests/native-container/ -n auto
```

## Troubleshooting

### Common Issues

1. **Service won't restart**: Check system resources and container service logs
2. **Permission denied**: Ensure script has execute permissions
3. **Container still stuck**: Manual intervention may be required

### Manual Recovery

If automatic recovery fails:

```bash
# Check container service status
container system status

# Manual service restart
container system stop
sleep 5
container system start

# Check container status
container list --all

# Force remove container if needed
container rm <container-id> --force
```

## Integration

The force restart functionality is seamlessly integrated into the main container management workflow:

1. **Normal operation**: Works transparently in the background
2. **Failure detection**: Automatically detects stop failures
3. **User interaction**: Provides clear prompts and choices
4. **Recovery**: Handles the entire recovery process
5. **Feedback**: Provides comprehensive status updates

## Future Enhancements

Potential improvements for future versions:

1. **Automatic retry**: Multiple retry attempts with exponential backoff
2. **Logging**: Enhanced logging for debugging
3. **Metrics**: Performance metrics for restart operations
4. **Configuration**: Configurable timeouts and retry counts
5. **Notifications**: System notifications for service events 