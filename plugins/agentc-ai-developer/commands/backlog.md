---
description: Generate backlog with incremental steps based on Brief Minimo specification
allowed-tools: Read, Write
argument-hint: '[create|view]'
---

# Backlog Command

## Preconditions

Verify README.md exists with Brief Minimo specification (from `/brief`).

## Create Backlog

1. Read README.md and extract Brief Minimo specification
1. Generate `docs/BACKLOG.md` with 3-5 increments following the template below
1. Each increment should be 3-6 hours (YAGNI principle)
1. Report completion with file path

## View Backlog

1. Read `docs/BACKLOG.md`
1. Display summary:
   - Total increments
   - Total estimated hours
   - Status distribution (⏳ Planejado / 🔄 Em Progresso / ✅ Completo)
1. Show next increment to start

## Backlog Template

```markdown
# Backlog - [Agent Name]

Brief extracted from: README.md

## Increments

### 1. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 3-4h
- **Objetivo**: [One sentence describing what this delivers]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

### 2. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 4-5h
- **Objetivo**: [One sentence describing what this delivers]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

### 3. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 3-6h
- **Objetivo**: [One sentence describing what this delivers]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

## Summary

- **Total Increments**: 3
- **Total Hours**: ~12h
- **Next Step**: Start with Increment 1
```

## Increment Guidelines

- **3-6 hours each** - Small enough to complete in one session
- **Complete feature** - Each increment delivers working functionality
- **Testable** - Each increment can be validated independently
- **No dependencies** - Increments can be reordered if needed
