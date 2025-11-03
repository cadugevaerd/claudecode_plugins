---
description: Atualiza versões de GitHub Actions nos workflows para as últimas versões disponíveis
---

# Update GitHub Actions Versions

Atualiza automaticamente as versões de GitHub Actions nos workflows do projeto para as últimas versões estáveis disponíveis no GitHub Marketplace.

## 🎯 Objetivo

Manter workflows GitHub Actions atualizados:

- Atualizar actions para últimas versões
- Aplicar correções de segurança
- Manter compatibilidade
- Gerar changelog de mudanças

## 📋 Como usar

````bash
/cicd-update

```text

Modo dry-run (preview sem modificar):

```bash
/cicd-update --dry-run

```text

Atualizar action específica:

```bash
/cicd-update --action actions/checkout

```text

## 🔍 Processo de Execução

### 1. Executar Análise de Workflows

**Primeiro, executar `/cicd-check`**:

```bash

# Internamente executa
/cicd-check

```text

**Analisar resultado**:
- Identificar actions desatualizadas
- Verificar versões disponíveis
- Calcular impacto de mudanças

### 2. Classificar Atualizações por Tipo

**Semantic Versioning aplicado**:

```python
def classify_update(current_version, latest_version):
    """
    Classifica tipo de atualização seguindo SemVer
    """
    current = parse_version(current_version)
    latest = parse_version(latest_version)

    if current.major < latest.major:
        return "MAJOR", "⚠️", "Pode ter breaking changes"
    elif current.minor < latest.minor:
        return "MINOR", "✅", "Novas features, compatível"
    elif current.patch < latest.patch:
        return "PATCH", "✅", "Bug fixes, seguro"
    else:
        return "SAME", "✅", "Já atualizada"

```text

**Classificação de risco**:

- 🟢 **BAIXO** (PATCH): v4.1.0 → v4.1.1
  - Bug fixes
  - Correções de segurança
  - Sem breaking changes
  - ✅ Atualização automática recomendada

- 🟡 **MÉDIO** (MINOR): v4.1.0 → v4.2.0
  - Novas features
  - Compatível com versão anterior
  - ⚠️  Revisar changelog antes de aplicar

- 🔴 **ALTO** (MAJOR): v4.1.0 → v5.0.0
  - Breaking changes
  - Pode requerer ajustes no workflow
  - ❌ Revisar documentação obrigatório

### 3. Buscar Informações de Atualização

**Para cada action a atualizar**:

#### a) Buscar Latest Release no GitHub

```bash

# Via gh CLI
gh api repos/{owner}/{repo}/releases/latest

```text

Exemplo de resposta:

```json
{
  "tag_name": "v5.0.0",
  "name": "v5.0.0",
  "body": "## What's Changed\n- Breaking: Removed deprecated parameters\n- Added new caching options",
  "published_at": "2025-01-15T10:00:00Z"
}

```text

#### b) Extrair Changelog

```python
def extract_breaking_changes(release_body):
    """
    Identifica breaking changes no changelog
    """
    breaking_indicators = [
        "breaking",
        "breaking change",
        "removed",
        "deprecated",
        "no longer supported",
        "incompatible",
    ]

    breaking_changes = []
    for line in release_body.split("\n"):
        if any(indicator in line.lower() for indicator in breaking_indicators):
            breaking_changes.append(line.strip())

    return breaking_changes

```text

### 4. Apresentar Preview de Mudanças

**Antes de aplicar, mostrar preview**:

```text

═══════════════════════════════════════════════════════════════
📦 ATUALIZAÇÕES DISPONÍVEIS
═══════════════════════════════════════════════════════════════

🟢 BAIXO RISCO - PATCH (2)
───────────────────────────────────────────────────────────────

✅ actions/checkout
   v4.1.0 → v4.1.1
   📅 Lançado: 2025-01-15
   📝 Mudanças:
      - Fix: Corrected submodule checkout issue
      - Security: Updated dependencies
   📁 Arquivos afetados:
      - .github/workflows/ci.yml
      - .github/workflows/deploy.yml

✅ actions/cache
   v3.3.2 → v3.3.3
   📅 Lançado: 2025-01-20
   📝 Mudanças:
      - Fix: Cache restoration on Windows
   📁 Arquivos afetados:
      - .github/workflows/ci.yml

