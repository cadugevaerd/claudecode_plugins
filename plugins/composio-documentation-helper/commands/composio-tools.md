---
name: composio-tools
description: List available tools and actions for a specific toolkit in Composio
argument-hint: "<toolkit_name>"
allowed-tools:
  - WebFetch
  - WebSearch
---

# Composio Toolkit Explorer

Explore available tools and actions for a specific Composio toolkit.

## Instructions

1. **Identify the Toolkit**: Parse toolkit name from user input
2. **Fetch Toolkit Info**: Get available actions and their parameters
3. **Provide Examples**: Show how to use the tools

## Documentation URLs

Base: `https://docs.composio.dev/`

- `/docs/tools` - Tools catalog overview
- `/robots-only/tools.json` - Machine-readable toolkit data

## Popular Toolkits

| Toolkit | Description | Example Actions |
|---------|-------------|-----------------|
| GitHub | Repository management | create_issue, create_pr, get_repo |
| Slack | Team communication | send_message, create_channel |
| Gmail | Email management | send_email, read_emails |
| Notion | Documentation | create_page, update_database |
| Linear | Issue tracking | create_issue, update_issue |
| Jira | Project management | create_issue, transition_issue |
| Figma | Design collaboration | get_file, get_comments |
| Supabase | Database operations | query, insert, update |

## Response Format

Provide:

### 1. Toolkit Overview
Brief description of what the toolkit does

### 2. Available Actions
List of actions with descriptions:
```
- action_name: Description of what it does
  - param1: (required) Description
  - param2: (optional) Description
```

### 3. Code Example

```python
from composio_openai import ComposioToolSet
from openai import OpenAI

client = OpenAI()
toolset = ComposioToolSet()

# Get specific tools
tools = toolset.get_tools(actions=["GITHUB_CREATE_ISSUE"])

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Create an issue..."}],
    tools=tools
)
```

```typescript
import { ComposioToolSet } from "@composio/openai";
import OpenAI from "openai";

const client = new OpenAI();
const toolset = new ComposioToolSet();

const tools = await toolset.getTools({
    actions: ["GITHUB_CREATE_ISSUE"]
});

const response = await client.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: "Create an issue..." }],
    tools
});
```

### 4. Related Toolkits
Similar or complementary toolkits

## Example Usage

```
/composio-tools github
/composio-tools slack
/composio-tools gmail
/composio-tools notion
```
