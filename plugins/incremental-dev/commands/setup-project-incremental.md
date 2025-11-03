---
description: Configura CLAUDE.md do projeto para usar desenvolvimento incremental e orientar Claude a seguir princípios YAGNI, além de criar PRD v0.1 inicial
---

# Setup Project for Incremental Development

Configura o projeto para desenvolvimento incremental:

1. Cria/atualiza `CLAUDE.md` com instruções YAGNI
1. Cria `docs/PRD.md v0.1` (Document inicial)

## Como usar

````bash
/setup-project-incremental
/setup-project-incremental "API REST para gerenciar tarefas"

```text

## O que é criado

### CLAUDE.md
Instruções para Claude seguir desenvolvimento incremental:
- Começar com MVP mínimo
- Questionar funcionalidades prematuras
- Evitar over-engineering
- Adicionar complexidade apenas quando necessário
- Refatorar quando padrões emergirem (Regra dos 3)

### PRD.md (v0.1 - Fase de Descoberta)
Documento vivo de requisitos:
- Problema que o projeto resolve
- Objetivos iniciais
- KPIs para medir sucesso
- Escopo inicial

## Processo

1. **Detectar tipo de projeto**:
   - Se existir código: Sugerir `/adopt-incremental` ou `/prd-retrofit`
   - Se novo: Prosseguir

2. **Criar CLAUDE.md**:
   - Template com YAGNI principles
   - Instruções de desenvolvimento
   - Links para comandos do plugin

3. **Criar PRD.md inicial**:
   - Seção de descoberta
   - Problema + objetivos
   - KPIs básicos
   - Placeholder para próximas fases

4. **Validar**:
   - CLAUDE.md válido
   - PRD.md estruturado corretamente

## Output esperado

```text

✅ PROJETO CONFIGURADO PARA INCREMENTAL

📝 CLAUDE.md criado
- Instruções YAGNI
- Comandos do plugin
- Princípios de desenvolvimento

📄 docs/PRD.md v0.1 criado
- Fase: Descoberta
- Pronto para evolução

🚀 Próximos passos:
1. /start-incremental (ou complementar PRD.md)
2. /add-increment "primeira feature"
3. /review-yagni (detectar over-engineering)

```text

## Próximos comandos

- `/start-incremental` - Criar PRD completo
- `/add-increment` - Adicionar primeira feature
- `/prd-view` - Ver PRD criado
````
