# Kubernetes Specialist Plugin

**Advanced plugin for Kubernetes resource management, troubleshooting, and best practices implementation based on 2025 industry standards.**

## 🎯 Overview

The Kubernetes Specialist plugin provides comprehensive tools for managing Kubernetes clusters effectively. It helps you:

- **Diagnose** pod failures and cluster issues quickly
- **Create** production-ready resources with security and optimization built-in
- **Optimize** resource allocation to reduce costs while maintaining performance
- **Learn** best practices from real-world patterns and solutions

This plugin is built around proven 2025 Kubernetes best practices focusing on:

- Resource right-sizing (addressing 99.94% over-provisioning issue)
- Security hardening (non-root, minimal capabilities)
- Cost optimization (10% average CPU utilization improvement opportunity)
- Production reliability (health checks, RBAC, observability)

## 📦 Components

### Commands (Slash Commands)

Quick access tools for immediate tasks:

#### `/k8s-diagnose [RESOURCE_TYPE] [RESOURCE_NAME] [NAMESPACE]`

Diagnose Kubernetes pod failures and identify root causes.

**Use this to:**

- Fix CrashLoopBackOff, OOMKilled, ImagePullBackOff pods
- Find performance bottlenecks
- Analyze resource utilization patterns
- Get step-by-step remediation guidance

**Example:**

```bash
/k8s-diagnose pod my-app production
```

**Output:**

- Problem summary
- Root cause analysis
- Immediate actions with kubectl commands
- Long-term recommendations
- Resource metrics comparison

#### `/k8s-create-resource [RESOURCE_KIND] [RESOURCE_NAME] [NAMESPACE]`

Generate production-ready Kubernetes manifests.

**Use this to:**

- Create Deployments with proper resource limits
- Generate Stateful Sets with PVCs
- Set up Services and ConfigMaps
- Apply security best practices automatically

**Example:**

```bash
/k8s-create-resource Deployment api-server production
```

**Output:**

- Complete YAML manifest
- Security configuration explanation
- Resource justification
- Scaling and modification guide
- Troubleshooting tips

#### `/k8s-optimize [NAMESPACE] [DEPLOYMENT_NAME]`

Analyze and optimize cluster resources for cost and performance.

**Use this to:**

- Identify over-provisioned resources
- Calculate potential cost savings
- Get HPA/VPA recommendations
- Plan capacity optimization phases

**Example:**

```bash
/k8s-optimize production
```

**Output:**

- Current resource efficiency metrics
- Over-provisioning opportunities with percentages
- Under-provisioning risk assessment
- Cost impact analysis
- Implementation roadmap with safe/validated/advanced phases

### Agents (Autonomous Processors)

Specialized agents that handle complex analysis tasks:

#### `k8s-resource-analyzer`

Analyzes Kubernetes cluster resources against best practices.

**Invoked via:**

```bash
# In a task or prompt, reference:
Task(subagent_type="kubernetes-resource-analyzer", prompt="Analyze all deployments for misconfigurations")
```

**Capabilities:**

- Collect resource metrics across cluster
- Validate security context compliance
- Identify over/under provisioning
- Score configuration against 2025 best practices
- Generate priority-ranked issue report

#### `k8s-troubleshooter`

Diagnoses and resolves pod failures.

**Invoked via:**

```bash
Task(subagent_type="kubernetes-troubleshooter", prompt="Debug why pod nginx-123 in production keeps crashing")
```

**Capabilities:**

- Analyze logs and events
- Classify failure type
- Root cause determination
- Step-by-step remediation
- Monitor and validation

### Skills (Knowledge References)

Comprehensive guides for learning and reference:

#### `k8s-best-practices`

2025 Kubernetes best practices reference.

**Covers:**

- Resource request/limit guidelines
- Over-provisioning analysis (99.94% reality check)
- Security context configuration
- RBAC and network policies
- Namespace and quota management
- Health check patterns
- HPA and VPA implementation
- Storage best practices
- Observability setup
- Common mistakes and solutions

#### `k8s-troubleshooting-patterns`

Diagnostic patterns for common pod failures.

**Covers:**

- CrashLoopBackOff diagnosis and fixes
- OOMKilled analysis and solutions
- ImagePullBackOff debugging
- Pending pod investigation
- CreateContainerConfigError
- ErrImagePull troubleshooting
- Diagnostic decision tree
- Essential kubectl commands
- Prevention strategies

## 🚀 Quick Start

### 1. Diagnose a Failing Pod

