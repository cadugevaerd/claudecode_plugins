---
name: composio-auth
description: Get authentication setup guide for a specific app or service in Composio
argument-hint: "<app_name>"
allowed-tools:
  - WebFetch
  - WebSearch
---

# Composio Authentication Guide

Get detailed authentication setup instructions for a specific app or service.

## Instructions

1. **Identify the App**: Parse the app name from user input
2. **Fetch Auth Documentation**: Get authentication details
3. **Provide Setup Guide**: Step-by-step instructions

## Documentation Sources

> **IMPORTANT**: The `docs.composio.dev` site blocks automated requests. Use alternatives:

### Primary Sources (GitHub)
- **Main README**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md`
- **Python SDK**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/python/README.md`
- **SDK Guide**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/CLAUDE.md`

### Search Strategy
- Use WebSearch: `Composio authentication <app> site:docs.composio.dev`
- Use GitHub API: `https://api.github.com/repos/ComposioHQ/composio/contents/`

## Auth Types in Composio

1. **OAuth 2.0**: GitHub, Google, Slack, etc.
2. **API Key**: Simple key-based auth
3. **Basic Auth**: Username/password
4. **Custom**: Custom authentication flows

## Response Format

Provide:

### 1. Auth Type
Identify which auth type the app uses (OAuth, API Key, etc.)

### 2. Setup Steps
```python
# Python example
from composio import ComposioToolSet

toolset = ComposioToolSet()

# Initiate connection
connection = toolset.initiate_connection(
    app="<APP_NAME>",
    entity_id="user_123"
)

# Get auth URL for OAuth apps
print(connection.redirect_url)
```

```typescript
// TypeScript example
import { ComposioToolSet } from "@composio/core";

const toolset = new ComposioToolSet();

const connection = await toolset.initiateConnection({
    app: "<APP_NAME>",
    entityId: "user_123"
});

console.log(connection.redirectUrl);
```

### 3. Verification
How to verify the connection is active

### 4. Common Issues
Troubleshooting tips for this specific app

## Example Usage

```
/composio-auth github
/composio-auth slack
/composio-auth gmail
/composio-auth notion
```
