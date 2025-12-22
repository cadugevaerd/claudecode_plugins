---
name: composio-search
description: Search Composio documentation for a specific topic and get detailed information
argument-hint: "<query>"
allowed-tools:
  - WebFetch
  - WebSearch
---

# Composio Documentation Search

Search the Composio documentation to find information about the user's query.

## Instructions

1. **Understand the Query**: Parse what the user is looking for
2. **Search Documentation**: Use WebFetch to search relevant pages
3. **Provide Summary**: Give a concise, actionable answer

## Documentation Sources

> **IMPORTANT**: The `docs.composio.dev` site blocks automated requests (returns 404). Use these alternatives:

### Primary Sources (GitHub - Always Works)
- **Main README**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md`
- **SDK Guide**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/CLAUDE.md`
- **Python SDK**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/python/README.md`
- **Fern Docs**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/fern/CLAUDE.md`
- **GitHub API**: `https://api.github.com/repos/ComposioHQ/composio/contents/`

### Search Strategy

1. **First**: Use WebSearch with query `Composio <user_query> site:docs.composio.dev` to find relevant pages
2. **Second**: Use WebFetch on GitHub raw URLs for SDK documentation
3. **Third**: Use GitHub API to explore repository structure
4. Summarize findings with code examples if applicable

## Example Usage

```
/composio-search OAuth setup
/composio-search GitHub integration
/composio-search MCP configuration
/composio-search triggers webhooks
```

## Response Format

Provide:
- Direct answer to the query
- Relevant code examples (Python/TypeScript)
- Link to official documentation
- Related topics for further reading
