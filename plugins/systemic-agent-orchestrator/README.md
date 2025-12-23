# Systemic Agent Orchestrator

Development orchestrator for production-ready AI Agents using LangGraph Graph API, AWS Bedrock Agent Core, Terraform, and Langsmith.

## Overview

This plugin enforces architectural guardrails and best practices for building enterprise-grade AI agents. It ensures:

- **Graph API Only**: Prohibits Functional API (@entrypoint, @task)
- **Langsmith Prompts**: All prompts stored in Langsmith, not in code
- **models.yaml**: Centralized LLM configuration
- **Code Quality**: 500-line limit, ruff linting, proper structure
- **Serena Integration**: Semantic code operations and persistent memory
- **AWS Infrastructure**: Full Terraform patterns for production deployment

---

## Features

### Phase 1: Core Guardrails + LangGraph (Complete)

#### Guardrail Hooks (Automatic)

| Hook | Purpose | Action |
|------|---------|--------|
| `validate_functional_api` | Block @entrypoint/@task | Block |
| `validate_local_prompts` | Block hardcoded prompts | Block |
| `validate_models_yaml` | Validate configuration | Block |
| `validate_file_size` | Enforce 500-line limit | Block |
| `run_ruff` | Linting check | Warn |
| `check_mcp_dependencies` | Verify required MCPs | Info |
| `enforce_serena_tools` | Suggest Serena tools | Info |

#### Skills

- **langgraph-graph-api**: StateGraph patterns, nodes, edges, state management
- **models-yaml-config**: LLM configuration, providers, loading patterns
- **hybrid-workflow-pattern**: Defined steps + LLM decisions architecture
- **langsmith-prompts**: Prompt versioning, retrieval, best practices
- **serena-onboarding**: Memory management, symbolic code operations

### Phase 2: AWS + Terraform (Complete)

#### Skills

- **bedrock-agent-core**: Agent runtime, short/long-term memory, MCP gateway
- **aurora-serverless**: Data API patterns, N+1 prevention, batch operations
- **step-functions-evaluation**: Agent vs Step Functions decision framework
- **terraform-patterns**: AWS infrastructure as code, tagging standards

#### Templates

- Terraform modules for Aurora, ECS, API Gateway, CloudWatch
- Environment-specific configurations (dev, homolog, prod)
- IAM policies with least privilege

### Phase 3: Deployment (Complete)

#### Skills

- **ci-cd-patterns**: GitHub Actions workflows, OIDC authentication
- **monitoring-observability**: Langsmith tracing, CloudWatch, custom metrics

#### Templates

- GitHub Actions deployment workflow
- Dockerfile for agent runtime
- PR template with checklist

---

## Commands

### New Projects
```bash
# Phase 1: Discovery - Deep context understanding before code
/systemic-agent-orchestrator:discovery [project-path]

# Initialize new agent project
/systemic-agent-orchestrator:init-agent my-agent planner,executor,reviewer
```

### Existing Projects (Resume Development)
```bash
# Resume work on existing project - loads context from Serena memories
/systemic-agent-orchestrator:resume-project [project-path]

# Add a new node to existing project
/systemic-agent-orchestrator:add-node summarizer llm "Summarize conversation"

# Validate entire project against all guardrails
/systemic-agent-orchestrator:validate-stack
```

### Utilities
```bash
# Check plugin dependencies (MCP servers)
/systemic-agent-orchestrator:check-deps
```

---

## Installation

```bash
# Add plugin to Claude Code
claude plugin add systemic-agent-orchestrator
```

## Requirements

### Required MCP Plugins

- **langchain-ecosystem-helper**: LangGraph/LangChain documentation
- **serena**: Semantic code analysis (highly recommended)

### Optional MCP Plugins

- **aws-documentation-helper**: AWS documentation and best practices

### Environment Variables

```bash
# Langsmith (required)
export LANGCHAIN_API_KEY="lsv2_..."
export LANGCHAIN_PROJECT="my-project"
export LANGCHAIN_TRACING_V2="true"

# AWS (for deployment)
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="123456789012"
```

---

## Quick Start

### 1. Discovery Phase (New Projects)

```bash
# Run discovery to understand requirements
/discovery

# This will:
# - Run Serena onboarding
# - Interview about agent purpose
# - Create memories in .serena/memories/
# - Update CLAUDE.md with references
```

### 2. Create Agent

```bash
# Initialize project structure
/init-agent customer-support planner,executor,reviewer
```

### 3. Configure Prompts

1. Create prompts at https://smith.langchain.com
2. Use naming convention: `my-org/node-name-prompt`

### 4. Configure models.yaml

```yaml
nodes:
  planner:
    model: "anthropic:claude-sonnet-4-20250514"
    temperature: 0.0
```

### 5. Develop with Guardrails

Hooks automatically validate all code changes.

### 6. Deploy

```bash
# Infrastructure
cd infra
terraform plan -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars

# Or use GitHub Actions (push to main)
```

---

## Project Structure

