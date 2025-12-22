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

## Documentation Structure

Base URL: `https://docs.composio.dev/`

### Main Sections
- `/docs/welcome` - Overview
- `/docs/quickstart` - Getting started
- `/docs/managed-authentication` - Auth patterns
- `/docs/tools` - 500+ toolkits
- `/docs/mcp-overview` - MCP servers
- `/docs/triggers` - Events and webhooks
- `/docs/python-sdk` - Python SDK
- `/docs/typescript-sdk` - TypeScript SDK

### Search Strategy

1. First, try to match the query to a known documentation page
2. Use WebFetch to retrieve the relevant page
3. If no direct match, use WebSearch with query: `site:docs.composio.dev <user_query>`
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
