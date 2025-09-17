# Kubernetes Troubleshooting Guide - English

This guide provides solutions to common issues encountered when deploying and managing the Neozork HLD Prediction project on Kubernetes.

## Table of Contents

1. [Pod Issues](#pod-issues)
2. [Service Connectivity](#service-connectivity)
3. [Storage Problems](#storage-problems)
4. [Resource Constraints](#resource-constraints)
5. [Network Issues](#network-issues)
6. [Configuration Problems](#configuration-problems)
7. [Security Issues](#security-issues)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Platform-Specific Issues](#platform-specific-issues)
10. [Performance Issues](#performance-issues)

## Pod Issues

### Pods Not Starting

**Symptoms:**
- Pods stuck in `Pending` or `ContainerCreating` state
- Pods repeatedly restarting
- Pods failing to start with error messages

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -l app=neozork-interactive

# Describe pod for detailed information
kubectl describe pod <pod-name>

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check pod logs
kubectl logs <pod-name> --previous
```

**Common Causes and Solutions:**

1. **Image Pull Errors**
   ```bash
   # Check if image exists and is accessible
   docker pull neozork-interactive:apple-latest
   
   # Verify image registry credentials
   kubectl get secrets
   kubectl describe secret <registry-secret>
   ```

2. **Resource Constraints**
   ```bash
   # Check node resources
   kubectl top nodes
   kubectl describe nodes
   
   # Check pod resource requests vs node capacity
   kubectl describe pod <pod-name> | grep -A 10 "Requests:"
   ```

3. **Node Selector Issues**
   ```bash
   # Check if nodes match selector
   kubectl get nodes --show-labels
   
   # Verify node architecture
   kubectl get nodes -o wide
   ```

### Pod Crash Loops

**Symptoms:**
- Pods continuously restarting
- High restart count
- Application crashes

**Diagnosis:**
```bash
# Check restart count
kubectl get pods -l app=neozork-interactive

# View crash logs
kubectl logs <pod-name> --previous

# Check container exit codes
kubectl describe pod <pod-name> | grep -A 5 "Last State"
```

**Solutions:**

1. **Application Errors**
   ```bash
   # Check application logs
   kubectl logs <pod-name> --tail=100
   
   # Debug with interactive shell
   kubectl exec -it <pod-name> -- /bin/bash
   ```

2. **Configuration Issues**
   ```bash
   # Verify environment variables
   kubectl exec <pod-name> -- env
   
   # Check mounted volumes
   kubectl exec <pod-name> -- ls -la /app/
   ```

3. **Resource Limits**
   ```bash
   # Check if pod is being killed due to resource limits
   kubectl describe pod <pod-name> | grep -A 10 "Events:"
   
   # Adjust resource limits if needed
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"4Gi","cpu":"2000m"}}}]}}}}'
   ```

## Service Connectivity

### Service Not Accessible

**Symptoms:**
- Cannot connect to service from outside cluster
- Service endpoints not found
- Connection timeouts

**Diagnosis:**
```bash
# Check service status
kubectl get services

# Check service endpoints
kubectl get endpoints

# Test service connectivity from within cluster
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -O- http://neozork-interactive-service:80/health
```

**Solutions:**

1. **Service Selector Issues**
   ```bash
   # Verify service selector matches pod labels
   kubectl get pods --show-labels
   kubectl describe service neozork-interactive-service
   ```

2. **Port Configuration**
   ```bash
   # Check if ports are correctly configured
   kubectl describe service neozork-interactive-service
   
   # Verify container ports
   kubectl describe pod <pod-name> | grep -A 5 "Ports:"
   ```

3. **LoadBalancer Issues**
   ```bash
   # Check LoadBalancer status
   kubectl get service neozork-interactive-service
   
   # Check for external IP assignment
   kubectl describe service neozork-interactive-service
   ```

### DNS Resolution Problems

**Symptoms:**
- Cannot resolve service names
- Inter-service communication failures

**Diagnosis:**
```bash
# Test DNS resolution from within cluster
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup neozork-interactive-service

# Check CoreDNS status
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

**Solutions:**
```bash
# Restart CoreDNS if needed
kubectl delete pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS configuration
kubectl get configmap -n kube-system coredns -o yaml
```

## Storage Problems

### Persistent Volume Issues

**Symptoms:**
- PVC stuck in `Pending` state
- Pods cannot mount volumes
- Data loss or corruption

**Diagnosis:**
```bash
# Check PVC status
kubectl get pvc

# Check PV status
kubectl get pv

# Check storage class
kubectl get storageclass
```

**Solutions:**

1. **Storage Class Issues**
   ```bash
   # Verify storage class exists
   kubectl get storageclass
   
   # Check storage class configuration
   kubectl describe storageclass fast-ssd
   ```

2. **Volume Provisioning**
   ```bash
   # Check for provisioner errors
   kubectl get events --sort-by=.metadata.creationTimestamp | grep -i volume
   
   # Check CSI driver status
   kubectl get pods -n kube-system | grep -i csi
   ```

