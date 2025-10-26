# GitHub Actions CI/CD Plugin

Plugin especializado em CI/CD usando GitHub Actions com implementação incremental, seguindo o princípio YAGNI (You Aren't Gonna Need It).

## 🎯 Visão Geral

Este plugin ajuda você a criar, manter e evoluir workflows GitHub Actions de forma incremental e segura, evitando complexidade desnecessária e aplicando as melhores práticas de segurança desde o início.

### Filosofia YAGNI Aplicada ao CI/CD

**YAGNI** (You Aren't Gonna Need It) é um princípio de desenvolvimento que diz: "Não adicione funcionalidades até que sejam realmente necessárias".

Aplicado ao CI/CD:
- ✅ Comece com workflow **mínimo e funcional**
- ✅ Adicione cache **quando installs ficarem lentos**
- ✅ Adicione matrix builds **quando precisar múltiplas versões**
- ✅ Adicione deploy **quando ambiente estiver pronto**
- ❌ **NÃO** adicione otimizações prematuras
- ❌ **NÃO** crie complexidade "para o futuro"

## 📦 Instalação

```bash
/plugin marketplace add cadugevaerd/claudecode_plugins
/plugin install github-actions-cicd
```

## ⚡ Quick Start

### 1. Setup do Projeto

Configure o CLAUDE.md do seu projeto com padrões de CI/CD:

```bash
/cicd-setup-project
```

Isso adiciona instruções ao CLAUDE.md para que Claude siga automaticamente:
- Princípio YAGNI
- Boas práticas de segurança
- Versões específicas de actions
- Evolução incremental

### 2. Inicializar CI/CD

Crie seu primeiro workflow MVP (Mínimo Viável):

```bash
/cicd-init
```

O plugin detecta automaticamente:
- Linguagem do projeto (Python, Node.js, Go, etc.)
- Gerenciador de dependências (uv, npm, cargo, etc.)
- Framework de testes (pytest, jest, go test, etc.)

E cria um workflow básico:
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
```

### 3. Verificar e Atualizar

Periodicamente, verifique se suas actions estão atualizadas:

```bash
/cicd-check
/cicd-update
```

## 🚀 Funcionalidades

### Comandos Disponíveis

#### `/cicd-init`
Inicializa CI/CD no projeto com workflow MVP.

**Características**:
- Detecta estrutura do projeto automaticamente
- Cria workflow mínimo funcional
- Aplica boas práticas de segurança
- Evita complexidade prematura

**Exemplo**:
```bash
/cicd-init
```

---

#### `/cicd-check`
Verifica workflows existentes, versões de actions e problemas de segurança.

**Características**:
- Valida sintaxe YAML
- Verifica versões de actions
- Identifica problemas de segurança
- Sugere melhorias

**Exemplo**:
```bash
/cicd-check
```

**Output**:
```
📊 ANÁLISE DE WORKFLOWS

✅ ci.yml: Válido
   - Actions atualizadas: 3/4
   - Security score: 85/100

⚠️  Atualizações disponíveis:
   - actions/setup-python: v4 → v5
```

---

#### `/cicd-update`
Atualiza versões de actions para as últimas versões disponíveis.

**Características**:
- Classifica updates (MAJOR/MINOR/PATCH)
- Preview antes de aplicar
- Detecta breaking changes
- Valida após mudanças

**Exemplo**:
```bash
/cicd-update
```

**Estratégia de atualização**:
- 🟢 **PATCH**: Atualização segura (bug fixes)
- 🟡 **MINOR**: Revisar changelog recomendado (novas features)
- 🔴 **MAJOR**: Revisão manual obrigatória (breaking changes)

---

#### `/cicd-setup-project`
Configura CLAUDE.md do projeto com padrões de CI/CD.

**Características**:
- Adiciona instruções para Claude
- Preserva conteúdo existente
- Customiza baseado no projeto
- Documenta boas práticas

**Exemplo**:
```bash
/cicd-setup-project
```

### Agentes Especializados

#### `cicd-assistant`
Agente especializado em criar e evoluir workflows incrementalmente.

**Use para**:
- Criar workflows MVP
- Evoluir workflows existentes
- Adicionar features quando necessário
- Aplicar "Regra dos 3" para refatoração

**Exemplo**:
```python
Task("Usar cicd-assistant para criar workflow básico de CI")
```

---

#### `workflow-analyzer`
Agente especializado em analisar workflows e sugerir melhorias.

**Use para**:
- Auditoria de segurança
- Análise de versões
- Detectar otimizações
- Identificar duplicação

**Exemplo**:
```python
Task("Usar workflow-analyzer para auditoria de segurança")
```

### Skills Auto-Invocadas

#### `workflow-validator`
Valida automaticamente sintaxe e estrutura de workflows.

**Ativa quando**:
- Criar/modificar workflows
- Revisar pull requests
- Detectar erros antes de commit

**Verifica**:
- ✅ Sintaxe YAML válida
- ✅ Campos obrigatórios presentes
- ✅ Boas práticas aplicadas
- ✅ Segurança configurada

---

#### `action-version-checker`
Verifica automaticamente versões de actions.

**Ativa quando**:
- Revisar workflows
- Atualizar dependências
- Auditoria de versões

**Detecta**:
- ⚠️  Actions desatualizadas
- 🔴 Actions usando @latest (inseguro)
- ✅ Actions atualizadas
- 📊 Tipo de update disponível

## 📚 Evolução Incremental

### Nível 1 - MVP (Comece Aqui)

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
      - uses: astral-sh/setup-uv@v6
      - run: uv python install
      - run: uv sync
      - run: uv run pytest
```

**Quando usar**: SEMPRE comece aqui! É o mínimo funcional.

---

### Nível 2 - Cache (Quando Installs > 1min)

```yaml
# Adicionar APENAS quando necessário
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/uv
      .venv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}
```

**Quando adicionar**:
- ✅ Instalação demora > 1 minuto
- ✅ Builds lentos afetando produtividade
- ❌ **NÃO** adicionar "para otimizar depois"

---

### Nível 3 - Matrix (Quando Precisar Múltiplas Versões)

```yaml
# Adicionar APENAS quando necessário
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
```

**Quando adicionar**:
- ✅ Projeto precisa suportar múltiplas versões
- ✅ Requisito de compatibilidade explícito
- ❌ **NÃO** adicionar "para garantir compatibilidade"

---

### Nível 4 - Linting (Quando Ferramentas Configuradas)

```yaml
# Adicionar APENAS quando linters configurados
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: uv run black . --check
    - run: uv run flake8 .
```

**Quando adicionar**:
- ✅ black, flake8, mypy configurados no projeto
- ✅ Equipe usa linters localmente
- ❌ **NÃO** adicionar antes de configurar linters

---

### Nível 5 - Deploy (Quando Ambiente Pronto)

```yaml
# Adicionar APENAS quando ambiente existe
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    # ... deploy steps
```

**Quando adicionar**:
- ✅ Ambiente de staging/produção configurado
- ✅ Credenciais e secrets configurados
- ❌ **NÃO** adicionar antes de ter ambiente

## 🔒 Boas Práticas de Segurança

### 1. Permissions Mínimas

```yaml
# ✅ Correto - Mínimo necessário
permissions:
  contents: read

# ❌ Errado - Acesso excessivo
permissions: write-all
```

### 2. Versões Específicas

```yaml
# ✅ Correto - Versão específica
uses: actions/checkout@v4

# ❌ Errado - Branch/latest
uses: actions/checkout@latest
uses: actions/checkout@main
```

### 3. SHA Pinning (Produção)

```yaml
# 🔒 Máxima segurança - SHA commit
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608
```

### 4. Secrets Seguros

```yaml
# ✅ Correto - Em env variables
env:
  API_KEY: ${{ secrets.API_KEY }}
run: ./deploy.sh

# ❌ Errado - Inline (expõe em logs)
run: echo "API_KEY=${{ secrets.API_KEY }}"
```

### 5. OIDC para Cloud (Preferir)

```yaml
# ✅ Preferir OIDC ao invés de credentials estáticas
permissions:
  id-token: write
  contents: read

- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT:role/ROLE
    aws-region: us-east-1
```

## 📊 Actions Recomendadas

### Oficiais GitHub (Sempre Preferir)

| Action | Versão Atual | Descrição |
|--------|--------------|-----------|
| `actions/checkout` | v4 | Checkout de código |
| `actions/setup-python` | v5 | Setup Python |
| `actions/setup-node` | v4 | Setup Node.js |
| `actions/setup-go` | v5 | Setup Go |
| `actions/cache` | v4 | Cache de dependências |
| `actions/upload-artifact` | v4 | Upload de artifacts |
| `actions/download-artifact` | v4 | Download de artifacts |

### Python Específico

| Action | Versão Atual | Descrição |
|--------|--------------|-----------|
| `astral-sh/setup-uv` | v6 | Setup uv (PREFERIR) |
| `snok/install-poetry` | v1 | Setup poetry |

### Docker

| Action | Versão Atual | Descrição |
|--------|--------------|-----------|
| `docker/build-push-action` | v5 | Build e push de imagens |
| `docker/setup-buildx-action` | v3 | Setup BuildKit |

### Cloud

| Action | Versão Atual | Descrição |
|--------|--------------|-----------|
| `aws-actions/configure-aws-credentials` | v4 | AWS credentials |
| `google-github-actions/auth` | v2 | GCP auth |

## 🎨 Templates por Linguagem

### Python com uv (Recomendado)

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
      - uses: astral-sh/setup-uv@v6
      - run: uv python install
      - run: uv sync
      - run: uv run pytest
```

### Node.js

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
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install
      - run: npm test
```

### Go

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
      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'
      - run: go mod download
      - run: go test -v ./...
```

## 🔄 Manutenção e Atualizações

### Frequência Recomendada

- 🟢 **PATCH updates**: Semanal (automático com Dependabot)
- 🟡 **MINOR updates**: Mensal
- 🔴 **MAJOR updates**: Quando necessário (planejado)

### Configurar Dependabot (Recomendado)

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
```

### Workflow de Atualização

1. **Semanal**: `/cicd-check` para verificar versões
2. **Mensal**: `/cicd-update` para aplicar updates PATCH/MINOR
3. **Trimestral**: Revisar MAJOR updates manualmente
4. **Sempre**: Validar após atualizar

## 🎓 Recursos e Referências

### Documentação Oficial

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Security Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

### Guias Específicos

- [uv GitHub Actions Guide](https://docs.astral.sh/uv/guides/integration/github/)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)

### Princípios de Design

- [YAGNI Principle - Martin Fowler](https://martinfowler.com/bliki/Yagni.html)
- [Semantic Versioning](https://semver.org/)

## 💡 Melhores Práticas

### Princípio YAGNI em CI/CD

1. **Comece Simples**: MVP com checkout → install → test
2. **Evidência Antes de Adicionar**: Só adicione quando houver necessidade real
3. **Refatore no Momento Certo**: Regra dos 3 (padrão repetiu 3+ vezes)

### Segurança First

1. **Permissions**: Sempre defina mínimas necessárias
2. **Versões**: NUNCA use @latest ou @main
3. **Secrets**: Use env variables, não inline
4. **Third-Party**: Revise código antes de usar

### Evolução Incremental

1. **Cache**: Adicione quando install > 1min
2. **Matrix**: Adicione quando precisar múltiplas versões
3. **Linting**: Adicione quando ferramentas estiverem configuradas
4. **Deploy**: Adicione quando ambiente estiver pronto

## 🚨 Anti-Patterns a Evitar

### ❌ Complexidade Prematura

```yaml
# NÃO fazer logo de início
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11, 3.12]
    os: [ubuntu-latest, windows-latest, macos-latest]
# Quando projeto só precisa Python 3.11 em ubuntu
```

### ❌ Cache Desnecessário

```yaml
# NÃO adicionar se install é rápido (<30s)
- uses: actions/cache@v4
  # ... cache config
```

### ❌ Versões Inseguras

```yaml
# NUNCA usar
uses: actions/checkout@latest  # ❌
uses: actions/checkout@main    # ❌
```

## 📞 Suporte

Para dúvidas, problemas ou sugestões:
- GitHub Issues: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins/issues)
- Email: cadu.gevaerd@gmail.com

## 📄 Licença

MIT

## 👤 Autor

**Carlos Araujo**
- Email: cadu.gevaerd@gmail.com
- GitHub: [@cadugevaerd](https://github.com/cadugevaerd)

---

**Desenvolvido para claudecode_plugins marketplace** 🚀
