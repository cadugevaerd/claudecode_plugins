---
name: k8s-best-practices
description: Comprehensive Kubernetes 2025 best practices for resource management, security, and optimization. Use when designing K8s deployments, right-sizing resources (CPU/memory), implementing security controls (RBAC, SecurityContext), configuring health checks, setting up HPA, optimizing costs, or troubleshooting resource issues (OOMKilled, throttling). Covers request/limit guidelines, pod security, namespaces, storage, and observability patterns.
version: 1.0.0
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Kubernetes 2025 Best Practices

**A comprehensive reference on modern Kubernetes resource management, security, and optimization patterns.**

## 🎯 Overview

This skill provides actionable best practices for Kubernetes deployments in 2025, focusing on:

- Resource management and right-sizing
- Security and compliance
- Cost optimization
- High availability and resilience
- Observability and monitoring

## 📋 When to Use Me

Invoke this skill when you need to:

- **Design new Kubernetes deployments** with proper resource allocation and security controls
- **Right-size CPU and memory** requests and limits for production workloads
- **Implement security controls** including RBAC, SecurityContext, and Pod Security Standards
- **Configure health checks** with liveness, readiness, and startup probes
- **Set up horizontal pod autoscaling** (HPA) based on CPU/memory metrics
- **Optimize Kubernetes costs** by identifying over-provisioned resources (99.94% of clusters!)
- **Implement storage patterns** with PersistentVolumes, ConfigMaps, and Secrets
- **Troubleshoot resource issues** like OOMKilled, CPU throttling, or pod evictions
- **Design deployment strategies** with rolling updates and PodDisruptionBudgets
- **Set up observability** with Prometheus, centralized logging, and alerting rules

## 🎓 Core Knowledge

### Resource Management Fundamentals

**Request and Limit Guidelines**:

- **CPU Requests**: 250m baseline, Request = (P50 usage) × 1.2-1.5x
- **Memory Requests**: 256Mi baseline, Request = (P95 usage) × 1.2x
- **Limits**: CPU 2-4x requests, Memory 1.2-1.5x requests

**2025 Reality**: 99.94% of clusters over-provisioned with 10% CPU and 23% memory utilization

**Right-Sizing Process**: Baseline (2 weeks) → P95 calculation → Safety margin → Test staging → Production monitoring

### Security Fundamentals

**Key Security Controls**:

- **Security Context**: `runAsNonRoot: true`, drop ALL capabilities, read-only filesystem
- **Image Security**: Semantic versioning (never `latest`), vulnerability scanning (Trivy), private registries
- **RBAC**: Per-app service accounts, least privilege, namespace-scoped roles
- **Secrets Management**: External secret managers (Vault, AWS Secrets Manager), rotation monthly minimum
- **Network Policies**: Default deny all, allow specific traffic only

→ **See [SECURITY_GUIDE.md](./SECURITY_GUIDE.md)** for detailed security patterns, configurations, and hardening guidelines

### Namespace and Resource Quotas

**Purpose**: Prevent resource starvation, fair allocation, cost control

**Key Resources**:

- **ResourceQuota**: Total namespace limits (CPU, memory, pods, PVCs)
- **LimitRange**: Per-container min/max constraints

**Best Practice**: Set quotas in every namespace, monitor usage with `kubectl describe resourcequota`

### Health Checks

**Three Probe Types**:

1. **Liveness Probe**: Restart on failure (detect deadlocks)
1. **Readiness Probe**: Remove from Service on failure (traffic routing)
1. **Startup Probe**: Delay liveness/readiness for slow-starting apps

**Configuration Tips**:

- Liveness: `initialDelaySeconds` > startup time, `failureThreshold: 3`
- Readiness: `failureThreshold: 1` (quick removal), check dependencies
- Use separate endpoints: `/health` vs `/ready`

→ **See [PATTERNS.md](./PATTERNS.md)** for detailed probe configurations, HPA patterns, storage, and deployment strategies

### Horizontal Pod Autoscaling (HPA)

**Basic Approach**: Scale pods based on CPU/memory utilization

**Key Metrics**:

- Target CPU utilization: 70% (allows headroom)
- Target memory utilization: 80%
- Custom metrics: HTTP requests/sec, queue depth

**Scaling Behavior**: Fast scale-up (100% every 15s), slow scale-down (50% every 15s, wait 5 min)

### Storage Best Practices

**PersistentVolumes**:

- Choose StorageClass based on performance needs (SSD vs HDD)
- Set `reclaimPolicy: Retain` for production data
- Use `volumeBindingMode: WaitForFirstConsumer` to avoid cross-zone issues
- Backup regularly with Velero or cloud snapshots

**ConfigMaps and Secrets**:

- ConfigMaps: Non-sensitive config (< 1MB)
- Secrets: Credentials, tokens, keys (encrypted at rest)
- Use external secret managers for production (Vault, AWS Secrets Manager)
- Rotate secrets monthly minimum

### Deployment Strategies

**Rolling Update**: Zero-downtime deployments (default)

- `maxSurge: 1` - Create 1 extra pod
- `maxUnavailable: 0` - No pods down during update

**Alternative Strategies**:

- **Blue-Green**: Instant rollback, traffic switch
- **Canary**: Gradual rollout, A/B testing
- **Recreate**: StatefulSets, incompatible versions

**Pod Disruption Budget (PDB)**: Ensure minimum availability during voluntary disruptions

### Observability Setup

**Metrics Collection**:

- Prometheus with 30s scrape interval
- Key metrics: CPU/memory usage, pod restarts, API latency, error rates

**Logging Best Practices**:

- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARN, ERROR
- Centralized logging (ELK, Loki, Cloud Logging)
- 30-day retention minimum

**Alerting Rules**:

- Pod restart rate > 1/hour
- CPU throttling detected
- Memory approaching limits
- Node not ready
- PVC usage > 80%

## 📚 Reference Files

For detailed information, consult these reference files:

- **[SECURITY_GUIDE.md](./SECURITY_GUIDE.md)** - Security patterns, SecurityContext, RBAC, image scanning, secrets management, network policies
- **[PATTERNS.md](./PATTERNS.md)** - Health check configurations, HPA patterns, storage patterns, deployment strategies, observability
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common mistakes, diagnostic commands, issue resolution (OOMKilled, throttling, ImagePullBackOff)

## 💡 Quick Examples

### Example 1: Well-Configured Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      serviceAccountName: app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: app
        image: myapp:1.2.3  # Semantic version
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

### Example 2: Namespace with Quotas

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
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
```

### Example 3: HPA with Custom Behavior

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: production-app
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
```

## 🎯 Key Takeaways

**Resource Management**:

- Always set requests and limits
- Right-size based on P95 usage + safety margin
- Monitor and optimize continuously

**Security**:

- Run as non-root with minimal capabilities
- Use semantic versioning, never `latest`
- Implement RBAC with least privilege

**Reliability**:

- Configure liveness and readiness probes
- Use rolling updates with PodDisruptionBudgets
- Set up HPA for dynamic scaling

**Cost Optimization**:

- Address over-provisioning (99.94% of clusters!)
- Use tools like Goldilocks for VPA-based recommendations
- Implement cluster autoscaling

**Observability**:

- Collect metrics with Prometheus
- Use structured JSON logging
- Set up alerts for critical issues

## 📖 Additional Resources

- [Kubernetes Best Practices 2025](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)
- [Resource Management Documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Security Best Practices](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Production Checklist](https://www.pulumi.com/blog/kubernetes-best-practices-i-wish-i-had-known-before/)
