# LangChain Ecosystem Helper

A comprehensive Claude Code plugin for LangGraph agent development, LangChain orchestration, and LangSmith observability.

## Features

- **LangChain Docs MCP Integration**: Direct access to LangChain documentation via MCP
- **LangGraph Development Guide**: Complete guide for building AI agents (2025 best practices)
- **LangChain Architecture**: LCEL, chains, prompts, RAG patterns
- **LangSmith Observability**: Tracing, debugging, evaluation setup

## Installation

```bash
claude plugins add langchain-ecosystem-helper
```

Or add to your Claude Code settings:

```json
{
  "plugins": [
    "langchain-ecosystem-helper@claudecode-plugins"
  ]
}
```

## Requirements

- Claude Code CLI
- Internet access for MCP documentation queries

## Available Commands

### `/langchain-search <query>`
Search LangChain, LangGraph, and LangSmith documentation.

```bash
/langchain-search create_react_agent
/langchain-search LCEL pipe syntax
/langchain-search LangSmith evaluation
```

### `/langgraph-agent <type> [features]`
Generate LangGraph agent templates with best practices.

```bash
/langgraph-agent react memory,streaming
/langgraph-agent supervisor hitl,tools
/langgraph-agent custom memory,hitl,streaming,tools
```

### `/langsmith-setup <action>`
Set up LangSmith tracing and evaluation.

```bash
/langsmith-setup trace      # Setup tracing
/langsmith-setup evaluate   # Create evaluators
/langsmith-setup dataset    # Create datasets
```

## Skills

### LangGraph Development
Complete guide for building AI agents with LangGraph 0.3+:
- ReAct agents with `create_react_agent`
- Graph API vs Functional API
- State management and checkpointing
- Memory (short-term and long-term)
- Human-in-the-loop with `interrupt`
- Multi-agent systems
- Streaming patterns

### LangChain Architecture
LangChain patterns and best practices:
- LCEL (LangChain Expression Language)
- Prompts and output parsers
- Chat models and tool binding
- RAG (Retrieval-Augmented Generation)
- Document loaders and text splitters
- Embeddings and vector stores

### LangSmith Observability
Tracing, debugging, and evaluation:
- Automatic and custom tracing
- Dataset creation and management
- Custom evaluators (code and LLM-as-judge)
- Online and offline evaluation
- Prompt management

## Agent

### LangChain Knowledge Agent
Autonomous expert that can:
- Answer questions about LangGraph, LangChain, LangSmith
- Search documentation for specific topics
- Provide working code examples
- Explain trade-offs and best practices

## MCP Integration

This plugin integrates with the LangChain Documentation MCP Server:

```json
{
  "mcpServers": {
    "langchain-docs": {
      "url": "https://docs.langchain.com/mcp",
      "type": "http"
    }
  }
}
```

### Available MCP Tool
- `SearchDocsByLangChain`: Search across LangChain documentation

## Version Compatibility (2025)

| Component | Version |
|-----------|---------|
| LangGraph | 0.3+ |
| LangChain | 1.0+ |
| LangSmith | Latest |

## Key Updates in 2025

- **Functional API** (January 2025): Alternative to Graph API
- **`interrupt` function** (LangGraph 0.2.31+): Simplified HITL
- **OpenTelemetry** (March 2025): End-to-end tracing
- **LangGraph Platform GA** (October 2025): Production deployment
- **Memory deprecation**: Use LangGraph checkpointers instead of LangChain memory

## Companies Using LangGraph in Production

- LinkedIn
- Uber
- Replit
- Klarna
- Elastic

## License

MIT License

## Author

Carlos Araujo ([@cadugevaerd](https://github.com/cadugevaerd))

## Links

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/docs/)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai)
