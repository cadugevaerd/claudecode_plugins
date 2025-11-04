---
description: Generate, update, view, or refine incremental development backlog with impact assessment and estimated hours
allowed-tools: Read, Write, Grep
argument-hint: '[create|update|view|refine]'
---

# Backlog Management

## Preconditions

1. Verify README.md exists (from `/brief` or project)
1. Verify docs/SPIKE.md exists (from `/spike-agentic`) - optional
1. Ensure Brief Minimo specification is complete

If prerequisites missing: Stop and guide user to run `/brief` first.

## Create New Backlog

1. Read README.md and extract Brief Minimo specification
1. Read docs/SPIKE.md if exists
1. Generate docs/BACKLOG.md with following structure for each increment:

### Increment Structure

For each of 3-5 increments, generate:

- **Name**: Clear, action-oriented increment name
- **Status**: ⏳ PLANEJADO / 🔄 EM PROGRESSO / ✅ COMPLETO
- **Objetivo**: What it delivers
- **Escopo**: Feature checklist
- **Critérios de Sucesso**: Validation criteria
- **Horas Estimadas**: Auto-generated based on:
  - Simple data fetching/display: 2-4 hours
  - Medium complexity (API + processing): 4-8 hours
  - Complex logic (state management + integration): 8-16 hours
- **Impacto**: Auto-generated assessment:
  - HIGH: Critical feature, enables core functionality
  - MEDIUM: Important feature, supports primary workflow
  - LOW: Nice-to-have, polish or utility

1. Validate all increments follow YAGNI principles
1. Report creation with file path and summary

## Update Existing Backlog

1. Read existing docs/BACKLOG.md
1. Identify changes needed:
   - Mark completed increments as ✅ COMPLETO
   - Update in-progress as 🔄 EM PROGRESSO
   - Add new planned increments as ⏳ PLANEJADO
1. For new increments: Generate Horas Estimadas and Impacto automatically
1. Preserve implementation notes section
1. Report update success

## View Backlog Status

1. Read docs/BACKLOG.md
1. Display summary:
   - Count: Completed ✅ / In-progress 🔄 / Planned ⏳
   - Total estimated hours for all increments
   - Impact distribution (HIGH/MEDIUM/LOW count)
1. Show next recommended increment to start
1. Calculate and display progress percentage

## Refine Existing Backlog

Triggered by `/analyze-slices` when slices fail S1.1 gates.

1. Read existing docs/BACKLOG.md
1. Read list of failing slices (provided as context)
1. For each failing slice, analyze which gates failed:
   - **Duration issue** (not 3-6h): Recommend splitting large slices or grouping small ones
   - **Score issue** (\<2.0): Re-assess impact or reduce estimated hours
   - **Reversibility issue**: Add rollback plan documentation
   - **Coupling issue**: Reduce dependencies, focus scope
   - **Success rate issue**: Reframe objective to align with MVP metrics
1. Propose refinement for each failing slice:
   - Break large slices (>6h) into 2-3 smaller increments
   - Increase estimated impact or reduce hours for low-score slices
   - Add reversibility/rollback documentation
   - Clarify scope isolation and dependencies
   - Align objective with MVP success metrics
1. Update docs/BACKLOG.md with refined slices
1. Re-run analysis to validate improvements
1. Report refinement results and next steps

## Impact Assessment Rules

Assign impact level based on:

- **HIGH**: Delivers core agent functionality, enables critical workflows, foundational feature
- **MEDIUM**: Enhances existing features, important workflow improvement, extends core functionality
- **LOW**: Polish, utilities, optional improvements, non-blocking features

## Hour Estimation Rules

Apply these guidelines:

- **2-4h**: Simple single-function features (basic retrieval, display, validation)
- **4-8h**: Medium complexity (API integration, data processing, moderate UI)
- **8-16h**: Complex features (state management, multi-step workflows, system integration)
- Maximum 16h per increment (break larger work into smaller increments)

## Output

Display completion summary:

- File path where backlog was created/updated
- Total increments generated
- Aggregated hours and impact distribution
- Validation status
