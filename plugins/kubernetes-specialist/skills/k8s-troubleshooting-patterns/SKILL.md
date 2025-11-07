---
name: k8s-troubleshooting-patterns
description: Diagnostic patterns and solutions for common Kubernetes pod failures. Use when troubleshooting CrashLoopBackOff, OOMKilled, ImagePullBackOff, Pending pods, CreateContainerConfigError. Includes kubectl diagnostic commands, debugging techniques, and prevention strategies for production workloads.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
---

# Kubernetes Troubleshooting Patterns

**Diagnostic patterns and solutions for common Kubernetes failures.**

## 🎯 When to Use Me

Use this skill when:

- 🔴 Diagnosing pod failures: CrashLoopBackOff, OOMKilled, CreateContainerConfigError
- 🟠 Resolving image pull issues: ImagePullBackOff, ErrImagePull
- 🟡 Troubleshooting scheduling: Pending pods, resource constraints
- 🔧 Learning kubectl diagnostic commands and debugging techniques
- 📊 Following decision trees for Kubernetes failures
- 🛡️ Implementing prevention strategies for production workloads

## 📚 Overview

This skill provides diagnostic flowcharts and solutions for the most common Kubernetes pod failure patterns encountered in production environments. Covers troubleshooting methodology, debugging commands, and resolution strategies.

## 🔴 CrashLoopBackOff

**Definition**: Container starts but immediately crashes, causing repeated restart attempts with exponential backoff delays (10s → 20s → 40s → max 5 minutes).

### Diagnosis

```bash
# Get pod status and events
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# Check last crash logs
kubectl logs [POD_NAME] -n [NAMESPACE] --previous

# Check current logs if still crashing
kubectl logs [POD_NAME] -n [NAMESPACE] -f

# Debug with ephemeral container (kubectl 1.23+)
kubectl debug [POD_NAME] -n [NAMESPACE] -it --image=busybox:1.28

# Check exit code and reason
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

### Common Causes and Solutions

| Cause | Symptoms | Solution |
|-------|----------|----------|
| App error | Error logs in previous logs | Fix application code, test locally |
| Missing environment variables | "variable not found" in logs | Add ENV vars to deployment |
| Missing files/config | "file not found" in logs | Mount ConfigMap or Secret |
| Port binding error | "Address already in use" in logs | Change app port or remove port binding |
| Failed health checks | Exit code 1, "probe failed" | Fix liveness probe timeout values |

### Quick Fix Template

```bash
# 1. Get previous logs
kubectl logs [POD_NAME] -n [NAMESPACE] --previous | tail -50

# 2. Review the error
# 3. Fix the issue (update deployment)
kubectl patch deployment [DEPLOYMENT_NAME] -n [NAMESPACE] -p '{"spec":{"template":{"spec":{"containers":[{"name":"[CONTAINER]","env":[{"name":"KEY","value":"VALUE"}]}]}}}}'

# 4. Verify pod restarts
kubectl get pod [POD_NAME] -n [NAMESPACE] -w
```

## 🟠 OOMKilled (Out of Memory)

**Definition**: Container killed due to exceeding memory limit. Exit code **137** (128 + 9 SIGKILL) indicates OOMKilled.

### Diagnosis

```bash
# Check termination reason and exit code
kubectl describe pod [POD_NAME] -n [NAMESPACE] | grep -A 5 "Last State"

# Verify exit code 137 = OOMKilled
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'

# Check current memory usage vs limit
kubectl top pod [POD_NAME] -n [NAMESPACE] --containers

# Get resource limits and requests
kubectl get pod [POD_NAME] -n [NAMESPACE] -o yaml | grep -A 5 "resources:"

# Monitor memory trend over time
watch kubectl top pod [POD_NAME] -n [NAMESPACE] --containers
```

### Root Causes

- **Memory leak**: App not releasing memory → Check application code, profile with tools
- **Insufficient limit**: Limit too low for workload → Increase limit based on observed usage
- **Spike load**: Temporary high usage → Increase limit or implement HPA (Horizontal Pod Autoscaling)
- **Misconfigured requests**: Request < actual need → Update deployment resources

### Solution Steps

```bash
# 1. Analyze current usage
kubectl top pod [POD_NAME] -n [NAMESPACE] --containers
# Get the actual peak usage from metric

# 2. Check current limits vs requests
kubectl get pod [POD_NAME] -n [NAMESPACE] -o yaml | grep -A 4 "resources:"

# 3. Increase limit (1.5-2x current observed usage)
kubectl set resources deployment [DEPLOYMENT_NAME] \
  --limits=memory=1Gi \
  -n [NAMESPACE]

