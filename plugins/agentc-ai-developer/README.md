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
1. **What is the INPUT?** - Type, format, maximum size, real example
1. **What is the OUTPUT?** - Expected structure, success example, error example
1. **What is the TOOL/API?** - Single tool, access confirmation, cost, backup alternative
1. **What is SUCCESS?** - Quantifiable metric, minimum target, measurement method, dataset availability

## Installation

````bash
/plugin install agentc-ai-developer

```text

## MCP Integration

**Model Context Protocol (MCP)** integration provides real-time access to LangChain and LangGraph documentation during development.

### What is MCP?

MCP (Model Context Protocol) is an open standard that connects LLMs with external tools and data sources. This plugin uses MCP to access:

- **LangChain Documentation**: Latest Python LangChain API reference and guides
- **LangGraph Documentation**: Up-to-date LangGraph patterns and best practices

### Benefits

✅ **Always Up-to-Date**: Access latest documentation without manual updates
✅ **Context-Aware Help**: Get relevant examples during `/spike-agentic` and development
✅ **Faster Development**: Quick access to API signatures and usage patterns
✅ **Best Practices**: Learn from official documentation and examples

### How It Works

The MCP server is automatically configured when you install the plugin. It uses:

- **Transport**: stdio (standard input/output)
- **Tool**: `mcpdoc` via `uvx` (no manual installation needed)
- **Sources**:
  - LangChain: `https://python.langchain.com/llms.txt`
  - LangGraph: `https://langchain-ai.github.io/langgraph/llms.txt`

### Usage

MCP documentation is automatically available during:

- **`/spike-agentic`**: Get LangGraph architecture patterns and code examples
- **`/novo-incremento`**: Access API references while implementing features
- **Development**: Query LangChain/LangGraph docs on-demand through Claude Code

No additional configuration required - it just works! 🚀

## Quick Start

### Microprocesso 1.1: Planning with Brief Minimo

Start your agent planning session:

```bash
/brief

```text

This launches an interactive interview that guides you through the Brief Minimo process. The agent automatically detects your context and offers relevant options.

**Result**: README.md with complete agent specification ✅

### Microprocesso 1.2: Environment Setup & Observability

After `/brief` creates your project repository, continue with environment setup:

```bash
/setup-local-observability

```text

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

```text

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

```text

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

```text

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

```text

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

```text

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

```text

## Using in Existing Projects

The plugin works seamlessly with existing projects:

1. **Run `/brief`** - Agent detects your existing setup
2. **Choose Mode** - Select from: New Agent, Update, Validate, or Document
3. **Answer Questions** - Brief interview adapted to your mode
4. **Get Output** - New specification, updated brief, validation report, or documentation
5. **Use as Reference** - Keep brief as specification for future improvements

### Example: Updating a Production Agent

```text

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

```text

### Example: Documenting a Legacy Agent

```text

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

```text

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

```text

Success example:

```json
{
  "priority": "high",
  "category": "system_outage",
  "summary": "Production database unreachable",
  "action_required": true
}

```text

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

**Version 0.5.0** (Current)
- **Microprocesso 1.1**: Brief Minimo planning methodology (fully interactive `/brief` command)
- **Microprocesso 1.2**: Environment setup with Python venv, dependencies, and LangSmith observability
- **Microprocesso 1.2 Skill**: `microprocesso-1-2` skill with comprehensive setup knowledge and progressive disclosure
- **Microprocesso 1.3**: Spike Agentic with agentic loop validation (autonomous `/spike-agentic` command + skill)
- **Microprocesso 1.3 Skill**: `spike-agentic` skill with LangGraph architecture guidance and agentic loop knowledge
- **Project Integration**: `/update-claude-md` command for CLAUDE.md setup (≤40 lines, progressive disclosure)
- **Help Assistant**: Specialized support for guidance and troubleshooting (help-assistant agent)
- Interactive commands: `/brief`, `/setup-local-observability`, `/spike-agentic`, `/update-claude-md`
- Skills with auto-discovery for detailed guidance
- Seamless integration with existing projects
- Environment validation and reproducibility
- Complete observability integration with LangSmith

**Planned Features**
- **Microprocesso 1.4**: Agent Robustness (error handling, real tools, production tests)
- **Microprocesso 1.5**: Stakeholder Validation
- Architecture & Design documentation
- Multi-step agent design patterns
- Advanced agent patterns (multi-agent, hierarchical, self-improving)
- Integration with version control (git history analysis)
- Collaborative briefing for team alignment
- CI/CD integration for automated validation

## Commands

### /brief
Launches the **Microprocesso 1.1** - Brief Minimo 30-minute agent planning interview.

```bash
/brief