```bash
# Pod crashed? Get diagnostic report
/k8s-diagnose pod my-failing-pod production

# Read the report → Follow immediate actions → Verify fix
```

### 2. Create a New Deployment

```bash
# Need a new deployment following best practices?
/k8s-create-resource Deployment my-api production

# Review manifest → Adjust as needed → Deploy with kubectl apply
```

### 3. Optimize Cluster Costs

```bash
# Want to reduce infrastructure costs?
/k8s-optimize production

# Review recommendations → Implement phase 1 (safe) → Monitor → Plan phase 2
```

### 4. Learn Best Practices

Use the skills for reference:

- Check `/skill k8s-best-practices` for configuration patterns
- Review `/skill k8s-troubleshooting-patterns` for common issues

## 💡 Common Use Cases

### Use Case 1: Production Incident Response

**Scenario:** Pod keeps restarting in production.

**Steps:**

1. Run `/k8s-diagnose pod [pod-name] production`
1. Read "Immediate Actions" section
1. Execute suggested kubectl commands
1. Monitor pod status with `kubectl get pod -w`
1. Review "Long-term Recommendations" to prevent recurrence

**Time to Resolution:** 2-5 minutes

### Use Case 2: Infrastructure Cost Reduction

**Scenario:** Cloud bill is too high.

**Steps:**

1. Run `/k8s-optimize production`
1. Review "Over-Provisioning Analysis" section
1. Implement Phase 1 changes (safe, immediate)
1. Monitor for 24-48 hours
1. Plan Phase 2 after validation

**Cost Savings:** Typically 20-40% from right-sizing alone

### Use Case 3: Deploying New Service

**Scenario:** Need to deploy new microservice.

**Steps:**

1. Run `/k8s-create-resource Deployment [service-name] production`
1. Review generated manifest for security and resource config
1. Adjust image, replicas, and ports as needed
1. Deploy: `kubectl apply -f manifest.yaml`
1. Verify: `kubectl get pods -n production -l app=[service-name]`

**Result:** Production-ready deployment in < 5 minutes

### Use Case 4: Learning Kubernetes Best Practices

**Scenario:** Team needs to improve K8s practices.

**Steps:**

1. Review `/skill k8s-best-practices` sections relevant to your needs
1. Check `/skill k8s-troubleshooting-patterns` to understand common failures
1. Apply recommendations to existing deployments
1. Use `/k8s-diagnose` to validate improvements

**Outcome:** Better practices, fewer incidents, lower costs

## 📊 Integration with Claude Code

This plugin works seamlessly within Claude Code:

```bash
# Use commands directly in Claude Code CLI
/k8s-diagnose pod my-pod default

# Reference agents in custom tasks
Task(subagent_type="kubernetes-resource-analyzer", prompt="...")

# Access skills for knowledge
# Type: "Check skill k8s-best-practices for resource limits"
```

## 🔗 Related Resources

### External Documentation

