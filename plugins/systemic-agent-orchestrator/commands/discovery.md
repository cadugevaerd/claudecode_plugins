---
description: Deep context understanding before any code generation - interview user and analyze existing codebase
argument-hint: "[project-path]"
allowed-tools:
  - mcp__plugin_serena_serena__read_file
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__search_for_pattern
  - mcp__plugin_serena_serena__write_memory
  - mcp__plugin_serena_serena__read_memory
  - mcp__plugin_serena_serena__list_memories
  - mcp__plugin_serena_serena__onboarding
  - mcp__plugin_serena_serena__check_onboarding_performed
  - WebSearch
  - AskUserQuestion
---

# Discovery Phase - Deep Context Understanding

**CRITICAL**: This command must be run BEFORE any code generation. It ensures deep understanding of the agent's purpose, constraints, and context.

## Purpose

Execute Phase 1 of the Development Workflow:
1. Analyze existing codebase (if present)
2. Interview user about agent purpose and requirements
3. Document findings in Serena memories
4. Create architectural decision record (ADR)

## Arguments

- `project-path`: Optional. Path to existing project. If empty, starts fresh discovery.

---

## Phase 1: Check Serena Onboarding

First, verify if Serena onboarding was performed:

```
1. Call check_onboarding_performed to see if project was analyzed
2. If NOT performed:
   - Call onboarding to analyze project structure
   - Wait for Serena to auto-generate initial memories about:
     - Project overview and tech stack
     - Coding standards and patterns
     - Development commands
3. Verify .serena/memories/ folder exists
```

---

## Phase 2: Analyze Existing Codebase (if project exists)

If `project-path` is provided or current directory has Python files:

### 2.1 Project Structure Analysis

```
1. List directory structure using list_dir recursive=true
2. Identify key files:
   - main.py (entry point)
   - state.py or similar (state definitions)
   - graph.py (workflow definition)
   - nodes/ directory (node implementations)
   - config/models.yaml (LLM configuration)
   - config/ (other configs)
   - tests/ (test files)
```

### 2.2 State Machine Analysis

```
1. Find AgentState definition using find_symbol("AgentState")
2. Analyze state fields and reducers
3. Document:
   - Current state schema
   - Accumulating vs replacing fields
   - Any custom reducers
```

### 2.3 Workflow Analysis

```
1. Find StateGraph usage using search_for_pattern("StateGraph")
2. Map current nodes and edges
3. Identify:
   - Entry points
   - Conditional routing
   - Exit points
   - Subgraphs (if any)
```

### 2.4 Integration Analysis

```
1. Search for external integrations:
   - API calls (requests, httpx)
   - Database connections (sqlalchemy, asyncpg)
   - AWS services (boto3, langchain_aws)
   - MCP tools
2. Document current integrations
```

---

## Phase 3: User Interview

Ask the user these questions using AskUserQuestion:

### 3.1 Agent Purpose

**Question**: "What is the primary purpose of this AI agent?"

Options:
- Customer service / Support
- Sales / Lead qualification
- Data processing / Analysis
- Content generation
- Workflow automation
- Other (please describe)

### 3.2 User Personas

**Question**: "Who will interact with this agent?"

Options:
- End customers directly
- Internal team members
- Other AI systems (API integration)
- Mixed audience

### 3.3 Conversation Memory Requirements

**Question**: "Does the agent need to remember previous conversations?"

Options:
- Yes, long-term memory required (human-facing)
- Session memory only (within conversation)
- No memory needed (stateless)

### 3.4 Integration Requirements

**Question**: "What external systems need integration?"

Options (multi-select):
- Database (Aurora/PostgreSQL)
- REST APIs
- AWS Services (S3, Lambda, etc.)
- Langsmith (tracing/prompts)
- MCP tools
- Other

### 3.5 Deployment Target

**Question**: "Where will this agent be deployed?"

Options:
- AWS (ECS/Lambda with API Gateway)
- Local development only
- Kubernetes
- LangGraph Cloud

### 3.6 Compliance Requirements

**Question**: "Any compliance or security requirements?"

Options:
- PII handling required
- Audit logging required
- No special requirements

---

## Phase 4: Create Serena Memories

Based on discovery, create memories in `.serena/memories/`:

### 4.1 Agent Overview Memory

```markdown
# Agent Overview - {agent_name}

## Purpose
{user_responses.purpose}

## Target Users
{user_responses.personas}

## Memory Requirements
{user_responses.memory}

## Key Integrations
{user_responses.integrations}

## Deployment
{user_responses.deployment}

## Compliance
{user_responses.compliance}

## Discovered Architecture (if existing project)
{codebase_analysis}
```

Use: `write_memory("agent_overview.md", content)`

### 4.2 Architecture Decision Record (ADR)

```markdown
# ADR: Agent Architecture

## Status
Proposed

## Context
{discovery_context}

## Decision
Use LangGraph Graph API with:
- State: {state_design}
- Nodes: {proposed_nodes}
- Routing: {routing_strategy}

## Consequences
- Pros: {pros}
- Cons: {cons}

## Alternatives Considered
{alternatives}
```

Use: `write_memory("arch_agent_design.md", content)`

---

## Phase 5: Output Summary

Present discovery summary to user:

```
=== Discovery Complete ===

Agent: {agent_name}
Purpose: {purpose_summary}

Key Findings:
- {finding_1}
- {finding_2}
- {finding_3}

Proposed Architecture:
┌──────────────────────────────────────────────┐
│  {architecture_diagram}                       │
└──────────────────────────────────────────────┘

Next Steps:
1. Review and approve architecture in ADR
2. Create prompts in Langsmith
3. Configure models.yaml
4. Run /init-agent or /add-node to implement

Serena Memories Created:
- agent_overview.md
- arch_agent_design.md

To retrieve memories later:
  Use read_memory("agent_overview") or read_memory("arch_agent_design")
```

---

## CLAUDE.md Update

After discovery, add to project's CLAUDE.md:

```markdown
## Project Memories (Serena MCP)

### Agent Design
- `agent_overview` - Agent purpose, users, requirements. Use: `read_memory('agent_overview')`
- `arch_agent_design` - Architecture decisions. Use: `read_memory('arch_agent_design')`
```

---

## DO NOT

- Skip the interview phase
- Generate code before completing discovery
- Assume requirements without asking
- Create prompts locally (must be in Langsmith)
- Configure models without models.yaml

## Success Criteria

Discovery is complete when:
- [ ] Serena onboarding performed (if new project)
- [ ] User interview completed
- [ ] Memories created in .serena/memories/
- [ ] ADR drafted and presented
- [ ] CLAUDE.md updated with memory references
