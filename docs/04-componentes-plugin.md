# 04 - Componentes do Plugin

## 📋 Visão Geral

Este documento detalha todos os componentes que podem fazer parte de um plugin do Claude Code: Commands, Agents, Hooks, MCP Servers e Skills.

---

## 🧩 Tipos de Componentes

Um plugin do Claude Code pode incluir:

1. **Commands** - Comandos personalizados (slash commands)
2. **Agents** - Agentes especializados para tarefas específicas
3. **Hooks** - Ganchos de ciclo de vida
4. **MCP Servers** - Servidores do Model Context Protocol
5. **Skills** - Habilidades para agentes

---

## 💬 1. Commands (Comandos)

### O que são?

Comandos são arquivos Markdown que aparecem como **slash commands** (`/comando`) no Claude Code.

### Localização

```
plugins/meu-plugin/
└── commands/
    ├── comando1.md
    ├── comando2.md
    └── comando3.md
```

### Estrutura de um Comando

```markdown
---
description: Descrição curta do comando (obrigatório)
---

Conteúdo do comando em Markdown.

Este texto será processado como um prompt pelo Claude Code quando o usuário executar o comando.
```

### Exemplo Básico

**Arquivo**: `commands/hello.md`

```markdown
---
description: Exibe uma mensagem de boas-vindas
---

Olá! 👋

Bem-vindo ao Claude Code!

Este é um comando personalizado que você pode usar a qualquer momento.
```

**Uso**: `/hello`

### Exemplo com Variáveis

**Arquivo**: `commands/greet.md`

```markdown
---
description: Cumprimenta uma pessoa específica
---

Olá {{name}}! 👋

É um prazer te conhecer. Como posso ajudar você hoje?
```

**Uso**: `/greet name="João"`

### Exemplo Avançado

**Arquivo**: `commands/create-component.md`

```markdown
---
description: Cria um novo componente React
---

# Criar Novo Componente React

Vou criar um componente React para você.

## Informações necessárias:

- Nome do componente: {{componentName}}
- Tipo: {{type}} (functional/class)
- Com TypeScript: {{typescript}} (yes/no)

## Arquivo que será criado:

```typescript
// src/components/{{componentName}}/{{componentName}}.tsx

import React from 'react';

interface {{componentName}}Props {
  // Props aqui
}

export const {{componentName}}: React.FC<{{componentName}}Props> = (props) => {
  return (
    <div>
      <h1>{{componentName}}</h1>
    </div>
  );
};
```

Deseja que eu crie este arquivo?
```

**Uso**:
```bash
/create-component componentName="Button" type="functional" typescript="yes"
```

### Variáveis Disponíveis

Você pode usar variáveis de ambiente e variáveis especiais:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{name}}` | Parâmetros customizados | `/cmd name="João"` |
| `{{date}}` | Data atual | `2025-01-15` |
| `{{time}}` | Hora atual | `14:30:00` |
| `${USER}` | Variável de ambiente | Nome do usuário do sistema |
| `${PWD}` | Diretório atual | `/home/user/project` |

---

## 🤖 2. Agents (Agentes)

### O que são?

Agentes são **sub-agentes especializados** que podem ser invocados para executar tarefas específicas de forma autônoma.

### Localização

```
plugins/meu-plugin/
└── agents/
    ├── test-runner.md
    ├── code-reviewer.md
    └── api-tester.md
```

### Estrutura de um Agente

```markdown
---
description: Descrição do agente (obrigatório)
---

# Nome do Agente

Descrição detalhada do que o agente faz.

## Responsabilidades:

1. Tarefa 1
2. Tarefa 2
3. Tarefa 3

## Como usar:

Instruções de uso.
```

### Exemplo: Test Runner Agent

**Arquivo**: `agents/test-runner.md`

```markdown
---
description: Executa testes automatizados do projeto
---

# Test Runner Agent

Sou um agente especializado em executar e analisar testes.

## Minhas Responsabilidades:

1. **Detectar framework de testes**
   - Jest, Mocha, PyTest, JUnit, etc.

2. **Executar testes**
   - Testes unitários
   - Testes de integração
   - Testes E2E

3. **Analisar resultados**
   - Identificar testes falhando
   - Calcular cobertura
   - Gerar relatórios

4. **Sugerir correções**
   - Analisar falhas
   - Propor soluções

## Como me usar:

Simplesmente peça para executar os testes e eu:

1. Identificarei o framework usado
2. Executarei os testes apropriados
3. Analisarei os resultados
4. Reportarei os achados
5. Sugerirei correções se necessário

## Exemplos:

- "Execute os testes unitários"
- "Rode todos os testes e me mostre a cobertura"
- "Teste apenas o módulo de autenticação"
```

### Exemplo: Code Reviewer Agent

**Arquivo**: `agents/code-reviewer.md`

```markdown
---
description: Revisa código seguindo as melhores práticas
---

# Code Reviewer Agent

Sou um agente especializado em revisar código.

## Critérios de Revisão:

### 1. Qualidade do Código
- Legibilidade
- Manutenibilidade
- Complexidade
- Duplicação

### 2. Boas Práticas
- Padrões de projeto
- SOLID principles
- Clean Code

### 3. Performance
- Complexidade algorítmica
- Uso de memória
- Otimizações possíveis

### 4. Segurança
- Vulnerabilidades
- Input validation
- Exposição de dados sensíveis

### 5. Testes
- Cobertura de testes
- Qualidade dos testes
- Edge cases

## Processo de Revisão:

1. Analisar o código alterado
2. Identificar problemas
3. Sugerir melhorias
4. Explicar o raciocínio
5. Fornecer exemplos de correção

## Como me usar:

Após fazer alterações no código, peça para revisar e eu farei uma análise completa.
```

### Exemplo: API Tester Agent

**Arquivo**: `agents/api-tester.md`

```markdown
---
description: Testa APIs REST e GraphQL
---

# API Tester Agent

Especialista em testar APIs REST e GraphQL.

## Capacidades:

### REST APIs
- GET, POST, PUT, DELETE, PATCH
- Autenticação (Bearer, Basic, API Key)
- Headers customizados
- Validação de resposta

### GraphQL
- Queries
- Mutations
- Subscriptions
- Schema validation

## Processo de Teste:

1. **Configuração**
   - Endpoint
   - Autenticação
   - Headers

2. **Execução**
   - Fazer requisições
   - Medir tempo de resposta
   - Capturar erros

3. **Validação**
   - Status code
   - Response body
   - Response headers
   - Schema validation

4. **Relatório**
   - Resultados
   - Métricas
   - Problemas encontrados

## Exemplo de Uso:

```
Teste a API em https://api.example.com/users
com autenticação Bearer e valide:
- Status 200
- Array de usuários
- Cada usuário tem id, name, email
```
```

---

## 🪝 3. Hooks (Ganchos)

### O que são?

Hooks permitem executar **ações automáticas** em momentos específicos do ciclo de vida do Claude Code.

### Localização

```
plugins/meu-plugin/
└── hooks/
    └── hooks.json