- [Kubernetes Official Best Practices](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [2025 Industry Benchmarks](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)

### Tools Referenced

- **kubectl**: Official Kubernetes CLI (required)
- **Metrics Server**: For `kubectl top` commands (needed for `/k8s-optimize`)
- **Image registry access**: For `/k8s-create-resource` to validate images

## 🔌 MCP Server Integration

### Kubernetes Toolkit MCP

This plugin includes **Kubernetes Toolkit MCP server** integration, providing AI-powered Kubernetes cluster management through the Model Context Protocol.

**Features:**

- Direct Kubernetes API integration (not just kubectl wrapper)
- 40+ tools for managing Kubernetes resources
- Secure authentication with TLS and RBAC validation
- Read-only mode support for safer operations
- Real-time cluster insights and context

**Configuration:**

The plugin includes `.mcp.json` with pre-configured Kubernetes MCP server using `mcp-server-kubernetes` npm package.

**Required Environment Variables:**

```bash
# Optional: Custom kubeconfig path (defaults to ~/.kube/config)
KUBECONFIG_PATH=/path/to/your/kubeconfig

# Optional: Specify Kubernetes context to use
K8S_CONTEXT=my-cluster-context

# Optional: Default namespace (defaults to 'default')
K8S_NAMESPACE=production

# Optional: Enable read-only mode (defaults to 'false')
ALLOW_ONLY_NON_DESTRUCTIVE_TOOLS=false

# Optional: Log level (defaults to 'info')
LOG_LEVEL=info
```

**Setup:**

1. Create a `.env` file with your Kubernetes configuration (see `.env.example`)
1. Restart Claude Code to load the MCP server
1. The MCP server will automatically use your `~/.kube/config` if no custom path is provided
1. Test connection: Commands and agents in this plugin will automatically use MCP tools

**Security Best Practices (2025):**

- ✅ All API traffic is encrypted with TLS
- ✅ Authentication via kubeconfig certificates
- ✅ RBAC policies enforced based on kubeconfig identity
- ✅ Optional read-only mode prevents destructive operations
- ✅ Audit logging for all operations
- ✅ No credentials hardcoded in configuration

**Read-Only Mode (Recommended for Production):**

For safer operations in production clusters, enable read-only mode:

```bash
ALLOW_ONLY_NON_DESTRUCTIVE_TOOLS=true
```

This disables all destructive operations (delete pods, delete deployments, delete namespaces, etc.) while maintaining full diagnostic and read capabilities.

## ⚙️ Requirements

### Prerequisites

- ✅ kubectl installed and configured
- ✅ Access to Kubernetes cluster (read permissions minimum)
- ✅ Metrics server installed (for optimization commands)
- ✅ Network connectivity to image registries
- ✅ Node.js and npm (for MCP server - automatically handled via npx)

### Permissions Needed

- Read: Pods, Deployments, StatefulSets, Services, ConfigMaps, Secrets
- Write: For deployment creation (requires Deployments create permission)
- List: Nodes, Events, ResourceQuotas, Namespaces

## 🎓 Learning Path

### Beginner

1. Read: `/skill k8s-best-practices` - "Resource Management Patterns"
1. Try: `/k8s-diagnose` on any failing pod
1. Implement: Recommended fixes from diagnostic report

### Intermediate

1. Review: `/skill k8s-troubleshooting-patterns` - All sections
1. Practice: Use `/k8s-diagnose` to fix different failure types
1. Deploy: Create resources with `/k8s-create-resource`

### Advanced

1. Optimize: Use `/k8s-optimize` to reduce cluster costs
1. Monitor: Track improvements over time
1. Scale: Implement HPA/VPA recommendations
1. Integrate: Use agents in custom workflows

## 🐛 Troubleshooting

### "kubectl not found"

Ensure kubectl is installed and in your PATH:

```bash
which kubectl
kubectl version --client
```

### "Unable to connect to cluster"

Verify your kubeconfig is configured:

```bash
kubectl config current-context
kubectl cluster-info
```

### "Metrics not available for /k8s-optimize"

Install metrics server:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Commands not found in Claude Code

Ensure plugin is installed:

```bash
/plugin refresh
/plugin list | grep kubernetes
```

## 🔌 MCP Troubleshooting

### MCP Server Connection Failed

**Error:** `plugin:kubernetes-specialist:kubernetes-toolkit: npx -y mcp-server-kubernetes - ✗ Failed to connect`

**Cause:** MCP server cannot be initialized via stdio transport.

**Solutions:**

1. **Verify kubectl installation:**

   ```bash
   which kubectl
   kubectl version --client
   ```

   If not found, install via package manager or https://kubernetes.io/docs/tasks/tools/

1. **Verify kubeconfig exists:**

   ```bash
   ls -la ~/.kube/config
   kubectl config current-context
   ```

   If missing, obtain kubeconfig from your cluster:

   - **AWS EKS:** `aws eks update-kubeconfig --name <cluster-name>`
   - **Google GKE:** `gcloud container clusters get-credentials <cluster-name>`
   - **Azure AKS:** `az aks get-credentials --resource-group <rg> --name <cluster>`

1. **Verify Node.js and npx:**

   ```bash
   node --version
   which npx
   npx -y mcp-server-kubernetes --help
   ```

   If Node.js not found, install via nvm, apt, snap, or brew

1. **Test MCP server directly:**

   ```bash
   npx -y mcp-server-kubernetes --help
   ```

   Should show help output without errors

1. **Restart Claude Code:**

   - Close all Claude Code instances
   - Clear cache: Remove `.claude-code` directory if needed
   - Reopen Claude Code
   - Run `/plugin refresh`

**Still not working?** Run `/setup-kubernetes-specialist` which will validate all requirements and provide specific fixes.

### "No kubeconfig" Error

**Error:** MCP server starts but cannot authenticate to cluster

**Solutions:**

```bash
# Set KUBECONFIG environment variable if using custom path
export KUBECONFIG=/path/to/your/kubeconfig

# Or create .env file in plugin directory
echo "KUBECONFIG=/path/to/your/kubeconfig" > .env

# Then restart Claude Code
```

### "Context not found" Error

**Error:** Specified Kubernetes context doesn't exist

**Solutions:**

```bash
# List available contexts
kubectl config get-contexts

# Switch to desired context
kubectl config use-context <context-name>

# Or set via environment variable
export KUBERNETES_CONTEXT=<context-name>
```

### "Permission denied" Errors

**Cause:** Kubeconfig user lacks required permissions

**Solutions:**

1. Verify kubeconfig has proper permissions:

   ```bash
   ls -la ~/.kube/config
   # Should be: -rw------- (600)
   chmod 600 ~/.kube/config
   ```

1. Check cluster RBAC permissions:

   ```bash
   kubectl auth can-i list deployments -n default
   kubectl auth can-i list pods -n default
   ```

1. Enable read-only mode for safer operations:

   ```bash
   export ALLOW_ONLY_NON_DESTRUCTIVE_TOOLS=true
   ```

### MCP Server Hangs or Times Out

**Symptoms:** Commands start but never complete

**Solutions:**

1. Check cluster connectivity:

   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

1. Verify network access to Kubernetes API:

   ```bash
   curl -k https://$(kubectl config view -o jsonpath='{.clusters[0].cluster.server}')
   ```

1. Increase timeouts (if available):

   ```bash
   export LOG_LEVEL=debug
   # Restart Claude Code to see detailed logs
   ```

### Validate MCP Setup

Run the setup command to automatically validate all requirements:

```bash
/setup-kubernetes-specialist
```

This will check:

- ✅ kubectl installed and version
- ✅ kubeconfig exists and valid
- ✅ Node.js/npx available
- ✅ mcp-server-kubernetes accessible
- ✅ Kubernetes context active

And provide step-by-step fixes for any issues found.

## 📈 Performance Expectations

| Command | Typical Duration | Resource Usage |
|---------|-----------------|-----------------|
| `/k8s-diagnose` | 5-15 seconds | Minimal (read-only) |
| `/k8s-create-resource` | 10-30 seconds | Minimal |
| `/k8s-optimize` (cluster) | 30-60 seconds | Moderate (metrics collection) |
| `k8s-resource-analyzer` | 1-3 minutes | Moderate (full cluster scan) |
| `k8s-troubleshooter` | 30-90 seconds | Minimal (single pod focus) |

## 📝 Examples

### Example 1: Fix CrashLoopBackOff

```bash
# Issue: Pod nginx-app keeps crashing
$ /k8s-diagnose pod nginx-app production

# Output:
# Problem Summary: Container exiting with code 1
# Root Cause: Missing NGINX_PORT environment variable
# Immediate Actions:
#   1. kubectl patch deployment nginx-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","env":[{"name":"NGINX_PORT","value":"8080"}]}]}}}}'
#   2. kubectl get pod -w -n production
#
# Long-term: Add validation in deployment to catch missing env vars earlier

$ kubectl set env deployment/nginx-app NGINX_PORT=8080 -n production
deployment.apps/nginx-app patched

$ kubectl get pod -n production
NAME                         READY   STATUS    RESTARTS   AGE
nginx-app-7d4c5f9b9-abc12   1/1     Running   0          30s
```

### Example 2: Optimize Costs

```bash
# Run optimization analysis
$ /k8s-optimize production api

# Output:
# Current CPU Efficiency: 15% (request 2000m, use 300m)
# Memory Efficiency: 22% (request 2Gi, use 450Mi)
#
# Phase 1 (Safe):
#   1. Reduce api-server deployment CPU: 2000m → 500m (expected usage × 1.5)
#   2. Reduce memory: 2Gi → 700Mi (expected usage × 1.5)
#
# Estimated Savings: $240/month (20% reduction)

$ kubectl set resources deployment api-server --requests=cpu=500m,memory=700Mi -n production
deployment.apps/api-server resource requirements updated

$ # Monitor for 24 hours to ensure no issues...
```

## 🤝 Contributing

Found a bug or want to add features? This plugin is part of the Claude Code Kubernetes specialist ecosystem. Report issues and suggestions.

## 📄 License

MIT License - Use freely in personal and commercial projects

## 👤 Author

**Carlos Araujo** - DevOps and Kubernetes specialist

- Email: cadu.gevaerd@gmail.com
- Focus: Infrastructure automation, cost optimization, reliability

______________________________________________________________________

**Last Updated:** 2025-11-07
**Plugin Version:** 1.0.0
**Kubernetes Support:** 1.25+ (tested on 1.27, 1.28, 1.29)
