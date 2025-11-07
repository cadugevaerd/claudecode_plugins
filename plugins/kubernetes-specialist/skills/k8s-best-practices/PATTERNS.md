# Kubernetes Deployment and Configuration Patterns

**Detailed patterns for health checks, autoscaling, deployments, storage, and observability.**

## 🔍 Health Check Patterns

### Liveness Probe (Restart on Failure)

**Use case**: Detect frozen or deadlocked applications

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
    scheme: HTTP
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3  # Restart after 3 failures
```

**When it fails**: Kubelet restarts the container

**Best Practices**:

- Set `initialDelaySeconds` > application startup time
- Use lightweight health check endpoint
- Don't check external dependencies (DB, cache) in liveness
- `failureThreshold * periodSeconds` = time before restart

### Readiness Probe (Remove from Load Balancer)

**Use case**: Only send traffic to healthy pods

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 1  # Take out immediately on failure
```

**When it fails**: Pod removed from Service endpoints (no traffic)

**Best Practices**:

- Check external dependencies (DB connection, cache)
- Lower `failureThreshold` (1-2) to quickly remove unhealthy pods
- Separate `/health` (liveness) from `/ready` (readiness)
- Readiness can fail temporarily (DB maintenance) without restart

### Startup Probe (Slow Starting Apps)

**Use case**: Applications with long initialization

```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 30  # 30 * 10 = 300s (5 minutes) to start
```

**When it fails**: Liveness and readiness probes don't run until startup succeeds

**Best Practices**:

- Use for apps that take minutes to start (legacy apps, data loading)
- Once startup succeeds, liveness/readiness take over
- Prevents premature restarts during initialization

### Probe Comparison Table

| Probe Type | Purpose | Failure Action | Check Dependencies? |
|------------|---------|----------------|---------------------|
| Liveness | Detect deadlock | Restart container | ❌ No |
| Readiness | Traffic routing | Remove from Service | ✅ Yes |
| Startup | Slow initialization | Delay liveness/readiness | ❌ No |

## 📈 Horizontal Pod Autoscaling (HPA)

### Basic CPU-Based HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**How it works**:

- Monitors CPU utilization across all pods
- Scales up when average > 70%
- Scales down when average < 70%

### Multi-Metric HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
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

**Advanced features**:

- Multiple metrics (CPU + memory)
- Scaling behavior control
- Fast scale-up (100% increase every 15s)
- Slow scale-down (50% decrease every 15s, wait 5 min)

### Custom Metrics HPA

```yaml
metrics:
- type: Pods
  pods:
    metric:
      name: http_requests_per_second
    target:
      type: AverageValue
      averageValue: "1000"
```

**Use cases**:

- HTTP requests per second
- Queue depth
- Custom business metrics

**Requirements**:

- Metrics server or custom metrics API
- Prometheus Adapter for Prometheus metrics

### HPA Best Practices

1. **Set realistic targets**: 70% CPU allows headroom for spikes
1. **Start with CPU**: Simplest and most predictable
1. **Add memory carefully**: Memory-based scaling can be tricky
1. **Configure behavior**: Control scale-up/down velocity
1. **Monitor HPA events**: `kubectl describe hpa app-hpa`
1. **Test scaling**: Load test to verify scaling behavior

## 💾 Storage Patterns

### Persistent Volumes (PV) and Claims (PVC)

**StorageClass** (defines storage type):

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
```

**PersistentVolumeClaim**:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 50Gi
```

**Use in Pod**:

```yaml
volumes:
- name: data
  persistentVolumeClaim:
    claimName: app-data
containers:
- name: app
  volumeMounts:
  - name: data
    mountPath: /data
```

### Access Modes

- **ReadWriteOnce (RWO)**: Single pod read-write (most common)
- **ReadOnlyMany (ROX)**: Multiple pods read-only
- **ReadWriteMany (RWX)**: Multiple pods read-write (requires NFS-like storage)

### Storage Best Practices

