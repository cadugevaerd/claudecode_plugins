# Kubernetes Troubleshooting Guide

**Common mistakes, issues, and their solutions for Kubernetes deployments.**

## 🎯 Common Mistakes to Avoid

### ❌ Mistake 1: No Resource Limits

**Problem**: Pod can consume entire node resources

```yaml
# ❌ Bad - No limits
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
  - name: app
    image: myapp:1.0.0
    # No resources defined!
```

**Impact**:

- Pod can use all node CPU/memory
- Other pods starved of resources
- Node becomes unresponsive
- Potential cascading failures

**Solution**: Always set requests and limits

```yaml
# ✅ Good - Defined requests and limits
apiVersion: v1
kind: Pod
metadata:
  name: good-pod
spec:
  containers:
  - name: app
    image: myapp:1.0.0
    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "1000m"
        memory: "512Mi"
```

**Best Practice**:

- Requests: P95 usage × 1.2-1.5x
- Limits: 2-4x requests for CPU, 1.2-1.5x for memory

______________________________________________________________________

### ❌ Mistake 2: Running as Root

**Problem**: Security vulnerability

```yaml
# ❌ Bad - Running as root
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
  - name: app
    image: myapp:1.0.0
    # No securityContext!
```

**Impact**:

- Container has root privileges
- Potential privilege escalation
- Compromised container = compromised node
- Fails security audits

**Solution**: Run as non-root user

```yaml
# ✅ Good - Non-root with minimal capabilities
apiVersion: v1
kind: Pod
metadata:
  name: good-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: myapp:1.0.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

**Best Practice**:

- Always use `runAsNonRoot: true`
- Drop all capabilities, add only needed
- Use read-only root filesystem when possible

______________________________________________________________________

### ❌ Mistake 3: Using `latest` Image Tag

**Problem**: Unpredictable updates and rollbacks

```yaml
# ❌ Bad - Using latest tag
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bad-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
```

**Impact**:

- `latest` changes over time
- No reproducible builds
- Difficult to rollback
- Debugging is harder
- Incompatible updates pulled automatically

**Solution**: Use semantic versioning

```yaml
# ✅ Good - Specific version tag
apiVersion: apps/v1
kind: Deployment
metadata:
  name: good-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.2.3
```

**Best Practice**:

- Always use semantic versions (1.2.3)
- Tag with Git commit SHA for traceability
- Use `imagePullPolicy: IfNotPresent` with versioned tags

______________________________________________________________________

### ❌ Mistake 4: No Health Checks

**Problem**: Dead pods stay running, receive traffic

```yaml
# ❌ Bad - No health checks
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bad-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        # No liveness or readiness probes!
```

**Impact**:

- Frozen apps not restarted
- Unhealthy pods receive traffic
- Cascading failures
- Manual intervention required

**Solution**: Add liveness and readiness probes

```yaml
# ✅ Good - Health checks configured
apiVersion: apps/v1
kind: Deployment
metadata:
  name: good-deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 1
```

**Best Practice**:

- Liveness: Detect deadlocks, restart on failure
- Readiness: Remove from load balancer when not ready
- Separate endpoints: `/health` vs `/ready`

______________________________________________________________________

### ❌ Mistake 5: No RBAC Configuration

**Problem**: Anyone can do anything

```yaml
# ❌ Bad - Using default service account
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  # Using default service account with potential cluster-admin permissions
  containers:
  - name: app
    image: myapp:1.0.0
```

**Impact**:

- Over-privileged applications
- Potential unauthorized access
- Difficult to audit access
- Large blast radius if compromised

**Solution**: Least privilege RBAC

```yaml
# ✅ Good - Specific service account with minimal permissions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-binding
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: v1
kind: Pod
metadata:
  name: good-pod
spec:
  serviceAccountName: app-sa
  containers:
  - name: app
    image: myapp:1.0.0
```

**Best Practice**:

- Create service account per application
- Grant minimum required permissions
- Use Role (namespace-scoped), not ClusterRole
- Audit regularly

______________________________________________________________________

### ❌ Mistake 6: Unlimited Namespace Resources

**Problem**: One app starves others

```yaml
# ❌ Bad - No resource quotas
apiVersion: v1
kind: Namespace
metadata:
  name: production
# No ResourceQuota or LimitRange!
```

**Impact**:

- One misbehaving app consumes all resources
- Fair resource allocation impossible
- Difficult capacity planning
- Cost overruns

**Solution**: Set ResourceQuota and LimitRange

```yaml
# ✅ Good - Namespace with quotas
apiVersion: v1
kind: Namespace
metadata:
  name: production
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "100"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: container-limits
  namespace: production
spec:
  limits:
  - max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

**Best Practice**:

- Set namespace ResourceQuota
- Define LimitRange for containers
- Monitor quota usage
- Adjust based on actual usage

______________________________________________________________________

## 🔧 Common Issues and Solutions

### Issue 1: OOMKilled (Out of Memory)

**Symptoms**:

```bash
$ kubectl get pods
NAME        READY   STATUS      RESTARTS   AGE
app-pod     0/1     OOMKilled   5          10m
```

