---
description: Inicializa CI/CD com GitHub Actions no projeto usando abordagem incremental (YAGNI)
---

# Initialize CI/CD with GitHub Actions

Inicializa CI/CD no projeto atual usando GitHub Actions, seguindo abordagem incremental baseada no princípio YAGNI (You Aren't Gonna Need It).

## 🎯 Objetivo

Criar workflow GitHub Actions **mínimo e funcional** que:
- Detecta estrutura e linguagem do projeto
- Implementa apenas o necessário AGORA
- Evita features não utilizadas
- Permite evolução incremental futura

## 📋 Como usar

```bash
/cicd-init
```

Ou com contexto adicional:

```bash
/cicd-init "projeto Python com pytest e Django"
```

## 🔍 Processo de Execução

### 1. Detectar Estrutura do Projeto

**Analisar arquivos do projeto**:
- ✅ Linguagem principal (Python, Node.js, Go, Rust, etc.)
- ✅ Gerenciador de dependências (uv, poetry, npm, cargo, etc.)
- ✅ Framework de testes (pytest, jest, go test, etc.)
- ✅ Linters/formatters configurados
- ✅ Estrutura de diretórios

**Exemplos de detecção**:
- `pyproject.toml` + `uv.lock` → Python com uv
- `package.json` → Node.js com npm/yarn/pnpm
- `Cargo.toml` → Rust com cargo
- `go.mod` → Go com go modules

### 2. Verificar Workflows Existentes

**Verificar se `.github/workflows/` existe**:

```bash
# Se existe
ls -la .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null
```

**Se workflows já existem**:
- ⚠️  Avisar ao usuário
- 📋 Listar workflows existentes
- ❓ Perguntar se deseja:
  - Criar novo workflow com nome diferente
  - Substituir workflow existente
  - Cancelar operação

**Se NÃO existem**:
- ✅ Criar diretório `.github/workflows/`
- ✅ Prosseguir com criação

### 3. Criar Workflow MVP (Nível 1 - Básico)

**Princípio YAGNI aplicado**:
- ✅ Checkout do código
- ✅ Setup da linguagem/runtime
- ✅ Instalar dependências
- ✅ Executar testes (se detectados)
- ❌ **NÃO** adicionar cache (ainda)
- ❌ **NÃO** adicionar matrix builds (ainda)
- ❌ **NÃO** adicionar deploy (ainda)
- ❌ **NÃO** adicionar notifications (ainda)

**Template para Python com uv**:

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest
```

**Template para Node.js**:

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test
```

**Template para Go**:

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Install dependencies
        run: go mod download

      - name: Run tests
        run: go test -v ./...
```

### 4. Validar Workflow YAML

**Usar yamllint ou validação interna**:

```bash
# Validar sintaxe YAML
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
```

**Verificar**:
- ✅ Sintaxe YAML válida
- ✅ Campos obrigatórios presentes (`name`, `on`, `jobs`)
- ✅ Actions com versões específicas (não `@latest`)
- ✅ Permissions configuradas (mínimo necessário)

### 5. Sugerir Próximos Passos (Incrementais)

**Após criar workflow MVP, sugerir evolução**:

```
✅ Workflow CI básico criado: .github/workflows/ci.yml

📈 PRÓXIMOS PASSOS INCREMENTAIS (adicionar quando necessário):

Nível 2 - Otimização:
- [ ] Adicionar cache (quando installs ficarem lentos)
  Comando: /cicd-add-cache

Nível 3 - Múltiplas versões:
- [ ] Adicionar matrix builds (quando precisar testar múltiplas versões)
  Comando: /cicd-add-matrix

Nível 4 - Qualidade:
- [ ] Adicionar linting/formatting (quando houver ferramentas configuradas)
  Comando: /cicd-add-quality

Nível 5 - Deploy:
- [ ] Adicionar deploy (quando houver ambiente de staging/produção)
  Comando: /cicd-add-deploy

💡 PRINCÍPIO YAGNI: Adicione features APENAS quando a necessidade for real!
```

### 6. Atualizar CLAUDE.md (Opcional)

**Perguntar ao usuário**:

```
Deseja atualizar CLAUDE.md com padrões de CI/CD deste projeto? (s/n)
```

**Se SIM**:
- Executar `/cicd-setup-project` automaticamente

## 🔒 Boas Práticas de Segurança

**SEMPRE aplicar**:

1. **Versões Específicas de Actions**:
   - ✅ `actions/checkout@v4`
   - ❌ `actions/checkout@latest`
   - 💡 Pin com SHA para máxima segurança: `actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608`

2. **Permissions Mínimas**:
   ```yaml
   permissions:
     contents: read  # Apenas leitura por padrão
   ```

3. **Secrets**:
   - ✅ Usar `${{ secrets.API_KEY }}`
   - ❌ NUNCA hardcode credenciais
   - 💡 Preferir OIDC quando possível

4. **Third-Party Actions**:
   - ✅ Usar apenas actions verificadas
   - ✅ Revisar código antes de usar
   - ✅ Preferir actions oficiais (GitHub, Astral, etc.)

## 📝 Exemplos de Execução

**Exemplo 1 - Projeto Python simples**:

```bash
/cicd-init
```

Resultado:
- Detecta `pyproject.toml` e `uv.lock`
- Cria workflow com uv + pytest
- Arquivo: `.github/workflows/ci.yml`

**Exemplo 2 - Projeto Node.js com npm**:

```bash
/cicd-init "Node.js API com testes Jest"
```

Resultado:
- Detecta `package.json`
- Cria workflow com npm + jest
- Arquivo: `.github/workflows/ci.yml`

**Exemplo 3 - Projeto Go**:

```bash
/cicd-init
```

Resultado:
- Detecta `go.mod`
- Cria workflow com go test
- Arquivo: `.github/workflows/ci.yml`

## ⚠️ IMPORTANTE

**Este comando cria apenas o MÍNIMO necessário**:
- ✅ Workflow funcional e testável
- ✅ Segue boas práticas de segurança
- ✅ Usa versões específicas de actions
- ❌ NÃO adiciona otimizações prematuras
- ❌ NÃO adiciona features não utilizadas
- ❌ NÃO adiciona complexidade desnecessária

**Evolução incremental**:
- Use comandos específicos para adicionar features quando necessário
- Siga o princípio: "Adicione QUANDO precisar, NÃO antes"

## 🎓 Referências

- [GitHub Actions Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [uv GitHub Actions Guide](https://docs.astral.sh/uv/guides/integration/github/)
- [YAGNI Principle](https://martinfowler.com/bliki/Yagni.html)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