1. **Choose appropriate storage class**: SSD for databases, HDD for logs
1. **Set reclaim policy**: `Retain` for production data
1. **Use `WaitForFirstConsumer`**: Avoids cross-zone volume provisioning
1. **Backup regularly**: Use Velero or cloud-native snapshots
1. **Test restoration**: Verify backups work before disaster strikes
1. **Set resource limits**: Prevent storage exhaustion

### ConfigMaps and Secrets

**ConfigMap** (non-sensitive configuration):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    log.level=INFO
  database.url: "postgres://db:5432/mydb"
```

**Size limit**: 1MB per ConfigMap

**Secret** (sensitive data):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

**Best Practices**:

- ConfigMaps for non-sensitive config
- Secrets for credentials, keys, tokens
- Use external secret managers (Vault, AWS Secrets Manager) for production
- Rotate secrets regularly (monthly minimum)
- Mount as volumes, not environment variables (easier rotation)

## 🔄 Deployment Patterns

### Rolling Update Strategy

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # 1 extra pod during update
      maxUnavailable: 0     # 0 pods down during update
  progressDeadlineSeconds: 600
```

**How it works**:

1. Create 1 new pod (maxSurge: 1)
1. Wait for new pod to be ready
1. Terminate 1 old pod (maxUnavailable: 0)
1. Repeat until all pods updated

**Best for**: Zero-downtime deployments

### Recreate Strategy

```yaml
spec:
  strategy:
    type: Recreate
```

**How it works**:

1. Terminate all old pods
1. Create all new pods

**Best for**: StatefulSets, incompatible versions

### Blue-Green Deployment

**Blue (current)**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: blue
```

**Green (new)**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  selector:
    matchLabels:
      app: myapp
      version: green
```

**Switch traffic**:

```bash
kubectl patch service app-service -p '{"spec":{"selector":{"version":"green"}}}'
```

**Best for**: Instant rollback capability

### Canary Deployment

Deploy new version to small percentage of traffic:

```yaml
# Stable: 90% traffic
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
---
# Canary: 10% traffic
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
```

**Best for**: Gradual rollout, A/B testing

### Pod Disruption Budget (PDB)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

**Purpose**: Ensure minimum pod availability during voluntary disruptions (node drain, rolling updates)

**Best Practices**:

- Set `minAvailable` or `maxUnavailable`
- Use for critical applications
- Coordinate with HPA (`minAvailable` < `minReplicas`)

## 📊 Observability Patterns

### Prometheus Metrics

**ServiceMonitor** (Prometheus Operator):

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
```

**Key metrics to expose**:

- Request rate (requests/sec)
- Error rate (errors/sec)
- Duration (latency p50, p95, p99)
- Resource usage (CPU, memory)

### Structured Logging

**JSON format**:

```json
{
  "timestamp": "2025-01-07T10:30:00Z",
  "level": "ERROR",
  "message": "Database connection failed",
  "context": {
    "service": "api-gateway",
    "trace_id": "abc123",
    "user_id": "user456"
  }
}
```

**Log levels**:

- **DEBUG**: Detailed diagnostic info
- **INFO**: General informational messages
- **WARN**: Warning messages (potential issues)
- **ERROR**: Error messages (failures)

**Best Practices**:

- JSON format for centralized logging
- Include trace IDs for distributed tracing
- Use log levels consistently
- Don't log sensitive data (PII, credentials)

### Distributed Tracing

**OpenTelemetry** instrumentation:

```yaml
env:
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: "http://jaeger:4317"
- name: OTEL_SERVICE_NAME
  value: "my-app"
```

**Benefits**:

- Trace requests across microservices
- Identify bottlenecks
- Debug production issues

### Alerting Rules

**Prometheus AlertManager**:

```yaml
groups:
- name: app-alerts
  rules:
  - alert: HighPodRestartRate
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0.05
    for: 5m
    annotations:
      summary: "Pod restart rate > 1/hour"
  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
    for: 5m
    annotations:
      summary: "Memory usage > 90%"
```

**Key alerts**:

- Pod restart rate > 1/hour
- CPU throttling detected
- Memory approaching limits
- Node not ready
- PVC usage > 80%
- ImagePullBackOff errors

## 📚 References

- [Kubernetes Patterns Book](https://k8spatterns.io/)
- [Health Checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