```

### Tipos de Hooks (8 no total)

| Hook | Quando Dispara | Uso Comum |
|------|---------------|-----------|
| `user-prompt-submit` | Usuário envia prompt | Validação, logging, modificação |
| `tool-call-before` | Antes de chamar ferramenta | Validação, logging |
| `tool-call-after` | Depois de chamar ferramenta | Análise, modificação de resultado |
| `file-edit-before` | Antes de editar arquivo | Backup, validação |
| `file-edit-after` | Depois de editar arquivo | Formatação, linting |
| `session-start` | Início da sessão | Configuração, logging |
| `session-end` | Fim da sessão | Cleanup, relatórios |
| `error` | Quando ocorre erro | Logging, notificação |

### Estrutura do hooks.json

```json
{
  "hooks": [
    {
      "type": "nome-do-hook",
      "command": "comando-a-executar",
      "args": ["arg1", "arg2"],
      "env": {
        "VAR": "valor"
      }
    }
  ]
}
```

### Exemplo: Hook de Validação

**Arquivo**: `hooks/hooks.json`

```json
{
  "hooks": [
    {
      "type": "user-prompt-submit",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/validate-prompt.js"],
      "description": "Valida o prompt do usuário antes de processar"
    }
  ]
}
```

### Exemplo: Hook de Formatação Automática

```json
{
  "hooks": [
    {
      "type": "file-edit-after",
      "command": "prettier",
      "args": ["--write", "${FILE_PATH}"],
      "description": "Formata arquivo automaticamente após edição"
    },
    {
      "type": "file-edit-after",
      "command": "eslint",
      "args": ["--fix", "${FILE_PATH}"],
      "description": "Executa ESLint após edição"
    }
  ]
}
```

### Exemplo: Hook de Testes Automáticos

```json
{
  "hooks": [
    {
      "type": "file-edit-after",
      "command": "npm",
      "args": ["test", "--", "--testPathPattern=${FILE_PATH}"],
      "description": "Executa testes relacionados ao arquivo editado"
    }
  ]
}
```

### Exemplo Completo com Múltiplos Hooks

```json
{
  "hooks": [
    {
      "type": "session-start",
      "command": "echo",
      "args": ["🚀 Sessão iniciada em $(date)"],
      "description": "Log de início de sessão"
    },
    {
      "type": "user-prompt-submit",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/log-prompt.js"],
      "env": {
        "LOG_FILE": "${HOME}/.claude/prompts.log"
      },
      "description": "Registra todos os prompts"
    },
    {
      "type": "file-edit-after",
      "command": "prettier",
      "args": ["--write", "${FILE_PATH}"],
      "description": "Formata código"
    },
    {
      "type": "file-edit-after",
      "command": "git",
      "args": ["add", "${FILE_PATH}"],
      "description": "Adiciona ao stage automaticamente"
    },
    {
      "type": "error",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/log-error.js"],
      "description": "Registra erros"
    },
    {
      "type": "session-end",
      "command": "echo",
      "args": ["✅ Sessão finalizada"],
      "description": "Log de fim de sessão"
    }
  ]
}
```

### Variáveis Disponíveis em Hooks

| Variável | Disponível em | Descrição |
|----------|--------------|-----------|
| `${CLAUDE_PLUGIN_ROOT}` | Todos | Raiz do plugin |
| `${FILE_PATH}` | `file-edit-*` | Caminho do arquivo |
| `${TOOL_NAME}` | `tool-call-*` | Nome da ferramenta |
| `${PROMPT}` | `user-prompt-submit` | Prompt do usuário |
| `${ERROR_MESSAGE}` | `error` | Mensagem de erro |

---

## 🔗 4. MCP Servers (Model Context Protocol)

### O que são?

MCP Servers conectam **ferramentas e serviços externos** ao Claude Code.

### Configuração

Dois formatos possíveis:

#### 4.1. Arquivo .mcp.json (Standalone)

**Localização**:
```
plugins/meu-plugin/
└── .mcp.json
```

**Exemplo**:
```json
{
  "database-tools": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/db-server.js"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  },
  "api-client": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-mcp",
    "args": ["--verbose"],
    "env": {
      "API_KEY": "${MY_API_KEY}"
    }
  }
}
```

#### 4.2. Inline no plugin.json

**Exemplo**:
```json
{
  "name": "meu-plugin",
  "version": "1.0.0",
  "description": "Plugin com MCP",
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/db.js"],
      "env": {
        "DB_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Exemplo: MCP Server para Banco de Dados

**.mcp.json**:
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "POSTGRES_URL": "${DATABASE_URL}"
    }
  }
}
```

### Exemplo: MCP Server Personalizado

**Estrutura**:
```
plugins/api-plugin/
├── .mcp.json
└── servers/
    └── api-mcp/
        ├── index.js
        └── package.json
```

**.mcp.json**:
```json
{
  "custom-api": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/api-mcp/index.js"],
    "env": {
      "API_BASE_URL": "https://api.example.com",
      "API_KEY": "${MY_API_KEY}"
    }
  }
}
```

**servers/api-mcp/index.js** (simplificado):
```javascript
#!/usr/bin/env node

const MCP = require('@modelcontextprotocol/sdk');

const server = new MCP.Server({
  name: 'custom-api',
  version: '1.0.0'
});

// Registrar ferramenta
server.tool('fetch-data', async (params) => {
  const response = await fetch(
    `${process.env.API_BASE_URL}/data`,
    {
      headers: {
        'Authorization': `Bearer ${process.env.API_KEY}`
      }
    }
  );
  return await response.json();
});

server.start();
```

---

## 🎯 5. Skills (Habilidades para Agentes)

### O que são?

Skills são **capacidades reutilizáveis** que podem ser usadas por agentes.

### Localização

```
plugins/meu-plugin/
└── skills/
    ├── database-skill/
    │   └── SKILL.md
    └── api-skill/
        └── SKILL.md
```

### Estrutura de uma Skill

```markdown
---
description: Descrição da skill
---

