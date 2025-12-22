---
name: MCP Servers
description: This skill should be used when the user asks about Composio MCP servers, Model Context Protocol integration, Rube server, Claude Desktop configuration, MCP with Cursor/Windsurf, or MCP setup. Trigger on questions like 'Composio MCP setup', 'use Composio with Claude Desktop', 'Rube MCP server', 'MCP configuration', 'connect Composio to Cursor'.
version: 1.0.0
---

# Composio MCP Servers

Provide comprehensive guidance on setting up and using Composio MCP (Model Context Protocol) servers with various AI clients.

## When to Use This Skill

Use when user asks about:
- MCP server setup for Claude Desktop
- Composio integration with Cursor, Windsurf
- Rube MCP server configuration
- MCP tool exposure and control
- Streamable HTTP transport
- Per-user authentication in MCP

## Core Concepts

### What is Composio MCP?

Composio MCP exposes 500+ tools through Model Context Protocol, allowing:
- **Claude Desktop**: Use Composio tools directly
- **Cursor/Windsurf**: AI coding with external integrations
- **Custom MCP Clients**: Any MCP-compatible application

### Key Features

1. **Rube Server**: Single server, 500+ apps
2. **Streamable HTTP**: Only supported transport
3. **Per-User Auth**: Entity-based authentication
4. **Tool Limiting**: Control exposed tools

## Setup Guide

### Prerequisites

```bash
# Install Composio CLI
pip install composio

# Login to get API key
composio login

# Or set API key directly
export COMPOSIO_API_KEY="your-api-key"
```

### Claude Desktop Configuration

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "composio": {
      "command": "npx",
      "args": [
        "-y",
        "@composio/mcp@latest",
        "serve",
        "--apps", "github,slack,gmail,notion"
      ],
      "env": {
        "COMPOSIO_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### Cursor Configuration

Add to Cursor settings:

```json
{
  "mcp": {
    "servers": {
      "composio": {
        "command": "npx",
        "args": ["-y", "@composio/mcp@latest", "serve", "--apps", "github"],
        "env": {
          "COMPOSIO_API_KEY": "<your-api-key>"
        }
      }
    }
  }
}
```

### Windsurf Configuration

Similar to Cursor, add to Windsurf MCP settings.

## Configuration Options

### Limiting Apps

```json
{
  "args": [
    "-y", "@composio/mcp@latest", "serve",
    "--apps", "github,slack"
  ]
}
```

### Limiting Actions

```json
{
  "args": [
    "-y", "@composio/mcp@latest", "serve",
    "--actions", "GITHUB_CREATE_ISSUE,SLACK_SEND_MESSAGE"
  ]
}
```

### Entity ID (Multi-User)

```json
{
  "args": [
    "-y", "@composio/mcp@latest", "serve",
    "--entity-id", "user_123",
    "--apps", "github"
  ]
}
```

## Programmatic MCP Server

### TypeScript Server

```typescript
import { ComposioMCPServer } from "@composio/mcp";

const server = new ComposioMCPServer({
    apiKey: process.env.COMPOSIO_API_KEY,
    apps: ["github", "slack"],
    entityId: "user_123"
});

server.start();
```

### Python Server

```python
from composio_mcp import ComposioMCPServer

server = ComposioMCPServer(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    apps=["github", "slack"],
    entity_id="user_123"
)

server.start()
```

## Authentication Flow

When using MCP with Composio:

1. **First Tool Use**: Claude prompts for authentication
2. **Auth URL**: Click provided link to authorize
3. **Complete OAuth**: Authorize in browser
4. **Tool Ready**: Tool becomes available

```
User: "Create a GitHub issue"
Claude: "I need to authenticate with GitHub first.
        Please visit: https://composio.dev/auth/..."
User: *completes OAuth*
Claude: "Connected! Creating your issue now..."
```

## Best Practices

1. **Minimal Apps**: Only include apps you need
2. **API Key Security**: Use environment variables
3. **Entity Isolation**: Use entity_id for multi-user
4. **Tool Limiting**: Expose only necessary actions
5. **Restart After Config**: Restart client after changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tools not showing | Restart Claude Desktop |
| Auth popup blocked | Check browser popup settings |
| Connection refused | Verify API key is valid |
| npx fails | Install Node.js 18+ |
| Server timeout | Check network/firewall |

### Debug Mode

```json
{
  "args": [
    "-y", "@composio/mcp@latest", "serve",
    "--apps", "github",
    "--debug"
  ]
}
```

### Check Server Status

```bash
# Test MCP server directly
npx -y @composio/mcp@latest serve --apps github --debug
```

## Documentation URLs

- MCP Overview: https://docs.composio.dev/docs/mcp-overview
- MCP Quickstart: https://docs.composio.dev/docs/mcp-quickstart
- Claude Integration: https://docs.composio.dev/mcp/claude
- Provider Integrations: https://docs.composio.dev/docs/mcp-providers

Fetch latest documentation with WebFetch for current MCP setup instructions.
