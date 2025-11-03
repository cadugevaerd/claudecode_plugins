---
name: spike-agentic
description: Microprocesso 1.3 - Implement agent spike with agentic loop validation (3-4h). Validates architecture viability, creates graph with state, 4 nodes, loop agêntico. Guides through setup validation, graph construction (State/Nodes/Edges), 2 happy-path tests (with/without tool), LangSmith observability. Use when building agent with agentic loop (Pensar→Agir→Observar→Pensar), need architecture validation, or implementing LangGraph with tool calling.
allowed-tools: Read, Grep, Glob, Write, Bash
---

name: spike-agentic
description: Microprocesso 1.3 - Implement agent spike with agentic loop validation (3-4h). Validates architecture viability, creates graph with state, 4 nodes, loop agêntico. Guides through setup validation, graph construction (State/Nodes/Edges), 2 happy-path tests (with/without tool), LangSmith observability. Use when building agent with agentic loop (Pensar→Agir→Observar→Pensar), need architecture validation, or implementing LangGraph with tool calling.
allowed-tools: Read, Grep, Glob, Write, Bash

# Microprocesso 1.3: Spike Agentic

**Validation spike for agentic architecture with loop agêntico (Think→Act→Observe→Think again)**

This skill provides complete guidance for implementing the first agent spike following Brief Minimo methodology.

## What is a Spike

**Spike = Time-boxed exploration (3-4 hours)**

- ✅ Validates architecture viability
- ✅ Focuses on happy path + agentic loop
- ✅ Uses mock tools (no real APIs)
- ✅ Runs 2 tests only (with/without tool)
- ❌ No extensive error handling
- ❌ No production-ready code
- ❌ No edge cases

**Question answered:** "Is the agentic architecture viable?"

## How the Command Works

When user runs `/spike-agentic`:

1. **Validate Prerequisites** (1 min)

   - Check venv exists
   - Check deps installed (langchain, langgraph, etc)
   - Check .env configured with API key
   - Check README.md from `/brief`

1. **If validation fails:**

   - Tell user what's missing
   - Suggest `/setup-local-observability` or `/brief`
   - Exit

1. **If validation passes:**

   - **Generate** `docs/microprocesso-1.3-spike-agentic.md`
   - File contains 4 phases with all code, tests, validation steps
   - User follows guide to implement

**Skill's Role:**

- Provide complete knowledge for generation
- Validate inputs
- Guide implementation if user asks for help

## Pre-requisites (Microprocesso 1.2 Must Be Complete)

Before running `/spike-agentic`, validate:

````text

✅ venv/ exists (Python virtual environment)
✅ requirements.txt installed (langchain, langgraph, etc)
✅ .env configured (LLM API Key present)
✅ .gitignore protects secrets

```text

**If missing:** Run `/setup-local-observability` first


## The Agentic Loop: Critical Differentiator

### Without Loop (ROUTER):

```text

INPUT → AGENT_NODE (decide) → TOOL_NODE (execute) → OUTPUT_NODE (format) → END

```text

Problem: LLM decides and executes, **but never observes result**

### With Loop (TRUE AGENT):

```text

INPUT → AGENT_NODE (think) → TOOL_NODE (execute) → AGENT_NODE (think AGAIN) → OUTPUT_NODE → END
                                                           ↑
                                                    LOOP: Back to AGENT_NODE

```text

Benefit: LLM observes tool result and formulates coherent natural language response


## 4 Phases (3-4 Hours Total)

### PHASE 1: Setup ✅ ALREADY DONE
Via `/setup-local-observability`:
- Virtual environment
- Dependencies installed
- .env configured
- Structure ready

### PHASE 2: Graph Construction (60-90 min) ← START HERE
Build LangGraph with agentic loop

**State Definition:**

```python
class AgentState(TypedDict):
    input_text: str              # User input
    tool_name: str | None        # Which tool LLM decided to use
    tool_input: str | None       # Parameters for tool
    tool_result: str | None      # Tool result after execution
    agent_response: str | None   # Final response after observing result
    final_output: str            # Output to return to user

```text

**4 Nodes:**

1. **INPUT_NODE** - Receive and validate
   - Store user input in state
   - Pass to AGENT_NODE

2. **AGENT_NODE** - LLM thinks and decides
   - **1st execution:** See input + tool schema → Decide: use tool or respond?
   - **2nd execution:** See input + tool_result → Formulate final response
   - Pass to: TOOL_NODE (if decided tool) or END (if responding directly)

3. **TOOL_NODE** - Execute mock tool
   - Call `mock_search_tool(query)`
   - Store result in state
   - **Always goes back to AGENT_NODE** ← LOOP MAGIC

4. **OUTPUT_NODE** - Format output
   - Use agent_response
   - Store in final_output

**Edges & Conditional Logic:**

```text

START → INPUT_NODE → AGENT_NODE → (route_logic) → TOOL_NODE or OUTPUT_NODE
                         ↑                              ↓
                         └──────────────────────────────┘
                           (LOOP: Back to AGENT_NODE)

