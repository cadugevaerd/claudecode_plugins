---
name: Managed Authentication
description: This skill should be used when the user asks about Composio authentication, OAuth setup, API keys, custom auth configurations, connected accounts, multi-user authentication, or entity management. Trigger on questions like 'how to authenticate with Composio', 'OAuth setup for GitHub', 'API key configuration', 'handle multiple users auth', 'connected accounts management'.
version: 1.0.0
---

# Composio Managed Authentication

Provide comprehensive guidance on Composio's managed authentication system for connecting AI agents to external tools securely.

## When to Use This Skill

Use when user asks about:
- OAuth 2.0 setup for any integration
- API key authentication configuration
- Custom authentication flows
- Multi-user authentication (entity_id)
- Connected accounts management
- Checking connection status
- Authentication troubleshooting

## Core Concepts

### Entity Model

Composio uses **entities** to manage user-specific connections:

```python
from composio import ComposioToolSet

toolset = ComposioToolSet()

# Each user gets unique entity_id
entity = toolset.get_entity(id="user_123")

# Get user's connected accounts
connections = entity.get_connections()
```

### Authentication Types

1. **OAuth 2.0**: Most common, used by GitHub, Google, Slack, etc.
2. **API Key**: Simple key-based, used by OpenAI, Anthropic, etc.
3. **Basic Auth**: Username/password combination
4. **Bearer Token**: Token-based authentication
5. **Custom**: Define custom auth parameters

## Implementation Patterns

### Initiating OAuth Connection

```python
from composio import ComposioToolSet

toolset = ComposioToolSet()

# Start OAuth flow
connection_request = toolset.initiate_connection(
    app="github",
    entity_id="user_123",
    redirect_url="https://yourapp.com/callback"  # Optional
)

# User visits this URL to authorize
print(f"Auth URL: {connection_request.redirect_url}")

# Wait for completion (or poll)
connection = connection_request.wait_until_active(timeout=300)
```

```typescript
import { ComposioToolSet } from "@composio/core";

const toolset = new ComposioToolSet();

const connectionRequest = await toolset.initiateConnection({
    app: "github",
    entityId: "user_123",
    redirectUrl: "https://yourapp.com/callback"
});

console.log(`Auth URL: ${connectionRequest.redirectUrl}`);

const connection = await connectionRequest.waitUntilActive({ timeout: 300 });
```

### Checking Connection Status

```python
# Check if user has active connection
entity = toolset.get_entity(id="user_123")

try:
    connection = entity.get_connection(app="github")
    print("Connected!")
except Exception:
    print("Not connected, initiate auth flow")
```

### API Key Authentication

```python
# For apps that use API keys
connection = toolset.initiate_connection(
    app="openai",
    entity_id="user_123",
    auth_config={
        "api_key": "sk-..."
    }
)
```

### Custom Auth Configuration

```python
# Define custom auth parameters
connection = toolset.initiate_connection(
    app="custom_app",
    entity_id="user_123",
    auth_config={
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "scope": ["read", "write"]
    }
)
```

## Best Practices

1. **Always use entity_id**: Never share connections between users
2. **Handle auth expiry**: OAuth tokens expire, handle refresh
3. **Check before using**: Verify connection is active before tool calls
4. **Secure storage**: Never log or expose auth tokens
5. **Graceful fallback**: Provide auth URL when not connected

## Common Patterns

### Auth Check Middleware

```python
def ensure_authenticated(entity_id: str, app: str):
    """Ensure user is authenticated before tool use"""
    entity = toolset.get_entity(id=entity_id)

    try:
        connection = entity.get_connection(app=app)
        if connection.status == "active":
            return True
    except Exception:
        pass

    # Initiate new connection
    request = toolset.initiate_connection(
        app=app,
        entity_id=entity_id
    )
    return request.redirect_url
```

### Multi-App Authentication

```python
# Connect to multiple apps for same user
apps = ["github", "slack", "gmail"]

for app in apps:
    request = toolset.initiate_connection(
        app=app,
        entity_id="user_123"
    )
    print(f"{app}: {request.redirect_url}")
```

## Documentation Sources

> **Note**: Use GitHub sources as `docs.composio.dev` may block automated requests.

### Primary Sources (GitHub - Always Works)
- **README**: https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md
- **Python SDK**: https://raw.githubusercontent.com/ComposioHQ/composio/master/python/README.md
- **SDK Guide**: https://raw.githubusercontent.com/ComposioHQ/composio/master/CLAUDE.md

### Search for Specific Docs
Use WebSearch: `Composio authentication site:docs.composio.dev`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| OAuth redirect fails | Check redirect_url matches app config |
| Token expired | Re-initiate connection flow |
| Invalid scope | Verify required scopes in app settings |
| Connection not found | Use correct entity_id |

Fetch latest documentation with WebFetch if implementation details have changed.
