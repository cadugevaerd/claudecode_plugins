---
name: action-version-checker
description: Verifica versões de GitHub Actions nos workflows e compara com últimas versões disponíveis. Use quando atualizar workflows, revisar dependências de actions, checar se actions estão desatualizadas, fazer auditoria de versões.
allowed-tools: Read, Bash, Grep
---

# Action Version Checker Skill

## Instructions

Verifica automaticamente versões de GitHub Actions utilizadas nos workflows e compara com as últimas versões disponíveis no GitHub Marketplace.

### 1. Extrair Actions dos Workflows

```bash
# Buscar todas as linhas com 'uses:' nos workflows
grep -r "uses:" .github/workflows/ | grep -v "^#"
```

Output exemplo:
```
.github/workflows/ci.yml:      - uses: actions/checkout@v4
.github/workflows/ci.yml:      - uses: astral-sh/setup-uv@v6
.github/workflows/deploy.yml:  - uses: actions/setup-python@v4
```

### 2. Parse Action References

Para cada linha encontrada, extrair:
- **Action name**: `actions/checkout`
- **Version**: `v4`
- **Version type**: `major`, `semver`, `sha`, ou `branch`

Formato comum:
```
uses: {owner}/{repo}@{version}
uses: {owner}/{repo}/{path}@{version}
```

### 3. Classificar Tipo de Versão

```python
import re

def classify_version(version):
    if re.match(r'^v?\d+$', version):
        return 'major_only'  # v4, 4
    elif re.match(r'^v?\d+\.\d+$', version):
        return 'major_minor'  # v4.1
    elif re.match(r'^v?\d+\.\d+\.\d+$', version):
        return 'semver'  # v4.1.0
    elif re.match(r'^[a-f0-9]{40}$', version):
        return 'sha_commit'  # SHA completo
    elif version in ['latest', 'main', 'master']:
        return 'branch'  # ❌ INSEGURO
    else:
        return 'unknown'
```

### 4. Buscar Última Versão Disponível

#### Opção A: Usar gh CLI (Preferido)

```bash
# Buscar latest release
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# Exemplo para actions/checkout
gh api repos/actions/checkout/releases/latest --jq '.tag_name'
```

#### Opção B: Versões Conhecidas (Fallback)

```python
KNOWN_LATEST_VERSIONS = {
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
```

### 5. Comparar Versões

```python
def compare_versions(current, latest):
    """
    Retorna tipo de update: MAJOR, MINOR, PATCH, ou UP_TO_DATE
    """
    # Parse semver
    current_parts = parse_semver(current)
    latest_parts = parse_semver(latest)

    if current_parts[0] < latest_parts[0]:
        return 'MAJOR', '🔴', 'Breaking changes possíveis'
    elif current_parts[1] < latest_parts[1]:
        return 'MINOR', '🟡', 'Novas features, compatível'
    elif current_parts[2] < latest_parts[2]:
        return 'PATCH', '🟢', 'Bug fixes, seguro'
    else:
        return 'UP_TO_DATE', '✅', 'Atualizada'
```

### 6. Reportar Resultados

```
═══════════════════════════════════════════
🔍 VERIFICAÇÃO DE VERSÕES
═══════════════════════════════════════════

✅ actions/checkout@v4
   Latest: v4
   Status: Atualizada

⚠️  actions/setup-python@v4
   Latest: v5
   Status: Desatualizada (MINOR update)
   Changelog: https://github.com/actions/setup-python/releases/tag/v5.0.0

🔴 actions/cache@latest
   Latest: v4
   Status: INSEGURO (usando @latest)
   Fix: Mudar para @v4

───────────────────────────────────────────
📊 Resumo
───────────────────────────────────────────
Total: 8 actions
├─ ✅ Atualizadas: 5
├─ ⚠️  Desatualizadas: 2
└─ 🔴 Inseguras: 1

Comando para atualizar:
/cicd-update
═══════════════════════════════════════════
```

## When to Use

- Revisar workflows após período sem updates
- Antes de fazer deploy em produção
- Auditoria de segurança mensal/trimestral
- Após GitHub anunciar nova versão de action
- Troubleshooting de workflows quebrados
- Code review de PRs que modificam workflows

Termos de gatilho:
- "versões de actions"
- "atualizar GitHub Actions"
- "actions desatualizadas"
- "latest version"
- "check versions"
- "dependências de workflow"

## Examples

### Exemplo 1: Action Atualizada

```yaml
uses: actions/checkout@v4
```

