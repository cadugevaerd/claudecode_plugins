---
name: prd-manager
description: Automatically manages and updates PRD (Product Requirements Document) by detecting appropriate update moments based on project phase. Use when working with PRD, requirements, product documentation, MVP definition, architectural decisions, learnings from increments, or transitioning between development phases (discovery, planning, design, increments). Trigger terms - requisitos, objetivos, MVP, incremento completo, decisões arquiteturais, aprendizados, lições aprendidas, ADR, Product Vision, épicos, User Stories.
allowed-tools: Read, Write, Edit, Grep, Bash
---

# PRD Manager Skill

Skill que gerencia automaticamente o PRD (Product Requirements Document), detectando momentos apropriados para atualizar e validando consistência entre código e documentação.

## 🎯 Quando Me Usar

Invoque automaticamente quando:

1. **Incremento completado** - "Pronto, funcionalidade X completa"
2. **Planejamento de MVP** - "Vamos definir MVP", "features principais"
3. **Arquitetura definida** - "Stack definido", "modelagem pronta"
4. **Decisão técnica importante** - "Escolhemos pattern X", ADR
5. **Pergunta sobre projeto** - Usuário questiona objetivos, MVP
6. **Implementação fora do MVP** - Detectar YAGNI violations

### Termos Gatilho
- "atualizar PRD", "PRD", "requisitos"
- "incremento completo", "funcionalidade pronta"
- "decisão arquitetural", "ADR"
- "aprendizado", "retrospectiva"
- "MVP", "Product Vision", "épicos"

## 📊 Responsabilidades

### 1. Detecção de Momento de Atualização
- Incremento completado → sugerir `/prd-update incremento`
- MVP definido → sugerir `/prd-update planejamento`
- Arquitetura pronta → sugerir `/prd-update design`
- Decisão importante → sugerir registrar ADR

### 2. Validação de Completude
Verificar se PRD tem campos obrigatórios por fase:

| Fase | Versão | Obrigatório |
|------|--------|-------------|
| **Descoberta** | 0.1 | Problema, 3+ objetivos, KPIs |
| **Planejamento** | 1.0 | Product Vision, MVP, épicos |
| **Design** | 1.1 | Arquitetura, stack, modelagem |
| **Desenvolvimento** | 1.x+ | Incrementos, aprendizados, ADRs |

### 3. Sugerir Próxima Fase
Baseado em progresso: v0.1 ✅ → sugira planejamento (v1.0)

### 4. Validar Consistência Código ↔ PRD
Detectar divergências: código implementa feature fora do MVP?

### 5. Alertar sobre YAGNI
Se código implementa features **fora do MVP** definido no PRD

## 📋 Fases do PRD

### Fase 0: Descoberta (v0.1)
**O que é o problema?**
- Problema definido
- 3+ objetivos claros
- KPIs para medir sucesso

### Fase 1: Planejamento (v1.0)
**O que vamos construir?**
- Product Vision
- MVP claramente definido
- Features fora do MVP (YAGNI)
- Épicos/user stories principais

### Fase 2: Design (v1.1)
**Como vamos construir?**
- Arquitetura de alto nível
- Stack tecnológica
- Modelagem de dados
- APIs/contratos

### Fase 3: Desenvolvimento (v1.x)
**Construindo incrementalmente**
- Incrementos documentados
- Aprendizados registrados
- ADRs para decisões importantes

### Fase 4: Finalizado (v2.0)
**As-Built documentation**
- Projeto completo
- Lições aprendidas
- Retrospectiva final

## 🔍 Detecção de Divergências

**Cenário**: PRD define MVP, código implementa features fora do MVP

```
⚠️  DIVERGÊNCIA DETECTADA

PRD MVP:
✅ Upload PDF
✅ Extração texto
❌ Dashboard

Código implementa:
✅ Upload PDF
✅ Extração texto
⚠️  Dashboard (FORA DO MVP!)

Ações:
A) Remover código (seguir MVP)
B) Atualizar PRD (é essencial afinal)
C) Documentar exceção
```

## 💡 Princípios

1. **Proativo, não invasivo**: Sugerir, não forçar
2. **Contextual**: Baseado em progresso real
3. **Educativo**: Explicar POR QUE sugerir
4. **Validador**: Consistência código ↔ documentação
5. **Orientador YAGNI**: Alertar features fora do MVP

## 📚 Referência Detalhada

Para instruções passo-a-passo:

- **TEMPLATE.md** - Template completo de PRD com todas as fases
- **PATTERNS.md** - Exemplos de invocação automática

## ⚡ Objetivo

✅ PRD sempre sincronizado com código
✅ Momentos apropriados para atualizar detectados
✅ Divergências código/PRD alertadas cedo
✅ YAGNI violations questionadas
✅ Fase do PRD evolui com projeto

**Valor**: Documentação viva que guia desenvolvimento incremental.
