# Emergency Restart Service

## Overview

The Emergency Restart Service functionality provides a solution for handling container deletion failures in the NeoZork HLD Prediction native container management system. When the standard container stop process fails with the error "delete failed for one or more containers", the system now offers an automated recovery mechanism.

## Problem Description

Sometimes when stopping containers, you may encounter the following error:

```
Error: internalError: "delete failed for one or more containers: ["neozork-hld-prediction"]"
[ERROR] Failed to remove container
[WARNING] Cleanup completed (some resources may remain)
```

This typically indicates:
- A stuck container process
- Container service issues
- Resource conflicts
- System-level container management problems

## Solution: Emergency Restart Service

### Automatic Detection

The system now automatically detects container deletion failures and provides a recommended solution:

```
Error: Container deletion failed
This usually indicates a stuck container or service issue

Recommended emergency restart service, choose p4 "Restart service"
```

### Manual Restart Service Option

You can also manually trigger the restart service from the main menu:

```
Main Menu:
1) Start Container (Full Sequence)
2) Stop Container (Full Sequence)
3) Show Container Status
4) Restart Service
5) Help
0) Exit
```

### Restart Service Sequence

When you select "Restart Service" (option 4), the system executes the following sequence:

1. **Stop Container System**
   ```bash
   container system stop
   ```
   - Gracefully stops the container system
   - Releases all container resources
   - Clears stuck processes

2. **Start Container System**
   ```bash
   container system start
   ```
   - Restarts the container system
   - Reinitializes container management
   - Prepares for new container operations

3. **Check System Status**
   ```bash
   container system status
   ```
   - Verifies the system is running properly
   - Confirms all services are operational
   - Reports any remaining issues

### Automatic Retry After Restart

When the emergency restart is triggered automatically during container stop:

1. **Service Restart**: Executes the restart sequence above
2. **Container Stop Retry**: Attempts to stop the container again
3. **Final Cleanup**: Performs final resource cleanup
4. **Status Verification**: Confirms successful completion

## Usage Examples

### Interactive Mode

```bash
./scripts/native-container/native-container.sh
```

Then select option 4 for "Restart Service"

### Non-Interactive Mode

```bash
# Stop container system
container system stop

# Start container system  
container system start

# Check status
container system status
```

## Error Handling

### Automatic Recovery

The system automatically:
- Detects deletion failures
- Prompts for emergency restart
- Executes restart sequence
- Retries container operations
- Reports final status

### Manual Recovery

If automatic recovery fails:
1. Use option 4 "Restart Service" from main menu
2. Wait for completion
3. Try container operations again
4. Check system logs if issues persist

## Troubleshooting

### Common Issues

1. **Service Won't Stop**
   - Check for running containers: `container list`
   - Force stop containers: `container kill <container_id>`
   - Restart system if needed

2. **Service Won't Start**
   - Check system resources: `container system status`
   - Verify permissions and dependencies
   - Check system logs for errors

3. **Persistent Failures**
   - Restart the entire system
   - Check for conflicting processes
   - Verify container system installation

### Log Analysis

Check logs for detailed error information:
```bash
# System logs
sudo log show --predicate 'process == "container"' --last 1h

# Container logs
container logs <container_id>
```

## Integration

### With Existing Workflow

The emergency restart functionality integrates seamlessly with existing workflows:

- **Start Container**: No changes, works as before
- **Stop Container**: Enhanced with automatic error detection and recovery
- **Status Check**: Unchanged, provides current state
- **Help**: Updated with restart service documentation

### Script Integration

The functionality is implemented in:
- `scripts/native-container/native-container.sh` - Main interface
- `tests/native-container/test_emergency_restart.py` - Test coverage
- This documentation - User guide

## Testing

Run the emergency restart tests:

```bash
uv run pytest tests/native-container/test_emergency_restart.py -v
```

Test coverage includes:
- Function existence verification
- Menu option validation
- Error handling structure
- Script syntax validation
- Interactive prompt testing

## Best Practices

1. **Use Automatic Recovery**: Let the system handle most issues automatically
2. **Monitor Logs**: Check logs if issues persist after restart
3. **Verify Status**: Always check system status after restart
4. **Report Issues**: Document persistent problems for investigation

## Future Enhancements

Potential improvements:
- Automatic log analysis and reporting
- Enhanced error categorization
- Integration with system monitoring
- Automated health checks
- Performance optimization

## Support

For issues with the emergency restart functionality:
1. Check this documentation
2. Review system logs
3. Test with manual restart sequence
4. Report persistent issues with detailed logs 