3. **Volume Mount Issues**
   ```bash
   # Check volume mounts in pod
   kubectl describe pod <pod-name> | grep -A 10 "Mounts:"
   
   # Verify volume permissions
   kubectl exec <pod-name> -- ls -la /app/data
   ```

### Data Corruption

**Symptoms:**
- Application errors related to data access
- Inconsistent data state
- File system errors

**Solutions:**
```bash
# Check file system integrity
kubectl exec <pod-name> -- fsck /app/data

# Backup and restore data
kubectl exec <pod-name> -- tar czf /tmp/backup.tar.gz /app/data
kubectl cp <pod-name>:/tmp/backup.tar.gz ./backup.tar.gz
```

## Resource Constraints

### CPU and Memory Issues

**Symptoms:**
- Pods being killed due to resource limits
- Slow application performance
- High resource usage

**Diagnosis:**
```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Check resource requests and limits
kubectl describe pod <pod-name> | grep -A 10 "Requests:"
```

**Solutions:**

1. **Adjust Resource Limits**
   ```bash
   # Increase memory limits
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"8Gi"}}}]}}}}'
   
   # Increase CPU limits
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"cpu":"4000m"}}}]}}}}'
   ```

2. **Optimize Application**
   ```bash
   # Check for memory leaks
   kubectl exec <pod-name> -- ps aux
   
   # Monitor resource usage over time
   kubectl top pods --containers
   ```

### Node Resource Exhaustion

**Symptoms:**
- Pods stuck in `Pending` state
- No available nodes for scheduling

**Solutions:**
```bash
# Check node capacity
kubectl describe nodes

# Add more nodes to cluster
# (Cloud provider specific commands)

# Implement resource quotas
kubectl create quota neozork-quota --hard=cpu=4,memory=8Gi,pods=10
```

## Network Issues

### Network Policy Problems

**Symptoms:**
- Pods cannot communicate with each other
- External access blocked
- DNS resolution failures

**Diagnosis:**
```bash
# Check network policies
kubectl get networkpolicies

# Test connectivity between pods
kubectl exec <pod-1> -- ping <pod-2-ip>
```

**Solutions:**
```bash
# Temporarily disable network policies for testing
kubectl delete networkpolicy neozork-network-policy

# Update network policy rules
kubectl apply -f network-policy.yaml
```

### Ingress Issues

**Symptoms:**
- Cannot access application from outside
- SSL/TLS certificate errors
- Routing problems

**Diagnosis:**
```bash
# Check ingress status
kubectl get ingress

# Check ingress controller
kubectl get pods -n ingress-nginx
```

**Solutions:**
```bash
# Check ingress controller logs
kubectl logs -n ingress-nginx <ingress-controller-pod>

# Verify TLS certificates
kubectl describe secret neozork-tls
```

## Configuration Problems

### Environment Variable Issues

**Symptoms:**
- Application not starting
- Incorrect configuration values
- Missing environment variables

**Diagnosis:**
```bash
# Check environment variables in pod
kubectl exec <pod-name> -- env

# Check ConfigMap
kubectl get configmap app-config -o yaml
```

**Solutions:**
```bash
# Update ConfigMap
kubectl patch configmap app-config -p '{"data":{"LOG_LEVEL":"DEBUG"}}'

# Restart deployment to pick up changes
kubectl rollout restart deployment neozork-interactive-apple
```

### Secret Management Issues

**Symptoms:**
- Authentication failures
- Database connection errors
- Missing sensitive data

**Diagnosis:**
```bash
# Check secrets
kubectl get secrets

# Verify secret data (base64 encoded)
kubectl get secret app-secrets -o yaml
```

**Solutions:**
```bash
# Update secret
kubectl create secret generic app-secrets \
  --from-literal=database-password=new-password \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods to pick up new secrets
kubectl rollout restart deployment neozork-interactive-apple
```

## Security Issues

### RBAC Problems

**Symptoms:**
- Permission denied errors
- Service account issues
- Access control failures

**Diagnosis:**
```bash
# Check service account
kubectl get serviceaccount

# Check RBAC rules
kubectl get role,rolebinding,clusterrole,clusterrolebinding
```

**Solutions:**
```bash
# Create service account with proper permissions
kubectl create serviceaccount neozork-sa

# Create role and role binding
kubectl apply -f rbac.yaml
```

### Pod Security Issues

**Symptoms:**
- Pods failing to start due to security policies
- Permission denied errors
- Security context violations

**Solutions:**
```bash
# Check pod security policies
kubectl get psp

# Update security context
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"securityContext":{"runAsUser":1000,"runAsGroup":1000}}}}}'
```

## Monitoring and Logging

### Metrics Collection Issues

**Symptoms:**
- No metrics appearing in Prometheus
- Grafana dashboards not working
- ServiceMonitor not discovering targets

