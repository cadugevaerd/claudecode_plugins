---
name: composio-mcp
description: Setup guide for Composio MCP servers with Claude Desktop or other MCP clients
allowed-tools:
  - WebFetch
  - WebSearch
---

# Composio MCP Server Setup

Get instructions to set up Composio MCP servers for use with Claude Desktop, Cursor, or other MCP clients.

## Instructions

1. **Explain MCP Concept**: What MCP is and why use Composio's MCP
2. **Fetch Documentation**: Get latest MCP setup guide
3. **Provide Configuration**: Show exact config for the user's client

## Documentation Sources

> **IMPORTANT**: The `docs.composio.dev` site blocks automated requests. Use alternatives:

### Primary Sources (GitHub)
- **Main README**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md`
- **SDK Guide**: `https://raw.githubusercontent.com/ComposioHQ/composio/master/CLAUDE.md`

### Search Strategy
- Use WebSearch: `Composio MCP setup site:docs.composio.dev`
- Use GitHub API: `https://api.github.com/repos/ComposioHQ/composio/contents/`

## What is Composio MCP?

Composio MCP (Model Context Protocol) servers expose all 500+ Composio tools through a standardized protocol. This allows:

- **Claude Desktop**: Use Composio tools directly in Claude
- **Cursor**: AI-powered coding with external integrations
- **Custom Clients**: Any MCP-compatible application

## Key Features

1. **Rube MCP**: Single server connecting 500+ apps
2. **Streamable HTTP**: Only transport type supported
3. **Per-User Auth**: Each user authenticates independently
4. **Tool Limiting**: Control which tools are exposed

## Claude Desktop Configuration

Provide the user with:

### 1. Get API Key
```bash
# Install Composio CLI
pip install composio

# Login and get key
composio login
```

### 2. Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent:

```json
{
  "mcpServers": {
    "composio": {
      "command": "npx",
      "args": [
        "-y",
        "@composio/mcp@latest",
        "serve",
        "--apps", "github,slack,gmail"
      ],
      "env": {
        "COMPOSIO_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

### 4. Authenticate Apps
When using a tool for the first time, Claude will prompt for authentication.

## Troubleshooting

- **Tools not appearing**: Restart Claude Desktop
- **Auth failing**: Check API key and app permissions
- **Connection issues**: Verify network access to Composio servers

## Response Format

Provide:
1. Step-by-step setup guide
2. Configuration file content
3. Verification steps
4. Common troubleshooting tips
