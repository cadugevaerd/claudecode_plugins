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

```bash
/cicd-setup-project
```

Ou com contexto do projeto:

```bash
/cicd-setup-project "projeto Python com uv, pytest e deploy AWS"
```

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
```

### 3. Adicionar Instruções do Plugin

Adicionar seção formatada ao CLAUDE.md:

```markdown
---

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
```

### Nível 2 - Com Cache (quando installs ficarem lentos)
```yaml
# Adicionar apenas quando necessário
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}
```

### Nível 3 - Matrix (quando precisar múltiplas versões)
```yaml
# Adicionar apenas quando necessário
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
```

### Nível 4 - Deploy (quando houver ambiente)
```yaml
# Adicionar apenas quando houver staging/prod configurado
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  # ... deploy steps
```

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

## Comandos Disponíveis

- `/cicd-init` - Inicializa CI/CD com workflow MVP
- `/cicd-check` - Verifica workflows e versões de actions
- `/cicd-update` - Atualiza actions para últimas versões
- `/cicd-setup-project` - Atualiza este CLAUDE.md

## Workflow de Desenvolvimento CI/CD

1. **Iniciar Simples**
   - Use `/cicd-init` para criar workflow MVP
   - Apenas checkout → install → test

2. **Evoluir Incrementalmente**
   - Adicione cache quando installs ficarem lentos
   - Adicione matrix quando precisar múltiplas versões
   - Adicione linting quando ferramentas estiverem configuradas
   - Adicione deploy quando ambiente estiver pronto

3. **Manter Atualizado**
   - Use `/cicd-check` semanalmente
   - Use `/cicd-update` para atualizar actions

4. **Revisar Segurança**
   - Sempre revisar third-party actions
   - Usar SHA pinning em produção
   - Configurar permissions mínimas

## Scripts Python para CI/CD

**Quando usar scripts Python**:
- ✅ Validação de workflows YAML
- ✅ Verificação de versões de actions
- ✅ Análise de logs
- ✅ Automação complexa
- ✅ Integrações com APIs

**Exemplo de estrutura**:
```
.github/
├─ workflows/
│  └─ ci.yml
└─ scripts/
   ├─ validate_workflow.py
   ├─ check_versions.py
   └─ requirements.txt  # ou use uv
```

## Boas Práticas de Segurança

1. **Permissions**
   ```yaml
   permissions:
     contents: read      # Padrão
     pull-requests: write  # Só quando necessário
   ```

2. **Secrets**
   ```yaml
   # ✅ Correto
   env:
     API_KEY: ${{ secrets.API_KEY }}

   # ❌ Errado
   run: echo "API_KEY=${{ secrets.API_KEY }}"  # Expõe em logs
   ```

3. **OIDC para Cloud**
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

---
```

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
```

### Cache uv
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/uv
      .venv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}
```
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
```
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
```
""")
```

### 5. Confirmar com Usuário

Mostrar preview:

```
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
---
[Preview das instruções personalizadas]
---

Adicionar ao CLAUDE.md? (s/n)
```

### 6. Criar/Atualizar Arquivo

Se confirmado:
- ✅ Criar ou atualizar CLAUDE.md
- ✅ NUNCA sobrescrever conteúdo existente
- ✅ SEMPRE adicionar ao final com separador
- ✅ Validar markdown syntax

### 7. Confirmar Sucesso

```
✅ CLAUDE.md configurado com sucesso!

Instruções de GitHub Actions CI/CD adicionadas.

Próximos passos:
1. Revisar CLAUDE.md
2. Executar /cicd-init para criar primeiro workflow
3. Claude agora está orientado para CI/CD incremental!

═══════════════════════════════════════════
```

## 🎨 Templates por Linguagem/Framework

### Python com uv
```yaml
- uses: astral-sh/setup-uv@v6
- run: uv python install
- run: uv sync
- run: uv run pytest
```

### Python com poetry
```yaml
- uses: actions/setup-python@v5
- uses: snok/install-poetry@v1
- run: poetry install
- run: poetry run pytest
```

### Node.js
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
- run: npm install
- run: npm test
```

### Go
```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.21'
- run: go mod download
- run: go test -v ./...
```

### Rust
```yaml
- uses: actions-rs/toolchain@v1
  with:
    toolchain: stable
- run: cargo build --release
- run: cargo test
```

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