**Diagnosis:**
```bash
# Check ServiceMonitor
kubectl get servicemonitor

# Check Prometheus targets
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
# Open http://localhost:9090/targets
```

**Solutions:**
```bash
# Verify metrics endpoint
kubectl exec <pod-name> -- curl http://localhost:8080/metrics

# Check ServiceMonitor configuration
kubectl describe servicemonitor neozork-metrics
```

### Logging Problems

**Symptoms:**
- No logs appearing
- Log aggregation failures
- Log rotation issues

**Solutions:**
```bash
# Check log volume mounts
kubectl describe pod <pod-name> | grep -A 5 "Mounts:"

# Verify log directory permissions
kubectl exec <pod-name> -- ls -la /app/logs

# Check log rotation configuration
kubectl exec <pod-name> -- cat /etc/logrotate.conf
```

## Platform-Specific Issues

### Apple Silicon Issues

**Symptoms:**
- Pods not scheduling on ARM64 nodes
- Performance issues
- MLX framework errors

**Solutions:**
```bash
# Verify node architecture
kubectl get nodes -o wide

# Check node labels
kubectl get nodes --show-labels | grep arch

# Update node selector
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"nodeSelector":{"kubernetes.io/arch":"arm64"}}}}}'
```

### x86 Compatibility Issues

**Symptoms:**
- Image compatibility problems
- CUDA/OpenCL errors
- Performance degradation

**Solutions:**
```bash
# Check image architecture
docker inspect neozork-interactive:latest | grep Architecture

# Verify CUDA availability
kubectl exec <pod-name> -- nvidia-smi

# Update environment variables
kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","env":[{"name":"CUDA_ENABLED","value":"true"}]}]}}}}'
```

## Performance Issues

### Slow Application Performance

**Symptoms:**
- High response times
- Resource bottlenecks
- Poor user experience

**Diagnosis:**
```bash
# Check resource usage
kubectl top pods --containers

# Check for resource throttling
kubectl describe pod <pod-name> | grep -A 5 "Limits:"
```

**Solutions:**

1. **Scale Horizontally**
   ```bash
   # Increase replica count
   kubectl scale deployment neozork-interactive-apple --replicas=5
   ```

2. **Scale Vertically**
   ```bash
   # Increase resource limits
   kubectl patch deployment neozork-interactive-apple -p '{"spec":{"template":{"spec":{"containers":[{"name":"neozork-interactive","resources":{"limits":{"memory":"8Gi","cpu":"4000m"}}}]}}}}'
   ```

3. **Optimize Application**
   ```bash
   # Enable performance profiling
   kubectl exec <pod-name> -- curl http://localhost:8080/debug/pprof/
   ```

### Database Performance

**Symptoms:**
- Slow database queries
- Connection pool exhaustion
- High database CPU usage

**Solutions:**
```bash
# Check database resource usage
kubectl top pods -l app=postgres

# Scale database
kubectl scale deployment postgres-deployment --replicas=2

# Optimize database configuration
kubectl exec <postgres-pod> -- psql -c "SHOW shared_buffers;"
```

## Emergency Procedures

### Quick Recovery Steps

1. **Restart Deployment**
   ```bash
   kubectl rollout restart deployment neozork-interactive-apple
   ```

2. **Scale to Zero and Back**
   ```bash
   kubectl scale deployment neozork-interactive-apple --replicas=0
   kubectl scale deployment neozork-interactive-apple --replicas=2
   ```

3. **Delete and Recreate**
   ```bash
   kubectl delete deployment neozork-interactive-apple
   kubectl apply -f k8s/neozork-apple-deployment.yaml
   ```

### Data Recovery

```bash
# Backup current data
kubectl exec <pod-name> -- tar czf /tmp/emergency-backup.tar.gz /app/data

# Copy backup to local machine
kubectl cp <pod-name>:/tmp/emergency-backup.tar.gz ./emergency-backup.tar.gz

# Restore from backup
kubectl cp ./emergency-backup.tar.gz <new-pod>:/tmp/
kubectl exec <new-pod> -- tar xzf /tmp/emergency-backup.tar.gz -C /
```

## Getting Help

### Log Collection

```bash
# Collect comprehensive logs
kubectl logs -l app=neozork-interactive --all-containers=true > neozork-logs.txt
kubectl describe pods -l app=neozork-interactive > pod-descriptions.txt
kubectl get events --sort-by=.metadata.creationTimestamp > events.txt
```

### Support Resources

- Check the [Configuration Reference](./configuration-reference-en.md) for all available options
- Review the [Deployment Guide](./deployment-guide-en.md) for detailed setup instructions
- Open an issue in the project repository with collected logs and error messages
- Consult Kubernetes documentation for general Kubernetes issues

This troubleshooting guide should help resolve most common issues. For complex problems, consider reaching out to the development team with detailed logs and error messages.
