---
description: Manage LangGraph node development tasks tracking progress and state across nodes
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: '[create|view|finalize]'
model: claude-sonnet-4-5
---

# Manage LangGraph Node Development Backlog

Track and manage task completion for developing individual LangGraph nodes with structured testing, debugging, and evaluation workflows.

## Prerequisites

1. `ARQUITECTURE.md` exists with complete LangGraph node definition (from `/create-arquitecture`)
1. Node structure documented: nodes, edges, state schema, flow diagram

## Create Node Development Backlog

1. **Validate or Create BACKLOG.md**

   - Check if `BACKLOG.md` exists
   - If not: Create with template and current node
   - If exists: Load and analyze current state

1. **Analyze ARQUITECTURE.md**

   - Read node definitions from `ARQUITECTURE.md`
   - Extract nodes from "🏗️ Nodes Esperados" section
   - Determine order: Start with entry nodes (START → first_node)
   - Identify next node to develop (not yet started)

1. **Generate Node Development Tasks**

   - For the current/next node, create 4-phase task structure:
     - **Phase 1: Implementation** - Create Node, Edges, Reducers
     - **Phase 2: Debug** - Visual debugging with LangSmith 🔍
     - **Phase 3: Testing** - Validation tests + Coverage ✅
     - **Phase 4: Evaluation** - Evals and Prompt/Model Engineering

1. **Generate BACKLOG.md**

   - Track current node in development
   - List all tasks for current node
   - Show progress indicator
   - Document completed nodes

## BACKLOG.md Template

```markdown
# Node Development Backlog

**Projeto**: [Agent Name from ARQUITECTURE.md]
**Data Criação**: [Date]
**Último Update**: [Date]

## 🎯 Current Node Development

### Node: `[node-name]`

**Responsabilidade**: [From ARQUITECTURE.md]
**Input**: [State keys read]
**Output**: [State keys written]
**Status**: 🔄 Em Desenvolvimento

#### Phase 1: Implementation ⚙️
- [ ] Create node function with proper type hints
- [ ] Implement node logic based on ARQUITECTURE spec
- [ ] Define edges (incoming and outgoing)
- [ ] Update state schema if new fields needed
- [ ] Add reducers for accumulated fields
- [ ] Integration test node in isolation

**Estimated Time**: 1.5h
**Progress**: X/6 tasks complete

#### Phase 2: Debug 🔍
- [ ] Configure LangSmith observability
- [ ] Run node with sample inputs
- [ ] Visualize state flow in LangSmith
- [ ] Validate edge routing logic
- [ ] Check state mutations (no side effects)
- [ ] Document debug findings

**Estimated Time**: 1h
**Progress**: X/6 tasks complete

#### Phase 3: Testing ✅
- [ ] Write unit tests (happy path + edge cases)
- [ ] Test state input validation
- [ ] Test output formatting
- [ ] Validate edge conditions
- [ ] Achieve 80%+ coverage for node module
- [ ] All tests passing

**Estimated Time**: 1h
**Progress**: X/6 tasks complete

#### Phase 4: Evaluation 📊
- [ ] Create evaluation dataset (5-10 examples)
- [ ] Run LangSmith evals on node outputs
- [ ] Assess prompt quality (if LLM node)
- [ ] Test model performance if applicable
- [ ] Document evaluation results
- [ ] Iterate on prompt/model if needed

**Estimated Time**: 1h
**Progress**: X/6 tasks complete

---

## ✅ Completed Nodes

### Node: `[previous-node-name]`
- **Status**: ✅ Concluído
- **Completed**: [Date]
- **Total Time**: Xh

### Node: `[previous-node-name-2]`
- **Status**: ✅ Concluído
- **Completed**: [Date]
- **Total Time**: Xh

---

## 📊 Progress Summary

- **Total Nodes**: [X nodes from ARQUITECTURE.md]
- **Nodes Completed**: [X]
- **Nodes In Progress**: 1 (`[current-node]`)
- **Nodes Pending**: [X]
- **Estimated Time Remaining**: Xh
- **Overall Progress**: X%

## 📋 Node Sequence

[Based on ARQUITECTURE.md flow, list order of nodes to develop]

1. `node-name` - [Responsabilidade]
2. `node-name-2` - [Responsabilidade]
3. `node-name-3` - [Responsabilidade]
```

## View Backlog Status

1. Read `BACKLOG.md` from current directory
1. Display:
   - Current node in development
   - Tasks completed/remaining for current node
   - Progress bars for each phase
   - List of completed nodes
   - Next node to develop
   - Estimated time remaining
1. Flag any tasks with issues or blockers

## Finalize Node

When all 4 phases completed for a node:

1. Mark current node as ✅ Concluído
1. Identify next node from BACKLOG.md sequence
1. Create new BACKLOG.md section for next node
1. Update progress summary
1. Report completion with metrics

Usage: `/backlog finalize`

## Node Development Task Rules

Each node must complete ALL 4 phases before finalization:

### Phase 1: Implementation (1.5h)

- Node function implements ARQUITECTURE spec exactly
- Proper type hints on inputs/outputs
- Edges correctly routed (incoming + outgoing)
- State schema supports new fields with reducers
- Passes isolated unit test

### Phase 2: Debug (1h)

- LangSmith integration configured
- Sample inputs tested end-to-end
- State mutations visible and correct
- Edge routing verified
- All outputs formatted correctly

### Phase 3: Testing (1h)

- Unit tests cover happy path + 3+ edge cases
- Input validation tested
- Output validation tested
- Edge conditions verified
- Coverage ≥ 80% for node code

### Phase 4: Evaluation (1h)

- Evaluation dataset created (5-10 examples)
- LangSmith evals run and documented
- If LLM node: prompt quality assessed
- If tool node: output correctness verified
- Results documented and acceptable

## Task Completion Criteria

Each task must satisfy:

- ✅ Code is implemented and working
- ✅ Tests passing (where applicable)
- ✅ No console errors or warnings
- ✅ Type hints complete
- ✅ Documentation clear
- ✅ Changes follow project conventions
- ✅ No breaking changes to existing nodes

## Time Tracking

Per node estimated breakdown:

- Phase 1 (Implementation): 1.5h
- Phase 2 (Debug): 1h
- Phase 3 (Testing): 1h
- Phase 4 (Evaluation): 1h
- **Total per node**: ~4.5h

Adjust based on node complexity:

- Simple utility nodes: 3-4h
- LLM nodes: 5-6h
- Complex conditional nodes: 4-5h
