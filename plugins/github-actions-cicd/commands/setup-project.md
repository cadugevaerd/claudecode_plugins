---
description: Configura CLAUDE.md do projeto com padrões de CI/CD e GitHub Actions
---

# Setup GitHub Actions CI/CD for Project

Configura o arquivo `CLAUDE.md` do projeto atual com instruções para que Claude siga padrões de CI/CD e GitHub Actions corretamente.

## 🎯 Objetivo

Adicionar ao `CLAUDE.md` instruções para que Claude:

- Siga princípio YAGNI ao criar workflows
- Use versões específicas de actions (nunca @latest)
- Aplique boas práticas de segurança
- Implemente CI/CD incrementalmente
- Prefira actions oficiais do GitHub Marketplace
- Use scripts Python ao invés de bash complexo

## 📋 Como usar

````bash
/cicd-setup-project

```text

Ou com contexto do projeto:

```bash
/cicd-setup-project "projeto Python com uv, pytest e deploy AWS"

```text

## 🔍 Processo de Execução

### 1. Detectar ou Criar CLAUDE.md

**Se CLAUDE.md existe**:
- ✅ Ler arquivo atual
- ✅ Adicionar seção ao final (NUNCA sobrescrever)
- ✅ Preservar conteúdo existente
- ✅ Usar separador claro (`---`)

**Se CLAUDE.md NÃO existe**:
- ✅ Criar arquivo na raiz do projeto
- ✅ Adicionar template completo

### 2. Analisar Estrutura do Projeto

**Detectar informações relevantes**:

```python
project_info = {
    "language": detect_language(),           # Python, Node.js, Go, etc.
    "package_manager": detect_package_mgr(), # uv, npm, cargo, etc.
    "test_framework": detect_test_framework(), # pytest, jest, go test
    "has_docker": os.path.exists("Dockerfile"),
    "has_workflows": os.path.exists(".github/workflows"),
    "deploy_target": detect_deploy_target(),  # AWS, GCP, Vercel, etc.
}

```text

### 3. Adicionar Instruções do Plugin

Adicionar seção formatada ao CLAUDE.md:

```markdown

# GitHub Actions CI/CD

**IMPORTANTE**: Este projeto usa GitHub Actions para CI/CD com abordagem incremental.

## Regras de CI/CD

### ✅ SEMPRE Fazer

- **YAGNI First**: Comece com workflow mínimo, adicione complexidade APENAS quando necessário
- **Versões Específicas**: Use `@v4`, `@v5`, NUNCA `@latest` ou `@main`
- **Security First**: Configure `permissions` mínimas necessárias
- **Official Actions**: Prefira actions oficiais (actions/, github/, astral-sh/)
- **SHA Pinning**: Para máxima segurança, pin com commit SHA
- **Python Scripts**: Use scripts Python ao invés de bash para lógica complexa
- **Incremental Evolution**: Adicione cache, matrix, deploy progressivamente

### ❌ NUNCA Fazer

- ❌ Usar `@latest`, `@main` ou `@master` em actions
- ❌ Criar workflow complexo logo no início (violação YAGNI)
- ❌ Adicionar matrix builds sem necessidade real
- ❌ Adicionar cache antes de identificar lentidão
- ❌ Usar bash complexo (use Python scripts)
- ❌ Expor secrets em logs
- ❌ Usar `permissions: write-all`
- ❌ Usar third-party actions sem revisar código

## Estrutura de Workflows

### Nível 1 - MVP (COMEÇAR AQUI)

```yaml
name: CI
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6  # Para Python com uv
      - run: uv python install
      - run: uv sync
      - run: uv run pytest

```text

### Nível 2 - Com Cache (quando installs ficarem lentos)

```yaml

# Adicionar apenas quando necessário
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}

```text

### Nível 3 - Matrix (quando precisar múltiplas versões)

```yaml

# Adicionar apenas quando necessário
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']

```text

### Nível 4 - Deploy (quando houver ambiente)

```yaml

# Adicionar apenas quando houver staging/prod configurado
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  # ... deploy steps

```text

## Actions Recomendadas

### Oficiais GitHub
- `actions/checkout@v4` - Checkout de código
- `actions/setup-python@v5` - Setup Python
- `actions/setup-node@v4` - Setup Node.js
- `actions/setup-go@v5` - Setup Go
- `actions/cache@v4` - Cache de dependências
- `actions/upload-artifact@v4` - Upload de artifacts
- `actions/download-artifact@v4` - Download de artifacts

### Python Específico
- `astral-sh/setup-uv@v6` - Setup uv (PREFERIR para Python)
- `actions/setup-python@v5` - Setup Python (fallback)

### Docker
- `docker/build-push-action@v5` - Build e push de imagens
- `docker/setup-buildx-action@v3` - Setup BuildKit

## 🤖 Agentes Especializados Disponíveis

Este plugin fornece **2 agentes especializados** que Claude pode invocar automaticamente:

### 1. cicd-assistant
**Responsabilidade**: Criar e evoluir workflows GitHub Actions incrementalmente seguindo YAGNI

