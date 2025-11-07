---
description: Create a new Claude Code plugin with semantic versioning and structure
allowed-tools: Read, Write, Glob, Grep, Bash(git:*), WebSearch, Task, SlashCommand
model: claude-sonnet-4-5
argument-hint: <plugin-description>
---

# Create Plugin

## Knowledge Research Phase

1. **Search for relevant Skills**: Check available skills matching the plugin theme
1. **Research best practices**: Use Web Search to find patterns and frameworks relevant to the plugin
1. **Analyze existing plugins**: Review similar plugins in `plugins/` to understand patterns

## Plugin Analysis

1. Check if plugin name already exists in `plugins/` directory
1. If exists: Stop and inform user that plugin already exists
1. Determine plugin type: Integration, Automation, Development, Testing, Documentation, or Utilities

## Create Plugin Structure

1. Create directory: `plugins/[plugin-name]/`

1. Create `.claude-plugin/plugin.json` with **ONLY valid fields**:

   - `name`: Plugin identifier (kebab-case)
   - `version`: 1.0.0 (semantic versioning)
   - `description`: Brief description of the plugin
   - `author`: Object with `name` and `email` (Carlos Araujo, `cadu.gevaerd@gmail.com`)
   - `license`: MIT
   - `commands`: Empty array `[]` (will be populated when creating commands)
   - `agents`: Empty array `[]` (will be populated when creating agents)
   - `hooks`: Path string (only if using hooks)
   - `mcp`: Path string (only if using MCP - e.g., ".mcp.json")

   **CRITICAL - DO NOT include these fields (they are INVALID):**

   - ❌ `category` - Not part of plugin.json schema
   - ❌ `tags` - Not part of plugin.json schema
   - ❌ `skills` - Skills are auto-discovered, never register in plugin.json

1. Create `README.md` with complete documentation

1. Create component directories based on plugin type:

   - commands/ → .md files for slash commands
   - agents/ → .md files for specialized agents
   - skills/ → subdirectories with SKILL.md files
   - hooks/ → hooks.json if needed
   - servers/ → server code if using MCP (not mcp/)

## Generate Plugin Content

### Use Specialized Commands for Component Creation

For each component type, use the appropriate specialized command:

1. **For Commands** (if plugin needs slash commands):

   - Use `/create-slash-command COMMAND_NAME "Description" plugins/[plugin-name]/commands/`
   - Example: `/create-slash-command quick-commit "Fast commit with validation" plugins/git-helper/commands/`
   - This ensures proper YAML frontmatter, structure validation, and best practices

1. **For Agents** (if plugin needs specialized agents):

   - Use `/create-agent AGENT_NAME "Description"`
   - When prompted for location, specify `plugins/[plugin-name]/agents/`
   - Example: `/create-agent commit-assistant "Automates commit workflow with validations"`
   - This ensures single-file architecture (50-200 lines) and proper structure

1. **For Skills** (if plugin needs reusable knowledge):

   - Use `/create-skill SKILL_NAME "Description" plugins/[plugin-name]/skills/`
   - Example: `/create-skill commit-validator "Validates commit messages following Conventional Commits" plugins/git-helper/skills/`
   - This ensures progressive disclosure, YAML frontmatter, and auto-discovery

1. **For MCP Servers** (if plugin needs Model Context Protocol integration):

   - Use `/create-mcp-client MCP_NAME [SCOPE]` for MCP server integration
   - When prompted for location, use `project` scope for plugin-bundled MCP
   - Example: `/create-mcp-client database-connector project`
   - Creates `.mcp.json` at plugin root with proper transport configuration
   - Ensures stdio/HTTP transport setup and environment variable handling
   - Place MCP server code in `servers/` directory

### After Creating Components

1. Update plugin.json with created components:

   - **Commands**: Add to `commands` array with structure: `{"name": "command-name", "description": "Description", "path": "commands/file.md"}`
   - **Agents**: Add to `agents` array with structure: `{"name": "agent-name", "description": "Description", "path": "agents/file.md"}`
   - **Skills**: Auto-discovered from `skills/` directory - **DO NOT** register in plugin.json
   - **MCP Servers**: If using MCP, add field `"mcp": ".mcp.json"` to plugin.json root (not inside arrays)

1. Write comprehensive README with:

   - Clear description and use cases
   - List of components (commands, agents, skills)
   - Usage examples for each component
   - Installation instructions

## Validate and Register

1. Validate all JSON files (plugin.json, marketplace.json)
1. Verify plugin name is unique across marketplace
1. Register in `.claude-plugin/marketplace.json`:
   - Add plugin entry with complete metadata
   - Include version 1.0.0, namespace, tags
1. Verify directory structure is complete and valid

## 📊 Formato de Saída

Display final summary in this format:

```markdown
# ✅ Plugin Created: [plugin-name]

**Location:** `plugins/[plugin-name]/`
**Version:** 1.0.0
**Author:** Carlos Araujo

## 📦 Components Created

### Commands
- `/[command-name]` - [Description]

### Agents
- `[agent-name]` - [Description]

### Skills
- `[skill-name]` - [Description]

## ✅ Validation Results

- [✅|❌] plugin.json valid
- [✅|❌] marketplace.json updated
- [✅|❌] Directory structure complete
- [✅|❌] README.md created

## 🚀 Next Steps

1. Test plugin: `/plugin refresh && /plugin list`
2. Review components in `plugins/[plugin-name]/`
3. Commit changes: `/commit`
```

## ✅ Critérios de Sucesso

