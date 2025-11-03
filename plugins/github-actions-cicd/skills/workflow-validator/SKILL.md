---
name: workflow-validator
description: Valida sintaxe e estrutura de workflows GitHub Actions YAML. Use quando criar, modificar ou revisar arquivos de workflow, verificar erros de sintaxe, validar boas práticas em .github/workflows.
allowed-tools: Read, Bash, Grep
---

name: workflow-validator
description: Valida sintaxe e estrutura de workflows GitHub Actions YAML. Use quando criar, modificar ou revisar arquivos de workflow, verificar erros de sintaxe, validar boas práticas em .github/workflows.
allowed-tools: Read, Bash, Grep

# Workflow Validator Skill

## Instructions

Valida workflows GitHub Actions automaticamente, verificando sintaxe YAML, estrutura obrigatória e boas práticas.

### 1. Detectar Workflows

````bash

# Buscar arquivos de workflow
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null

```text

### 2. Validar Sintaxe YAML

Para cada arquivo encontrado:

```bash

# Validar usando Python
python3 -c "import yaml; yaml.safe_load(open('$FILE'))" 2>&1

# Ou usando yq (se disponível)
yq eval '.' "$FILE" > /dev/null 2>&1

```text

### 3. Verificar Estrutura Obrigatória

Campos obrigatórios em workflows GitHub Actions:
- `name`: Nome do workflow
- `on`: Triggers (push, pull_request, etc.)
- `jobs`: Pelo menos um job definido

### 4. Validar Boas Práticas

Verificações de segurança:
- ✅ `permissions` está definido (evitar write-all)
- ✅ Actions usam versões específicas (não @latest)
- ✅ Não expõe secrets em comandos echo
- ✅ Jobs têm steps definidos

### 5. Reportar Resultados

Formato de output:

```text

✅ .github/workflows/ci.yml: Válido
   - Sintaxe YAML: OK
   - Estrutura: OK
   - Boas práticas: OK

⚠️  .github/workflows/deploy.yml: Avisos
   - Sintaxe YAML: OK
   - Estrutura: OK
   - Boas práticas: 2 avisos
     • Permissions não definidas
     • Action usando @latest

❌ .github/workflows/broken.yml: Erro
   - Sintaxe YAML: ERRO (linha 15: mapeamento inválido)

```text

## When to Use

- Criar novo workflow GitHub Actions
- Modificar workflow existente
- Revisar workflows em pull requests
- Detectar problemas antes de commit
- Validar após merge de branches
- Troubleshooting de workflows que falharam

Termos de gatilho:
- "validar workflow"
- "checar sintaxe YAML"
- "verificar GitHub Actions"
- "workflow quebrado"
- "erro no workflow"
- ".github/workflows"

## Examples

### Exemplo 1: Validação Básica

```yaml

# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello"

```text

Resultado:

```text

⚠️  Avisos encontrados:
- Permissions não definidas (recomendado: permissions: contents: read)

```text

### Exemplo 2: Detectar Problemas

```yaml

# .github/workflows/broken.yml
name: Broken
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@latest  # ❌ Usando @latest
      - run: echo "${{ secrets.API_KEY }}"  # ❌ Expondo secret

```text

Resultado:

```text

❌ Problemas críticos:
1. Action usando @latest (linha 7)
   Fix: Usar actions/checkout@v4

2. Possível exposição de secret (linha 8)
   Fix: Usar env variables

```text

## Validation Checklist

### Sintaxe YAML
- [ ] YAML parseable sem erros
- [ ] Indentação consistente
- [ ] Aspas balanceadas
- [ ] Listas formatadas corretamente

### Estrutura Obrigatória
- [ ] Campo `name` presente
- [ ] Campo `on` presente
- [ ] Pelo menos um job em `jobs`
- [ ] Cada job tem `runs-on`
- [ ] Cada job tem `steps`

### Boas Práticas
- [ ] `permissions` definido
- [ ] Actions com versões específicas (v4, não @latest)
- [ ] Secrets não expostos em echo/print
- [ ] Branches válidos nos triggers
- [ ] Names descritivos em steps

### Segurança
- [ ] Não usa `permissions: write-all`
- [ ] Não usa `@latest` ou `@main` em actions
- [ ] Secrets usados em `env:` não em `run:`
- [ ] Third-party actions são de fontes confiáveis

## Common Errors and Fixes

### Erro 1: YAML Syntax Error

```text

Error: mapping values are not allowed here
  in "<unicode string>", line 10, column 15

```text

Fix: Verificar indentação e uso de `:` nas linhas anteriores.

### Erro 2: Unknown Field

```text

Error: "build" is not a valid job name

```text

Fix: Verificar se campo está no lugar correto da hierarquia.

### Erro 3: Missing Required Field

```text

Error: "on" is required

```text

Fix: Adicionar campo obrigatório no nível correto.

## Performance Optimization

- Validar apenas arquivos modificados (usar git diff)
- Cache de resultados de validação (evitar re-validar)
- Validação paralela de múltiplos workflows
- Skip validação se workflow não mudou

## Integration

Pode ser invocado automaticamente:
- Ao salvar arquivo .yml em .github/workflows/
- Antes de commits (pre-commit hook)
- Em pull requests (CI check)
- Periodicamente (weekly review)
````
