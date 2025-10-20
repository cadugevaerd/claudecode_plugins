# 01 - Estrutura do Repositório de Plugins

## 📋 Visão Geral

Este documento detalha a estrutura completa de um repositório de plugins para o Claude Code, incluindo todos os diretórios, arquivos e suas finalidades.

---

## 🗂️ Estrutura Completa

```
meu-marketplace-plugins/
├── .claude-plugin/
│   └── marketplace.json              # ⚙️ Configuração do marketplace
│
├── plugins/                          # 📦 Diretório com todos os plugins
│   │
│   ├── plugin-exemplo/               # 🔌 Plugin individual
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # 📄 Manifesto do plugin
│   │   │
│   │   ├── .mcp.json                # 🔗 Configuração MCP (opcional)
│   │   │
│   │   ├── commands/                # 💬 Comandos personalizados (slash commands)
│   │   │   ├── hello.md
│   │   │   ├── build.md
│   │   │   └── deploy.md
│   │   │
│   │   ├── agents/                  # 🤖 Agentes especializados
│   │   │   ├── test-runner.md
│   │   │   ├── code-reviewer.md
│   │   │   └── api-tester.md
│   │   │
│   │   ├── hooks/                   # 🪝 Hooks de ciclo de vida
│   │   │   └── hooks.json
│   │   │
│   │   ├── skills/                  # 🎯 Skills para agentes
│   │   │   ├── database-skill/
│   │   │   │   └── SKILL.md
│   │   │   └── api-skill/
│   │   │       └── SKILL.md
│   │   │
│   │   └── README.md                # 📖 Documentação do plugin
│   │
│   ├── outro-plugin/
│   │   └── ...
│   │
│   └── mais-um-plugin/
│       └── ...
│
├── .github/                          # 🐙 Configurações do GitHub (opcional)
│   └── workflows/
│       └── validate-plugins.yml     # ✅ CI/CD para validação
│
├── docs/                            # 📚 Documentação do marketplace
│   └── ...
│
├── examples/                        # 💡 Exemplos de uso (opcional)
│   └── ...
│
├── README.md                        # 📖 Documentação principal
├── LICENSE                          # ⚖️ Licença
└── .gitignore                       # 🚫 Arquivos ignorados

```

---

## 📂 Detalhamento dos Diretórios

### 1. `.claude-plugin/` (Raiz do Marketplace)

**Localização**: Na raiz do repositório

**Conteúdo**:
- `marketplace.json` - Arquivo de configuração principal que lista todos os plugins disponíveis

**Obrigatório**: ✅ Sim

**Exemplo**:
```
.claude-plugin/
└── marketplace.json
```

---

### 2. `plugins/` (Diretório de Plugins)

**Localização**: Na raiz do repositório

**Conteúdo**: Todos os plugins individuais do marketplace

**Obrigatório**: ✅ Sim

**Estrutura**:
```
plugins/
├── plugin-1/
├── plugin-2/
└── plugin-n/
```

---

### 3. Estrutura de um Plugin Individual

Cada plugin dentro de `plugins/` segue esta estrutura:

#### 3.1. `.claude-plugin/plugin.json`

**Obrigatório**: ✅ Sim

**Descrição**: Manifesto do plugin com metadados

**Exemplo**:
```json
{
  "name": "meu-plugin",
  "version": "1.0.0",
  "description": "Descrição do plugin",
  "author": {
    "name": "Seu Nome",
    "email": "email@exemplo.com"
  }
}
```

#### 3.2. `commands/` (Comandos)

**Obrigatório**: ❌ Não (mas recomendado)

**Descrição**: Comandos personalizados que aparecem como `/comando` no Claude Code

**Formato**: Arquivos Markdown (`.md`)

**Exemplo**:
```
commands/
├── hello.md          # Comando /hello
├── build.md          # Comando /build
└── test.md           # Comando /test
```

#### 3.3. `agents/` (Agentes)

**Obrigatório**: ❌ Não

**Descrição**: Agentes especializados para tarefas específicas

**Formato**: Arquivos Markdown (`.md`)

**Exemplo**:
```
agents/
├── test-runner.md        # Agente para executar testes
├── code-reviewer.md      # Agente para revisar código
└── database-manager.md   # Agente para gerenciar banco de dados
```

#### 3.4. `hooks/` (Hooks)

**Obrigatório**: ❌ Não

**Descrição**: Hooks que executam em momentos específicos do ciclo de vida

**Formato**: Arquivo JSON (`hooks.json`)

**Exemplo**:
```
hooks/
└── hooks.json
```

#### 3.5. `skills/` (Skills)

