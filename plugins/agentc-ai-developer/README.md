# Agentc AI Developer

Complete guide for developing AI agents from conception to production through structured **Microprocessos**. This plugin implements the **Brief Minimo** methodology with integrated commands for planning, setup, and execution.

## Overview

Agentc AI Developer is your partner in building production-ready AI agents through proven methodologies:

- **Microprocesso 1.1** (`/brief`) - Agent planning with Brief Minimo methodology
- **Microprocesso 1.2** (`/setup-local-observability`) - Environment setup with reproducibility and observability

Works with **new agents** and integrates seamlessly with **existing projects**.

## What is Brief Minimo?

Brief Minimo is a structured planning methodology that answers 5 fundamental questions about your AI agent:

1. **What does the agent DO?** - Core functionality in one clear action verb
2. **What is the INPUT?** - Type, format, maximum size, real example
3. **What is the OUTPUT?** - Expected structure, success example, error example
4. **What is the TOOL/API?** - Single tool, access confirmation, cost, backup alternative
5. **What is SUCCESS?** - Quantifiable metric, minimum target, measurement method, dataset availability

## Installation

```bash
/plugin install agentc-ai-developer
```

## Quick Start

### Microprocesso 1.1: Planning with Brief Minimo

Start your agent planning session:

```bash
/brief
```

This launches an interactive interview that guides you through the Brief Minimo process. The agent automatically detects your context and offers relevant options.

**Result**: README.md with complete agent specification ✅

### Microprocesso 1.2: Environment Setup & Observability

After `/brief` creates your project repository, continue with environment setup:

```bash
/setup-local-observability
```

This guides you interactively through:
- ✅ Python virtual environment setup
- ✅ Dependency installation (langchain, anthropic, langsmith)
- ✅ Environment configuration (.env + .gitignore)
- ✅ LangSmith integration for observability
- ✅ Complete validation and testing

**Result**: Reproducible environment with complete observability ready for development! 🚀

**Total time**: ~2 hours (planning + environment setup)

## How It Works

### 1. Run the Command

```bash
/brief
```

### 2. Interactive Interview

The command conducts a conversational interview directly:

- Welcomes you and explains the process
- Asks each of the 5 fundamental questions
- Collects concrete examples (not vague descriptions)
- Validates completeness before proceeding
- Clarifies with follow-up questions as needed

### 3. Specification Document

At the end, you receive a comprehensive **README.md** containing:

- Your agent's complete specification
- Input/output examples
- Tool/API requirements
- Success metrics and measurement strategy
- Next steps for development

### 4. Use as Blueprint

Use the generated specification document as the reference for:

- Architecture and design phase
- Development and implementation
- Testing and validation
- Production deployment

### 5. Project Integration (Optional)

After planning and environment setup, run `/update-claude-md` to integrate guidance into your project's CLAUDE.md:

```bash
/update-claude-md
```

This adds a concise section (≤40 lines) with command references and next steps for ongoing development.

## Features

### Structured Planning

- **5 Fundamental Questions** - Proven framework for agent design
- **30-minute Interview** - Lightweight but comprehensive process
- **Concrete Examples** - Emphasis on specificity, not vague descriptions
- **Validation Built-in** - Confirms all essential information is provided

### Conversation-Driven

- Friendly, encouraging tone
- Asks clarifying questions if answers are vague
- Pushes back gently on scope creep
- Validates understanding before proceeding

### Complete Specification

Generated document includes:

- Agent purpose and core functionality
- Input type, format, size, and examples
- Output structure with success and error examples
- Tool/API requirements and backup alternatives
- Success metrics with measurement strategy
- Next steps in development process

## Why Brief Minimo?

This methodology prevents common agent planning failures:

| Problem | Solution |
|---------|----------|
| ❌ Vague requirements | ✅ Crystal clear specifications |
| ❌ Scope creep | ✅ Focused single responsibility |
| ❌ Undefined success | ✅ Quantifiable metrics |
| ❌ Technical surprises | ✅ Tool/API validation upfront |
| ❌ Hidden costs | ✅ Budget awareness from day one |
| ❌ Integration nightmares | ✅ Input/output specs before coding |