# 4. Update requests (80% of limit recommended)
kubectl set resources deployment [DEPLOYMENT_NAME] \
  --requests=memory=800Mi \
  -n [NAMESPACE]

# 5. Trigger rolling restart
kubectl rollout restart deployment [DEPLOYMENT_NAME] -n [NAMESPACE]

# 6. Monitor memory trend
watch kubectl top pod [POD_NAME] -n [NAMESPACE] --containers
```

### Best Practices

- **Set resource requests**: Helps K8s schedule pods correctly
- **Set resource limits**: Prevents resource hogging
- **Ratio**: Requests = 70-80% of limits
- **Monitor constantly**: Use Prometheus/Grafana for trending

## 🟠 ImagePullBackOff

**Definition**: Pod cannot pull container image from registry.

### Diagnosis

```bash
# Check image pull error
kubectl describe pod [POD_NAME] -n [NAMESPACE] | grep -A 3 "ImagePull"

# Check image name in pod spec
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.spec.containers[0].image}'

# Check image pull secrets
kubectl get secrets -n [NAMESPACE] | grep -i docker
```

### Root Causes and Solutions

| Cause | Check Command | Fix |
|-------|---------------|-----|
| Image doesn't exist | Image name/tag typo | Verify in registry, update deployment |
| Private registry | No image pull secret | Create secret, add to deployment |
| Wrong credentials | Secret data incorrect | Recreate secret with correct credentials |
| Network unreachable | Can't reach registry | Check firewall, proxy, DNS |

### Quick Fix

```bash
# 1. Verify image exists
docker pull [IMAGE_NAME]:[TAG]

# 2. If private, create secret
kubectl create secret docker-registry regcred \
  --docker-server=[REGISTRY_URL] \
  --docker-username=[USERNAME] \
  --docker-password=[PASSWORD] \
  -n [NAMESPACE]

# 3. Update deployment to use secret
kubectl patch deployment [DEPLOYMENT_NAME] -n [NAMESPACE] -p \
  '{"spec":{"template":{"spec":{"imagePullSecrets":[{"name":"regcred"}]}}}}'
```

## 🟡 Pending Pod

**Definition**: Pod stuck in Pending state, not scheduled to any node.

### Diagnosis

```bash
# Check why pending
kubectl describe pod [POD_NAME] -n [NAMESPACE] | grep -A 5 "Events"

# Check node resources
kubectl top nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check PVC status (if using volumes)
kubectl get pvc -n [NAMESPACE]

# Check quotas
kubectl describe resourcequota -n [NAMESPACE]
```

### Root Causes

- **No resources**: Cluster full, nodes overcommitted
- **Affinity/taints**: Pod can't schedule due to constraints
- **Unbound PVC**: Volume not available
- **Quota exceeded**: Namespace quota full

### Solutions

```bash
# Option 1: Add more nodes
# (Contact cloud provider or add physical hardware)

# Option 2: Remove affinity constraints (if safe)
kubectl patch deployment [DEPLOYMENT_NAME] -n [NAMESPACE] --type json \
  -p='[{"op": "remove", "path": "/spec/template/spec/affinity"}]'

# Option 3: Check and fix quotas
kubectl describe resourcequota -n [NAMESPACE]
# Increase quota or delete resources

# Option 4: Wait for resources to free up
# Monitor: kubectl get pod [POD_NAME] -n [NAMESPACE] -w
```

## 🔴 CreateContainerConfigError

**Definition**: Pod configuration invalid, container can't start.

### Diagnosis

```bash
# Get full error
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# Check YAML syntax
kubectl get pod [POD_NAME] -n [NAMESPACE] -o yaml | head -50
```

### Common Issues

- **Invalid YAML**: Syntax errors in spec
- **Bad ConfigMap reference**: ConfigMap doesn't exist
- **Bad Secret reference**: Secret doesn't exist
- **Invalid image pull secret**: Secret not found

### Fix Template

```bash
# 1. Validate YAML
kubectl apply -f deployment.yaml --dry-run=client

# 2. Check referenced ConfigMap/Secret exists
kubectl get configmap [NAME] -n [NAMESPACE]
kubectl get secret [NAME] -n [NAMESPACE]

# 3. Fix and reapply
kubectl apply -f deployment.yaml
```

## 🔴 ErrImagePull

**Definition**: Similar to ImagePullBackOff but first attempt failed.

### Quick Diagnosis

```bash
kubectl describe pod [POD_NAME] -n [NAMESPACE]
```

### Immediate Actions

```bash
# Check image accessibility
docker pull [IMAGE_NAME]:[TAG]