**Obrigatório**: ❌ Não

**Descrição**: Skills que podem ser usadas pelos agentes

**Formato**: Diretórios com arquivo `SKILL.md`

**Exemplo**:
```
skills/
├── database-skill/
│   └── SKILL.md
└── api-testing-skill/
    └── SKILL.md
```

#### 3.6. `.mcp.json` (Configuração MCP)

**Obrigatório**: ❌ Não

**Descrição**: Configuração de MCP Servers para o plugin

**Formato**: Arquivo JSON

**Exemplo**:
```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

---

## 📋 Arquivo Obrigatórios vs Opcionais

### ✅ Obrigatórios

1. **`.claude-plugin/marketplace.json`** (raiz do repositório)
   - Lista todos os plugins disponíveis

2. **`plugins/{nome-plugin}/.claude-plugin/plugin.json`** (para cada plugin)
   - Manifesto do plugin com metadados

### ⭐ Recomendados

3. **`plugins/{nome-plugin}/commands/`**
   - Pelo menos um comando para tornar o plugin útil

4. **`README.md`** (raiz do repositório)
   - Documentação sobre o marketplace

5. **`plugins/{nome-plugin}/README.md`**
   - Documentação sobre cada plugin

### ❌ Opcionais

6. **`plugins/{nome-plugin}/agents/`**
   - Agentes especializados

7. **`plugins/{nome-plugin}/hooks/`**
   - Hooks de ciclo de vida

8. **`plugins/{nome-plugin}/skills/`**
   - Skills para agentes

9. **`plugins/{nome-plugin}/.mcp.json`**
   - Configuração de MCP Servers

10. **`.github/workflows/`**
    - CI/CD para validação automática

---

## 🎯 Estruturas Mínimas

### Estrutura Mínima de um Marketplace

```
meu-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── meu-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── commands/
│           └── hello.md
└── README.md
```

### Estrutura Mínima de um Plugin

```
meu-plugin/
├── .claude-plugin/
│   └── plugin.json        # Manifesto
└── commands/              # Pelo menos um comando
    └── exemplo.md
```

---

## 🔍 Variáveis de Ambiente Especiais

Ao criar plugins, você tem acesso a variáveis especiais:

### `${CLAUDE_PLUGIN_ROOT}`

Aponta para o diretório raiz do plugin.

**Uso**: Em configurações de MCP servers

**Exemplo**:
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server"
}
```

### Variáveis de Ambiente Personalizadas

Você pode usar variáveis de ambiente do sistema:

**Exemplo**:
```json
{
  "env": {
    "DATABASE_URL": "${DATABASE_URL}",
    "API_KEY": "${MY_API_KEY}"
  }
}
```

---

## 🎨 Organização por Tipo de Plugin

### Marketplace Simples (Comandos apenas)

```
simple-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/
    ├── git-commands/
    │   ├── .claude-plugin/plugin.json
    │   └── commands/
    │       ├── commit.md
    │       └── push.md
    └── docker-commands/
        ├── .claude-plugin/plugin.json
        └── commands/
            ├── build.md
            └── run.md
```

### Marketplace Completo (Todos os componentes)

```
complete-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/
    └── full-featured-plugin/
        ├── .claude-plugin/plugin.json
        ├── .mcp.json
        ├── commands/
        ├── agents/
        ├── hooks/
        ├── skills/
        └── README.md
```

### Marketplace por Categoria

```
categorized-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/
    ├── backend/
    │   ├── database-plugin/
    │   └── api-plugin/
    ├── frontend/
    │   ├── react-plugin/
    │   └── vue-plugin/
    └── devops/
        ├── docker-plugin/
        └── kubernetes-plugin/
```

---

## ✅ Checklist de Estrutura

Antes de publicar seu marketplace, verifique:

- [ ] `.claude-plugin/marketplace.json` existe na raiz
- [ ] Cada plugin tem `.claude-plugin/plugin.json`
- [ ] Cada plugin tem pelo menos um componente (command, agent, hook ou MCP)
- [ ] README.md na raiz documenta o marketplace
- [ ] Cada plugin tem seu próprio README.md
- [ ] Nomes de plugins são únicos
- [ ] Versões estão definidas corretamente
- [ ] Paths em `marketplace.json` estão corretos

---

## 🚀 Próximos Passos

Agora que você entende a estrutura, aprenda a:

➡️ [02 - Configuração do Marketplace](./02-configuracao-marketplace.md)

---

[⬅️ Voltar ao Índice](./README.md) | [➡️ Próximo: Configuração do Marketplace](./02-configuracao-marketplace.md)