**Quando Claude deve usar**:
- Criar novos workflows MVP
- Adicionar features a workflows existentes (cache, matrix, deploy)
- Evoluir workflows incrementalmente
- Aplicar "Regra dos 3" para refatoração

**Invocação automática por contexto**:

```python

# Usuário: "criar workflow CI para este projeto"
Task("Usar cicd-assistant para criar workflow MVP para projeto Python com uv")

# Usuário: "adicionar cache ao workflow"
Task("Usar cicd-assistant para adicionar cache ao workflow quando necessário")

# Usuário: "evoluir workflow para produção"
Task("Usar cicd-assistant para analisar e sugerir próximo passo incremental")

```text

**Conhecimento especializado**:
- Detecção automática de linguagem/framework
- Templates para Python (uv, poetry), Node.js, Go, Rust
- Aplicação de princípios YAGNI e Incremental Development
- Validação de workflows com boas práticas de segurança

### 2. workflow-analyzer
**Responsabilidade**: Analisar workflows existentes, auditar segurança e sugerir melhorias

**Quando Claude deve usar**:
- Revisar workflows existentes
- Auditar segurança (permissions, secrets, versões)
- Verificar se actions estão atualizadas
- Detectar oportunidades de otimização
- Identificar anti-patterns

**Invocação automática por contexto**:

```python

# Usuário: "revisar meus workflows"
Task("Usar workflow-analyzer para analisar .github/workflows/ci.yml")

# Usuário: "verificar se actions estão atualizadas"
Task("Usar workflow-analyzer para verificar versões de actions")

# Usuário: "analisar segurança dos workflows"
Task("Usar workflow-analyzer para auditoria de segurança completa")

```text

**Conhecimento especializado**:
- Validação de sintaxe YAML
- Auditoria de permissions e secrets
- Comparação de versões (MAJOR/MINOR/PATCH)
- Detecção de duplicação entre workflows
- Score de qualidade (segurança, atualização, otimização)

## Comandos Disponíveis

- `/cicd-init` - Inicializa CI/CD com workflow MVP (invoca cicd-assistant)
- `/cicd-check` - Verifica workflows e versões de actions (invoca workflow-analyzer)
- `/cicd-update` - Atualiza actions para últimas versões
- `/cicd-setup-project` - Atualiza este CLAUDE.md

## Workflow de Desenvolvimento CI/CD

### 1. **Iniciar Simples** (Agente: cicd-assistant)
   - Use `/cicd-init` para criar workflow MVP
   - Apenas checkout → install → test
   - Agente aplica YAGNI automaticamente

### 2. **Evoluir Incrementalmente** (Agente: cicd-assistant)
   - Adicione cache quando installs ficarem lentos
   - Adicione matrix quando precisar múltiplas versões
   - Adicione linting quando ferramentas estiverem configuradas
   - Adicione deploy quando ambiente estiver pronto
   - Agente sugere próximos passos baseado em evidências

### 3. **Manter Atualizado** (Agente: workflow-analyzer)
   - Use `/cicd-check` semanalmente
   - Use `/cicd-update` para atualizar actions
   - Agente identifica actions desatualizadas automaticamente

### 4. **Revisar Segurança** (Agente: workflow-analyzer)
   - Sempre revisar third-party actions
   - Usar SHA pinning em produção
   - Configurar permissions mínimas
   - Agente audita segurança e gera relatório completo

## Orientações para Claude Code

### Detecção Automática de Contexto

Ao receber solicitações relacionadas a GitHub Actions, Claude deve:

1. **Identificar tipo de solicitação**:
   - Criação/evolução → Usar **cicd-assistant**
   - Análise/auditoria → Usar **workflow-analyzer**

2. **Invocar agente apropriado via Task tool**:
   ```python
   Task("Usar cicd-assistant para criar workflow básico de CI para projeto Python com uv")
   Task("Usar workflow-analyzer para analisar workflow e sugerir próximo passo incremental")
````

3. **Seguir princípios dos agentes**:

   - YAGNI: Não adicionar complexidade prematura
   - Incremental: Evoluir baseado em evidências
   - Security First: Sempre aplicar boas práticas

1. **Documentar decisões tomadas pelo agente**

### Exemplos de Invocação por Contexto

| Solicitação do Usuário | Agente | Motivo |
|------------------------|--------|--------|
| "criar workflow CI" | cicd-assistant | Criar novo workflow |
| "adicionar cache" | cicd-assistant | Evoluir workflow existente |
| "revisar workflows" | workflow-analyzer | Análise completa |
| "verificar segurança" | workflow-analyzer | Auditoria de segurança |
| "actions atualizadas?" | workflow-analyzer | Análise de versões |
| "otimizar workflow" | workflow-analyzer → cicd-assistant | Análise + Implementação |

### Fluxo Típico de Trabalho

````text

┌─────────────────────────────────────────┐
│ Usuário: "melhorar meu workflow CI"     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Claude detecta: análise + melhorias     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Passo 1: Invocar workflow-analyzer      │
│ → Analisar workflow atual               │
│ → Identificar problemas e oportunidades │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Passo 2: Invocar cicd-assistant         │
│ → Implementar melhorias sugeridas       │
│ → Aplicar YAGNI e boas práticas         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Resultado: Workflow otimizado e seguro  │
└─────────────────────────────────────────┘

```text