```text

Conducts an interactive session and generates a comprehensive agent specification document (README.md) with complete agent specification.

### /setup-local-observability
Launches the **Microprocesso 1.2** - Interactive environment setup and configuration guide.

```bash
/setup-local-observability

```text

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

```text

Reads your Brief Minimo specification from README.md and creates a focused CLAUDE.md section (≤40 lines) with:
- Available Agentc commands and when to use them
- Links to full plugin documentation
- Next steps for ongoing development
- Support for help-assistant

Follows progressive disclosure pattern - keeps CLAUDE.md lightweight while referencing comprehensive docs.

### /spike-agentic
Launches the **Microprocesso 1.3** - Agent spike with agentic loop validation (3-4 hours).

```bash
/spike-agentic

```text

Validates that Microprocesso 1.2 is complete, then generates `docs/microprocesso-1.3-spike-agentic.md` with:
- Prerequisites validation checklist
- Phase 2: Build LangGraph with 4 nodes + agentic loop
- Phase 3: Happy-path tests (with/without tool)
- Phase 4: LangSmith observability validation
- Complete code snippets ready to implement

Validates architecture viability by confirming the **agentic loop** (Think → Act → Observe → Think again) works correctly.

### /backlog
Manages development backlog with slice creation, prioritization, and tracking.

```bash
/backlog create       # Create BACKLOG.md with initial slices
/backlog view        # View current backlog status
/backlog update      # Update slice priorities and status

```text

Organizes slices for Microprocesso Stage 2 (development) with features:
- Auto-generated slice templates with acceptance criteria
- Prioritization scoring (Impact × Success Weight)
- Fast-Track identification for quick wins
- Issue tracking and dependencies

### /analyze-slices
Validates slices against S1.1 decision gates and prepares them for development.

```bash
/analyze-slices          # Analyze all slices
/analyze-slices validate # Validate specific slice gates
/analyze-slices refine   # Suggest refinements for failed gates
/analyze-slices auto     # Auto-refine and update status

```text

Executes 5 decision gates:
1. **Gate 1**: Duration 3-6h
2. **Gate 2**: Score ≥ 2.0 (Impact / Hours/3)
3. **Gate 3**: Reversible (rollback plan exists)
4. **Gate 4**: Isolated (low coupling)
5. **Gate 5**: Increases success_rate

Creates `docs/slices/SLICE_N_TRACKER.md` for each GO slice with:
- Planning section (Section 1)
- Placeholder for development tracking (Section 2+)
- Decision gates evaluation results

### /iniciar-slice
Begins development on next slice from backlog.

```bash
/iniciar-slice       # Interactive mode - select slice and confirm
/iniciar-slice auto  # Auto-select highest priority TODO slice

```text

For selected slice:
1. Creates git branch: `slice-{N}-{kebab-case-title}`
2. Captures baseline metrics (success_rate, test_count, latency)
3. Updates `SLICE_N_TRACKER.md` Section 2 (DESENVOLVIMENTO)
4. Initializes development checklist and environment setup

Results in:
- Active git branch with baseline metrics
- Ready-to-code development environment
- Tracked progress in SLICE_TRACKER.md

### /novo-incremento
Creates the next incremental development task within active slice.

```bash
/novo-incremento       # Interactive - review and accept AI suggestion
/novo-incremento auto  # Auto-accept AI suggestion

```text

Analysis-driven increment creation:
1. **Analyzes current state**: Pending criteria, git history, code direction
2. **Suggests next increment**: Ensures ≤30 lines, 15-20 min, testable
3. **Creates Section 3**: Documents Incremento with checklist
4. **Validates criteria**: Acceptance criteria, reversibility, testability

Each increment addresses 1-2 acceptance criteria with specific activities:
- Atomic code changes (≤30 lines)
- Testing requirements (TDD approach)
- Regression validation checkpoints

### /finalizar-incremento
Completes current increment with comprehensive validation.

```bash
/finalizar-incremento   # Interactive - review all validations

```text

Validation pipeline:
1. **Metrics Collection**: Runs CI.py to capture success_rate, test_count, latency
2. **Coverage Validation** (BLOCKING): Ensures test coverage ≥70% with pytest-cov
3. **Regression Detection**: Confirms no tests broken, maintains test_count
4. **Self-Review Checklist**: Code quality, testing completeness, architecture
5. **Automatic Decision**: Applies 3 stopping criteria:
   - Success rate ≥ target?
   - Regressão = 0?
   - Self-review ✅?

