---
description: Analyze and optimize Kubernetes resource allocation and costs
allowed-tools: Bash, Read, Grep, WebFetch
model: claude-sonnet-4-5
argument-hint: '[NAMESPACE] [DEPLOYMENT_NAME]'
---

# Optimize Kubernetes Resources

Analyze cluster resource utilization, identify optimization opportunities, and provide recommendations following 2025 cost management best practices.

## 🎯 Objetivo

- Identify over-provisioned resources (high request, low actual usage)
- Detect under-provisioned resources (risk of OOMKilled or throttling)
- Recommend appropriate resource values based on actual metrics
- Calculate estimated cost savings
- Provide scaling recommendations using HPA and VPA patterns

## 🔧 Instruções

### 1. Gather Current Metrics

1. Collect resource usage data:
   - Run `kubectl top nodes` to see node utilization
   - Run `kubectl top pods -n [namespace] --containers` for pod usage
   - Run `kubectl describe nodes` to see allocatable resources
1. Retrieve resource specifications:
   - Run `kubectl get pods -n [namespace] -o json` to get current requests/limits
   - Parse requests, limits, and actual usage for comparison
1. Identify time period (last 24h, 7d, 30d) for trend analysis

### 2. Analyze Over-Provisioning

1. For each pod, calculate efficiency metrics:

   - CPU efficiency = actual CPU usage / CPU request
   - Memory efficiency = actual memory usage / memory request
   - Identify pods with efficiency < 25% (severely over-provisioned)

1. Flag these patterns:

   - CPU request >> actual usage (requests 500m, uses 50m)
   - Memory request >> actual usage (requests 512Mi, uses 100Mi)
   - Large number of over-provisioned replicas

1. Calculate potential savings:

   - Total over-allocated CPU: sum of (request - recommended)
   - Total over-allocated memory: sum of (request - recommended)
   - Estimated monthly cost reduction

### 3. Analyze Under-Provisioning

1. Identify risk indicators:

   - Pods with OOMKilled events in last week
   - Pods throttled due to CPU limits
   - Pods pending due to insufficient node resources
   - Memory/CPU usage approaching limits (>85%)

1. Calculate required adjustments:

   - Recommended limits = 120% of 95th percentile usage
   - Recommended requests = 100% of 95th percentile usage

1. Flag pods at risk of failure

### 4. Provide Optimization Recommendations

1. **Immediate Cost Optimizations** (safe, no risk):

   - Reduce over-provisioned requests to 150% of actual usage
   - Consolidate light-weight pods on fewer nodes

1. **Scaling Strategy Recommendations**:

   - Configure Horizontal Pod Autoscaler (HPA) for traffic-dependent apps
   - Configure Vertical Pod Autoscaler (VPA) for variable-load apps
   - Suggest node autoscaling policies

1. **Advanced Optimizations** (requires testing):

   - Resource quotas per namespace
   - Pod disruption budgets for graceful scaling
   - Priority and preemption policies
   - Right-sizing based on cluster cost analysis

### 5. Generate Optimization Report

1. Create detailed analysis with:

   - Current state: Total allocated vs actual usage
   - Over-provisioning opportunities: Specific resources and potential savings
   - Under-provisioning risks: Pods at risk with remediation steps
   - Cost projections: Current spend vs optimized spend

1. Provide implementation roadmap:

   - Safe changes (phase 1): Can be applied immediately
   - Validated changes (phase 2): Requires testing in staging
   - Advanced changes (phase 3): Architectural changes

## 📊 Formato de Saída

