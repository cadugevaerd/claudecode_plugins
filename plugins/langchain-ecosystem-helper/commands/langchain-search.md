---
description: Search LangChain, LangGraph, and LangSmith documentation for specific topics, APIs, or examples
arguments:
  - name: query
    description: The search query (e.g., "create_react_agent", "LCEL", "LangSmith tracing")
    required: true
allowed_tools:
  - mcp__langchain-docs__SearchDocsByLangChain
  - WebSearch
  - WebFetch
---

# LangChain Documentation Search

Search across the LangChain ecosystem documentation to find relevant information about:

- **LangGraph**: Agents, state management, checkpointing, multi-agent
- **LangChain**: LCEL, chains, prompts, retrievers, embeddings
- **LangSmith**: Tracing, evaluation, datasets, prompts

## Instructions

1. Use the MCP tool `SearchDocsByLangChain` to search the official documentation
2. If the MCP doesn't return sufficient results, use WebSearch to find additional resources
3. Present the results with:
   - Clear explanation of the topic
   - Code examples when available
   - Links to official documentation
   - Related topics to explore

## Search Query

**Query**: $ARGUMENTS.query

## Response Format

### [Topic] - Search Results

**Overview**:
[Brief explanation of what was found]

**Key Information**:
[Relevant details from documentation]

**Code Example** (if applicable):
```python
# Example code
```

**Documentation Links**:
- [Link 1](url)
- [Link 2](url)

**Related Topics**:
- Topic 1
- Topic 2
