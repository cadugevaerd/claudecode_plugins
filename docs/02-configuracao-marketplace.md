# 02 - Configuração do Marketplace

## 📋 Visão Geral

Este documento detalha como configurar o arquivo `marketplace.json` que define seu marketplace de plugins e o arquivo `plugin.json` que define cada plugin individual.

---

## 🗂️ Arquivo marketplace.json

### Localização

```
.claude-plugin/
└── marketplace.json
```

### Schema

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "string",
  "version": "string",
  "description": "string",
  "owner": {
    "name": "string",
    "email": "string"
  },
  "plugins": []
}
```

---

## 📦 Estrutura Completa do marketplace.json

### Exemplo Completo

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "meu-marketplace",
  "version": "1.0.0",
  "description": "Marketplace de plugins personalizados para desenvolvimento",
  "owner": {
    "name": "João Silva",
    "email": "joao@empresa.com"
  },
  "plugins": [
    {
      "name": "git-helper",
      "description": "Comandos úteis para Git",
      "source": "./plugins/git-helper",
      "version": "1.2.0",
      "author": {
        "name": "João Silva"
      },
      "category": "development",
      "tags": ["git", "vcs", "productivity"]
    },
    {
      "name": "docker-tools",
      "description": "Ferramentas para Docker e containers",
      "source": "./plugins/docker-tools",
      "version": "2.0.0",
      "category": "devops",
      "tags": ["docker", "containers", "deployment"],
      "strict": true
    },
    {
      "name": "api-tester",
      "description": "Teste APIs REST facilmente",
      "source": "https://github.com/user/api-tester-plugin",
      "category": "testing",
      "strict": false
    }
  ]
}
```

---

## 🔑 Campos do marketplace.json

### Campos do Marketplace (Raiz)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `$schema` | string | ❌ Não | URL do schema JSON para validação |
| `name` | string | ✅ Sim | Nome único do marketplace |
| `version` | string | ✅ Sim | Versão do marketplace (semver) |
| `description` | string | ✅ Sim | Descrição do marketplace |
| `owner` | object | ✅ Sim | Informações do proprietário |
| `owner.name` | string | ✅ Sim | Nome do proprietário |
| `owner.email` | string | ✅ Sim | Email do proprietário |
| `plugins` | array | ✅ Sim | Array de plugins disponíveis |

### Campos de Cada Plugin

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | ✅ Sim | Nome único do plugin |
| `description` | string | ✅ Sim | Descrição curta do plugin |
| `source` | string | ✅ Sim | Caminho relativo ou URL do plugin |
| `version` | string | ❌ Não | Versão do plugin (se `strict: false`) |
| `author` | object | ❌ Não | Informações do autor (se `strict: false`) |
| `author.name` | string | ❌ Não | Nome do autor |
| `author.email` | string | ❌ Não | Email do autor |
| `category` | string | ❌ Não | Categoria do plugin |
| `tags` | array | ❌ Não | Tags para busca/filtro |
| `strict` | boolean | ❌ Não | Se `true` (padrão), requer `plugin.json` |

---

## ⚙️ Modo Strict vs Non-Strict

### Strict Mode (Padrão: `strict: true`)

**Comportamento**:
- O plugin **DEVE** ter um arquivo `plugin.json`
- Campos no `marketplace.json` complementam/sobrescrevem o `plugin.json`
- Recomendado para plugins completos e bem estruturados

**Exemplo**:
```json
{
  "name": "meu-plugin",
  "source": "./plugins/meu-plugin",
  "strict": true,
  "category": "development"
}
```

**Estrutura do Plugin**:
```
plugins/meu-plugin/
├── .claude-plugin/
│   └── plugin.json       # ✅ OBRIGATÓRIO
└── commands/
    └── test.md
```

### Non-Strict Mode (`strict: false`)

**Comportamento**:
- O arquivo `plugin.json` é **OPCIONAL**
- O `marketplace.json` serve como manifesto completo
- Útil para plugins simples ou referências externas

**Exemplo**:
```json
{
  "name": "simple-plugin",
  "description": "Plugin simples sem plugin.json",
  "version": "1.0.0",
  "author": {
    "name": "João Silva"
  },
  "source": "./plugins/simple-plugin",
  "strict": false
}
```

**Estrutura do Plugin**:
```
plugins/simple-plugin/
├── commands/              # plugin.json não é necessário
│   └── hello.md
└── README.md
```

