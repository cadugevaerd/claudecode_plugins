---
description: Verifica workflows GitHub Actions existentes, versões de actions e sugere atualizações
---

# Check GitHub Actions Workflows

Analisa workflows GitHub Actions existentes no projeto, verifica versões de actions utilizadas e sugere atualizações quando disponíveis.

## 🎯 Objetivo

Realizar auditoria completa de workflows GitHub Actions:

- Detectar workflows existentes
- Verificar versões de actions
- Comparar com últimas versões disponíveis no GitHub Marketplace
- Identificar problemas de segurança
- Sugerir melhorias

## 📋 Como usar

````bash
/cicd-check

```text

Com análise detalhada:

```bash
/cicd-check --detailed

```text

## 🔍 Processo de Execução

### 1. Detectar Workflows Existentes

**Buscar workflows em `.github/workflows/`**:

```bash

# Listar todos os workflows
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null

```text

**Se NÃO encontrar workflows**:

```text

❌ Nenhum workflow GitHub Actions encontrado.

💡 Para inicializar CI/CD, use:
   /cicd-init

```text

**Se encontrar workflows**:

```text

✅ Workflows encontrados:

📁 .github/workflows/
├─ ci.yml
├─ deploy.yml
└─ release.yml

Analisando...

```text

### 2. Analisar Cada Workflow

**Para cada arquivo `.yml` ou `.yaml`**:

#### a) Validar Sintaxe YAML

```python
import yaml

try:
    with open(workflow_file) as f:
        workflow = yaml.safe_load(f)
    print(f"✅ {workflow_file}: YAML válido")
except yaml.YAMLError as e:
    print(f"❌ {workflow_file}: Erro de sintaxe YAML")
    print(f"   {e}")

```text

#### b) Extrair Informações do Workflow

```python
workflow_info = {
    "name": workflow.get("name", "Sem nome"),
    "triggers": list(workflow.get("on", {}).keys()),
    "jobs": list(workflow.get("jobs", {}).keys()),
    "actions_used": []
}

```text

#### c) Identificar Actions Utilizadas

**Buscar por `uses:` em todos os steps**:

```python
for job_name, job_config in workflow.get("jobs", {}).items():
    for step in job_config.get("steps", []):
        if "uses" in step:
            action = step["uses"]
            workflow_info["actions_used"].append({
                "action": action,
                "job": job_name,
                "step_name": step.get("name", "Sem nome")
            })

```text

### 3. Verificar Versões de Actions

**Para cada action identificada**:

#### a) Extrair Nome e Versão

```python

# Exemplo: actions/checkout@v4

# Exemplo: astral-sh/setup-uv@v6

# Exemplo: actions/setup-python@8ade135a41bc03ea155e62e844d188df1ea18608

import re

match = re.match(r"([^@]+)@(.+)", action)
if match:
    action_name = match.group(1)
    current_version = match.group(2)

```text

#### b) Classificar Tipo de Versão

```python
def classify_version(version):
    if re.match(r"^v?\d+$", version):
        return "major_only", "⚠️"  # v4, 4
    elif re.match(r"^v?\d+\.\d+$", version):
        return "major_minor", "✅"  # v4.1, 4.1
    elif re.match(r"^v?\d+\.\d+\.\d+$", version):
        return "semver", "✅"  # v4.1.0, 4.1.0
    elif re.match(r"^[a-f0-9]{40}$", version):
        return "sha_pinned", "🔒"  # commit SHA
    elif version == "latest" or version == "main" or version == "master":
        return "branch", "❌"  # NUNCA usar!
    else:
        return "unknown", "❓"

```text

#### c) Buscar Última Versão no GitHub

**Usar GitHub API para buscar releases**:

```bash

# Via gh CLI
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# Exemplo para actions/checkout
gh api repos/actions/checkout/releases/latest --jq '.tag_name'

```text

**Actions populares e versões (atualizadas 2025)**:

```python
KNOWN_ACTIONS_VERSIONS = {
    "actions/checkout": "v4",
    "actions/setup-python": "v5",
    "actions/setup-node": "v4",
    "actions/setup-go": "v5",
    "actions/cache": "v4",
    "astral-sh/setup-uv": "v6",
    "actions/upload-artifact": "v4",
    "actions/download-artifact": "v4",
    "docker/build-push-action": "v5",
    "docker/setup-buildx-action": "v3",
}

```text

### 4. Identificar Problemas de Segurança

**Verificar práticas inseguras**:

```python
security_issues = []

# 1. Uso de @latest, @main, @master
if version in ["latest", "main", "master"]:
    security_issues.append({
        "severity": "CRITICAL",
        "issue": f"Action usando branch '{version}' ao invés de versão específica",
        "recommendation": f"Use versão específica como @v4 ou SHA commit"
    })

# 2. Permissions muito amplas
if "permissions" not in workflow or workflow["permissions"] == "write-all":
    security_issues.append({
        "severity": "HIGH",
        "issue": "Permissions não definidas ou muito amplas",
        "recommendation": "Defina permissions mínimas necessárias"
    })

