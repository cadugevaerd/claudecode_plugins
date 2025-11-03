---
description: Generate agent spike implementation plan (SPIKE.md) with suggested code structure, file organization, and agentic loop architecture based on Brief Minimo specification
allowed-tools: Read, Write, Bash(mkdir:*)
---

# Microprocesso 1.3: Spike Agentic

Generate SPIKE.md with comprehensive implementation plan including file structure, code organization, and agentic loop architecture (3-4 hours).

## Prerequisites

- README.md exists in project root with Brief Minimo specification (from `/brief`)
- Virtual environment configured (from `/setup-local-observability`)
- Dependencies installed: langchain, langgraph, langsmith

## What This Command Generates

Creates `docs/SPIKE.md` containing:

- Project context extracted from README.md
- Suggested Python file structure and organization
- Code organization patterns for LangGraph agent
- Agentic loop architecture explanation
- Mock tool implementation guidelines
- Test structure recommendations
- LangSmith integration setup
- Implementation timeline (breakdown by phase)

## Execution Steps

1. Read README.md from project root to extract Brief Minimo data
2. Parse agent name, purpose, tools, and success criteria
3. Create docs directory if it does not exist
4. Generate SPIKE.md with:
   - Overview section with agent specification
   - Suggested directory structure
   - Core components (State, Nodes, Graph, Tools)
   - Agentic loop pattern with diagram
   - File creation checklist
   - Phase-by-phase implementation plan
   - LangSmith validation steps

## SPIKE.md Contents

### Section 1: Agent Context

- Agent name and purpose (from README.md)
- Input/output specifications
- Success criteria

### Section 2: Directory Structure

- Recommended Python package layout
- Core module files to create
- Test directory structure

### Section 3: Implementation Plan

- Phase 1: Build graph skeleton (30 min)
- Phase 2: Implement state and nodes (45 min)
- Phase 3: Create mock tools and route logic (30 min)
- Phase 4: Write validation tests (30 min)
- Phase 5: LangSmith setup and trace verification (30 min)

### Section 4: Code Patterns

- TypedDict state definition template
- Node function signatures
- Graph compilation pattern
- Loop validation checklist

## Next Steps

After generation, open `docs/SPIKE.md` and follow the implementation plan phase by phase using suggested code structure and file organization.