## Best Practices

### When Using Brief Minimo

✅ **DO**:
- Provide specific, concrete examples
- Include real data samples (not conceptual ones)
- Be honest about constraints and budget
- Have stakeholders available for clarification
- Document everything the brief defines

❌ **DON'T**:
- Accept vague answers - ask "Can you show me an example?"
- Plan multiple tools at once - start with ONE
- Skip the metric definition - "We'll see if it works" isn't good enough
- Assume common knowledge - always ask for clarification
- Put off decisions - Brief Minimo is faster than discovering requirements during development

### Question-by-Question Tips

#### Question 1 (What does it DO?)

- Use strong action verbs: analyze, classify, fetch, generate, summarize
- One sentence should describe the complete function
- Example: "Classifies customer support emails by priority (high/medium/low)"

#### Question 2 (What is the INPUT?)

- Be specific about format: plain text, JSON, CSV, email body, etc.
- Include realistic maximum size limits
- Show a real example from your actual data
- Example: "Plain text email subject + body, max 10 KB, from support inbox"

#### Question 3 (What is the OUTPUT?)

- Define exact JSON/data structure with field names and types
- Show what success looks like with real output
- Show what errors look like (null values, error messages, etc.)
- Example: {priority: "high", category: "system_outage", ...}

#### Question 4 (What is the TOOL/API?)

- Choose ONE primary tool to start with
- Have API keys and access confirmed
- Understand the cost (free tier? pricing limits?)
- Define the backup plan explicitly
- Example: "OpenWeather API, free tier, backup is cached data"

#### Question 5 (What is SUCCESS?)

- Define as a specific percentage or number, not a feeling
- 85% accuracy, 1-second response time, 0 false positives, etc.
- Have test data available to measure this metric
- Know how often you'll validate this metric
- Example: "85% classification accuracy measured weekly on 100 emails"

## Usage Modes

The `brief-assistant` agent adapts to your context and automatically offers the right mode:

### Mode 1: New Agent (Default)

**When**: Starting a new agent from scratch
**Output**: Complete specification document (README.md)
**Duration**: ~30 minutes

```bash
/brief
# Agent detects no existing agents
# → "Let's create a new agent brief!"
# → Full 30-minute interview
```

### Mode 2: Existing Agent Update

**When**: Refining or updating an already developed agent
**Use Cases**:
- Document production agents that evolved during development
- Refine scope of existing agents
- Plan improvements and new features
- Keep brief aligned with current implementation

**Output**: Updated brief reflecting current state
**Duration**: ~15-20 minutes

```bash
/brief
# Agent detects existing agents in project
# → "Update existing agent or create new one?"
# → Select agent to update
# → Interview focused on changes since original planning
```

### Mode 3: Validate Agent

**When**: Checking if existing agent matches Brief Minimo criteria
**Use Cases**:
- Quality assurance and completeness check
- Scope verification
- Identify specification gaps
- Team alignment on agent requirements

**Output**: Validation report with gaps and recommendations
**Duration**: ~20 minutes

```bash
/brief
# → "Validate agent against Brief Minimo criteria"
# → Assessment of each criterion (purpose, input/output, tools, success)
# → Report with gaps and improvement suggestions
```

### Mode 4: Document Existing Agent

**When**: Adding brief documentation to already-built agents
**Use Cases**:
- Retroactive documentation of production agents
- Team onboarding and knowledge sharing
- Creating specification from working implementation
- Preserving institutional knowledge

**Output**: Brief specification created retroactively
**Duration**: ~20 minutes

```bash
/brief
# → "Document existing agent implementation"
# → Questions about what agent actually does (from code review)
# → Generate brief based on current implementation
```

## Using in Existing Projects

The plugin works seamlessly with existing projects:

1. **Run `/brief`** - Agent detects your existing setup
2. **Choose Mode** - Select from: New Agent, Update, Validate, or Document
3. **Answer Questions** - Brief interview adapted to your mode
4. **Get Output** - New specification, updated brief, validation report, or documentation
5. **Use as Reference** - Keep brief as specification for future improvements

### Example: Updating a Production Agent

```
You have a "email_classifier" agent running in production for 6 months.

1. Run: /brief
2. Agent detects existing agents
3. Choose: "Update existing agent"
4. Select: "email_classifier"
5. Interview focuses on:
   - What has changed since original planning?
   - Any changes to input/output specs?
   - Updated success metrics?
   - Changes to tool/API or costs?
6. Output: Updated brief reflecting current state and improvements
7. Share with team: New team members reference updated brief
```

### Example: Documenting a Legacy Agent

```
You have an "error_processor" agent built 2 years ago with minimal docs.

1. Run: /brief
2. Agent detects existing agents
3. Choose: "Document existing agent"
4. Select: "error_processor"
5. Interview questions focus on current implementation:
   - What does this agent really do? (from code analysis)
   - What inputs does it accept? (from actual usage)
   - What outputs does it produce? (from current behavior)
   - What tool/API does it use? (from implementation)
   - How do you measure its success? (from monitoring/logs)
6. Output: Brief specification retroactively created
7. Store as reference: New developers understand agent without reading code
```

## Example: Email Priority Agent

Here's how the Brief Minimo process works for a real agent:

### Question 1: What does it DO?
"Analyzes customer support emails and assigns priority levels (high/medium/low) based on urgency and issue type"

### Question 2: What is the INPUT?
- Type: Plain text email
- Format: Subject and body separated by newline
- Max size: 10 KB (roughly 2000 tokens)
- Example: Real customer support email from your inbox

### Question 3: What is the OUTPUT?
```json
{
  "priority": "high|medium|low",
  "category": "system_outage|bug|feature_request|billing|other",
  "summary": "Brief one-liner description",
  "action_required": true|false
}
```

Success example:
```json
{
  "priority": "high",
  "category": "system_outage",
  "summary": "Production database unreachable",
  "action_required": true
}
```

### Question 4: What is the TOOL/API?
- Primary: OpenWeather API (if weather-based classifications are needed)
- Endpoint: api.openweathermap.org/data/2.5/weather
- Auth: Free API key
- Cost: Free tier available, no charge for this use case
- Backup: Use cached weather data from file if API unavailable

### Question 5: What is SUCCESS?
- Metric: Classification accuracy (% of emails correctly prioritized)
- Target: 85% minimum accuracy
- Measurement: Manual review of 100 random emails weekly
- Dataset: 2 years of labeled historical customer support emails
- Success indicator: 85+ emails correctly classified in weekly test set

**Result**: Complete specification ready for architecture and development!

## Roadmap

**Version 0.3.0** (Current)
- **Microprocesso 1.1**: Brief Minimo planning methodology (fully interactive `/brief` command)
- **Microprocesso 1.2**: Environment setup with Python venv, dependencies, and LangSmith observability
- **Project Integration**: `/update-claude-md` command for CLAUDE.md setup (≤40 lines, progressive disclosure)
- **Help Assistant**: Specialized support for guidance and troubleshooting (help-assistant agent)
- Interactive commands: `/brief`, `/setup-local-observability`, `/update-claude-md`
- Seamless integration with existing projects
- Environment validation and reproducibility
- Complete observability integration with LangSmith

**Planned Features**
- **Microprocesso 1.3**: Spike Agentic (agent building and testing)
- Architecture & Design macroprocess
- Multi-step agent design patterns
- Testing and validation strategies
- Production deployment guides
- Advanced agent patterns (multi-agent, hierarchical, self-improving)
- Integration with version control (git history analysis)
- Collaborative briefing for team alignment
- CI/CD integration for automated validation

## Commands