# Nome da Skill

Descrição do que a skill faz e como usar.

## Capacidades:

- Capacidade 1
- Capacidade 2

## Exemplos de Uso:

[Exemplos]
```

### Exemplo: Database Skill

**Arquivo**: `skills/database-skill/SKILL.md`

```markdown
---
description: Skill para interagir com bancos de dados
---

# Database Skill

Fornece capacidades para interagir com diferentes bancos de dados.

## Suporta:

- PostgreSQL
- MySQL
- SQLite
- MongoDB

## Capacidades:

### 1. Executar Queries
```sql
SELECT * FROM users WHERE active = true;
```

### 2. Criar Tabelas
```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2)
);
```

### 3. Migrations
- Criar migrations
- Executar migrations
- Rollback migrations

### 4. Análise
- Explicar query plans
- Sugerir índices
- Otimizar queries

## Uso em Agentes:

Agentes podem usar esta skill para:
- Consultar dados
- Modificar esquemas
- Analisar performance
- Gerar relatórios
```

### Exemplo: API Skill

**Arquivo**: `skills/api-skill/SKILL.md`

```markdown
---
description: Skill para trabalhar com APIs REST
---

# API Skill

Capacidades para interagir com APIs REST.

## Capacidades:

### 1. HTTP Methods
- GET - Buscar dados
- POST - Criar recursos
- PUT/PATCH - Atualizar recursos
- DELETE - Remover recursos

### 2. Autenticação
- Bearer Token
- API Key
- Basic Auth
- OAuth 2.0

### 3. Formatos
- JSON
- XML
- Form Data
- Multipart

### 4. Validação
- Schema validation
- Status codes
- Response headers
- Error handling

## Exemplo de Uso:

```javascript
// GET request
const users = await api.get('/users', {
  headers: {
    'Authorization': 'Bearer ${API_TOKEN}'
  }
});

// POST request
const newUser = await api.post('/users', {
  body: {
    name: 'João',
    email: 'joao@example.com'
  }
});
```

## Integração com Agentes:

Agentes podem usar esta skill para:
- Testar endpoints
- Documentar APIs
- Gerar clientes
- Validar contratos
```

---

## 📏 Tamanhos Recomendados e Separação de Responsabilidades

### A Regra de Ouro

```
Agent = COMO fazer (processo de execução, 50-200 linhas)
Command = Interface (invoca agents/MCPs, 20-100 linhas)
Skill = O QUE saber (conhecimento de domínio, <500 linhas)
```

### Tabela de Tamanhos

| Componente | Tamanho Ideal | Tamanho Máximo | Ação se Excedido |
|------------|--------------|----------------|------------------|
| **Agent** | 50-150 linhas | 200 linhas | Extrair conhecimento para skills OU dividir em múltiplos agents |
| **Command** | 20-50 linhas | 100 linhas | Extrair lógica para agent se contém lógica de negócio |
| **Skill (SKILL.md)** | 200-300 linhas | 500 linhas | Usar progressive disclosure (arquivos de referência) |
| **Setup addition to CLAUDE.md** | 20-30 linhas | 40 linhas | Usar progressive disclosure, link para README.md |

### Diferenças Críticas de Estrutura

#### Agents (Sub-agentes)

**❌ INCORRETO** - Agents NÃO são pastas:
```
.claude/agents/my-agent/
├── my-agent.md
└── reference.md        # ❌ NÃO SUPORTADO
```

**✅ CORRETO** - Agents são arquivos .md ÚNICOS:
```
.claude/agents/my-agent.md  # ← TODO o conteúdo em UM arquivo
```

**Por quê?**
- Agents operam em contexto isolado
- Precisam de system prompt completo em arquivo único
- **NÃO suportam progressive disclosure**
- Devem incluir TODAS as instruções em um .md

#### Skills

**✅ CORRETO** - Skills PODEM ter múltiplos arquivos:
```
.claude/skills/my-skill/
├── SKILL.md           # Visão geral (< 500 linhas)
├── reference.md       # Documentação de suporte
└── patterns.md        # Biblioteca de padrões
```

**Por quê?**
- Usam padrão de progressive disclosure
- Carregam arquivos adicionais on-demand via Read tool
- Podem organizar conhecimento em múltiplos arquivos
- SKILL.md serve como overview/índice

### Quando Extrair Conhecimento para Skills

**Extrair para skill se**:

1. **Agent > 200 linhas**
2. **Seções de documentação ou referência**
3. **Múltiplas tabelas de referência**
4. **Padrões de código ou templates**
5. **Conhecimento duplicado entre agents**

### Exemplo de Refatoração

#### Antes (Agent com 310 linhas)

```markdown
# test-generator.md (310 linhas)