# 3. Secrets expostos
for job in workflow.get("jobs", {}).values():
    for step in job.get("steps", []):
        if "run" in step and "${{" in step["run"]:
            if "secrets" in step["run"].lower():
                security_issues.append({
                    "severity": "MEDIUM",
                    "issue": "Possível exposição de secrets em logs",
                    "recommendation": "Use environment variables ao invés de inline"
                })

# 4. Third-party actions não verificadas
for action_info in actions_used:
    action_name = action_info["action"].split("@")[0]
    if "/" in action_name and not action_name.startswith(("actions/", "github/")):
        # É third-party, verificar se é conhecida
        if action_name not in TRUSTED_ACTIONS:
            security_issues.append({
                "severity": "MEDIUM",
                "issue": f"Action third-party: {action_name}",
                "recommendation": "Revisar código da action antes de usar"
            })

```text

### 5. Gerar Relatório Completo

**Formato de saída**:

```text

═══════════════════════════════════════════════════════════════
📊 ANÁLISE DE WORKFLOWS GITHUB ACTIONS
═══════════════════════════════════════════════════════════════

📁 Projeto: /path/to/project
📅 Data: 2025-10-26

───────────────────────────────────────────────────────────────
📋 WORKFLOWS ENCONTRADOS (3)
───────────────────────────────────────────────────────────────

1️⃣  ci.yml
    Nome: CI
    Triggers: push, pull_request
    Jobs: test, lint
    Actions: 5

2️⃣  deploy.yml
    Nome: Deploy to Production
    Triggers: push (branch: main)
    Jobs: build, deploy
    Actions: 8

3️⃣  release.yml
    Nome: Release
    Triggers: workflow_dispatch
    Jobs: release
    Actions: 3

───────────────────────────────────────────────────────────────
🔍 VERSÕES DE ACTIONS
───────────────────────────────────────────────────────────────

✅ actions/checkout@v4
   Status: ✅ Atualizada (latest: v4)
   Tipo: Major version pinning
   Usado em: ci.yml (test), deploy.yml (build)

⚠️  actions/setup-python@v4
   Status: ⚠️  Desatualizada (latest: v5)
   Tipo: Major version pinning
   Usado em: ci.yml (test)
   💡 Atualização disponível!

🔒 astral-sh/setup-uv@v6
   Status: ✅ Atualizada (latest: v6)
   Tipo: Major version pinning
   Usado em: ci.yml (test)

❌ actions/cache@latest
   Status: ❌ INSEGURO (usando @latest)
   Tipo: Branch reference
   Usado em: ci.yml (test)
   🚨 CRÍTICO: Usar versão específica!

───────────────────────────────────────────────────────────────
🔒 PROBLEMAS DE SEGURANÇA (3)
───────────────────────────────────────────────────────────────

🔴 CRÍTICO (1)
├─ Action usando branch 'latest' ao invés de versão específica
│  Arquivo: ci.yml
│  Action: actions/cache@latest
│  💡 Recomendação: Use @v4

🟡 MÉDIO (2)
├─ Permissions não definidas
│  Arquivo: deploy.yml
│  💡 Recomendação: Adicione 'permissions: contents: read'
│
└─ Action third-party não verificada
   Arquivo: deploy.yml
   Action: someuser/custom-action@v1
   💡 Recomendação: Revisar código antes de usar

───────────────────────────────────────────────────────────────
💡 RECOMENDAÇÕES
───────────────────────────────────────────────────────────────

🔄 Atualizações Disponíveis (1)
└─ actions/setup-python: v4 → v5

🔒 Melhorias de Segurança (2)
├─ Adicionar permissions explícitas em deploy.yml
└─ Pin actions/cache com versão específica

📈 Otimizações Possíveis
├─ Considerar SHA pinning para máxima segurança
└─ Adicionar caching para dependências Python

───────────────────────────────────────────────────────────────
🚀 PRÓXIMOS PASSOS
───────────────────────────────────────────────────────────────

Para atualizar actions automaticamente:
   /cicd-update

Para aplicar correções de segurança:
   /cicd-fix-security

Para mais detalhes sobre uma action específica:
   /cicd-check --action actions/setup-python

═══════════════════════════════════════════════════════════════

```text

## 🔧 Opções Avançadas

**Verificar action específica**:

```bash
/cicd-check --action actions/checkout

```text

**Exportar relatório JSON**:

```bash
/cicd-check --format json --output cicd-report.json

```text

**Verificar apenas segurança**:

```bash
/cicd-check --security-only

```text

## 📊 Métricas Calculadas

O comando também calcula:

- **Coverage de CI/CD**: % de branches com workflows
- **Security Score**: 0-100 baseado em práticas
- **Update Status**: Quantas actions estão desatualizadas
- **Complexity Score**: Complexidade dos workflows

## ⚡ Performance

**Otimizações**:
- Cache de versões de actions (15 minutos)
- Análise paralela de múltiplos workflows
- Rate limiting inteligente para GitHub API

## 🎓 Referências

- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Dependabot for GitHub Actions](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
````
