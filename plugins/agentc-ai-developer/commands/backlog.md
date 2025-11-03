---
description: Generate or update incremental development backlog from Brief Minimo specification. Creates BACKLOG.md with YAGNI-compliant increments.
allowed-tools: Read, Write
argument-hint: "[create|update|view]"
---

# Backlog Management

Generate or update incremental development backlog for AI agent projects.

## Modes

**Mode 1: Create** - Generate new docs/BACKLOG.md from Brief Minimo specification

**Mode 2: Update** - Update existing backlog with completed increments or new features

**Mode 3: View** - Display current backlog status and progress

## Prerequisites

Validate before execution:
1. Check README.md exists (from `/brief`)
2. Check docs/SPIKE.md exists (from `/spike-agentic`) - optional
3. Verify Brief Minimo specification is complete

If missing: Guide user to run `/brief` first.

## Execution: Mode 1 - Create New Backlog

1. Read README.md and extract Brief Minimo specification
2. Read docs/SPIKE.md if exists
3. Generate docs/BACKLOG.md with:
   - Agent context (from Brief Minimo summary)
   - 3-5 initial increments (YAGNI-compliant, independently deliverable)
   - Each increment: Objective, Scope, Success Criteria, Duration
4. Validate backlog follows incremental development principles
5. Report creation success with file path

## Execution: Mode 2 - Update Existing Backlog

1. Read existing docs/BACKLOG.md
2. Ask user: "What changed? (completed increments, new features, adjustments)"
3. Update BACKLOG.md:
   - Mark completed increments as ✅ COMPLETO
   - Update in-progress as 🔄 EM PROGRESSO
   - Add new planned increments as ⏳ PLANEJADO
4. Preserve implementation notes section
5. Report update success

## Execution: Mode 3 - View Status

1. Read docs/BACKLOG.md
2. Display summary:
   - Completed: X increments ✅
   - In-progress: Y increments 🔄
   - Planned: Z increments ⏳
3. Show next recommended increment
4. Display progress percentage

## Backlog Generation Rules

Apply YAGNI principles:
- Each increment independently deliverable
- Start with smallest viable feature
- Maximum 2-4 hours per increment initially
- Avoid premature optimization
- Focus on happy path first

## BACKLOG.md Format

Generate with this structure:

```
# Backlog - [Agent Name]

## Contexto
[Brief Minimo summary extracted from README.md]

## Incrementos Planejados

### Incremento 1: [Name] - ✅ COMPLETO
**Objetivo:** [What it delivers]
**Escopo:**
- [x] Feature 1
- [x] Feature 2
**Critérios de Sucesso:** [How to validate]
**Duração estimada:** 2-4h

[Repeat for other increments with status: 🔄 EM PROGRESSO or ⏳ PLANEJADO]

## Notas de Implementação
[Technical decisions, trade-offs, learnings]
```

## Next Steps

After backlog creation:
- Recommend starting Increment 1
- Suggest reviewing after each completed increment
- Mention `/spike-agentic` if spike not done yet
