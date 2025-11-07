---
description: Update CLAUDE.md with Agentc AI Developer commands and MCP integration
allowed-tools: Read, Write
argument-hint: '[mode: silent|verbose] - controle de verbosidade'
model: claude-sonnet-4-5
---

# Update Project CLAUDE.md

Automatically integrate Agentc AI Developer guidance into your project's CLAUDE.md file.

## 🎯 Objetivo

- Integrar guidance do Agentc AI Developer no CLAUDE.md do projeto
- Adicionar referências aos 8 comandos disponíveis (Stage 1: /brief, /setup-local-observability, /spike-agentic, /backlog; Stage 2: /analyze-slices, /iniciar-slice, /novo-incremento, /finalizar-incremento)
- Documentar integração MCP langchain-docs para acesso à documentação LangChain/LangGraph
- Manter documentação concisa (≤60 linhas)
- Preservar conteúdo existente do CLAUDE.md
- Usar padrão de progressive disclosure com links para documentação completa

## Pré-requisitos

Verificar antes da execução:

1. Completed `/brief` command (Microprocesso 1.1)
1. README.md exists with Brief Minimo specification
1. Project's CLAUDE.md exists or will be created automatically

## Execução

1. **Ler contexto do projeto**

   - Locate README.md (from `/brief` command)
   - Extract Brief Minimo specification (agent name, purpose)
   - Validate Microprocesso 1.1 completion

1. **Generate CLAUDE.md section**

   - Create concise guidance section (≤60 lines)
   - Include all 8 Agentc commands organized by stage:
     - Stage 1 (Planning): `/brief`, `/setup-local-observability`, `/spike-agentic`, `/backlog`
     - Stage 2 (Development): `/analyze-slices`, `/iniciar-slice`, `/novo-incremento`, `/finalizar-incremento`
   - Document MCP langchain-docs integration for LangChain/LangGraph documentation access
   - Add usage context: when to use each command
   - Link to `plugins/agentc-ai-developer/README.md` for details

1. **Update or create CLAUDE.md**

   - If CLAUDE.md exists: Add Agentc section (update if already present)
   - If CLAUDE.md missing: Create with Agentc section only
   - Preserve existing content, never remove

1. **Report completion**

   - Confirm CLAUDE.md location and updated section
   - Show generated content
   - Display execution time (\<1 minute)

## Generated Section Example

```markdown
## Agentc AI Developer - Brief Minimo Methodology

Complete workflow for AI agent development from planning to production-ready implementation.

### Stage 1: Planning & Architecture

- **`/brief`**: Create Brief Minimo specification (5 fundamental questions)
- **`/setup-local-observability`**: Configure Python venv, dependencies, .env, LangSmith
- **`/spike-agentic`**: Validate agent architecture with agentic loop (3-4h time-boxed)
- **`/backlog`**: Generate incremental development backlog with prioritization

### Stage 2: Development Workflow

- **`/analyze-slices`**: Validate slices with Gates S1.1 and Fast-Track criteria
- **`/iniciar-slice`**: Initialize slice development with baseline metrics
- **`/novo-incremento`**: Execute incremental development loop (PASSO A-E)
- **`/finalizar-incremento`**: Finalize increment with validation and regression tests

### MCP Integration

**langchain-docs** server provides real-time access to LangChain/LangGraph documentation:
- Auto-activated during `/spike-agentic` and development commands
- Provides current API references and best practices
- Accessible via plugin's `.mcp.json` configuration

**Documentation**: See `plugins/agentc-ai-developer/README.md`
```

## 📝 Exemplo

```bash
# Modo padrão (verbose)
/update-claude-md

# Modo silencioso (apenas reporta sucesso/erro)
/update-claude-md silent

# Resultado esperado:
# ✅ README.md lido com sucesso
# ✅ Brief Minimo extraído: Agent Name = "Task Automation Agent"
# ✅ CLAUDE.md atualizado com seção Agentc AI Developer
# ✅ Seção organizada por Stage 1 (Planning) e Stage 2 (Development)
# ✅ 8 comandos documentados
# ✅ Integração MCP langchain-docs incluída
# ✅ 52 linhas adicionadas
# ⏱️ Executado em 0.9s
```

## Solução de Problemas

### README.md não encontrado

- Execute `/brief` primeiro para criar especificação Brief Minimo

### CLAUDE.md não existe

- Comando cria CLAUDE.md automaticamente com apenas seção Agentc

### Seção já existe

- Comando atualiza seção existente (sem duplicação)
- Todo o conteúdo existente do CLAUDE.md é preservado

## ❌ Anti-Patterns

### ❌ Erro 1: Executar sem Brief Minimo

Não execute este comando antes de criar o Brief Minimo:

```bash
# ❌ Errado - Executar sem /brief
/update-claude-md
# Resultado: Falha ao extrair especificação do README.md

# ✅ Correto - Seguir workflow
/brief
# ... criar Brief Minimo
/update-claude-md
```

### ❌ Erro 2: Editar Manualmente Seção Gerada

Não edite manualmente a seção "Agentc AI Developer" no CLAUDE.md:

```markdown
# ❌ Errado - Editar seção manualmente
## Agentc AI Developer
- Meu comando customizado aqui
# Será sobrescrito na próxima execução

# ✅ Correto - Adicionar seções próprias separadamente
## Agentc AI Developer
[Seção gerada automaticamente]

## Meus Comandos Customizados
[Suas adições aqui - não serão sobrescritas]
```

### ❌ Erro 3: Remover Links de Documentação

Não remova links para documentação completa:

```markdown
# ❌ Errado - Remover link
## Agentc AI Developer
[comandos listados]
# Link removido: plugins/agentc-ai-developer/README.md

# ✅ Correto - Preservar link
**Documentation**: See `plugins/agentc-ai-developer/README.md`
# Usuários precisam acessar documentação detalhada
```

## ✅ Critérios de Sucesso

- [ ] README.md lido e Brief Minimo extraído com sucesso
- [ ] CLAUDE.md localizado ou criado
- [ ] Seção "Agentc AI Developer" adicionada ou atualizada
- [ ] Seção contém ≤60 linhas
- [ ] Todos os 8 comandos listados (Stage 1: 4 comandos, Stage 2: 4 comandos)
- [ ] Integração MCP langchain-docs documentada
- [ ] Link para documentação completa incluído
- [ ] Conteúdo existente do CLAUDE.md preservado
- [ ] Nenhuma duplicação de seção
- [ ] Execução completada em \<1 minuto
