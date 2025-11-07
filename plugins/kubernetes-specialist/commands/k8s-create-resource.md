---
description: Generate and deploy Kubernetes resources following best practices
allowed-tools: Write, Read, Bash, WebFetch
model: sonnet
argument-hint: '[RESOURCE_KIND] [RESOURCE_NAME] [NAMESPACE]'
---

# Create Kubernetes Resource

Generate production-ready Kubernetes manifests following 2025 best practices for resource management, security, and optimization.

## 🎯 Objetivo

- Generate properly structured Kubernetes YAML manifests
- Apply security best practices (RBAC, security context, network policies)
- Configure resource requests and limits appropriately
- Validate syntax and apply to cluster
- Document resource configuration and purpose

## 🔧 Instruções

### 1. Determine Resource Requirements

1. Ask user for resource kind: Pod, Deployment, StatefulSet, Service, ConfigMap, Secret, Ingress, PVC
1. Gather essential parameters:
   - Resource name and namespace
   - Container image and version
   - Number of replicas (if applicable)
   - Resource requests and limits
   - Port and protocol information
1. Ask about optional configurations:
   - Health checks (liveness/readiness probes)
   - Environment variables
   - Volume mounts
   - Security requirements

### 2. Generate Manifest

1. Create YAML manifest with:

   - Proper API version for resource kind
   - Metadata (name, namespace, labels for organization)
   - Spec section with resource-specific configuration
   - Security context (non-root, read-only filesystem where applicable)
   - Resource requests and limits based on 2025 best practices:
     - **Request baseline**: 250m CPU, 256Mi memory
     - **Limit multiplier**: 2-4x requests (prevent runaway)
   - Labels following Kubernetes conventions:
     - `app: [application-name]`
     - `version: [semantic-version]`
     - `managed-by: kubernetes-specialist`

1. Apply security best practices:

   - Set `runAsNonRoot: true` when possible
   - Use `allowPrivilegeEscalation: false`
   - Set `readOnlyRootFilesystem: true` for immutable containers
   - Include resource quotas in namespace if needed

1. Add health checks:

   - Liveness probe for crash recovery
   - Readiness probe for traffic readiness
   - Use appropriate probe types (HTTP, TCP, exec)

### 3. Validate Manifest

1. Validate YAML syntax: `kubectl apply --dry-run=client -f manifest.yaml`
1. Check if resource already exists in namespace
1. Verify resource quotas are not exceeded
1. Validate image accessibility (if private registry)

### 4. Generate Documentation

1. Create comment block explaining:

   - Resource purpose and responsibilities
   - Key configurations and why they were chosen
   - How to scale or modify the resource
   - Monitoring and troubleshooting tips

1. Generate update guide:

   - How to modify the resource
   - Scaling procedures (for Deployments/StatefulSets)
   - Health check adjustment guidelines

### 5. Deploy to Cluster

1. Confirm manifest with user before deployment
1. Apply manifest: `kubectl apply -f manifest.yaml`
1. Verify deployment success:
   - Check pod status: `kubectl get pods -n [namespace]`
   - Verify readiness: `kubectl get deploy -n [namespace] -o wide`
   - Check resource metrics: `kubectl top pod -n [namespace]`

## 📊 Formato de Saída

```markdown
# 🎯 Kubernetes Resource: [RESOURCE_KIND]

## Resource Specification

**Name**: [resource-name]
**Namespace**: [namespace]
**Kind**: [Deployment/Pod/StatefulSet/etc]
**Labels**:
- app: [app-name]
- version: [version]
- managed-by: kubernetes-specialist

## Manifest

\`\`\`yaml
# [Brief description of resource]
apiVersion: apps/v1
kind: [KIND]
metadata:
  name: [name]
  namespace: [namespace]
  labels:
    app: [app]
    version: [version]
spec:
  # Configuration here...
\`\`\`

## Configuration Details

### Security Context
- Runs as non-root user
- Read-only root filesystem
- No privilege escalation

### Resource Management
| Resource | Request | Limit | Rationale |
|----------|---------|-------|-----------|
| CPU | 250m | 500m | [Explanation] |
| Memory | 256Mi | 512Mi | [Explanation] |

### Health Checks
- **Liveness**: [Type and config]
- **Readiness**: [Type and config]

## Deployment Steps

1. Review the manifest above
2. Adjust as needed for your environment
3. Deploy: \`kubectl apply -f manifest.yaml\`
4. Verify: \`kubectl get pods -n [namespace]\`
5. Monitor: \`kubectl logs -f [pod-name] -n [namespace]\`

## Scaling & Modification

- To scale replicas: \`kubectl scale deployment [name] --replicas=N -n [namespace]\`
- To update image: \`kubectl set image deployment/[name] [container]=[image] -n [namespace]\`
- To modify resource limits: \`kubectl set resources deployment [name] --limits=cpu=500m,memory=512Mi -n [namespace]\`

## Monitoring

- View resource usage: \`kubectl top pod [pod-name] -n [namespace]\`
- Check events: \`kubectl describe pod [pod-name] -n [namespace]\`
- View logs: \`kubectl logs [pod-name] -n [namespace]\`

## Troubleshooting

If pods don't start:
1. Check events: \`kubectl describe pod [pod-name] -n [namespace]\`
2. View logs: \`kubectl logs [pod-name] -n [namespace] --previous\`
3. Verify image: \`kubectl get pod [pod-name] -n [namespace] -o yaml | grep image\`
```

## ✅ Critérios de Sucesso

- [ ] Resource kind identified and appropriate
- [ ] Manifest generated with proper API version and structure
- [ ] Security context configured appropriately
- [ ] Resource requests and limits defined
- [ ] Health checks configured (if applicable)
- [ ] Labels and metadata complete
- [ ] YAML syntax validated
- [ ] Documentation generated with scaling/modification guide
- [ ] Deployment verified on cluster
- [ ] Resource metrics collected after deployment

## ❌ Anti-Patterns

### ❌ Erro 1: Missing Resource Limits

Never create resources without limits:

```yaml
# ❌ Errado
containers:
- name: app
  image: myapp:latest
  # Sem limits - pode consumir todos os recursos do node

# ✅ Correto
containers:
- name: app
  image: myapp:latest
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

### ❌ Erro 2: Running as Root

Never run containers as root unless absolutely necessary:

```yaml
# ❌ Errado
securityContext:
  runAsUser: 0  # Root user

# ✅ Correto
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
```

### ❌ Erro 3: Using Latest Tag

Never use "latest" tag in production:

```yaml
# ❌ Errado
image: myapp:latest

# ✅ Correto
image: myapp:v1.2.3  # Specific semantic version
```

### ❌ Erro 4: Missing Namespace Specification

Always specify namespace explicitly:

```yaml
# ❌ Errado
metadata:
  name: myapp
  # Usa default namespace implicitamente

# ✅ Correto
metadata:
  name: myapp
  namespace: production
```

## 📝 Exemplos

### Exemplo 1: Create Deployment

```bash
/k8s-create-resource Deployment my-api production
```

Gera um deployment completo com:

- 3 replicas por padrão
- Resource requests e limits
- Liveness e readiness probes
- Security context configurado

### Exemplo 2: Create StatefulSet

```bash
/k8s-create-resource StatefulSet database production
```

Gera um StatefulSet com:

- Headless service
- Persistent volume claims
- Ordered pod names
- Network policies

### Exemplo 3: Create ConfigMap

```bash
/k8s-create-resource ConfigMap app-config production
```

Gera um ConfigMap para:

- Variáveis de ambiente
- Arquivos de configuração
- Dados não-sensíveis