🟡 MÉDIO RISCO - MINOR (1)
───────────────────────────────────────────────────────────────

⚠️  astral-sh/setup-uv
   v5.0.0 → v5.1.0
   📅 Lançado: 2025-02-01
   📝 Mudanças:
      - Feature: Added Python version auto-detection
      - Feature: Improved caching strategy
   📁 Arquivos afetados:
      - .github/workflows/ci.yml
   💡 Recomendação: Revisar changelog completo

🔴 ALTO RISCO - MAJOR (1)
───────────────────────────────────────────────────────────────

❌ actions/setup-python
   v4.8.0 → v5.0.0
   📅 Lançado: 2025-01-10
   📝 Mudanças:
      ⚠️  Breaking: Removed 'python-version-file' parameter
      ⚠️  Breaking: Changed cache behavior
      - Feature: New caching mechanism
   📁 Arquivos afetados:
      - .github/workflows/ci.yml
   ❗ ATENÇÃO: Requer revisão manual e ajustes

───────────────────────────────────────────────────────────────
📊 RESUMO
───────────────────────────────────────────────────────────────

Total de atualizações: 4
├─ 🟢 Baixo risco (PATCH): 2
├─ 🟡 Médio risco (MINOR): 1
└─ 🔴 Alto risco (MAJOR): 1

Arquivos a modificar: 2
├─ .github/workflows/ci.yml (4 updates)
└─ .github/workflows/deploy.yml (1 update)

───────────────────────────────────────────────────────────────
⚙️  OPÇÕES DE ATUALIZAÇÃO
───────────────────────────────────────────────────────────────

1️⃣  Atualizar apenas PATCH (baixo risco)
   ✅ Recomendado para produção
   ✅ Sem breaking changes

2️⃣  Atualizar PATCH + MINOR (médio risco)
   ⚠️  Revisar changelog recomendado
   ⚠️  Testar após atualizar

3️⃣  Atualizar TUDO (incluindo MAJOR)
   ❌ Requer revisão manual obrigatória
   ❌ Pode requerer ajustes nos workflows

4️⃣  Cancelar

Escolha uma opção (1-4):

```text

### 5. Aplicar Atualizações

**Após confirmação do usuário**:

#### a) Criar Branch de Atualização (Opcional)

```bash

# Sugerir criar branch
git checkout -b update/github-actions-$(date +%Y%m%d)

```text

#### b) Atualizar Arquivos YAML

```python
import re

def update_action_version(content, action_name, old_version, new_version):
    """
    Atualiza versão de action em arquivo YAML
    """
    # Pattern: uses: actions/checkout@v4
    old_pattern = f"uses: {action_name}@{old_version}"
    new_pattern = f"uses: {action_name}@{new_version}"

    updated_content = content.replace(old_pattern, new_pattern)

    return updated_content

# Aplicar para cada arquivo
for workflow_file in workflows_to_update:
    with open(workflow_file, 'r') as f:
        content = f.read()

    for update in updates_to_apply:
        content = update_action_version(
            content,
            update["action_name"],
            update["old_version"],
            update["new_version"]
        )

    with open(workflow_file, 'w') as f:
        f.write(content)

```text

#### c) Validar YAML Após Mudanças

```python
import yaml

for workflow_file in modified_files:
    try:
        with open(workflow_file) as f:
            yaml.safe_load(f)
        print(f"✅ {workflow_file}: YAML válido após atualização")
    except yaml.YAMLError as e:
        print(f"❌ {workflow_file}: Erro após atualização!")
        print(f"   Revertendo mudanças...")
        # Reverter arquivo

```text

### 6. Gerar Changelog de Atualizações

**Criar arquivo com resumo**:

```markdown

# GitHub Actions Update - 2025-10-26

## Atualizações Aplicadas

### PATCH Updates (Baixo Risco)

- **actions/checkout**: v4.1.0 → v4.1.1
  - Fix: Corrected submodule checkout issue
  - Security: Updated dependencies

- **actions/cache**: v3.3.2 → v3.3.3
  - Fix: Cache restoration on Windows

### MINOR Updates (Médio Risco)

