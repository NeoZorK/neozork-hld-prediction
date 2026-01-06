# Ray Security Guidelines

## Overview

This document provides security guidelines for using Ray in the NeoZork HLD Prediction project, particularly regarding the Jobs Submission API vulnerability.

## Vulnerability Information

**Issue**: Ray allows arbitrary code execution via the jobs submission API  
**Affected Versions**: <= 2.49.2  
**Patched Version**: None (vendor considers this expected behavior)  
**Current Version**: 2.53.0 (safe, above vulnerable version)

**Note**: The vendor's position is that Ray is not intended for use outside of a strictly controlled network environment. This vulnerability is considered expected behavior when Ray is exposed to untrusted networks.

## Security Recommendations

### 1. Network Isolation

**CRITICAL**: Ray should only be used in a strictly controlled network environment.

- **Local Development**: Use Ray only on localhost (127.0.0.1)
- **Production**: Ensure Ray cluster is isolated from public networks
- **Network Segmentation**: Use firewalls and network policies to restrict access to Ray ports

### 2. Authentication

Enable authentication for Ray when network access is required:

```bash
export RAY_AUTH_MODE=token
```

This ensures that only authenticated users can interact with Ray interfaces, including:
- Dashboard
- Jobs API
- Cluster management interfaces

### 3. Firewall Configuration

Restrict access to Ray ports:

- **Default Ray ports**: 8265 (dashboard), 10001 (client), 6379 (Redis)
- **Production**: Block these ports from external access
- **Development**: Bind to localhost only

Example firewall rules:
```bash
# Block Ray ports from external access
iptables -A INPUT -p tcp --dport 8265 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 8265 -j DROP
iptables -A INPUT -p tcp --dport 10001 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 10001 -j DROP
```

### 4. Local Ray Initialization

In the project, Ray is initialized locally without network exposure:

```python
ray.init(
    num_cpus=torch.get_num_threads(),
    num_gpus=0,
    object_store_memory=2 * 1024 * 1024 * 1024,
    ignore_reinit_error=True
)
```

This is the **recommended** configuration for local development and single-machine usage.

### 5. Distributed Ray Clusters

If using distributed Ray clusters:

- **Private Network**: Deploy Ray cluster in a private network/VPC
- **VPN Access**: Require VPN for access to Ray cluster
- **Authentication**: Always enable `RAY_AUTH_MODE=token`
- **TLS/SSL**: Use encrypted connections for Ray communication
- **Access Control**: Implement network-level access controls

### 6. Jobs Submission API

**WARNING**: The Jobs Submission API should never be exposed to untrusted networks.

- **Local Only**: Use Jobs API only from trusted local processes
- **Authentication Required**: If network access is needed, require authentication
- **Input Validation**: Validate all job submission inputs
- **Sandboxing**: Consider running jobs in isolated containers/environments

### 7. Version Management

Current project configuration:

```toml
ray>=2.52.0,<2.54.0
```

This ensures:
- Version is above vulnerable version (2.49.2)
- Automatic updates within minor version range
- Compatibility with other dependencies

### 8. Production Deployment

For production environments:

1. **Network Isolation**: Deploy Ray in isolated network segment
2. **Authentication**: Enable `RAY_AUTH_MODE=token`
3. **Monitoring**: Monitor Ray cluster for unauthorized access attempts
4. **Logging**: Enable detailed logging for security auditing
5. **Updates**: Keep Ray updated to latest version within constraints

### 9. Development Best Practices

- **Local Development**: Always use local Ray initialization
- **Testing**: Test Ray functionality in isolated environments
- **Code Review**: Review any changes to Ray configuration
- **Documentation**: Document any network exposure of Ray

### 10. Incident Response

If Ray cluster is exposed to untrusted networks:

1. **Immediate**: Disconnect from network or shut down Ray cluster
2. **Assessment**: Review logs for unauthorized access
3. **Containment**: Isolate affected systems
4. **Remediation**: Apply network restrictions and authentication
5. **Monitoring**: Increase monitoring for suspicious activity

## References

- [Ray Security Documentation](https://docs.ray.io/en/latest/ray-core/security.html)
- [Ray Authentication](https://docs.ray.io/en/latest/ray-core/security.html#authentication)
- Project: `pyproject.toml` - Ray version constraints
- Code: `schr-levels-gluon.py` - Ray initialization

## Last Updated

2025-01-XX - Initial security guidelines for Ray Jobs Submission API vulnerability