Created projects follow this structure:

```
my-agent/
├── config/
│   └── models.yaml          # LLM configurations
├── src/
│   ├── __init__.py
│   ├── state.py             # AgentState TypedDict
│   ├── config.py            # Configuration loader
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── planner.py       # Planner node
│   │   ├── executor.py      # Executor node
│   │   └── reviewer.py      # Reviewer node
│   └── graph.py             # StateGraph builder
├── tests/
│   ├── __init__.py
│   └── test_nodes.py
├── infra/                    # Terraform infrastructure
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── backend.tf
│   ├── modules/
│   │   ├── agent-runtime/
│   │   ├── database/
│   │   ├── api/
│   │   └── monitoring/
│   └── environments/
│       ├── dev.tfvars
│       ├── homolog.tfvars
│       └── prod.tfvars
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline
├── main.py                   # Agent entry point
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Architecture Rules

### 1. Graph API Only

```python
# CORRECT
from langgraph.graph import StateGraph, START, END
graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)

# PROHIBITED
@entrypoint
def main():
    pass
```

### 2. Langsmith Prompts

```python
# CORRECT
from langsmith import Client
client = Client()
prompt = client.pull_prompt("my-org/planner-prompt")

# PROHIBITED
prompt = ChatPromptTemplate.from_template("You are...")
```

### 3. models.yaml Configuration

```yaml
# config/models.yaml
nodes:
  planner:
    model: "anthropic:claude-sonnet-4-20250514"
    temperature: 0.0
```

```python
# CORRECT
from config import get_model_for_node
model = get_model_for_node("planner")

# PROHIBITED
model = ChatAnthropic(model="claude-sonnet-4-20250514")
```

### 4. Aurora Data API (N+1 Prevention)

```python
# CORRECT - Batch operations
client.batch_execute_statement(
    sql="INSERT INTO messages ...",
    parameterSets=parameter_sets
)

# PROHIBITED - N+1 queries
for message in messages:
    client.execute_statement(sql="INSERT INTO messages ...")
```

### 5. Tagging Standards

```hcl
# All tags MUST be UPPERCASE
tags = {
  PROJETO   = "MY-AGENT"
  AMBIENTE  = "PRD"  # PRD, HMLG, DEV
  PRODUTO   = "AI-AGENTS"
}
```

---

## Development Workflow

### New Projects

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEW PROJECT WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: Discovery                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /discovery → Serena onboarding → Interview → Document    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Phase 2: Design                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Load Context → State Machine → ADR → CLAUDE.md Update    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Phase 3: Implementation                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /init-agent → Nodes → Tests → /validate-stack            │  │
│  │                                                           │  │
│  │  ⚠️ Guardrails active: Deviation = Immediate redirect    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Phase 4: Integration                                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Research API → Serena write_memory → CLAUDE.md → MCP?    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Phase 5: Deployment                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Terraform Plan → Review → Apply → Monitor                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Existing Projects (Resume Development)

```
┌─────────────────────────────────────────────────────────────────┐
│                 EXISTING PROJECT WORKFLOW                        │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: Resume Context                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /resume-project → Load memories → Analyze state          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Step 2: Validate Current State                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /validate-stack → Fix issues → Confirm ready             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Step 3: Continue Development                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /add-node OR fix issues OR add features                  │  │
│  │                                                           │  │
│  │  ⚠️ Guardrails still active on all changes               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  Step 4: Validate & Deploy                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /validate-stack → Terraform → Deploy                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Memory & Documentation (Serena MCP)

### Creating Memories

```python
# Store API documentation
write_memory("api_stripe_integration.md", content)

# Store architecture decisions
write_memory("arch_agent_design.md", content)
```

### CLAUDE.md References

```markdown
## Project Memories (Serena MCP)

### API Integrations
- `api_stripe_integration` - Stripe payment API docs
  Use: `read_memory('api_stripe_integration')`

### Architecture
- `arch_agent_design` - Agent state machine design
  Use: `read_memory('arch_agent_design')`
```

---

## Monitoring & Observability

### Langsmith Tracing

- All LLM calls traced automatically
- Token usage and latency metrics
- Prompt version tracking

### CloudWatch

- Log retention by environment (1/3/7 days)
- Alarms for errors, latency, memory
- Custom dashboards per agent

### Custom Metrics

- Conversations completed
- Resolution time
- Escalation rate

---

## Success Criteria

The plugin ensures:

1. ✅ Developers create agents from zero to production
2. ✅ Architectural deviations are impossible (guardrails)
3. ✅ All prompts in Langsmith
4. ✅ All LLM configs in models.yaml
5. ✅ Test coverage ≥ 70%
6. ✅ Infrastructure via Terraform
7. ✅ Knowledge preserved in Serena memories
8. ✅ External APIs documented before integration
9. ✅ MCP servers evaluated for features
10. ✅ Hooks enforce all validation rules

---

## License

MIT

## Author

Carlos Araujo (cadu.gevaerd@gmail.com)
