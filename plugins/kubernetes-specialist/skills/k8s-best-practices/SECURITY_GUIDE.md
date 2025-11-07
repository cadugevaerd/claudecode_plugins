# Kubernetes Security Best Practices Guide

**Detailed security patterns, configurations, and hardening guidelines for Kubernetes deployments.**

## 🔐 Security Context Configuration

### Recommended Security Context Template

```yaml
securityContext:
  runAsNonRoot: true           # Never run as root
  runAsUser: 1000              # Non-root user ID
  fsGroup: 2000                # File system group
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true # When possible
  capabilities:
    drop:
      - ALL                    # Drop all capabilities
    add:
      - NET_BIND_SERVICE      # Add only if needed
```

### Security Context Fields Explained

**runAsNonRoot**: Ensures container does not run as root user. Prevents privilege escalation attacks.

**runAsUser**: Specifies UID for running the container. Use non-privileged UID (1000+).

**fsGroup**: Sets the filesystem group for mounted volumes. All files created will have this GID.

**allowPrivilegeEscalation**: Controls whether a process can gain more privileges than parent. Set to `false` to prevent escalation.

**readOnlyRootFilesystem**: Makes root filesystem read-only. Forces use of mounted volumes for writes.

**capabilities**: Fine-grained permissions. Drop ALL by default, add only what's needed.

### Common Capabilities

- `NET_BIND_SERVICE`: Bind to ports < 1024
- `SYS_TIME`: Modify system clock
- `NET_ADMIN`: Network administration
- `SYS_ADMIN`: System administration (dangerous!)

**Rule**: Drop ALL, add minimum required.

## 🖼️ Image Security

### Image Tag Best Practices

❌ **Never use**:

```yaml
image: nginx:latest
```

✅ **Always use semantic versions**:

```yaml
image: nginx:1.21.6-alpine
```

**Why?**

- `latest` changes unpredictably
- Semantic versions are immutable
- Enables rollback and debugging
- Reproducible builds

### Image Scanning

**Tools**:

- **Trivy**: Open-source vulnerability scanner
- **Snyk**: Commercial scanner with database
- **Clair**: Container vulnerability analysis
- **Anchore**: Deep inspection and policy enforcement

**Best Practice**:

```bash
# Scan before deployment
trivy image nginx:1.21.6-alpine

# Fail CI/CD if HIGH or CRITICAL found
trivy image --severity HIGH,CRITICAL --exit-code 1 nginx:1.21.6-alpine
```

### Private Registry Configuration

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-auth>
---
apiVersion: v1
kind: Pod
metadata:
  name: private-pod
spec:
  containers:
  - name: app
    image: myregistry.azurecr.io/app:1.0.0
  imagePullSecrets:
  - name: regcred
```

### Image Policy Enforcement

Use admission controllers to enforce:

- No `latest` tags
- Only approved registries
- Scanned images only
- Signed images (Notary, Cosign)

**Tools**:

- **OPA/Gatekeeper**: Policy enforcement
- **Kyverno**: Kubernetes-native policies
- **Admission Webhooks**: Custom validation

## 🔑 RBAC Best Practices

### Principle of Least Privilege

Create service accounts per application with minimum permissions:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

### RBAC Rules

1. **Per-application service accounts**: Never use `default` SA
1. **Namespace-scoped roles**: Avoid ClusterRole unless necessary
1. **Minimal verbs**: Only grant needed verbs (get, list, watch vs create, delete)
1. **Audit regularly**: Review RoleBindings quarterly
1. **Use aggregated roles**: For common patterns

### Common RBAC Mistakes

❌ **Too permissive**:

```yaml
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

❌ **ClusterAdmin to apps**:

```yaml
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  name: cluster-admin
```

✅ **Scoped and specific**:

```yaml
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["app-config"]
  verbs: ["get"]
```

## 🔒 Secrets Management

### Kubernetes Secrets

**Basic Secret**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: production
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=
```

**Consume in Pod**:

```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secret
      key: password
```

### Encryption at Rest

Enable encryption at rest in kube-apiserver:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <32-byte-base64-encoded-key>
  - identity: {}
```

### External Secret Managers

**Recommended**:

- **AWS Secrets Manager** + External Secrets Operator
- **Azure Key Vault** + CSI driver
- **HashiCorp Vault** + Agent Injector
- **Google Secret Manager** + Workload Identity

**Benefits**:

- Centralized secret management
- Automatic rotation
- Audit logging
- Access policies outside K8s

### Secret Rotation

**Manual rotation**:

1. Create new secret version
1. Update pods to use new secret
1. Rolling restart
1. Delete old secret

**Automatic rotation**:

- Use External Secrets Operator with rotation policy
- Implement sidecar for dynamic secret fetching
- Use CSI driver with auto-rotation

**Frequency**: Monthly minimum for production secrets.

## 🛡️ Network Policies

### Default Deny Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## 📋 Pod Security Standards

Kubernetes defines 3 levels:

1. **Privileged**: Unrestricted (for system components)
1. **Baseline**: Minimally restrictive (prevent known privilege escalations)
1. **Restricted**: Heavily restricted (defense in depth)

**Apply at namespace level**:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## 🔍 Security Auditing

### Regular Security Checks

- **kubectl**: `kubectl auth can-i --list --as=system:serviceaccount:prod:app-sa`
- **Trivy**: Scan images and K8s configs
- **Kubeaudit**: Audit cluster configuration
- **kube-bench**: CIS Kubernetes Benchmark

### Audit Logging

Enable audit logging in kube-apiserver for RBAC changes, secret access, and resource modifications.

**Key events to log**:

- Secret access
- RBAC changes
- Pod creation/deletion
- ConfigMap modifications
- Failed authentication attempts

## 📚 References

- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
