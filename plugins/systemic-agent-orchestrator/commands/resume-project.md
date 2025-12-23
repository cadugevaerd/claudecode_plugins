---
description: Resume work on an existing agent project - load context from Serena memories and continue development
argument-hint: "[project-path]"
allowed-tools:
  - mcp__plugin_serena_serena__read_file
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__search_for_pattern
  - mcp__plugin_serena_serena__read_memory
  - mcp__plugin_serena_serena__list_memories
  - mcp__plugin_serena_serena__check_onboarding_performed
  - AskUserQuestion
---

# Resume Project - Continue Development on Existing Agent

**PURPOSE**: Quickly resume development on an existing agent project by loading all context from Serena memories and analyzing current state.

## Arguments

- `project-path`: Optional. Path to agent project (default: current directory)

---

## Phase 1: Load Project Context

### 1.1 Verify Serena Onboarding

```
1. Call check_onboarding_performed
2. If NOT performed:
   - Redirect user to run /discovery first
   - EXIT
```

### 1.2 Load Existing Memories

```
1. Call list_memories to see all project memories
2. Read essential memories:
   - agent_overview (if exists)
   - arch_agent_design (if exists)
   - Any api_* memories for integrations
   - Any progress_* memories for feature status
3. Build context summary from memories
```

### 1.3 Analyze Current Project State

```
1. List project structure using list_dir recursive=true
2. Identify implemented components:
   - Count nodes in src/nodes/
   - Check models.yaml for configured nodes
   - Review graph.py for workflow structure
   - Check test coverage status
3. Identify work in progress:
   - Look for TODO comments in code
   - Check for incomplete implementations
   - Find test files without full coverage
```

---

## Phase 2: Generate Status Report

Present to user:

```
=== Project Resume - {project_name} ===

📋 FROM MEMORIES:
Agent Purpose: {from agent_overview}
Architecture: {from arch_agent_design}
Integrations: {list of api_* memories}

📊 CURRENT IMPLEMENTATION STATUS:

Nodes Implemented: {count}
  ✅ planner - LLM routing node
  ✅ executor - Action execution
  🚧 reviewer - Needs tests

Models Configured: {count}/{expected}
  ✅ planner: anthropic:claude-3-5-sonnet-20241022
  ✅ executor: anthropic:claude-3-5-sonnet-20241022
  ⚠️ reviewer: Missing in models.yaml

Tests:
  Coverage: {percentage}%
  Passing: {pass_count}/{total}

🔍 DETECTED ISSUES:
  - {issue_1}
  - {issue_2}

📝 WORK IN PROGRESS:
  - {from progress_* memories}
  - {from TODO comments}

=== Ready to Continue ===
```

---

## Phase 3: Suggest Next Actions

Based on analysis, suggest appropriate next steps:

### If Missing Configurations:
```
Recommended: Fix configuration issues first
1. Run /validate-stack to see all issues
2. Add missing entries to models.yaml
3. Create Langsmith prompts if missing
```

### If Incomplete Nodes:
```
Recommended: Complete in-progress work
1. Finish implementing {node_name}
2. Add tests for {node_name}
3. Update graph.py with proper edges
```

### If Ready for New Features:
```
Recommended: Continue development
1. Use /add-node to implement next feature
2. Run tests after each addition
3. Update memories with progress
```

### If Ready for Deployment:
```
Recommended: Prepare for deployment
1. Run /validate-stack for final check
2. Review Terraform configurations
3. Check CI/CD pipeline
```

---

## Phase 4: Ask User Intent

Ask user what they want to do:

**Question**: "What would you like to work on?"

Options:
- Fix detected issues first
- Continue implementing {next_incomplete_node}
- Add a new node/feature
- Review and improve existing code
- Prepare for deployment
- Run validation checks

---

## Context Preservation

After resuming, ensure context is maintained:

1. **Active Memory**: Keep key memories loaded in context
2. **Progress Tracking**: Update progress_* memories as work continues
3. **Issue Tracking**: Document any new issues found

---

## DO NOT

- Start coding without loading project context
- Ignore existing memories
- Skip validation of current state
- Assume project structure without checking

## Success Criteria

Resume is complete when:
- [ ] All relevant memories loaded
- [ ] Current implementation status understood
- [ ] Issues and gaps identified
- [ ] User has clear next action