Updates `SLICE_TRACKER.md` Section 3 with:
- Final metrics and deltas
- Coverage report
- Regression analysis
- Decision: Continue or Conclude Slice

**If all 3 criteria met**: Suggests `/concluir-slice` to finalize

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

## Skills

### microprocesso-1-2
Complete knowledge base for Microprocesso 1.2 (Setup Local + Observability) - Python virtual environment setup, dependency installation, .env configuration, LangSmith integration, validation, and troubleshooting.

**When Claude auto-invokes**: When you need detailed guidance on Microprocesso 1.2 setup activities, encounter errors during environment configuration, or need troubleshooting help with dependencies, .env files, or LangSmith integration.

**Responsibilities**:
- Provide step-by-step guidance for all 8 setup activities
- Document Python venv creation and activation
- Explain dependency installation (langchain, anthropic, langsmith, python-dotenv)
- Guide .env file configuration with templates
- Detail .env.example documentation
- Explain requirements.txt creation and reproducibility
- Document .gitignore setup for secret protection
- Provide LangSmith integration testing
- Supply comprehensive validation scripts
- Offer troubleshooting for common setup issues
- Explain all three operating modes (Guiado, Automático, Misto)

**Key Capabilities**:
- Hands-on environment setup guidance with copy/paste templates
- Complete troubleshooting for Python venv, dependencies, and configuration
- LangSmith integration testing and validation
- Environment validation scripts (validate_setup.py)
- Progressive disclosure pattern with detailed knowledge
- Support for all three operating modes with mode-specific instructions
- Real examples and sample code for every activity

**Auto-discovery**: This skill is automatically used by Claude when you request help with Microprocesso 1.2, mention setup issues, or need detailed guidance on any of the 8 activities.

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

## Work Keywords

- **"create brief"** / **"agent specification"** / **"start planning"**: Execute `/brief`
- **"setup environment"** / **"configure local"** / **"install dependencies"**: Execute `/setup-local-observability`
- **"create spike"** / **"validate architecture"** / **"spike implementation"**: Execute `/spike-agentic`
- **"create backlog"** / **"generate backlog"**: Execute `/backlog create`
- **"update backlog"** / **"refresh backlog"**: Execute `/backlog update`
- **"view backlog"** / **"show backlog"** / **"backlog status"**: Execute `/backlog view`
- **"analyze slices"** / **"validate gates"** / **"slice validation"**: Execute `/analyze-slices`
- **"start slice"** / **"begin development"** / **"start coding slice"**: Execute `/iniciar-slice`
- **"create increment"** / **"next increment"** / **"start increment"**: Execute `/novo-incremento`
- **"complete increment"** / **"finish increment"** / **"validate increment"**: Execute `/finalizar-incremento`
- **"update project config"** / **"integrate agentc"**: Execute `/update-claude-md`

## Support & Contributing

This is version 0.10.0 of Agentc AI Developer. It features Brief Minimo methodology with integrated microprocessos and stage 2 development workflow:
- **Microprocesso 1.1** - `/brief` (Planning)
- **Microprocesso 1.2** - `/setup-local-observability` (Environment setup)
- **Microprocesso 1.3** - `/spike-agentic` (Architecture validation)
- **Stage 2 Development** - `/backlog`, `/analyze-slices`, `/iniciar-slice` (Slice management)
- **Stage 2 Dev Loop** - `/novo-incremento`, `/finalizar-incremento` (Incremental development with metrics validation)
- **Project Integration** - `/update-claude-md` (CLAUDE.md setup)
- **MCP Integration** - Real-time LangChain/LangGraph documentation access

Includes `help-assistant` agent, `microprocesso-1-2` and `spike-agentic` skills for comprehensive guidance with progressive disclosure. Full incremental development workflow with automatic metrics validation, coverage checking (≥70%), regression detection, and decision logic. MCP support for always-updated LangChain/LangGraph docs.

For issues, suggestions, or contributions related to the Claude Code marketplace, visit the [plugin repository](https://github.com/cadugevaerd/claudecode_plugins).

## License

MIT

## Author

**Carlos Araujo**
Email: [cadu.gevaerd@gmail.com](mailto:cadu.gevaerd@gmail.com)
Repository: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)


## Quick Links

- **Brief Minimo Methodology**: See `/brief` command for detailed explanation
- **Quick Start**: Run `/brief` to begin agent planning
- **Need Help?**: Use `help-assistant` for guidance during any microprocesso
- **Project Integration**: Run `/update-claude-md` after environment setup
- **Plugin Marketplace**: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)

Start planning your AI agent today with `/brief`!
````