- **astral-sh/setup-uv**: v5.0.0 → v5.1.0
  - Feature: Added Python version auto-detection
  - Feature: Improved caching strategy
  - ⚠️  Recomendação: Testar workflows após merge

## Arquivos Modificados

- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`

## Próximos Passos

1. [ ] Revisar mudanças: `git diff`
2. [ ] Testar workflows localmente (se possível)
3. [ ] Fazer commit: `git commit -m "chore: update GitHub Actions versions"`
4. [ ] Abrir PR para revisão
5. [ ] Aguardar CI passar
6. [ ] Merge após aprovação

## Atualizações Pendentes (Requerem Atenção Manual)

### MAJOR Updates (Alto Risco)

- **actions/setup-python**: v4.8.0 → v5.0.0
  - ⚠️  Breaking Changes detectadas
  - Requer revisão manual antes de atualizar
  - Ver: https://github.com/actions/setup-python/releases/tag/v5.0.0

```text

### 7. Confirmar Sucesso

**Após aplicar**:

```text

═══════════════════════════════════════════════════════════════
✅ ATUALIZAÇÕES APLICADAS COM SUCESSO
═══════════════════════════════════════════════════════════════

📦 Atualizações: 3
📁 Arquivos modificados: 2
📝 Changelog: .github/ACTIONS_UPDATE_20251026.md

───────────────────────────────────────────────────────────────
🔍 VALIDAÇÃO
───────────────────────────────────────────────────────────────

✅ Sintaxe YAML validada em todos os arquivos
✅ Nenhum erro detectado
✅ Workflows prontos para commit

───────────────────────────────────────────────────────────────
🚀 PRÓXIMOS PASSOS
───────────────────────────────────────────────────────────────

1. Revisar mudanças:
   git diff .github/workflows/

2. Fazer commit:
   git add .github/
   git commit -m "chore: update GitHub Actions to latest versions"

3. Push e criar PR:
   git push origin update/github-actions-20251026
   gh pr create --title "Update GitHub Actions versions"

4. Aguardar CI:
   - Workflows serão testados automaticamente
   - Verificar se tudo passa

───────────────────────────────────────────────────────────────
⚠️  ATUALIZAÇÕES PENDENTES
───────────────────────────────────────────────────────────────

MAJOR updates não foram aplicadas (requerem atenção manual):

❌ actions/setup-python: v4.8.0 → v5.0.0
   Breaking changes detectadas
   Para atualizar manualmente:
   /cicd-update --action actions/setup-python --force

═══════════════════════════════════════════════════════════════

```text

## 🔒 Segurança e Validação

**Validações aplicadas**:

1. ✅ Backup automático antes de modificar
2. ✅ Validação YAML após cada mudança
3. ✅ Rollback automático se erro detectado
4. ✅ Verificação de breaking changes
5. ✅ Confirmação do usuário antes de aplicar

**Estratégia de atualização segura**:

```python

# Sempre aplicar em ordem de risco
update_order = [
    "PATCH",   # Primeiro, mais seguro
    "MINOR",   # Depois, se aprovado
    "MAJOR",   # Por último, com confirmação explícita
]

```text

## 🎛️ Opções Avançadas

**Força atualização MAJOR**:

```bash
/cicd-update --action actions/setup-python --force

```text

**Pin com SHA ao invés de tag**:

```bash
/cicd-update --pin-sha

```text

Resultado:
- ❌ `uses: actions/checkout@v4`
- ✅ `uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608`

**Criar PR automaticamente**:

```bash
/cicd-update --create-pr

```text

## 📊 Estratégia de Atualização Recomendada

**Frequência sugerida**:

- 🟢 **PATCH**: Semanal (automático com Dependabot)
- 🟡 **MINOR**: Mensal (review trimestral)
- 🔴 **MAJOR**: Quando necessário (planejado)

**Configurar Dependabot** (recomendado):

```yaml

# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "github-actions"

```text

## 🎓 Referências

- [GitHub Actions Versioning](https://docs.github.com/en/actions/creating-actions/about-custom-actions#using-release-management-for-actions)
- [Dependabot for GitHub Actions](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
- [Semantic Versioning](https://semver.org/)
````