## Instructions
[80 linhas de processo]

## Mock Patterns for LangChain    # ← Conhecimento - EXTRAIR!
[150 linhas de patterns]

## Pytest Best Practices    # ← Conhecimento - EXTRAIR!
[80 linhas de docs]
```

**Problemas**:
- ❌ Agent muito grande (310 linhas)
- ❌ Mistura processo com conhecimento
- ❌ Conhecimento não reutilizável
- ❌ Difícil manutenção

#### Depois (Agent 90 linhas + Skills)

**Agent focado no processo**:
```markdown
# test-generator.md (90 linhas)

## Instructions
For LangChain mock patterns, see skill `langchain-mock-patterns`
For pytest best practices, see skill `pytest-best-practices`

[80 linhas de processo essencial]
```

**Skills reutilizáveis**:
```
plugins/python-test-generator/
├── agents/
│   └── test-generator.md         # 90 linhas
└── skills/
    ├── langchain-mock-patterns/
    │   └── SKILL.md               # 150 linhas
    └── pytest-best-practices/
        └── SKILL.md               # 80 linhas
```

**Benefícios**:
- ✅ Agent focado (90 linhas)
- ✅ Skills reutilizáveis por outros agents
- ✅ Manutenção mais fácil
- ✅ Conhecimento organizado por domínio
- ✅ Performance otimizada

### O Fluxo Correto

#### 1. Agents Executam Tarefas (COMO fazer)

- Processo de execução passo-a-passo
- Lógica de orquestração
- Invocação de tools
- **Arquivo .md único** (sem progressive disclosure)
- **50-200 linhas ideal**

**Exemplo**:
```markdown
# commit-assistant.md (150 linhas)

For conventional commit rules, see skill `conventional-commits`
For CI detection, see skill `ci-detection`

## Process:
1. Validate security
2. Run CI/CD (see skill for tool detection)
3. Analyze changes
4. Generate commit message (see skill for format)
5. Commit and push
```

#### 2. Commands Facilitam Invocação (Interface)

- Interface voltada para o usuário
- Invoca agents via Task tool
- Invoca MCPs
- **SEM lógica de negócio** (delega para agents)
- **20-100 linhas**

**Exemplo**:
```markdown
# commit.md (19 linhas)

Use agent commit-assistant to execute full commit process
```

#### 3. Skills Fornecem Conhecimento (O QUE saber)

- Conhecimento de domínio
- Documentação de API
- Melhores práticas
- Padrões de código
- **Auto-descobertas por Claude**
- **Progressive disclosure suportado** (estrutura de pasta)
- **SKILL.md < 500 linhas**

**Exemplo**:
```
skills/
├── conventional-commits/        # Pasta com múltiplos arquivos
│   ├── SKILL.md                 # Conhecimento
│   └── examples.md
└── ci-detection/
    └── SKILL.md
```

### Sinais de Alerta

**🚨 Agent Precisa Refatoração**:

- ✅ Agent > 200 linhas
- ✅ Seções com "Documentation" ou "Reference"
- ✅ Múltiplas tabelas de referência
- ✅ Conhecimento duplicado entre agents
- ✅ Agent faz "tudo"

**Ação**: Identificar seções de conhecimento → Extrair para skills → Agent reduzido para ~150 linhas

**🚨 Command com Lógica de Negócio**:

- ✅ Command > 100 linhas
- ✅ Contém passos de processo
- ✅ Contém lógica de decisão complexa

**Ação**: Criar agent com processo → Command apenas invoca agent (~50 linhas)

### Processo de Refatoração

#### Para Agent > 200 linhas:

1. **Identificar seções**:
   - Processo/execução → manter no agent
   - Conhecimento/docs → extrair para skill

2. **Para cada seção de conhecimento**:
   - \> 50 linhas? → extrair para skill
   - Usado por outro agent? → extrair para skill
   - < 50 linhas & específico? → pode manter

3. **Criar skills separadas** (com estrutura de pasta)

4. **Agent referencia skills**: "See skill X for Y"

5. **Validar**: agent agora < 200 linhas?

#### Para Command com Lógica:

1. **Identificar passos independentes do workflow**

2. **Criar agent** (~150 linhas) com processo

3. **Command invoca agent** (~50 linhas)

4. **Validar**: command < 100 linhas?

### Exemplo Completo: Antes & Depois

#### Antes: Command Monolítico (906 linhas)

```markdown
# setup-project-incremental.md (906 linhas)

