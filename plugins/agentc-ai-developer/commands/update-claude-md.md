---
description: Update project CLAUDE.md with Agentc AI Developer guidance and commands
allowed-tools: Read, Write
argument-hint: '[silent|verbose]'
model: ''
---

# Update Project CLAUDE.md

Automatically integrate Agentc AI Developer guidance into your project's CLAUDE.md file.

## 🎯 Objetivo

- Integrar guidance do Agentc AI Developer no CLAUDE.md do projeto
- Adicionar referências aos comandos disponíveis (/brief, /setup-local-observability, /spike-agentic, /backlog)
- Manter documentação concisa (≤40 linhas)
- Preservar conteúdo existente do CLAUDE.md
- Usar padrão de progressive disclosure com links para documentação completa

## Prerequisites

Verify before execution:

1. Completed `/brief` command (Microprocesso 1.1)
1. README.md exists with Brief Minimo specification
1. Project's CLAUDE.md exists or will be created automatically

## Execution

1. **Read project context**

   - Locate README.md (from `/brief` command)
   - Extract Brief Minimo specification (agent name, purpose)
   - Validate Microprocesso 1.1 completion

1. **Generate CLAUDE.md section**

   - Create concise guidance section (≤40 lines)
   - Include available Agentc commands: `/brief`, `/setup-local-observability`, `/spike-agentic`, `/backlog`
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
## Agentc AI Developer (Microprocesso 1.1-1.4)

Commands for AI agent planning, environment setup, architecture validation, and incremental development:

- **`/brief`**: Create or review Brief Minimo specification
- **`/setup-local-observability`**: Configure Python venv, dependencies, .env, LangSmith
- **`/spike-agentic`**: Validate agent architecture with agentic loop
- **`/backlog`**: Generate incremental development backlog

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
# ✅ 28 linhas adicionadas
# ⏱️ Executado em 0.8s
```

## Troubleshooting

### README.md not found

- Execute `/brief` first to create Brief Minimo specification

### CLAUDE.md doesn't exist

- Command creates CLAUDE.md automatically with Agentc section only

### Section already exists

- Command updates existing section (no duplication)
- All other CLAUDE.md content preserved

## ✅ Critérios de Sucesso

- [ ] README.md lido e Brief Minimo extraído com sucesso
- [ ] CLAUDE.md localizado ou criado
- [ ] Seção "Agentc AI Developer" adicionada ou atualizada
- [ ] Seção contém ≤40 linhas
- [ ] Todos os 4 comandos listados (/brief, /setup-local-observability, /spike-agentic, /backlog)
- [ ] Link para documentação completa incluído
- [ ] Conteúdo existente do CLAUDE.md preservado
- [ ] Nenhuma duplicação de seção
- [ ] Execução completada em \<1 minuto
