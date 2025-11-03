# Generating Microprocesso 1.3 Implementation Guide

This file contains the template and instructions for generating `docs/microprocesso-1.3-spike-agentic.md`

## Generation Process

When `/spike-agentic` is invoked, Claude should:

1. **Validate prerequisites**
   - Check venv exists
   - Check requirements.txt installed
   - Check .env file with API key
   - Check README.md from `/brief`

2. **If validation passes**
   - Create file: `docs/microprocesso-1.3-spike-agentic.md`
   - Use template below
   - Customize based on Brief Minimo if available

3. **If validation fails**
   - Tell user what's missing
   - Suggest running `/setup-local-observability` first

---

## Document Structure

The generated guide should follow this structure:

```
# 🚀 Microprocesso 1.3: Spike Agentic - Implementation Guide

[Header with time, goal, question]

## Phase 1: Validate Prerequisites ✅
- Verify commands and expected outputs
- Check marks for each validation

## Phase 2: Build Graph (60-90 minutes)
### 2.1 - State Definition
- Code snippet for TypedDict
- Explanation of each field

### 2.2 - Mock Tool
- Code snippet
- Why mock?

### 2.3 - 4 Nodes
- INPUT_NODE code
- AGENT_NODE code (detailed with both executions)
- TOOL_NODE code
- OUTPUT_NODE code

### 2.4 - Route Logic
- Single decision function
- Why it works

### 2.5 - Graph Compilation
- All edges including loop
- Compiled agent

## Phase 3: Run Tests (30 minutes)
### 3.1 - Test Script
- Full `run_spike.py` code
- Validations for both tests

### 3.2 - Run Tests
- Bash commands
- Expected output

## Phase 4: LangSmith Validation (30 minutes)
### 4.1 - Access Dashboard
- Steps to check traces

### 4.2 - Inspect Test 1 (WITH TOOL)
- Tree structure with AGENT_NODE 2x

### 4.3 - Inspect Test 2 (WITHOUT TOOL)
- Tree structure with AGENT_NODE 1x

### 4.4 - Validate Difference
- Proof of agentic loop

## Success Criteria
- Table with all criteria

## Red Flags
- Common failures and solutions

## Next Steps
- Microprocesso 1.4 path
- Failed spike path

## Key Concepts
- Definitions of State, Nodes, Edges, Loop Agêntico
```

---

## Content Guidelines

### Tone
- Direct and instructional
- Code-focused (show, don't tell)
- Practical examples from Brief Minimo when available

### Code Quality
- All code snippets are runnable
- Include imports
- Include comments for clarity
- No pseudo-code

### Explanations
- Keep brief (why this matters)
- Use visuals for flows/trees
- Link concepts back to "loop agêntico"

### Customization Points
If README.md from `/brief` exists, extract:
- Agent name (Question 1)
- Input/Output format (Questions 2-3)
- Tool name (Question 4)
- Success metrics (Question 5)

Use these to customize examples in Phase 2/3/4.

---

## File Paths

**Generate this file:**
```
docs/microprocesso-1.3-spike-agentic.md
```

**Reference files the user will create:**
```
src/agent.py          (Main graph - copy from Phase 2.5)
src/mock_tool.py      (Mock tool - copy from Phase 2.2)
run_spike.py          (Test script - copy from Phase 3.1)
```

---

## Validation Checklist

Before considering generation complete:

- ✅ All 4 phases included
- ✅ All code snippets are complete and runnable
- ✅ Phase 2.5 shows complete graph with loop
- ✅ Phase 3 test script is copy-paste ready
- ✅ Phase 4 shows clear tree structures
- ✅ Success criteria clearly listed
- ✅ Next steps are explicit
- ✅ Markdown formatting is correct

---

This guide helps Claude know exactly what to generate when `/spike-agentic` is invoked.
