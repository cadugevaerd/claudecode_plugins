---
name: SDK Integration
description: This skill should be used when the user asks about Composio SDKs, Python SDK, TypeScript SDK, framework integrations, OpenAI integration, Anthropic integration, LangChain with Composio, CrewAI with Composio, or Vercel AI SDK. Trigger on questions like 'install Composio SDK', 'use Composio with Python', 'TypeScript Composio', 'LangChain Composio integration', 'CrewAI tools'.
version: 1.0.0
---

# Composio SDK Integration

Provide comprehensive guidance on using Composio SDKs with various AI frameworks and languages.

## When to Use This Skill

Use when user asks about:
- Installing Composio SDKs
- Python SDK usage
- TypeScript/JavaScript SDK
- Framework integrations (OpenAI, Anthropic, LangChain, etc.)
- SDK configuration and best practices

## Installation

### Python SDK

```bash
# Core SDK
pip install composio-core

# Framework-specific packages
pip install composio-openai      # OpenAI integration
pip install composio-anthropic   # Anthropic/Claude
pip install composio-langchain   # LangChain
pip install composio-crewai      # CrewAI
pip install composio-autogen     # AutoGen
pip install composio-llamaindex  # LlamaIndex
```

### TypeScript/JavaScript SDK

```bash
# Core SDK
npm install @composio/core

# Framework-specific packages
npm install @composio/openai     # OpenAI integration
npm install @composio/langchain  # LangChain
npm install @composio/vercel-ai  # Vercel AI SDK
```

## Framework Integrations

### OpenAI (Python)

```python
from openai import OpenAI
from composio_openai import ComposioToolSet, Action

client = OpenAI()
toolset = ComposioToolSet()

# Get tools
tools = toolset.get_tools(actions=[Action.GITHUB_CREATE_ISSUE])

# Create completion with tools
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Create a bug report issue in myrepo"}
    ],
    tools=tools
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    result = toolset.handle_tool_call(response)
    print(result)
```

### OpenAI (TypeScript)

```typescript
import OpenAI from "openai";
import { ComposioToolSet } from "@composio/openai";

const client = new OpenAI();
const toolset = new ComposioToolSet();

const tools = await toolset.getTools({
    actions: ["GITHUB_CREATE_ISSUE"]
});

const response = await client.chat.completions.create({
    model: "gpt-4",
    messages: [
        { role: "user", content: "Create a bug report issue" }
    ],
    tools
});

if (response.choices[0].message.tool_calls) {
    const result = await toolset.handleToolCall(response);
    console.log(result);
}
```

### Anthropic/Claude (Python)

```python
from anthropic import Anthropic
from composio_claude import ComposioToolSet, Action

client = Anthropic()
toolset = ComposioToolSet()

tools = toolset.get_tools(actions=[Action.SLACK_SEND_MESSAGE])

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Send hello to #general channel"}
    ],
    tools=tools
)

result = toolset.handle_tool_call(response)
```

### LangChain (Python)

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from composio_langchain import ComposioToolSet, Action

llm = ChatOpenAI(model="gpt-4")
toolset = ComposioToolSet()

tools = toolset.get_tools(actions=[
    Action.GITHUB_CREATE_ISSUE,
    Action.GITHUB_LIST_ISSUES
])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful GitHub assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "List open issues in myrepo"})
```

### LangGraph (Python)

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet

llm = ChatOpenAI(model="gpt-4")
toolset = ComposioToolSet()

tools = toolset.get_tools(apps=["github"])

agent = create_react_agent(llm, tools)

result = agent.invoke({
    "messages": [("human", "Create an issue for the bug")]
})
```

### CrewAI (Python)

```python
from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, Action

toolset = ComposioToolSet()
tools = toolset.get_tools(actions=[Action.GITHUB_CREATE_ISSUE])

developer = Agent(
    role="Developer",
    goal="Manage GitHub issues",
    tools=tools
)

task = Task(
    description="Create a bug report issue",
    agent=developer
)

crew = Crew(agents=[developer], tasks=[task])
result = crew.kickoff()
```

### Vercel AI SDK (TypeScript)

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { ComposioToolSet } from "@composio/vercel-ai";

const toolset = new ComposioToolSet();
const tools = await toolset.getTools({ actions: ["GITHUB_CREATE_ISSUE"] });

const result = await generateText({
    model: openai("gpt-4"),
    prompt: "Create a bug report issue",
    tools
});
```

## Configuration

### API Key Setup

```python
# Option 1: Environment variable
import os
os.environ["COMPOSIO_API_KEY"] = "your-api-key"

# Option 2: Direct initialization
toolset = ComposioToolSet(api_key="your-api-key")
```

```typescript
// Option 1: Environment variable
process.env.COMPOSIO_API_KEY = "your-api-key";

// Option 2: Direct initialization
const toolset = new ComposioToolSet({ apiKey: "your-api-key" });
```

### Entity Configuration

```python
# Tools for specific user
toolset = ComposioToolSet(entity_id="user_123")

# Or per-request
tools = toolset.get_tools(
    actions=[Action.GITHUB_CREATE_ISSUE],
    entity_id="user_123"
)
```

## Best Practices

1. **Framework-Specific Packages**: Use `composio-openai`, not just `composio-core`
2. **Entity Isolation**: Always use entity_id for multi-user apps
3. **Minimal Tools**: Only get tools you need
4. **Error Handling**: Wrap tool calls in try/catch
5. **API Key Security**: Use environment variables

## Common Patterns

### Agentic Loop

```python
while True:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason == "tool_calls":
        result = toolset.handle_tool_call(response)
        messages.append(response.choices[0].message)
        messages.append({
            "role": "tool",
            "content": str(result),
            "tool_call_id": response.choices[0].message.tool_calls[0].id
        })
    else:
        break

print(response.choices[0].message.content)
```

### Multi-Tool Execution

```python
# Execute multiple tool calls
results = toolset.handle_tool_calls(response)  # Note: plural

for result in results:
    print(f"Tool: {result.tool_name}, Result: {result.output}")
```

## Documentation URLs

- Python SDK: https://docs.composio.dev/docs/python-sdk
- TypeScript SDK: https://docs.composio.dev/docs/typescript-sdk
- OpenAI Integration: https://docs.composio.dev/docs/providers/openai
- LangChain Integration: https://docs.composio.dev/docs/providers/langchain
- API Reference: https://docs.composio.dev/api-reference/

Fetch latest documentation with WebFetch for current SDK versions and APIs.