### /brief
Launches the **Microprocesso 1.1** - Brief Minimo 30-minute agent planning interview.

```bash
/brief
```

Conducts an interactive session and generates a comprehensive agent specification document (README.md) with complete agent specification.

### /setup-local-observability
Launches the **Microprocesso 1.2** - Interactive environment setup and configuration guide.

```bash
/setup-local-observability
```

Guides you through 8 interactive activities:
- Python virtual environment setup
- Dependency installation (langchain, anthropic, langsmith, python-dotenv)
- Environment variables configuration (.env + .env.example)
- LangSmith integration for observability
- Environment validation and testing

Results in a fully reproducible environment with complete observability, ready for agent development.

### /update-claude-md
Adds concise project integration section to your CLAUDE.md file.

```bash
/update-claude-md
```

Reads your Brief Minimo specification from README.md and creates a focused CLAUDE.md section (≤40 lines) with:
- Available Agentc commands and when to use them
- Links to full plugin documentation
- Next steps for ongoing development
- Support for help-assistant

Follows progressive disclosure pattern - keeps CLAUDE.md lightweight while referencing comprehensive docs.

## Agents

### help-assistant
Specialist agent for providing support, guidance, and troubleshooting during Microprocessos 1.1 and 1.2.

**When to use**: When you need help with `/brief`, `/setup-local-observability`, or general guidance

**Responsibilities**:
- Explain Brief Minimo concepts and methodology
- Clarify the 5 fundamental questions
- Provide troubleshooting for errors during setup
- Explain technical concepts (venv, .env, LangSmith, traces, Docker, etc.)
- Offer practical alternatives and workarounds
- Suggest best practices for completing microprocessos
- Reference official documentation when needed

**Key Capabilities**:
- Context-aware help for all Microprocesso phases
- Clear explanations of methodology and concepts
- Practical troubleshooting for common issues
- Encouraging support throughout the process

## Legacy Agents

### brief-assistant
Specialist agent that conducts the Brief Minimo interview and generates specifications, validation reports, or documentation.

**When to use**: When running `/brief` command

**Operating Modes**:
1. **New Agent** - Plan new agent from scratch (30 minutes)
2. **Update Existing** - Refine agent running in production (15-20 minutes)
3. **Validate Agent** - Check against Brief Minimo criteria (20 minutes)
4. **Document Existing** - Create brief retroactively (20 minutes)

**Responsibilities**:
- Detect project context (new vs existing)
- Welcome and explain the process
- Offer appropriate mode based on context
- Guide through adapted interview questions
- Collect concrete examples and specifics
- Validate completeness
- Generate comprehensive README.md, validation report, or updated brief
- Adapt interview flow based on mode

**Key Capabilities**:
- Context detection for seamless integration
- Mode-aware questioning adapted to user's situation
- Production agent documentation
- Legacy agent specification creation
- Quality assurance and validation
- Team alignment and knowledge preservation

## Support & Contributing

This is version 0.3.0 of Agentc AI Developer. It features Brief Minimo methodology with integrated microprocessos: `/brief` (Microprocesso 1.1 - planning), `/setup-local-observability` (Microprocesso 1.2 - environment setup), and `/update-claude-md` (project integration). Includes `help-assistant` for guidance throughout the process.

For issues, suggestions, or contributions related to the Claude Code marketplace, visit the [plugin repository](https://github.com/cadugevaerd/claudecode_plugins).

## License

MIT

## Author

**Carlos Araujo**
Email: [cadu.gevaerd@gmail.com](mailto:cadu.gevaerd@gmail.com)
Repository: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)

---

## Quick Links

- **Brief Minimo Methodology**: See `/brief` command for detailed explanation
- **Quick Start**: Run `/brief` to begin agent planning
- **Need Help?**: Use `help-assistant` for guidance during any microprocesso
- **Project Integration**: Run `/update-claude-md` after environment setup
- **Plugin Marketplace**: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)

Start planning your AI agent today with `/brief`!
