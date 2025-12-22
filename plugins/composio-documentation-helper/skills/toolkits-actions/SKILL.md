---
name: Toolkits and Actions
description: This skill should be used when the user asks about Composio toolkits, available integrations, specific actions, tool parameters, or how to use tools with AI agents. Trigger on questions like 'what tools are available', 'GitHub actions in Composio', 'how to use Slack toolkit', 'list available integrations', 'tool parameters'.
version: 1.0.0
---

# Composio Toolkits and Actions

Provide comprehensive guidance on Composio's 500+ toolkits and their actions for AI agent integrations.

## When to Use This Skill

Use when user asks about:
- Available toolkits and integrations
- Specific actions for a toolkit
- Action parameters and schemas
- Filtering and selecting tools
- Tool execution with AI frameworks
- Custom tool creation

## Core Concepts

### Toolkit Structure

Each toolkit contains multiple **actions**:

```
Toolkit: GitHub
├── GITHUB_CREATE_ISSUE
├── GITHUB_CREATE_PULL_REQUEST
├── GITHUB_GET_REPOSITORY
├── GITHUB_LIST_COMMITS
└── ... (50+ more actions)
```

### Getting Tools

```python
from composio_openai import ComposioToolSet, Action

toolset = ComposioToolSet()

# Get all tools for a toolkit
github_tools = toolset.get_tools(apps=["github"])

# Get specific actions
specific_tools = toolset.get_tools(actions=[
    Action.GITHUB_CREATE_ISSUE,
    Action.GITHUB_CREATE_PULL_REQUEST
])

# Get by tags
tagged_tools = toolset.get_tools(tags=["productivity"])
```

```typescript
import { ComposioToolSet } from "@composio/openai";

const toolset = new ComposioToolSet();

// Get all GitHub tools
const githubTools = await toolset.getTools({ apps: ["github"] });

// Get specific actions
const specificTools = await toolset.getTools({
    actions: ["GITHUB_CREATE_ISSUE", "GITHUB_CREATE_PULL_REQUEST"]
});
```

## Popular Toolkits

### Development
| Toolkit | Actions | Use Cases |
|---------|---------|-----------|
| GitHub | 50+ | Issues, PRs, repos, commits |
| GitLab | 40+ | Similar to GitHub |
| Linear | 30+ | Issue tracking, projects |
| Jira | 35+ | Enterprise project management |

### Communication
| Toolkit | Actions | Use Cases |
|---------|---------|-----------|
| Slack | 25+ | Messages, channels, files |
| Gmail | 20+ | Emails, labels, drafts |
| Discord | 15+ | Server management, messages |
| Teams | 20+ | Microsoft Teams integration |

### Productivity
| Toolkit | Actions | Use Cases |
|---------|---------|-----------|
| Notion | 30+ | Pages, databases, blocks |
| Google Drive | 25+ | Files, folders, sharing |
| Dropbox | 20+ | File storage |
| Airtable | 15+ | Database operations |

### Design & Media
| Toolkit | Actions | Use Cases |
|---------|---------|-----------|
| Figma | 15+ | Design files, comments |
| Canva | 10+ | Design creation |
| YouTube | 20+ | Video management |

### Data & Analytics
| Toolkit | Actions | Use Cases |
|---------|---------|-----------|
| Supabase | 15+ | Database, auth, storage |
| MongoDB | 10+ | Document operations |
| PostgreSQL | 10+ | SQL operations |

## Using Tools with AI Frameworks

### OpenAI

```python
from openai import OpenAI
from composio_openai import ComposioToolSet

client = OpenAI()
toolset = ComposioToolSet()

tools = toolset.get_tools(actions=["GITHUB_CREATE_ISSUE"])

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Create a bug report issue"}],
    tools=tools
)

# Execute tool calls
result = toolset.handle_tool_call(response)
```

### Anthropic/Claude

```python
from anthropic import Anthropic
from composio_claude import ComposioToolSet

client = Anthropic()
toolset = ComposioToolSet()

tools = toolset.get_tools(actions=["SLACK_SEND_MESSAGE"])

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Send hello to #general"}],
    tools=tools
)

result = toolset.handle_tool_call(response)
```

### LangChain

```python
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet

llm = ChatOpenAI(model="gpt-4")
toolset = ComposioToolSet()

tools = toolset.get_tools(actions=["GMAIL_SEND_EMAIL"])

agent = create_tool_calling_agent(llm, tools, prompt)
```

## Action Parameters

Each action has specific parameters:

```python
# Example: GITHUB_CREATE_ISSUE parameters
{
    "owner": "repository owner (required)",
    "repo": "repository name (required)",
    "title": "issue title (required)",
    "body": "issue description (optional)",
    "labels": ["bug", "enhancement"] (optional),
    "assignees": ["username"] (optional)
}
```

### Getting Action Schema

```python
# Get detailed schema for an action
schema = toolset.get_action_schema(action="GITHUB_CREATE_ISSUE")
print(schema)
```

## Tool Filtering

### By Use Case

```python
# Only get read actions
read_tools = toolset.get_tools(
    apps=["github"],
    tags=["read"]
)

# Only write actions
write_tools = toolset.get_tools(
    apps=["github"],
    tags=["write"]
)
```

### By Entity

```python
# Tools for specific user with their auth
tools = toolset.get_tools(
    apps=["github"],
    entity_id="user_123"
)
```

## Best Practices

1. **Minimal Tools**: Only include tools the agent needs
2. **Specific Actions**: Use specific actions vs entire toolkits
3. **Entity Scoping**: Always scope tools to entity_id
4. **Error Handling**: Handle tool execution failures gracefully
5. **Rate Limits**: Be aware of API rate limits

## Documentation Sources

> **Note**: Use GitHub sources as `docs.composio.dev` may block automated requests.

### Primary Sources (GitHub - Always Works)
- **README**: https://raw.githubusercontent.com/ComposioHQ/composio/master/README.md
- **Python SDK**: https://raw.githubusercontent.com/ComposioHQ/composio/master/python/README.md

### Search for Specific Docs
Use WebSearch: `Composio toolkit <name> site:docs.composio.dev`

Fetch latest documentation from GitHub for current action lists and parameters.