## Scripts Python para CI/CD

**Quando usar scripts Python**:
- ✅ Validação de workflows YAML
- ✅ Verificação de versões de actions
- ✅ Análise de logs
- ✅ Automação complexa
- ✅ Integrações com APIs

**Exemplo de estrutura**:

```text

.github/
├─ workflows/
│  └─ ci.yml
└─ scripts/
   ├─ validate_workflow.py
   ├─ check_versions.py
   └─ requirements.txt  # ou use uv

```text

## Boas Práticas de Segurança

1. **Permissions**
   ```yaml
   permissions:
     contents: read      # Padrão
     pull-requests: write  # Só quando necessário
````

2. **Secrets**

   ```yaml
   # ✅ Correto
   env:
     API_KEY: ${{ secrets.API_KEY }}

   # ❌ Errado
   run: echo "API_KEY=${{ secrets.API_KEY }}"  # Expõe em logs
   ```

1. **OIDC para Cloud**

   ```yaml
   # Preferir OIDC ao invés de credentials estáticas
   permissions:
     id-token: write
   ```

## Troubleshooting

### Workflow não executa

- Verificar triggers (`on:`)
- Verificar permissions
- Verificar branch name

### Actions desatualizadas

- Executar `/cicd-check`
- Executar `/cicd-update`

### Falhas de segurança

- Revisar permissions
- Verificar exposure de secrets
- Pin actions com SHA

````text

### 4. Adicionar Informações Específicas do Projeto

**Customizar seção baseado no projeto**:

```python

# Se projeto usa uv
if project_info["package_manager"] == "uv":
    add_section("""

## Projeto Python com uv

### Setup Recomendado

```yaml
- uses: astral-sh/setup-uv@v6
- run: uv python install
- run: uv sync
- run: uv run pytest

```text

### Cache uv

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/uv
      .venv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}

```text

""")

# Se projeto tem Docker
if project_info["has_docker"]:
    add_section("""

## Docker Build

### Build e Push

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: user/app:latest

```text

""")

# Se projeto tem deploy AWS
if project_info["deploy_target"] == "aws":
    add_section("""

## Deploy AWS

### OIDC Configuration (Recomendado)

```yaml
permissions:
  id-token: write
  contents: read

- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT:role/ROLE
    aws-region: us-east-1

```text

""")

```text

### 5. Confirmar com Usuário

Mostrar preview:

```text

═══════════════════════════════════════════
📝 SETUP GITHUB ACTIONS CI/CD
═══════════════════════════════════════════

Arquivo: CLAUDE.md
Ação: [CRIAR NOVO / ADICIONAR SEÇÃO]

Informações detectadas do projeto:
├─ Linguagem: Python
├─ Package Manager: uv
├─ Test Framework: pytest
├─ Docker: Sim
└─ Workflows existentes: Não

Conteúdo a ser adicionado:

[Preview das instruções personalizadas]

Adicionar ao CLAUDE.md? (s/n)

```text

### 6. Criar/Atualizar Arquivo

Se confirmado:
- ✅ Criar ou atualizar CLAUDE.md
- ✅ NUNCA sobrescrever conteúdo existente
- ✅ SEMPRE adicionar ao final com separador
- ✅ Validar markdown syntax

### 7. Confirmar Sucesso

```text

✅ CLAUDE.md configurado com sucesso!

Instruções de GitHub Actions CI/CD adicionadas.

Próximos passos:
1. Revisar CLAUDE.md
2. Executar /cicd-init para criar primeiro workflow
3. Claude agora está orientado para CI/CD incremental!

═══════════════════════════════════════════

```text

## 🎨 Templates por Linguagem/Framework

### Python com uv

```yaml
- uses: astral-sh/setup-uv@v6
- run: uv python install
- run: uv sync
- run: uv run pytest

```text

### Python com poetry

```yaml
- uses: actions/setup-python@v5
- uses: snok/install-poetry@v1
- run: poetry install
- run: poetry run pytest

```text

### Node.js

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
- run: npm install
- run: npm test

```text

### Go

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.21'
- run: go mod download
- run: go test -v ./...

```text

### Rust

```yaml
- uses: actions-rs/toolchain@v1
  with:
    toolchain: stable
- run: cargo build --release
- run: cargo test

```text

## ⚠️ IMPORTANTE

**Este comando NUNCA**:
- ❌ Sobrescreve CLAUDE.md existente
- ❌ Remove conteúdo existente
- ❌ Modifica seções de outros plugins

**Este comando SEMPRE**:
- ✅ Preserva conteúdo existente
- ✅ Adiciona ao final com separador
- ✅ Mostra preview antes de modificar
- ✅ Valida sintaxe markdown

## 🎓 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [YAGNI Principle](https://martinfowler.com/bliki/Yagni.html)
````
