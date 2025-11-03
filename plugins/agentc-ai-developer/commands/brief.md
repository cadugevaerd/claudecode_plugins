---
description: Interactive guide to create or update AI agent briefs. Plans new agents in 30 minutes or refines existing ones. Detect context automatically (new vs existing project).
---

# Brief Minimo - AI Agent Planning

This command guides you through the **Brief Minimo** methodology - a structured 30-minute process to define your AI agent's complete scope before writing any code.

It works with **new agents** and integrates seamlessly with **existing projects**.

## What is Brief Minimo?

Brief Minimo is a lightweight but comprehensive agent planning methodology that answers 5 fundamental questions:

1. **What does the agent DO?** - Core functionality in one clear action verb
2. **What is the INPUT?** - Data type, format, maximum size, real example
3. **What is the OUTPUT?** - Expected structure, success example, error example
4. **What is the TOOL/API?** - Single tool, access confirmation, cost, backup alternative
5. **What is SUCCESS?** - Quantifiable metric, minimum target, measurement method, dataset availability

## Usage Modes

The **brief-assistant** agent automatically detects your context and offers appropriate options:

### Mode 1: New Agent
**When**: Starting a new agent from scratch
**Output**: Complete specification document (README.md)
**Time**: 30 minutes

### Mode 2: Existing Agent Update
**When**: Refining or updating an already developed agent
**Use Case**: Document production agents, refine scope, plan improvements
**Output**: Updated brief reflecting current implementation

### Mode 3: Validate Agent
**When**: Checking if existing agent matches Brief Minimo criteria
**Use Case**: Quality assurance, scope verification, completeness check
**Output**: Validation report with gaps and recommendations

### Mode 4: Document Existing Agent
**When**: Adding brief documentation to already-built agents
**Use Case**: Retroactive documentation, team alignment, onboarding
**Output**: Brief specification for existing implementation

## How It Works

When you run `/brief`, the **brief-assistant** agent will:

1. **Detect Context** - Identify if you're in a new or existing project
2. **Offer Options** - Present relevant modes based on detected context
3. **Guide Workflow** - Conduct interactive interview for chosen mode
4. **Collect Specifics** - Emphasize concrete examples and measurable criteria
5. **Validate Data** - Ensure all essential information is complete
6. **Generate Output** - Create appropriate documentation

## Output

Depending on your mode:

- **New Agent** → Comprehensive README.md specification
- **Existing Agent Update** → Updated brief reflecting current state
- **Validate** → Validation report with recommendations
- **Document Existing** → Brief specification retroactively created

All outputs include:

- Agent's core purpose and functionality
- Detailed input/output specifications with examples
- Tool/API requirements and access details
- Success metrics and measurement strategy
- Next steps in development or improvement

## Getting Started

Simply run:

```bash
/brief
```

The **brief-assistant** agent will detect your context and guide you through the process.

Respond to each question with as much detail as possible:

- Provide concrete examples (not vague descriptions)
- Be specific about formats and sizes
- Include real data samples
- Define measurable success criteria

## Why Brief Minimo?

This methodology prevents common agent planning failures:

| Problem | Solution |
|---------|----------|
| ❌ Vague requirements | ✅ Crystal clear specifications |
| ❌ Scope creep | ✅ Focused single responsibility |
| ❌ Undefined success | ✅ Quantifiable metrics |
| ❌ Technical surprises | ✅ Tool/API validation upfront |
| ❌ Hidden costs | ✅ Budget awareness from day one |
| ❌ No documentation | ✅ Complete specification as-built |

## Using in Existing Projects

If you're in a project that already has agents:

1. **Run `/brief`** - Agent detects your existing setup
2. **Choose Mode** - Select from: Update, Validate, or Document Existing
3. **Answer Questions** - Brief interview about your agent
4. **Get Output** - Updated brief or validation report
5. **Use Reference** - Keep brief as specification for future improvements

## Next Steps After Brief

Once you complete your Brief Minimo:

1. For **new agents**: Your specification is ready for architecture and design
2. For **existing agents**: Brief serves as baseline for improvements and team alignment
3. Documentation phase: Brief becomes the reference for maintenance
4. Future work: Use brief as baseline for enhancements and scaling

---

Use the **brief-assistant** agent to get started. This is a conversational, interactive process - be as detailed as possible with your answers.