---

## 🎯 Tipos de Source (Origem)

### 1. Caminho Relativo (Recomendado)

**Uso**: Para plugins dentro do mesmo repositório

**Formato**: `./plugins/nome-do-plugin`

**Exemplo**:
```json
{
  "name": "meu-plugin",
  "source": "./plugins/meu-plugin"
}
```

### 2. URL de Repositório GitHub

**Uso**: Para plugins em repositórios externos

**Formatos aceitos**:
- `https://github.com/user/repo`
- `user/repo`
- `github:user/repo`

**Exemplo**:
```json
{
  "name": "external-plugin",
  "source": "https://github.com/user/plugin-repo"
}
```

### 3. URL Direta

**Uso**: Para plugins hospedados em qualquer URL

**Exemplo**:
```json
{
  "name": "remote-plugin",
  "source": "https://example.com/plugins/my-plugin.zip"
}
```

---

## 📄 Arquivo plugin.json

### Localização

```
plugins/nome-do-plugin/.claude-plugin/
└── plugin.json
```

### Schema

```json
{
  "name": "string",
  "version": "string",
  "description": "string",
  "author": {
    "name": "string",
    "email": "string"
  },
  "mcpServers": {}
}
```

### Exemplo Completo

```json
{
  "name": "git-helper",
  "version": "1.2.0",
  "description": "Comandos úteis para trabalhar com Git",
  "author": {
    "name": "João Silva",
    "email": "joao@empresa.com"
  },
  "homepage": "https://github.com/joao/git-helper",
  "repository": {
    "type": "git",
    "url": "https://github.com/joao/git-helper.git"
  },
  "keywords": ["git", "vcs", "productivity"],
  "license": "MIT",
  "mcpServers": {
    "git-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/git-mcp",
      "args": ["--verbose"],
      "env": {
        "GIT_AUTHOR": "${GIT_AUTHOR_NAME}"
      }
    }
  }
}
```

---

## 🔑 Campos do plugin.json

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | ✅ Sim | Nome único do plugin |
| `version` | string | ✅ Sim | Versão do plugin (semver) |
| `description` | string | ✅ Sim | Descrição do plugin |
| `author` | object | ⭐ Recomendado | Informações do autor |
| `author.name` | string | ⭐ Recomendado | Nome do autor |
| `author.email` | string | ❌ Não | Email do autor |
| `homepage` | string | ❌ Não | URL da página do plugin |
| `repository` | object | ❌ Não | Informações do repositório |
| `repository.type` | string | ❌ Não | Tipo (ex: "git") |
| `repository.url` | string | ❌ Não | URL do repositório |
| `keywords` | array | ❌ Não | Palavras-chave para busca |
| `license` | string | ❌ Não | Licença (ex: "MIT") |
| `mcpServers` | object | ❌ Não | Configuração inline de MCP servers |

---

## 🎨 Categorias Sugeridas

Embora você possa usar qualquer categoria, aqui estão algumas sugestões:

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| `development` | Ferramentas de desenvolvimento | Git, IDE helpers |
| `testing` | Ferramentas de teste | Test runners, API testers |
| `devops` | DevOps e infraestrutura | Docker, Kubernetes, CI/CD |
| `database` | Banco de dados | SQL helpers, migrations |
| `api` | Ferramentas de API | REST, GraphQL |
| `frontend` | Desenvolvimento frontend | React, Vue, Angular |
| `backend` | Desenvolvimento backend | Node.js, Python |
| `productivity` | Produtividade | Shortcuts, automation |
| `security` | Segurança | Scanners, validators |
| `documentation` | Documentação | Docs generators |

---

## 🏷️ Tags Úteis

Use tags para melhorar a descoberta dos seus plugins:

```json
{
  "tags": [
    "git",              // Ferramenta específica
    "vcs",              // Categoria ampla
    "productivity",     // Benefício
    "automation",       // Tipo de funcionalidade
    "workflow"          // Uso
  ]
}
```

---

## 📝 Exemplos Práticos