# If fails, check:
# 1. Image name spelling
# 2. Registry credentials (if private)
# 3. Network connectivity to registry

# Fix and trigger new pull
kubectl rollout restart deployment [DEPLOYMENT_NAME] -n [NAMESPACE]
```

## 🟢 Healthy Pod Checklist

A pod is truly healthy when:

- ✅ Status is "Running"
- ✅ All containers show "1/1" Ready
- ✅ Restart count is 0 (or stable)
- ✅ No recent events with warnings/errors
- ✅ Logs show application starting successfully
- ✅ Health probes passing
- ✅ CPU/memory usage stable
- ✅ Application responding to requests

## 📊 Diagnostic Decision Tree

```
Pod Not Running?
├─ Status: CrashLoopBackOff?
│  └─ Check: Previous logs for errors
├─ Status: OOMKilled?
│  └─ Increase: Memory limit
├─ Status: ImagePullBackOff?
│  └─ Check: Image name + credentials
├─ Status: Pending?
│  └─ Check: Node resources + quotas + affinity
├─ Status: CreateContainerConfigError?
│  └─ Check: ConfigMap/Secret existence
└─ Status: ErrImagePull?
   └─ Check: Registry connectivity
```

## 🔧 Essential Diagnostic Commands

### Basic Commands

```bash
# Complete pod diagnosis
kubectl describe pod [POD_NAME] -n [NAMESPACE]

# Previous logs (crash logs)
kubectl logs [POD_NAME] -n [NAMESPACE] --previous

# Current logs with follow
kubectl logs [POD_NAME] -n [NAMESPACE] -f

# Raw YAML configuration
kubectl get pod [POD_NAME] -n [NAMESPACE] -o yaml

# Resource usage
kubectl top pod [POD_NAME] -n [NAMESPACE] --containers

# Events related to pod
kubectl get events -n [NAMESPACE] --field-selector involvedObject.name=[POD_NAME]

# Watch pod status changes
kubectl get pod [POD_NAME] -n [NAMESPACE] -w

# Container shell access (if running)
kubectl exec -it [POD_NAME] -n [NAMESPACE] -- /bin/bash
```

### Advanced Debugging Commands (kubectl 1.23+)

```bash
# Debug with ephemeral container (add temporary debug container)
kubectl debug [POD_NAME] -n [NAMESPACE] -it --image=busybox:1.28

# Debug specific node
kubectl debug node/[NODE_NAME] -it --image=ubuntu

# Check exit code and termination message
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
kubectl get pod [POD_NAME] -n [NAMESPACE] -o jsonpath='{.status.containerStatuses[0].lastState.terminated.message}'
```

### Multi-Pod Debugging (with stern tool)

```bash
# Install stern
go install github.com/wercker/stern@latest

# Tail logs from multiple pods matching label
stern -n [NAMESPACE] -l app=[APP_NAME] --all-pods

# Follow logs with grep filtering
stern -n [NAMESPACE] [POD_PATTERN] | grep ERROR
```

## 📚 Prevention Strategy

### Essential Best Practices

1. **Always set resource requests + limits**

   - Requests: Guide K8s scheduling decisions
   - Limits: Prevent resource hogging
   - Recommended ratio: Requests = 70-80% of limits

1. **Use semantic versioning** (NEVER use `latest` tag)

   - Enables reproducible deployments
   - Facilitates rollback strategies
   - Example: `app:v1.2.3` instead of `app:latest`

1. **Implement health checks (probes)**

   - **Liveness probe**: Restart unhealthy containers
   - **Readiness probe**: Control traffic routing
   - **Startup probe**: Allow time for initialization
   - Recommended: All three for production workloads

1. **Test in staging before production**

   - Catch configuration issues early
   - Validate resource limits
   - Test failover scenarios

1. **Continuous monitoring & observability**

   - Monitor pod restart count
   - Track resource usage trends
   - Set up alerts for failure patterns
   - Use centralized logging (ELK, Splunk, etc.)

1. **Configuration management**

   - Version control YAML manifests
   - Use GitOps for deployments
   - Regular backup of working configurations
   - Document resource requirements

1. **Device-specific considerations (2025)**

   - Configure kubelet early for hardware workloads
   - Monitor device plugin health
   - Plan upgrades carefully
   - Avoid overloading nodes with critical workloads

### Monitoring Tools

- **Prometheus + Grafana**: Metrics and alerting
- **stern**: Multi-pod log tailing
- **kubectx/kubens**: Context and namespace switching
- **k9s**: Interactive Kubernetes dashboard
