---
description: Create incremental backlog with isolated, independently deliverable slices following Brief Minimo specification
allowed-tools: Read, Write
argument-hint: '[create|view]'
model: claude-sonnet-4-5
---

# Create Incremental Backlog

Generate increments as architecturally isolated slices with zero explicit dependencies.

## Prerequisites

Verify README.md exists with complete Brief Minimo specification (from `/brief`).

## Create Backlog

1. Read BRIEF_AGENTE_EMAIL.md and SPIKE.md to undestand the project and create Increments.
1. Extract global success criteria from "What is SUCCESS?" section
1. Assess impact level for each increment (HIGH/MEDIUM/LOW)
1. Generate `docs/BACKLOG.md` with 3-5 increments (each linked to success criteria and impact)
1. Apply isolation validation for each increment
1. Report completion with file path and validation status

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
- **Impacto**: HIGH / MEDIUM / LOW
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
- **Impacto**: HIGH / MEDIUM / LOW
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
- **Impacto**: HIGH / MEDIUM / LOW
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
- **Impact Distribution**: X HIGH / Y MEDIUM / Z LOW
- **Success Aligned**: All increments contribute to Brief Minimo metrics
- **Next Increment**: Start with Increment 1
```

## View Backlog

1. Read `docs/BACKLOG.md`
1. Display:
   - All increments and current status
   - Total estimated hours
   - Next recommended increment
1. Flag any increments violating isolation criteria

## Impact Assessment Rules

Assign impact level to each increment based on its contribution to agent goals:

### HIGH Impact

- Delivers core agent functionality
- Enables critical workflows required by Brief Minimo
- Foundational feature without which agent cannot operate
- Example: "Implement core classifier algorithm" for email prioritizer agent

### MEDIUM Impact

- Enhances existing features
- Important workflow improvement
- Extends core functionality with important capabilities
- Example: "Add edge case handling" for email prioritizer agent

### LOW Impact

- Polish and refinement
- Utilities and helper features
- Optional improvements for better UX/DX
- Non-blocking features
- Example: "Add formatted output options" for email prioritizer agent

## Time Calculation

When generating backlog, calculate total development time:

### Per-Increment Estimation

For each increment, estimate hours based on scope:

- **3 hours** - Simple, well-defined work (add functionality to existing component, simple tests)
- **4 hours** - Medium complexity (API integration, moderate logic, comprehensive tests)
- **5 hours** - Higher complexity (multi-step workflow, state management, edge cases)
- **6 hours** - Maximum complexity (maximum scope for single session, multiple integrations)

### Total Time Calculation

Calculate backlog totals:

1. **Sum all increment hours**: Add hours from each increment
1. **Buffer factor**: Add 10-15% buffer for discoveries and refinements
1. **Example**:
   - Increment 1: 4h
   - Increment 2: 5h
   - Increment 3: 3h
   - Subtotal: 12h
   - Buffer (15%): +1.8h
   - **Total estimated: ~14h (2 full days of development)**

### Time-to-Value Analysis

Calculate and report:

- **Time to MVP** (HIGH impact increments only): ~10h
- **Time to V1** (HIGH + MEDIUM): ~18h
- **Time to Polish** (ALL increments): ~20h

## Increment Design Rules

- **Duration**: 3-6 hours maximum (one development session)
- **Delivery**: Each increment produces working, testable code
- **Isolation**: Zero dependencies on other increments
- **Coupling**: No shared mutable state with other increments
- **Reordering**: Increments can be executed in any order without side effects
- **Testing**: Each increment has standalone test coverage
- **Impact**: Each increment assigned HIGH/MEDIUM/LOW based on contribution to agent goals
- **Time**: Each increment estimated 3-6h with buffer for total backlog calculation
