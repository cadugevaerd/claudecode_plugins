---
description: Create incremental backlog with isolated, independently deliverable slices following Brief Minimo specification
allowed-tools: Read, Write
argument-hint: '[create|view]'
---

# Create Incremental Backlog

Generate increments as architecturally isolated slices with zero explicit dependencies.

## Prerequisites

Verify README.md exists with complete Brief Minimo specification (from `/brief`).

## Create Backlog

1. Read README.md and extract Brief Minimo specification
2. Extract global success criteria from "What is SUCCESS?" section in README.md
3. Generate `docs/BACKLOG.md` with 3-5 increments (each linked to success criteria)
4. Apply isolation validation for each increment
5. Report completion with file path and validation status

## Isolation Validation Checklist

For each increment, verify **ALL** criteria below (YAGNI principle):

- **No explicit dependencies**: Increment does not require completion of other increments
- **Standalone delivery**: Increment can be deployed/tested independently
- **Clear boundaries**: Increment has defined inputs and outputs
- **Decoupled logic**: Increment uses no shared state with other increments
- **Self-contained scope**: All required code changes within increment scope
- **Testable alone**: Increment can be unit tested without other increments
- **No forward references**: Increment does not reference future features

## Backlog Template

```markdown
# Backlog - [Agent Name]

Brief: [One-line agent purpose from README.md]

## Success Criteria (from Brief Minimo)

- **Metric**: [Quantifiable metric from README]
- **Target**: [Minimum target value]
- **Measurement**: [How success will be measured]
- **Validation**: [How/when will be validated]

## Increments

### 1. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 3-6h
- **Objetivo**: [Specific deliverable in one sentence]
- **Isolamento**: [How this increment is architecturally isolated]
- **Sucesso**: [How this increment contributes to global success criteria]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

### 2. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 3-6h
- **Objetivo**: [Specific deliverable in one sentence]
- **Isolamento**: [How this increment is architecturally isolated]
- **Sucesso**: [How this increment contributes to global success criteria]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

### 3. [Increment Title]

- **Status**: ⏳ Planejado
- **Horas**: 3-6h
- **Objetivo**: [Specific deliverable in one sentence]
- **Isolamento**: [How this increment is architecturally isolated]
- **Sucesso**: [How this increment contributes to global success criteria]
- **Tarefas**:
  - [ ] Task 1
  - [ ] Task 2
  - [ ] Task 3

## Summary

- **Total Increments**: 3
- **Total Hours**: ~9-18h
- **Success Aligned**: All increments contribute to Brief Minimo metrics
- **Next Increment**: Start with Increment 1
```

## View Backlog

1. Read `docs/BACKLOG.md`
2. Display:
   - All increments and current status
   - Total estimated hours
   - Next recommended increment
3. Flag any increments violating isolation criteria

## Increment Design Rules

- **Duration**: 3-6 hours maximum (one development session)
- **Delivery**: Each increment produces working, testable code
- **Isolation**: Zero dependencies on other increments
- **Coupling**: No shared mutable state with other increments
- **Reordering**: Increments can be executed in any order without side effects
- **Testing**: Each increment has standalone test coverage