- [ ] Plugin name validado (único, kebab-case)
- [ ] Estrutura de diretórios criada (.claude-plugin/, README.md, components/)
- [ ] plugin.json criado e validado (JSON válido)
- [ ] Pelo menos um componente funcional criado (command/agent/skill)
- [ ] README.md completo com exemplos de uso
- [ ] Registrado em marketplace.json
- [ ] Validação JSON passou (jq empty plugin.json)
- [ ] Version 1.0.0 inicial definida
- [ ] Best practices pesquisadas e aplicadas

## ❌ Anti-Patterns

### ❌ Erro 1: Campos Inválidos no plugin.json

**NUNCA** adicione campos não suportados pelo schema do Claude Code:

```json
// ❌ ERRADO - Causará erro de validação
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin",
  "category": "development",        // ❌ Campo inválido
  "tags": ["kubernetes", "k8s"],    // ❌ Campo inválido
  "skills": [...]                    // ❌ Campo inválido (auto-descoberta)
}

// ✅ CORRETO - Apenas campos válidos
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin",
  "author": {
    "name": "Carlos Araujo",
    "email": "cadu.gevaerd@gmail.com"
  },
  "license": "MIT",
  "commands": [],
  "agents": []
}
```

**Regra de ouro:** Use APENAS os campos documentados no schema oficial:

- `name`, `version`, `description`, `author`, `license`
- Arrays: `commands`, `agents`
- Paths opcionais: `hooks`, `mcp`

### ❌ Erro 2: Nome de Plugin Inválido

Não use naming conventions incorretas:

```bash
# ❌ Errado
/create-plugin "MyAwesomePlugin"    # CamelCase não permitido
/create-plugin "my_plugin"          # Underscores não permitidos
/create-plugin "PLUGIN-NAME"        # Maiúsculas não permitidas

# ✅ Correto
/create-plugin "my-awesome-plugin"
/create-plugin "git-commit-helper"
/create-plugin "api-test-automation"
```

### ❌ Erro 3: Descrição Muito Vaga

Não fornecer descrição genérica ou incompleta:

```bash
# ❌ Errado
/create-plugin "helper plugin"              # Muito vago
/create-plugin "does stuff"                 # Não descreve funcionalidade
/create-plugin "plugin"                     # Sem contexto

# ✅ Correto
/create-plugin "Automates git commits with security validation and conventional messages"
/create-plugin "Generates unit tests for Python projects with mocks and fixtures"
/create-plugin "Creates API documentation from OpenAPI specifications"
```

### ❌ Erro 4: Não Validar JSON Antes de Finalizar

Sempre validar arquivos JSON após criação:

```bash
# ❌ Errado
# Criar plugin e assumir que JSON está válido

# ✅ Correto
# Após criar plugin, executar:
jq empty plugins/[plugin-name]/.claude-plugin/plugin.json
jq empty .claude-plugin/marketplace.json
```

### ❌ Erro 5: Plugin Muito Genérico ou Amplo

Não criar plugins com escopo indefinido:

```bash
# ❌ Errado
/create-plugin "general utilities"          # Escopo muito amplo
/create-plugin "development tools"          # Não específico

# ✅ Correto
/create-plugin "terraform-aws-validator with security best practices"
/create-plugin "markdown-linter with auto-fix capabilities"
```

### ❌ Erro 6: Diretório Incorreto para MCP Server

Não use `mcp/` como diretório para código do servidor MCP:

```bash
# ❌ Errado
plugins/my-plugin/
├── mcp/
│   └── server.py          # Diretório incorreto

# ✅ Correto
plugins/my-plugin/
├── servers/
│   └── server.py          # Diretório correto
├── .mcp.json              # Configuração MCP na raiz
```

## 📝 Exemplos

### Exemplo 1: Plugin de Automação de Commits

```bash
/create-plugin "Automates git commits with security validation and conventional messages"
```

**O que acontece:**

1. Pesquisa best practices de conventional commits e git workflows
1. Cria estrutura: `plugins/git-commit-helper/`
1. Gera comando `/commit` com validações de segurança
1. Cria agente `commit-assistant` para automação
1. Registra no marketplace com versão 1.0.0
1. Valida JSON e apresenta resultado

### Exemplo 2: Plugin de Testes Python

```bash
/create-plugin "Generates unit tests for Python projects with mocks and fixtures"
```

**O que acontece:**

1. Pesquisa patterns de teste unitário em Python
1. Cria estrutura: `plugins/python-test-generator/`
1. Gera comando `/py-test` para geração automática
1. Cria agente `test-assistant` para análise de cobertura
1. Adiciona skill `testing-patterns` com exemplos
1. Registra e valida

### Exemplo 3: Plugin de Documentação de API

```bash
/create-plugin "Creates API documentation from OpenAPI specifications"
```

**O que acontece:**

1. Pesquisa ferramentas de documentação OpenAPI
1. Cria estrutura: `plugins/api-docs-generator/`
1. Gera comando `/generate-api-docs` com argumentos para spec file
1. Cria agente `openapi-analyzer` para validação
1. Registra e apresenta componentes criados

### Exemplo 4: Plugin com MCP Server

```bash
/create-plugin "Integrates AWS services with Claude Code via MCP"
```

**O que acontece:**

1. Pesquisa AWS SDK e MCP integration patterns
1. Cria estrutura com `.mcp.json` e `servers/`
1. Configura MCP server para AWS integration
1. Gera comandos para operações AWS comuns
1. Registra MCP server em plugin.json
1. Valida configuração e apresenta resultado
