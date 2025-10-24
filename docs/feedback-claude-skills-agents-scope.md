# Feedback: Documentation Gap - Skills and Agents Interaction Scope

**Date**: 2025-10-24
**Topic**: Claude Code Plugins - Skills and Agents Interaction
**Documentation URLs Reviewed**:
- https://docs.claude.com/en/docs/claude-code/skills
- https://docs.claude.com/en/docs/claude-code/sub-agents
- https://docs.claude.com/en/docs/claude-code/plugins-reference
- https://docs.claude.com/en/api/agent-sdk/skills
- https://docs.claude.com/en/api/agent-sdk/subagents

---

## Summary

The current Claude Code documentation does not explicitly specify whether **agents/subagents have automatic access to Skills** installed in the system or within the same plugin. This creates uncertainty when designing plugin architectures that combine both components.

---

## Current Documentation State

### What IS Documented ✅

1. **Skills are model-invoked**:
   > "Skills are model-invoked—Claude autonomously decides when to use them based on your request and the Skill's description."

2. **Skills are auto-discovered from plugins**:
   > "Plugin Skills are automatically discovered when the plugin is installed."

3. **Agents/Subagents inherit tools by default**:
   > "If omitted, [subagents] inherit all tools from the main thread."

4. **Components are treated as parallel**:
   > Documentation presents Commands, Agents, and Skills as independent components invoked by task context.

### What Is NOT Documented ❌

1. **Whether agents/subagents running in isolated context have access to installed Skills**
2. **Whether Skills are treated as "tools" that agents can inherit**
3. **The scope hierarchy between Skills and Agents within plugins**
4. **Whether agents need explicit configuration to use Skills**
5. **Whether Skills auto-invoke when an agent is the execution context (not main thread)**

---

## Real-World Use Case

### Scenario: LangChain Testing Plugin

We created a plugin (`python-test-generator`) with:
- **Agent**: `test-assistant` - Generates Python unit tests
- **Skill**: `langchain-test-specialist` - Advanced LangChain/LangGraph testing patterns

### Questions We Cannot Answer from Documentation:

1. When `test-assistant` agent is invoked to test LangChain code, will Claude **automatically invoke** the `langchain-test-specialist` skill?

2. Does the agent need to:
   - **Option A**: Do nothing - Skills auto-invoke regardless of execution context?
   - **Option B**: Explicitly reference the skill in its prompt?
   - **Option C**: Include "Skill" in its `allowed-tools` array?

3. If the agent has a separate context window, does it inherit the global skill registry?

### Current Workaround

We're maintaining **redundant knowledge**:
- Agent has basic LangChain mock patterns
- Skill has advanced patterns (agentevals, VCR recording, etc.)

This is inefficient and leads to:
- Duplication of documentation
- Larger context consumption
- Maintenance burden (update two locations)
- Unclear single source of truth

---

## Documentation Improvement Suggestions

### 1. Add Explicit Section: "Skills and Agents Interaction"

**Location**: `/docs/claude-code/skills` or `/docs/claude-code/plugins-reference`

**Suggested Content**:

```markdown
## Skills and Agents Interaction

### When Agents Invoke Skills

Agents and subagents can automatically use Skills based on the following rules:

- **Main thread agents**: [YES/NO] - Skills are auto-invoked when agent runs in main context
- **Isolated subagents**: [YES/NO] - Skills are auto-invoked when agent has separate context window
- **Plugin-local scope**: Skills within the same plugin [ARE/ARE NOT] automatically available to agents in that plugin
- **Cross-plugin scope**: Skills from other plugins [ARE/ARE NOT] available to agents

### Configuration Requirements

To enable Skills for agents:
- [If needed] Add "Skill" to agent's `allowed-tools` array
- [If needed] Explicitly reference skill name in agent prompt
- [If automatic] No configuration needed - Skills auto-invoke based on context

### Example

[Provide concrete example of agent + skill interaction]
```

### 2. Update Agent SDK Documentation

**Location**: `/api/agent-sdk/subagents`

**Add**:
- Section on whether `allowed_tools` should include "Skill"
- Example of subagent configuration that can use Skills
- Clarify if Skills are inherited like other tools

### 3. Add to Plugins Reference

**Location**: `/docs/claude-code/plugins-reference`

**Add Table**:

| Component | Auto-Discovered | Auto-Invoked | Scope | Access to Other Components |
|-----------|-----------------|--------------|-------|----------------------------|
| Commands  | Yes             | No (user)    | Plugin | Can invoke agents |
| Agents    | Yes             | Yes (context)| Plugin | [SPECIFY: Skills access?] |
| Skills    | Yes             | Yes (context)| [Global/Plugin?] | N/A |

---

## Additional Examples Needed

### Example 1: Agent Using Skill (Implicit)
```markdown
# Agent: test-generator.md
---
description: Generates unit tests for Python code
---

[Does this agent automatically benefit from installed test-related Skills?]
```

### Example 2: Agent Using Skill (Explicit)
```markdown
# Agent: test-generator.md
---
description: Generates unit tests for Python code
allowed-tools: [Read, Write, Skill]  # ← Is this needed?
---

When generating tests for LangChain code, use the `langchain-test-specialist` skill.
```

**Documentation should clarify**: Which approach is correct?

---

## Expected Behavior Clarification

Please clarify the expected behavior in these scenarios:

### Scenario A: Main Thread
```
User → /command → Agent runs in main thread
Question: Are Skills auto-invoked?
Expected: [YES/NO]
```

### Scenario B: Isolated Subagent
```
User → /command → Agent with separate context
Question: Are Skills auto-invoked?
Expected: [YES/NO]
```

### Scenario C: Programmatic Agent (SDK)
```
SDK code defines agent with allowed_tools=['Read', 'Write']
Question: Does agent have access to Skills?
Expected: [YES/NO/ONLY IF 'Skill' IN allowed_tools]
```

### Scenario D: Plugin-Local Scope
```
Plugin A has: Agent X + Skill Y
Plugin B has: Agent Z + Skill W
Question: Can Agent X use Skill Y? Can Agent X use Skill W?
Expected: [Plugin-local only / Global scope]
```

---

## Impact

This documentation gap affects:
- **Plugin developers**: Uncertain about architecture decisions
- **Code maintainability**: Duplicating knowledge vs. trusting auto-invocation
- **Performance**: Unnecessary context usage if redundancy is not needed
- **Best practices**: No clear guidance on Skills + Agents design patterns

---

## Suggested Documentation Priority

🔴 **High Priority**:
- Clarify if agents/subagents auto-invoke Skills
- Add concrete examples of agent + skill interaction

🟡 **Medium Priority**:
- Document scope rules (plugin-local vs. global)
- Add decision tree for when to use redundant knowledge

🟢 **Low Priority**:
- Advanced patterns (agents coordinating multiple skills)
- Performance implications of skill auto-invocation in agent context

---

## Contact Information

**GitHub Issue**: [If applicable, create issue in anthropics/anthropic-sdk-python or relevant repo]
**Forum Post**: [If applicable, link to community forum discussion]
**Email**: cadu.gevaerd@gmail.com

---

Thank you for considering this feedback. Claude Code plugins are a powerful feature, and clearer documentation on component interaction will help developers build more effective and maintainable plugins.