**Diagnosis**:

```bash
$ kubectl describe pod app-pod
# Look for: "Last State: Terminated - Reason: OOMKilled"

$ kubectl logs app-pod --previous
# Check memory usage before crash
```

**Root Causes**:

- Memory limit too low
- Memory leak in application
- No memory limit (node OOM)

**Solutions**:

1. **Increase memory limit**:

   ```yaml
   resources:
     limits:
       memory: "1Gi"  # Increase from 512Mi
   ```

1. **Fix memory leak**: Profile application, fix code

1. **Set appropriate requests/limits**:

   - Request = P95 usage × 1.2x
   - Limit = Request × 1.2-1.5x

______________________________________________________________________

### Issue 2: CPU Throttling

**Symptoms**:

- Slow application performance
- High CPU usage (near limit)
- No container restart

**Diagnosis**:

```bash
$ kubectl top pod app-pod
NAME        CPU(cores)   MEMORY(bytes)
app-pod     995m         256Mi

# Check if CPU is at limit (1000m)
```

**Root Causes**:

- CPU limit too restrictive
- Inefficient code
- CPU-intensive operations

**Solutions**:

1. **Increase CPU limit**:

   ```yaml
   resources:
     limits:
       cpu: "2000m"  # Increase from 1000m
   ```

1. **Optimize application code**

1. **Use HPA** to scale horizontally instead of vertically

______________________________________________________________________

### Issue 3: ImagePullBackOff

**Symptoms**:

```bash
$ kubectl get pods
NAME        READY   STATUS              RESTARTS   AGE
app-pod     0/1     ImagePullBackOff    0          2m
```

**Diagnosis**:

```bash
$ kubectl describe pod app-pod
# Look for: "Failed to pull image" errors
```

**Root Causes**:

- Image doesn't exist
- Wrong image name/tag
- Missing imagePullSecrets for private registry
- Rate limiting (Docker Hub)

**Solutions**:

1. **Verify image exists**:

   ```bash
   docker pull myapp:1.0.0
   ```

1. **Fix image name/tag**:

   ```yaml
   image: myregistry.azurecr.io/myapp:1.0.0
   ```

1. **Add imagePullSecrets**:

   ```yaml
   imagePullSecrets:
   - name: regcred
   ```

______________________________________________________________________

### Issue 4: CrashLoopBackOff

**Symptoms**:

```bash
$ kubectl get pods
NAME        READY   STATUS             RESTARTS   AGE
app-pod     0/1     CrashLoopBackOff   10         15m
```

**Diagnosis**:

```bash
$ kubectl logs app-pod --previous
# Check logs from previous container run

$ kubectl describe pod app-pod
# Check events and exit codes
```

**Root Causes**:

- Application crashes on startup
- Missing configuration (ConfigMap/Secret)
- Liveness probe failing immediately
- Command/args incorrect

**Solutions**:

1. **Fix application startup**: Check logs for errors

1. **Verify configuration**:

   ```bash
   kubectl get configmap app-config -o yaml
   kubectl get secret app-secret -o yaml
   ```

1. **Adjust liveness probe**:

   ```yaml
   livenessProbe:
     initialDelaySeconds: 60  # Increase delay
   ```

______________________________________________________________________

### Issue 5: Pending Pods

**Symptoms**:

```bash
$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
app-pod     0/1     Pending   0          5m
```

**Diagnosis**:

```bash
$ kubectl describe pod app-pod
# Look for: "Insufficient cpu" or "Insufficient memory"
```

**Root Causes**:

- Insufficient cluster resources
- Node affinity/taints not met
- PVC not bound
- Resource quotas exceeded

**Solutions**:

1. **Add cluster capacity**: Scale nodes

1. **Reduce resource requests**:

   ```yaml
   resources:
     requests:
       cpu: "250m"  # Reduce from 1000m
   ```

1. **Check node affinity/taints**:

   ```bash
   kubectl describe node node-1
   ```

1. **Check resource quotas**:

   ```bash
   kubectl describe resourcequota -n production
   ```

______________________________________________________________________

## 📊 Diagnostic Commands

### Pod Troubleshooting

```bash
# Get pod status
kubectl get pods

# Detailed pod info
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Previous container instance

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pod <pod-name>
```

### Node Troubleshooting

```bash
# Get node status
kubectl get nodes

# Detailed node info
kubectl describe node <node-name>

# Check resource usage
kubectl top nodes

# View node events
kubectl get events --field-selector involvedObject.name=<node-name>
```

### Deployment Troubleshooting

```bash
# Check deployment status
kubectl rollout status deployment/<deployment-name>

# View rollout history
kubectl rollout history deployment/<deployment-name>

# Rollback to previous version
kubectl rollout undo deployment/<deployment-name>

# Check replica set status
kubectl get replicaset
```

______________________________________________________________________

## 📚 References

- [Kubernetes Debugging Guide](https://kubernetes.io/docs/tasks/debug/)
- [Troubleshooting Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
- [Common Pitfalls](https://komodor.com/learn/kubernetes-troubleshooting-the-complete-guide/)
