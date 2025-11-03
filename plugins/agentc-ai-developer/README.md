# Agentc AI Developer

Complete guide for developing AI agents from conception to production. This plugin features the **Brief Minimo** methodology - a lightweight but comprehensive 30-minute planning process that defines your agent's complete scope before any coding begins.

## Overview

Agentc AI Developer is your partner in building production-ready AI agents. It guides you through proven methodologies and best practices, starting with the Brief Minimo process.

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

Start your agent planning session with:

```bash
/brief
```

This launches an interactive interview that guides you through the Brief Minimo process. The agent automatically detects your context and offers relevant options.

## How It Works

### 1. Run the Command

```bash
/brief
```

### 2. Interactive Interview

The **brief-assistant** agent conducts a conversational interview:

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

**Version 0.1.0** (Current)
- Brief Minimo methodology with 4 operating modes
- Context detection (new vs existing projects)
- Interactive interview via `/brief` command
- Brief generation for new agents
- Agent update and refinement
- Agent validation and assessment
- Retroactive documentation for existing agents
- Seamless integration with existing projects

**Planned Features**
- Architecture & Design macroprocess
- Multi-step agent design patterns
- Testing and validation strategies
- Production deployment guides
- Advanced agent patterns (multi-agent, hierarchical, self-improving)
- Integration with version control (git history analysis)
- Collaborative briefing for team alignment

## Commands

### /brief
Launches the Brief Minimo 30-minute agent planning interview.

```bash
/brief
```

Conducts an interactive session and generates a comprehensive agent specification document.

## Agents

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

This is version 0.1.0 of Agentc AI Developer. It features Brief Minimo methodology with 4 operating modes, seamlessly integrating with both new and existing projects.

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
- **Agent Planning Guide**: See `agents/brief-assistant.md` for complete interview flow
- **Plugin Marketplace**: [claudecode_plugins](https://github.com/cadugevaerd/claudecode_plugins)

Start planning your AI agent today with `/brief`!