```markdown
# 📊 Kubernetes Resource Optimization Report

**Analyzed**: [namespace] / [deployment/all]
**Time Period**: [24h/7d/30d]
**Generated**: [timestamp]

## 📈 Current State Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total CPU Requested | [X]m | 🟡 |
| Total CPU Used (P95) | [X]m | 🟢 |
| CPU Efficiency | [X]% | 🔴 |
| Total Memory Requested | [X]Mi | 🟡 |
| Total Memory Used (P95) | [X]Mi | 🟢 |
| Memory Efficiency | [X]% | 🔴 |
| Number of Pods | [N] | 🟢 |
| Pods at Risk | [N] | 🔴 |

## 🎯 Over-Provisioning Analysis

### Pods with High Efficiency Margin

| Pod | CPU Request | CPU Used (P95) | Margin | Suggested |
|-----|-------------|----------------|--------|-----------|
| [pod-name] | 500m | 50m | 90% over | 100m |
| [pod-name] | 512Mi | 100Mi | 80% over | 150Mi |

**Total Potential Savings**: [X] CPU / [X]Mi Memory per cycle

### Consolidation Opportunities

- Pods [A, B, C] can run on single node → Save 1 node
- Estimated savings: $[X]/month

## ⚠️ Under-Provisioning Risks

### Pods at Risk

| Pod | Resource | Current | P95 Usage | Risk Level |
|-----|----------|---------|-----------|------------|
| [pod-name] | Memory | 512Mi | 480Mi | 🔴 High |
| [pod-name] | CPU | 250m | 240m | 🟡 Medium |

**Action Required**: Increase limits and implement monitoring

## 💰 Cost Impact Analysis

| Scenario | Monthly Cost | vs Current | Savings |
|----------|-------------|-----------|---------|
| Current State | $[X] | — | — |
| Phase 1 (Safe) | $[X] | -[X]% | $[X]/mo |
| Phase 2 (Validated) | $[X] | -[X]% | $[X]/mo |
| Phase 3 (Advanced) | $[X] | -[X]% | $[X]/mo |

## 📋 Implementation Roadmap

### Phase 1: Immediate Cost Reductions (Safe)

1. **Pod [name]**: Reduce CPU request from 500m to 100m
   \`\`\`bash
   kubectl set resources deployment [name] --requests=cpu=100m -n [namespace]
   \`\`\`

2. **Pod [name]**: Reduce Memory request from 512Mi to 150Mi
   \`\`\`bash
   kubectl set resources deployment [name] --requests=memory=150Mi -n [namespace]
   \`\`\`

**Estimated Savings**: $[X]/month | Risk: Low | Timeline: Immediate

### Phase 2: Scaling Strategy (Requires Testing)

1. **Implement HPA for [deployment]**:
   \`\`\`yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: [deployment]-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: [deployment]
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   \`\`\`

**Estimated Savings**: $[X]/month | Risk: Medium | Timeline: 1-2 weeks

### Phase 3: Advanced Optimizations (Architectural)

1. **Resource Quotas per Namespace**
2. **Priority and Preemption Policies**
3. **Node Pool Optimization**

**Estimated Savings**: $[X]/month | Risk: High | Timeline: 1 month

## 📚 Additional Resources

- [Kubernetes Resource Management Best Practices](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Vertical Pod Autoscaler Documentation](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)
- [Cost Optimization Strategies](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)

## ✅ Next Steps

1. Review Phase 1 recommendations
2. Test Phase 2 in staging environment
3. Schedule Phase 3 for next quarter
4. Monitor costs weekly after implementation
```

## ✅ Critérios de Sucesso

- [ ] Current resource utilization metrics collected
- [ ] Over-provisioning identified with specific pods and percentages
- [ ] Under-provisioning risks identified with failure probability
- [ ] Cost savings calculated with specific values
- [ ] Implementation roadmap provided with kubectl commands
- [ ] HPA/VPA recommendations included where applicable
- [ ] Risk assessment provided for each recommendation
- [ ] Timeline estimates provided
- [ ] Follow-up monitoring plan included

## ❌ Anti-Patterns

### ❌ Erro 1: Recommending Blind Reductions

Never recommend resource reductions without actual usage data:

```bash
# ❌ Errado
"Reduce all CPU requests to 100m to save money"

# ✅ Correto
"Pod [name] has CPU request 500m but uses only 50m (P95).
Recommend reducing to 100m (2x usage buffer).
Projected savings: $120/month with low risk."
```

### ❌ Erro 2: Ignoring Burst Requirements

Don't optimize peak resources away:

```yaml
# ❌ Errado
# CPU: uses 50m average, 500m peak → recommend 100m

# ✅ Correto
# CPU: uses 50m average, 500m peak → recommend 600m limit
# (Keep headroom for legitimate bursts)
```

### ❌ Erro 3: Missing Safety Margins

Never right-size to exact 100th percentile:

```bash
# ❌ Errado
# Memory P95 = 256Mi → recommend exactly 256Mi

# ✅ Correto
# Memory P95 = 256Mi → recommend 307Mi (120% buffer)
# (Protects against anomalies)
```

## 📝 Exemplos

### Exemplo 1: Optimize Single Namespace

```bash
/k8s-optimize production
```

Analisa todos os pods no namespace `production` e gera relatório com:

- Over-provisioning opportunities
- Cost savings estimates
- Implementation steps com kubectl commands

### Exemplo 2: Optimize Specific Deployment

```bash
/k8s-optimize production api-server
```

Analisa apenas o deployment `api-server` no namespace `production` com análise detalhada de:

- Replica optimization opportunities
- Scaling strategy recommendations
- Cost projection

### Exemplo 3: Full Cluster Analysis

```bash
/k8s-optimize
```

Escaneia todos os namespaces, identifica as maiores oportunidades de economia e prioriza por impacto.