Verificação:
```
✅ actions/checkout@v4
   Latest: v4
   Status: Atualizada
```

### Exemplo 2: Action Desatualizada

```yaml
uses: actions/setup-python@v4
```

Verificação:
```
⚠️  actions/setup-python@v4
   Latest: v5
   Update: MINOR (v4 → v5)
   Breaking: Não
   Changelog: https://github.com/actions/setup-python/releases/tag/v5.0.0

   💡 Atualização recomendada:
   uses: actions/setup-python@v5
```

### Exemplo 3: Action Insegura

```yaml
uses: actions/cache@latest
```

Verificação:
```
🔴 actions/cache@latest
   Status: INSEGURO (usando @latest)
   Latest: v4
   Severidade: CRÍTICA

   ❌ NUNCA use @latest ou @main
   ✅ Use versão específica: @v4

   Fix:
   - uses: actions/cache@latest
   + uses: actions/cache@v4
```

## Version Update Matrix

| Current | Latest | Type | Risk | Recomendação |
|---------|--------|------|------|--------------|
| v4.1.0 | v4.1.1 | PATCH | 🟢 Baixo | Atualizar automaticamente |
| v4.1.0 | v4.2.0 | MINOR | 🟡 Médio | Revisar changelog |
| v4.1.0 | v5.0.0 | MAJOR | 🔴 Alto | Revisar breaking changes |
| @latest | v4.0.0 | - | 🔴 Crítico | Mudar para versão específica |

## Known Actions Database

### Official GitHub Actions

```python
GITHUB_ACTIONS = {
    "actions/checkout": {
        "current_version": "v4",
        "repository": "actions/checkout",
        "type": "official",
        "trust_level": "high"
    },
    "actions/setup-python": {
        "current_version": "v5",
        "repository": "actions/setup-python",
        "type": "official",
        "trust_level": "high"
    },
    # ... mais actions
}
```

### Third-Party Trusted

```python
TRUSTED_THIRD_PARTY = {
    "astral-sh/setup-uv": {
        "current_version": "v6",
        "maintainer": "Astral (creators of uv, ruff)",
        "trust_level": "high"
    },
    "docker/build-push-action": {
        "current_version": "v5",
        "maintainer": "Docker Inc",
        "trust_level": "high"
    },
}
```

## Security Checks

### Unsafe Version Patterns

```python
UNSAFE_PATTERNS = {
    "@latest": "CRITICAL - Use specific version",
    "@main": "CRITICAL - Use specific version",
    "@master": "CRITICAL - Use specific version",
    "@develop": "HIGH - Use stable release",
    "@HEAD": "CRITICAL - Use specific version",
}
```

### Recommended Pinning Strategy

```yaml
# 🟢 Bom - Major version pinning
uses: actions/checkout@v4

# 🟡 Melhor - Semver pinning
uses: actions/checkout@v4.1.0

# 🔒 Máximo - SHA pinning (produção)
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608
```

## Performance Optimization

- **Cache de versões**: Armazenar últimas versões por 24h
- **Batch queries**: Agrupar chamadas à GitHub API
- **Rate limiting**: Respeitar limites da API (5000/hour)
- **Parallel checking**: Verificar múltiplas actions simultaneamente

## Error Handling

### API Rate Limit

```
⚠️  GitHub API rate limit alcançado
Tentando usar versões conhecidas...

Fallback para KNOWN_LATEST_VERSIONS
```

### Network Error

```
❌ Erro ao buscar versão de actions/custom-action
Usando última versão conhecida: v1.2.0 (cache)
```

### Unknown Action

```
❓ Action desconhecida: user/unknown-action@v1
- Não encontrada no GitHub Marketplace
- Verificar se repositório existe
- Considerar usar action oficial alternativa
```

## Integration with Update Command

Skill fornece dados para `/cicd-update`:

```python
{
    "actions_to_update": [
        {
            "name": "actions/setup-python",
            "current": "v4",
            "latest": "v5",
            "type": "MINOR",
            "files": [".github/workflows/ci.yml"],
            "safe_to_auto_update": True
        }
    ],
    "actions_with_issues": [
        {
            "name": "actions/cache",
            "current": "latest",
            "issue": "Using branch instead of version",
            "severity": "CRITICAL"
        }
    ]
}
```

## References

- [GitHub Actions Versioning](https://docs.github.com/en/actions/creating-actions/about-custom-actions#using-release-management-for-actions)
- [GitHub Releases API](https://docs.github.com/en/rest/releases/releases)
- [Semantic Versioning](https://semver.org/)