### Marketplace Simples (1 Plugin)

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "simple-marketplace",
  "version": "1.0.0",
  "description": "Meu primeiro marketplace",
  "owner": {
    "name": "João Silva",
    "email": "joao@email.com"
  },
  "plugins": [
    {
      "name": "hello-world",
      "description": "Plugin de exemplo",
      "source": "./plugins/hello-world"
    }
  ]
}
```

### Marketplace com Múltiplos Plugins

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "empresa-tools",
  "version": "2.0.0",
  "description": "Ferramentas internas da empresa",
  "owner": {
    "name": "Equipe DevOps",
    "email": "devops@empresa.com"
  },
  "plugins": [
    {
      "name": "deploy-helper",
      "description": "Automatiza deploys",
      "source": "./plugins/deploy-helper",
      "category": "devops",
      "tags": ["deployment", "automation"]
    },
    {
      "name": "db-migration",
      "description": "Gerencia migrações de banco",
      "source": "./plugins/db-migration",
      "category": "database",
      "tags": ["database", "migration", "sql"]
    },
    {
      "name": "code-standards",
      "description": "Valida padrões de código",
      "source": "./plugins/code-standards",
      "category": "development",
      "tags": ["linting", "quality", "standards"]
    }
  ]
}
```

### Marketplace com Plugins Externos

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json",
  "name": "curated-plugins",
  "version": "1.0.0",
  "description": "Coleção curada de plugins úteis",
  "owner": {
    "name": "João Silva",
    "email": "joao@email.com"
  },
  "plugins": [
    {
      "name": "local-plugin",
      "description": "Plugin local",
      "source": "./plugins/local-plugin"
    },
    {
      "name": "github-plugin",
      "description": "Plugin do GitHub",
      "source": "https://github.com/user/plugin"
    },
    {
      "name": "another-github",
      "description": "Outro plugin do GitHub",
      "source": "user/repo"
    }
  ]
}
```

---

## ✅ Validação e Boas Práticas

### Checklist de Validação

- [ ] `name` é único e descritivo
- [ ] `version` segue [Semantic Versioning](https://semver.org/) (ex: 1.0.0)
- [ ] `description` é clara e concisa (< 100 caracteres)
- [ ] `owner.email` é um email válido
- [ ] `source` aponta para um diretório/URL válido
- [ ] Todos os plugins têm nomes únicos
- [ ] Tags e categorias são relevantes

### Boas Práticas

1. **Versionamento**
   - Use Semantic Versioning (MAJOR.MINOR.PATCH)
   - Incremente MAJOR para breaking changes
   - Incremente MINOR para novas features
   - Incremente PATCH para bug fixes

2. **Descrições**
   - Seja conciso (1-2 linhas)
   - Foque no benefício principal
   - Use linguagem clara

3. **Categorização**
   - Use categorias consistentes
   - Limite a 1 categoria por plugin
   - Use tags para classificações adicionais

4. **Organização**
   - Agrupe plugins relacionados
   - Use prefixos para plugins relacionados (ex: `git-commit`, `git-push`)
   - Mantenha a lista de plugins ordenada

---

## 🛠️ Ferramentas de Validação

### Validação Manual com JSON Schema

Se você usa VS Code, adicione no topo do seu `marketplace.json`:

```json
{
  "$schema": "https://api.claude.ai/schemas/marketplace-v1.json"
}
```

Isso habilita autocompletar e validação automática.

### Script de Validação (Opcional)

Crie um script simples para validar seu marketplace:

```bash
#!/bin/bash
# validate-marketplace.sh

echo "Validando marketplace.json..."

# Verifica se o arquivo existe
if [ ! -f ".claude-plugin/marketplace.json" ]; then
    echo "❌ Erro: marketplace.json não encontrado!"
    exit 1
fi

# Valida JSON
if ! jq empty .claude-plugin/marketplace.json 2>/dev/null; then
    echo "❌ Erro: JSON inválido!"
    exit 1
fi

# Verifica campos obrigatórios
if ! jq -e '.name and .version and .description and .owner and .plugins' .claude-plugin/marketplace.json >/dev/null; then
    echo "❌ Erro: Campos obrigatórios faltando!"
    exit 1
fi

echo "✅ marketplace.json válido!"
```

---

## 🚀 Próximos Passos

Agora que você configurou seu marketplace, aprenda a:

➡️ [03 - Criando um Plugin](./03-criando-plugin.md)

---

[⬅️ Anterior: Estrutura do Repositório](./01-estrutura-do-repositorio.md) | [⬅️ Voltar ao Índice](./README.md) | [➡️ Próximo: Criando um Plugin](./03-criando-plugin.md)