```text

**Route Function (THE ONLY DECISION):**

```python
def route_logic(state) -> str:
    if state["tool_name"]:
        return "call_tool"        # Go to TOOL_NODE
    else:
        return "format_output"    # Go to OUTPUT_NODE

```text

Why this works:
- ✅ Single decision point (after AGENT_NODE)
- ✅ TOOL_NODE always loops back (no conditional needed)
- ✅ Simple and guaranteed

**Mock Tool Example:**

```python
def mock_search_tool(query: str) -> str:
    """Mock tool - returns hardcoded response"""
    responses = {
        "Python": "Python is a versatile language created in 1991...",
        "AI": "Artificial Intelligence is the field of...",
    }
    return responses.get(query, "Not found in mock")

```text

Why mock? Your uncertainty is about LangGraph + LLM decision making, not API connectivity.

### PHASE 3: Testing (30 min)
Run 2 happy-path tests only

**Test 1: WITH Tool**
- Input: "Search for Python"
- Expected: AGENT_NODE executes 2x (loop), tool_result filled, response natural

**Test 2: WITHOUT Tool**
- Input: "Hi, how are you?"
- Expected: AGENT_NODE executes 1x (no loop), tool skipped, response natural

**Validation Script:**

```bash
python run_spike.py test1  # With tool
python run_spike.py test2  # Without tool

```text

### PHASE 4: LangSmith Validation (30 min)
Verify observability and agentic loop

**Dashboard checklist:**
- ✅ 2 runs appear in LangSmith
- ✅ Test 1 tree: INPUT → AGENT (1st) → TOOL → AGENT (2nd) ← PROVES LOOP
- ✅ Test 2 tree: INPUT → AGENT (1st) → OUTPUT (no loop, tool skipped)

**Difference proves loop works!**


## Success Criteria

| Criterion | Status | Description |
|:----------|:-------|:-----------|
| ✅ Prerequisites validated | REQUIRED | venv, deps, .env ready |
| ✅ Graph compiles | REQUIRED | No compilation errors |
| ✅ Test 1 passes (with tool) | REQUIRED | Input triggers tool correctly |
| ✅ Test 2 passes (without tool) | REQUIRED | Input skips tool correctly |
| ✅ Agentic loop works | REQUIRED | AGENT_NODE executes 2x in test 1 |
| ✅ Traces in LangSmith | REQUIRED | Both runs visible with node tree |
| ❌ Error handling | NOT APPLICABLE | Leave for Microprocesso 1.4 |
| ❌ Structured JSON | NOT APPLICABLE | Leave for Microprocesso 1.4 |
| ❌ Edge cases | NOT APPLICABLE | Leave for Microprocesso 1.4 |


## Red Flags (Spike Failed)

- ⏰ **"I'm at 2.5 hours still in PHASE 2"** → Spike failed, capture uncertainties
- 🔴 **"LLM can't decide to use tool correctly"** → Uncertainty resolved (LLM choice may be wrong)
- 📡 **"LangSmith shows nothing"** → Observability needs adjustment
- 🔄 **"Loop doesn't work (AGENT_NODE executes 1x)"** → Check route_logic and edges


## After Spike

### If Validated ✅
→ **Microprocesso 1.4 (Robustness)**
- Add error handling
- Use real tool
- Create 10+ varied tests
- Structured JSON output
- Pytest automation

### If Invalidated ❌
→ **Refine Spike**
- Try different LLM
- Adjust prompts/schemas
- Consider alternative architecture
- Retest


## Why This Approach Works

| Aspect | Before (2h Unrealistic) | After (3-4h Realistic) |
|:-------|:----------------------|:----------------------|
| Expectations | ❌ Unrealistic | ✅ Achievable |
| Focus | ❌ Mixed | ✅ Clear (viability) |
| Failure risk | ❌ High | ✅ Low |
| Uncertainty | ❌ Partial | ✅ Complete |
| Happy path % | ❌ 30% | ✅ 80% |


## Key Concepts

**State = The Warehouse**
All data flowing through the graph lives in State. Each node reads from and writes to State.

**Nodes = Workers**
INPUT_NODE receives, AGENT_NODE decides, TOOL_NODE executes, OUTPUT_NODE formats.

**Edges = Connections**
Routes between nodes. Some are conditional (via route_logic), some always happen (TOOL_NODE → AGENT_NODE).

**Loop Agêntico = The Magic**
TOOL_NODE → AGENT_NODE creates loop. Without it: router. With it: true agent.

**Mock Tool = No Variables**
Removes network/API uncertainty. If test fails, it's about LangGraph + LLM, not external services.


## Integration with Brief Minimo

This spike validates the Brief Minimo specification you created with `/brief`:

- **Question 1** (What does it DO?): Agents' core functionality
- **Question 2-3** (INPUT/OUTPUT): State structure and response format
- **Question 4** (TOOL/API): Mock tool in TOOL_NODE
- **Question 5** (SUCCESS): Success criteria (loop works, tests pass)

Spike implementation directly follows your brief specification.


**This is Microprocesso 1.3. Next is Microprocesso 1.4 (Robustness).**
````
