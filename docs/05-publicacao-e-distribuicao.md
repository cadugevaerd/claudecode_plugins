# 05 - Publicação e Distribuição

## 📋 Visão Geral

Este documento apresenta o guia completo para publicar e distribuir seu marketplace de plugins do Claude Code, incluindo GitHub, versionamento, CI/CD e manutenção.

---

## 🚀 Passo a Passo para Publicação

### Passo 1: Preparar o Repositório

#### 1.1. Validar Estrutura

Antes de publicar, verifique:

```bash
# Validar JSON
jq empty .claude-plugin/marketplace.json

# Validar plugin.json de cada plugin
find plugins -name "plugin.json" -exec jq empty {} \;

# Verificar estrutura
tree -L 3
```

#### 1.2. Criar .gitignore

**Arquivo**: `.gitignore`

```gitignore
# Dependências
node_modules/
venv/
__pycache__/
*.pyc

# Ambiente
.env
.env.local
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/

# Temporários
tmp/
temp/
*.tmp
```

#### 1.3. Criar README.md Principal

**Arquivo**: `README.md` (raiz do repositório)

```markdown
# Nome do Marketplace

Descrição do seu marketplace de plugins para Claude Code.

## 🚀 Instalação

### Adicionar o Marketplace

```bash
/plugin marketplace add seu-usuario/seu-marketplace
```

### Instalar Plugins

```bash
# Listar plugins disponíveis
/plugin list

# Instalar um plugin específico
/plugin install nome-do-plugin
```

## 📦 Plugins Disponíveis

### Plugin 1: Nome do Plugin
Descrição breve do plugin.

**Comandos**:
- `/comando1` - Descrição
- `/comando2` - Descrição

**Instalação**:
```bash
/plugin install plugin-1
```

### Plugin 2: Outro Plugin
[...]

## 🛠️ Desenvolvimento

### Estrutura

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── plugin-1/
│   └── plugin-2/
└── README.md
```

### Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Licença

MIT

## 👥 Autor

