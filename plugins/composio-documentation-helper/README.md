# Composio Documentation Helper

A comprehensive Claude Code plugin for accessing Composio documentation, providing guidance on AI agent integrations, managed authentication, 500+ toolkits, MCP servers, and event-driven workflows.

## Features

- **Knowledge Agent**: Autonomous expert for Composio questions
- **Documentation Search**: Quick access to official docs
- **Authentication Guides**: OAuth, API keys, multi-user auth
- **Toolkit Explorer**: Browse 500+ integrations
- **MCP Setup**: Claude Desktop and Cursor configuration
- **SDK Integration**: Python and TypeScript examples

## Installation

### Claude Code CLI

```bash
claude mcp add composio-documentation-helper --plugin
```

### Manual Installation

Clone this repository and add the plugin path to your Claude Code configuration.

## Components

### Commands

| Command | Description |
|---------|-------------|
| `/composio-search <query>` | Search Composio documentation |
| `/composio-auth <app>` | Get authentication guide for an app |
| `/composio-tools <toolkit>` | List tools for a toolkit |
| `/composio-mcp` | MCP server setup guide |

### Agent

- **composio-knowledge-agent**: Autonomous expert that answers questions about Composio integrations, authentication, toolkits, MCP servers, triggers, and SDKs.

### Skills

| Skill | Triggers On |
|-------|-------------|
| **managed-authentication** | OAuth, API keys, connected accounts, entity management |
| **toolkits-actions** | Available integrations, actions, tool parameters |
| **mcp-servers** | MCP setup, Claude Desktop, Cursor, Rube server |
| **triggers-events** | Webhooks, real-time events, automated workflows |
| **sdk-integration** | Python/TypeScript SDK, framework integrations |

## Usage Examples

### Search Documentation

```
/composio-search OAuth setup for GitHub
```

### Get Auth Guide

```
/composio-auth slack
```

### Explore Toolkit

```
/composio-tools github
```

### Setup MCP

```
/composio-mcp
```

### Natural Language Questions

The agent triggers automatically for questions like:
- "How do I connect my AI agent to GitHub?"
- "What's the difference between OAuth and API key auth?"
- "How do I set up Composio with LangChain?"
- "How do I create a trigger for new emails?"

## Documentation Sources

This plugin fetches information from:
- https://docs.composio.dev/ (official documentation)
- https://github.com/ComposioHQ/composio (GitHub repository)

## Supported Integrations

Composio supports 500+ integrations including:

**Development**: GitHub, GitLab, Linear, Jira, Bitbucket
**Communication**: Slack, Discord, Gmail, Teams, Telegram
**Productivity**: Notion, Google Drive, Dropbox, Airtable
**Design**: Figma, Canva
**Data**: Supabase, MongoDB, PostgreSQL
**AI/ML**: OpenAI, Anthropic, HuggingFace

## Framework Support

- OpenAI SDK
- Anthropic/Claude SDK
- LangChain / LangGraph
- CrewAI
- Vercel AI SDK
- AutoGen
- LlamaIndex

## Requirements

- Claude Code CLI
- Internet connection (for WebFetch)

## License

MIT License - see [LICENSE](LICENSE) file.

## Author

Carlos Araujo (cadu.gevaerd@gmail.com)

## Links

- [Composio Documentation](https://docs.composio.dev/)
- [Composio GitHub](https://github.com/ComposioHQ/composio)
- [Plugin Repository](https://github.com/cadugevaerd/claudecode_plugins)