## Processo de Execução
### 1. Detectar Tipo de Projeto (Novo vs Legacy)
[Lógica detalhada de detecção - 200 linhas]

### 2. Configurar CLAUDE.md
[Lógica de configuração - 300 linhas]

### 3. Criar PRD
[Lógica de criação - 400 linhas]
```

**Problemas**:
- ❌ Command com lógica de negócio (906 linhas!)
- ❌ Deveria ser agent
- ❌ Viola padrão de separação

#### Depois: Command + Agent (50 + 150 linhas)

**Command** (50 linhas):
```markdown
# setup-project-incremental.md (50 linhas)

Use agent setup-assistant to configure project with YAGNI principles

[Documentação de uso]
```

**Agent** (150 linhas):
```markdown
# setup-assistant.md (150 linhas)

## Process:
1. Detect project type
2. Configure CLAUDE.md (≤40 lines)
3. Create PRD v0.1
4. Validate setup
```

**Benefícios**:
- ✅ Command leve (50 linhas)
- ✅ Agent focado em processo (150 linhas)
- ✅ Separação clara de responsabilidades
- ✅ Reutilizável

### Regras Finais

1. **Agent = COMO, Skill = O QUE**
   - Processo → Agent
   - Conhecimento → Skill

2. **1 Agent = 1 Responsabilidade**
   - Múltiplas responsabilidades → quebrar

3. **Agent > 200 linhas? Revisar!**
   - Identificar conhecimento extraível
   - Ou quebrar em sub-agents

4. **Teste do Copy-Paste**
   - Se copiaria entre agents → extrair para skill

5. **Progressive Disclosure (APENAS SKILLS!)**
   - ✅ Skill > 500 lines → arquivos de referência
   - ❌ Agent > 200 lines → NÃO suporta progressive disclosure
   - → Extrair para skills OU dividir agents

6. **Agents são ARQUIVOS ÚNICOS**
   - ✅ `agents/my-agent.md`
   - ❌ `agents/my-agent/my-agent.md`

7. **Skills são PASTAS**
   - ✅ `skills/my-skill/SKILL.md`
   - ❌ `skills/my-skill.md` (sem progressive disclosure)

8. **Reuso > Especificidade**
   - Conhecimento reutilizável → sempre skill
   - Processo único → pode ficar no agent

---

## 🎨 Combinando Componentes

### Exemplo: Plugin Completo de Testes

**Estrutura**:
```
plugins/test-suite/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── commands/
│   ├── test.md
│   ├── coverage.md
│   └── watch.md
├── agents/
│   ├── test-runner.md
│   └── test-generator.md
├── hooks/
│   └── hooks.json
└── skills/
    └── testing-skill/
        └── SKILL.md
```

**Fluxo de Uso**:
1. Usuário executa `/test`
2. Comando invoca o **test-runner agent**
3. Agent usa a **testing-skill** para detectar framework
4. Agent usa **MCP server** para executar testes
5. **Hook** `file-edit-after` roda testes automaticamente após edições

---

## ✅ Checklist de Componentes

Ao criar um plugin, considere incluir:

### Essencial
- [ ] Pelo menos 1 comando útil
- [ ] README.md documentando uso

### Recomendado
- [ ] Agente especializado para tarefa principal
- [ ] Hooks para automação
- [ ] Skills reutilizáveis

### Avançado
- [ ] MCP server para integrações externas
- [ ] Múltiplos agentes para tarefas complexas
- [ ] Suite completa de hooks

---

## 🚀 Próximos Passos

Agora que você conhece todos os componentes, aprenda a:

➡️ [05 - Publicação e Distribuição](./05-publicacao-e-distribuicao.md)

---

[⬅️ Anterior: Criando um Plugin](./03-criando-plugin.md) | [⬅️ Voltar ao Índice](./README.md) | [➡️ Próximo: Publicação e Distribuição](./05-publicacao-e-distribuicao.md)
