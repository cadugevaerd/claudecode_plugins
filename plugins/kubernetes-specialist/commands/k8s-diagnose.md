---
description: Diagnose Kubernetes problems and provide actionable solutions
allowed-tools: Bash, Read, Grep, WebFetch
model: sonnet
argument-hint: '[RESOURCE_TYPE] [RESOURCE_NAME] [NAMESPACE]'
---

# Diagnose Kubernetes Problems

Analyze Kubernetes resources, identify issues, and provide step-by-step solutions based on 2025 best practices.

## 🎯 Objetivo

- Identify root cause of Kubernetes issues (CrashLoopBackOff, OOMKilled, ImagePullBackOff, etc.)
- Analyze resource utilization and quotas
- Provide actionable remediation steps
- Generate diagnostic report with context

## 🔧 Instruções

### 1. Gather Cluster Context

1. Execute `kubectl get nodes` to verify cluster status
1. Check current context with `kubectl config current-context`
1. List namespaces with `kubectl get namespaces`
1. Identify target namespace from arguments or use default

### 2. Analyze Resource State

1. If RESOURCE_TYPE provided:
   - Run `kubectl get $1 $2 -n $NAMESPACE -o yaml`
   - Run `kubectl describe $1 $2 -n $NAMESPACE`
1. If no arguments:
   - Check pods with issues: `kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded`
   - List recent events: `kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20`

### 3. Identify Common Problems

Check for these patterns:

**CrashLoopBackOff**:

- Run `kubectl logs $POD_NAME -n $NAMESPACE --previous`
- Check for application errors in logs
- Verify liveness/readiness probes configuration

**OOMKilled / Memory Issues**:

- Run `kubectl top pod $POD_NAME -n $NAMESPACE`
- Check memory limits vs requests in pod spec
- Analyze historical memory usage trends

**ImagePullBackOff**:

- Verify image name and tag exist
- Check image pull secrets: `kubectl get secrets -n $NAMESPACE`
- Test image accessibility from cluster

**Pending Pods**:

- Check node resources: `kubectl top nodes`
- Verify PVC status: `kubectl get pvc -n $NAMESPACE`
- Review pod events for scheduling failures

**Network Issues**:

- Test service connectivity: `kubectl get svc -n $NAMESPACE`
- Check NetworkPolicy restrictions
- Verify DNS resolution with `kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default`

### 4. Analyze Resource Management

1. Check resource requests and limits:
   - `kubectl describe pod $POD_NAME -n $NAMESPACE | grep -A 5 "Requests\|Limits"`
1. Verify namespace quotas:
   - `kubectl get resourcequota -n $NAMESPACE`
1. Check for over-provisioning or under-provisioning

### 5. Generate Diagnostic Report

Provide structured output with:

1. **Problem Summary**: Brief description of issue
1. **Root Cause**: Technical explanation
1. **Impact**: What's affected and severity
1. **Immediate Actions**: Steps to resolve now
1. **Long-term Recommendations**: Prevent recurrence
1. **Relevant Logs**: Key log excerpts (max 20 lines)
1. **Resource Metrics**: Current vs recommended values

## 📊 Formato de Saída

````markdown
# 🔍 Kubernetes Diagnostic Report

## Resource Information
- **Type**: [Pod/Deployment/StatefulSet/etc]
- **Name**: [resource-name]
- **Namespace**: [namespace]
- **Status**: [Current status]

## Problem Summary
[Brief description of the issue]

## Root Cause Analysis
[Technical explanation of what's causing the problem]

## Impact Assessment
- **Severity**: [Critical/High/Medium/Low]
- **Affected Components**: [List]
- **User Impact**: [Description]

## Immediate Actions

1. [Step-by-step action]
2. [Command to execute]
3. [Validation step]

## Long-term Recommendations

- [Best practice 1]
- [Best practice 2]
- [Resource optimization suggestion]

## Relevant Logs

```text
[Last 20 lines of relevant logs]
````

## Resource Metrics

| Metric | Current | Recommended | Status |
|--------|---------|-------------|--------|
| CPU Request | [value] | [value] | [🟢/🟡/🔴] |
| CPU Limit | [value] | [value] | [🟢/🟡/🔴] |
| Memory Request | [value] | [value] | [🟢/🟡/🔴] |
| Memory Limit | [value] | [value] | [🟢/🟡/🔴] |

## Additional Resources

- [Link to relevant K8s documentation]
- [Link to troubleshooting guide]

````

## ✅ Critérios de Sucesso

- [ ] Cluster context verified and accessible
- [ ] Resource state retrieved successfully
- [ ] Problem identified with clear root cause
- [ ] Logs analyzed for error patterns
- [ ] Resource metrics collected (if applicable)
- [ ] Immediate actions provided with kubectl commands
- [ ] Long-term recommendations based on 2025 best practices
- [ ] Diagnostic report generated with all sections
- [ ] Commands tested and validated before suggesting

## ❌ Anti-Patterns

### ❌ Erro 1: Suggesting Commands Without Context

Não sugira comandos genéricos sem validar o contexto atual:

```bash
# ❌ Errado
"Run kubectl delete pod my-pod" # Sem verificar namespace ou impacto

# ✅ Correto
"First check pod dependencies: kubectl get pod my-pod -n production -o yaml | grep -A 5 ownerReferences
Then safely delete: kubectl delete pod my-pod -n production"
````

### ❌ Erro 2: Ignoring Resource Quotas

Não ignore limites de recursos ao recomendar mudanças:

```yaml
# ❌ Errado
resources:
  limits:
    memory: "16Gi"  # Pode exceder quota do namespace

# ✅ Correto
# Primeiro verificar: kubectl get resourcequota -n $NAMESPACE
resources:
  limits:
    memory: "2Gi"  # Dentro dos limites do namespace
```

### ❌ Erro 3: Missing Security Context

Não recomende soluções que comprometam segurança:

```yaml
# ❌ Errado
securityContext:
  privileged: true  # Risco de segurança desnecessário

# ✅ Correto
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

## 📝 Exemplos

### Exemplo 1: Diagnose Specific Pod

```bash
/k8s-diagnose pod my-app-pod production
```

Analisa o pod `my-app-pod` no namespace `production` e gera relatório completo.

### Exemplo 2: Find All Problems

```bash
/k8s-diagnose
```

Escaneia todos os namespaces, identifica pods com problemas e prioriza por severidade.

### Exemplo 3: Check Deployment Issues

```bash
/k8s-diagnose deployment api-server default
```

Analisa o deployment `api-server` no namespace `default`, verifica replicas, rolling updates e resource health.