Seu Nome - [@seu-usuario](https://github.com/seu-usuario)
```

#### 1.4. Criar LICENSE

**Arquivo**: `LICENSE`

```
MIT License

Copyright (c) 2025 Seu Nome

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### Passo 2: Publicar no GitHub

#### 2.1. Inicializar Git

```bash
# Navegue até a raiz do seu marketplace
cd /caminho/para/seu-marketplace

# Inicialize o repositório
git init

# Adicione todos os arquivos
git add .

# Crie o primeiro commit
git commit -m "chore: initial commit - marketplace setup"
```

#### 2.2. Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Preencha:
   - **Repository name**: `seu-marketplace`
   - **Description**: Descrição do marketplace
   - **Public**: Marque como público
   - **NÃO** inicialize com README (já temos um)
4. Clique em "Create repository"

#### 2.3. Conectar e Enviar

```bash
# Adicione o remote
git remote add origin https://github.com/seu-usuario/seu-marketplace.git

# Crie a branch main
git branch -M main

# Envie o código
git push -u origin main
```

---

### Passo 3: Configurar Releases e Versionamento

#### 3.1. Semantic Versioning

Use [Semantic Versioning](https://semver.org/):

**Formato**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (ex: 1.0.0 → 2.0.0)
- **MINOR**: Novas funcionalidades (ex: 1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (ex: 1.0.0 → 1.0.1)

**Exemplos**:
- `1.0.0` - Primeira versão estável
- `1.1.0` - Nova funcionalidade adicionada
- `1.1.1` - Correção de bug
- `2.0.0` - Breaking change (API mudou)

#### 3.2. Criar uma Release no GitHub

```bash
# Crie uma tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release"

# Envie a tag
git push origin v1.0.0
```

**Ou via interface do GitHub**:
1. Acesse seu repositório
2. Clique em "Releases"
3. Clique em "Create a new release"
4. Preencha:
   - **Tag version**: v1.0.0
   - **Release title**: v1.0.0 - Initial Release
   - **Description**: Descrição das mudanças
5. Clique em "Publish release"

#### 3.3. CHANGELOG.md

**Arquivo**: `CHANGELOG.md`

```markdown
# Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/),
e este projeto adere ao [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- [Mudanças futuras]

## [1.0.0] - 2025-01-15

### Added
- Plugin git-helper com comandos /commit, /push, /status
- Plugin docker-tools com comandos /build, /run
- Marketplace inicial com 2 plugins

### Changed
- Nada

### Fixed
- Nada

## [0.1.0] - 2025-01-10

### Added
- Estrutura inicial do marketplace
- Documentação básica

[Unreleased]: https://github.com/usuario/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/usuario/repo/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/usuario/repo/releases/tag/v0.1.0
```

---

### Passo 4: Configurar CI/CD (Opcional)

#### 4.1. GitHub Actions - Validação de JSON

**Arquivo**: `.github/workflows/validate.yml`

```yaml
name: Validate Plugins

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Validate marketplace.json
      run: |
        jq empty .claude-plugin/marketplace.json
        echo "✅ marketplace.json is valid"

    - name: Validate plugin.json files
      run: |
        find plugins -name "plugin.json" -exec jq empty {} \;
        echo "✅ All plugin.json files are valid"

    - name: Check required fields in marketplace.json
      run: |
        if ! jq -e '.name and .version and .description and .owner and .plugins' .claude-plugin/marketplace.json > /dev/null; then
          echo "❌ Required fields missing in marketplace.json"
          exit 1
        fi
        echo "✅ All required fields present"
```

#### 4.2. GitHub Actions - Auto Release

**Arquivo**: `.github/workflows/release.yml`

```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

#### 4.3. GitHub Actions - Testes

**Arquivo**: `.github/workflows/test.yml`

```yaml
name: Test Plugins

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Test plugin structure
      run: |
        # Verifica se cada plugin tem pelo menos um componente
        for plugin in plugins/*/; do
          if [ ! -d "$plugin/commands" ] && \
             [ ! -d "$plugin/agents" ] && \
             [ ! -d "$plugin/hooks" ] && \
             [ ! -f "$plugin/.mcp.json" ]; then
            echo "❌ Plugin $plugin has no components"
            exit 1
          fi
        done
        echo "✅ All plugins have at least one component"
```

---

## 📢 Distribuição e Divulgação

### Opção 1: Marketplace Público

#### Como Usuários Instalam

```bash
# Adicionar seu marketplace
/plugin marketplace add seu-usuario/seu-marketplace

# Listar plugins disponíveis
/plugin list

# Instalar um plugin
/plugin install nome-do-plugin
```

### Opção 2: Marketplace Privado (Empresa)

Para uso interno da empresa:

```bash
# URL privada
/plugin marketplace add https://github.com/empresa/plugins-internos

# Ou repositório privado com autenticação
/plugin marketplace add git@github.com:empresa/plugins-privados.git
```

### Opção 3: Plugin Individual

Usuários podem instalar diretamente sem marketplace:

```bash
# Instalar plugin de uma URL
/plugin install https://github.com/usuario/plugin-repo

# Ou de um caminho local
/plugin install /caminho/local/para/plugin
```

---

## 🌟 Promover seu Marketplace

### 1. README Atrativo

Use badges, GIFs, screenshots:

```markdown
# Meu Marketplace

![GitHub stars](https://img.shields.io/github/stars/usuario/repo)
![GitHub forks](https://img.shields.io/github/forks/usuario/repo)
![GitHub issues](https://img.shields.io/github/issues/usuario/repo)
![License](https://img.shields.io/github/license/usuario/repo)

## 🎬 Demo

![Demo GIF](./assets/demo.gif)

## ✨ Features

- ⚡ Rápido e eficiente
- 🔧 Fácil de usar
- 📦 Bem documentado
- 🎨 Customizável
```

### 2. Documentação Completa

- README detalhado
- Exemplos de uso
- Screenshots
- Vídeos (opcional)

### 3. Compartilhar

- Twitter/X com hashtag #ClaudeCode
- Reddit: r/ClaudeAI
- Dev.to
- Hacker News
- LinkedIn

### 4. Contribuir para Awesome Lists

Submeta para:
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins)

---

## 🔄 Manutenção e Atualizações

### Workflow de Desenvolvimento

#### 1. Branches

```bash
main         # Produção (estável)
├── develop  # Desenvolvimento
│   ├── feature/novo-plugin
│   ├── feature/melhoria-x
│   └── fix/correcao-y
```

#### 2. Adicionar Novo Plugin

```bash
# Crie uma branch
git checkout -b feature/novo-plugin

# Desenvolva o plugin
mkdir -p plugins/novo-plugin
# ... desenvolvimento ...

# Atualize marketplace.json
# ... adicione o plugin ...

# Commit
git add .
git commit -m "feat: add novo-plugin with commands X, Y"

# Push
git push origin feature/novo-plugin

# Crie Pull Request no GitHub
```

#### 3. Atualizar Plugin Existente

```bash
# Crie uma branch
git checkout -b fix/plugin-x-bug

# Faça as correções
# ...

# Atualize a versão no plugin.json
# 1.0.0 → 1.0.1 (bug fix)
# 1.0.0 → 1.1.0 (new feature)

# Commit
git add .
git commit -m "fix(plugin-x): corrige bug Y"

# Push e PR
git push origin fix/plugin-x-bug
```

#### 4. Release

```bash
# Merge develop → main
git checkout main
git merge develop

# Atualize versão do marketplace
# Edite .claude-plugin/marketplace.json
# "version": "1.1.0"

# Atualize CHANGELOG.md
# [1.1.0] - 2025-01-20
# ### Added
# - Novo plugin X

# Commit
git add .
git commit -m "chore: release v1.1.0"

# Tag
git tag -a v1.1.0 -m "Release v1.1.0"

# Push
git push origin main
git push origin v1.1.0
```

---

## 📊 Métricas e Monitoramento

### GitHub Insights

Acompanhe:
- Stars ⭐
- Forks 🍴
- Clones 📥
- Visitors 👥
- Issues/PRs 📝

### Analytics (Opcional)

Adicione analytics ao README:

```markdown
[![GitHub Stats](https://api.githubtrends.io/user/svg/usuario/repo)](https://githubtrends.io)
```

---

## 🛡️ Segurança e Boas Práticas

### 1. Nunca Commite Segredos

```bash
# Adicione ao .gitignore
.env
*.key
*.pem
secrets/
credentials/
```

### 2. Use Variáveis de Ambiente

Em vez de:
```json
{
  "env": {
    "API_KEY": "abc123xyz"
  }
}
```

Use:
```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}"
  }
}
```

### 3. Validação de Entrada

Em hooks e scripts, sempre valide entrada do usuário.

### 4. Dependências

Mantenha dependências atualizadas:

```bash
# Se usar Node.js
npm audit
npm update

# Se usar Python
pip-audit
pip install --upgrade -r requirements.txt
```

---

## 📝 Templates Úteis

### CONTRIBUTING.md

```markdown
# Contribuindo

Obrigado por considerar contribuir!

## Como Contribuir

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: add nova-feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Diretrizes

- Use commits semânticos (feat, fix, docs, etc.)
- Atualize a documentação
- Adicione testes se aplicável
- Siga o estilo de código existente

## Reportar Bugs

Use as [GitHub Issues](https://github.com/usuario/repo/issues)
```

### PULL_REQUEST_TEMPLATE.md

**Arquivo**: `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Descrição

[Descreva as mudanças]

## Tipo de Mudança

- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Checklist

- [ ] Testei localmente
- [ ] Atualizei a documentação
- [ ] Atualizei o CHANGELOG.md
- [ ] Segui as convenções de commit
- [ ] Validei os arquivos JSON
```

### ISSUE_TEMPLATE.md

**Arquivo**: `.github/ISSUE_TEMPLATE/bug_report.md`

```markdown
---
name: Bug Report
about: Reporte um bug
---

## Descrição do Bug

[Descrição clara do bug]

## Para Reproduzir

1. Execute '...'
2. Veja o erro

## Comportamento Esperado

[O que deveria acontecer]

## Screenshots

[Se aplicável]

## Ambiente

- OS: [ex: Windows 10]
- Claude Code Version: [ex: 1.2.3]
- Plugin Version: [ex: 1.0.0]
```

---

## ✅ Checklist Final

Antes de tornar seu marketplace público:

### Estrutura
- [ ] `.claude-plugin/marketplace.json` válido
- [ ] Todos os `plugin.json` válidos
- [ ] Estrutura de diretórios correta
- [ ] Pelo menos 1 plugin funcional

### Documentação
- [ ] README.md completo
- [ ] LICENSE presente
- [ ] CHANGELOG.md criado
- [ ] Cada plugin tem README.md

### Git/GitHub
- [ ] Repositório inicializado
- [ ] `.gitignore` configurado
- [ ] Código no GitHub
- [ ] Primeira release criada

### Qualidade
- [ ] JSON validado
- [ ] Comandos testados
- [ ] Sem segredos commitados
- [ ] CI/CD configurado (opcional)

### Marketing
- [ ] README atrativo
- [ ] Badges adicionados
- [ ] Screenshots/GIFs (opcional)
- [ ] Compartilhado em redes sociais (opcional)

---

## 🎓 Recursos Adicionais

### Documentação Oficial

- [Claude Code Plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MCP Documentation](https://docs.claude.com/en/docs/claude-code/mcp)

### Comunidade

- [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)
- [Discord da Anthropic](https://discord.gg/anthropic)
- [Awesome Claude Code Plugins](https://github.com/ccplugins/awesome-claude-code-plugins)

### Ferramentas

- [JSON Schema Validator](https://www.jsonschemavalidator.net/)
- [Semantic Versioning Calculator](https://semver.npmjs.com/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## 🎉 Conclusão

Parabéns! Você agora sabe como:

✅ Criar um marketplace de plugins
✅ Publicar no GitHub
✅ Gerenciar versões e releases
✅ Configurar CI/CD
✅ Distribuir e promover seus plugins
✅ Manter e atualizar seu marketplace

**Próximos passos**:

1. Crie seu primeiro marketplace
2. Desenvolva plugins úteis
3. Compartilhe com a comunidade
4. Contribua para o ecossistema Claude Code

Boa sorte! 🚀

---

[⬅️ Anterior: Componentes do Plugin](./04-componentes-plugin.md) | [⬅️ Voltar ao Índice](./README.md)
