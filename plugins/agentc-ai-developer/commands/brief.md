---
description: Interactive guide through Brief Minimo - 5 fundamental questions to define your AI agent. Collects structured responses, then uses brief-assistant agent for validation and README.md generation.
---

# Brief Minimo - AI Agent Planning

**Interactive command** that guides you through 5 fundamental questions to define your AI agent's scope, then delegates to the **brief-assistant** agent for validation and final documentation.

## The 5 Fundamental Questions

The Brief Minimo methodology asks you to answer these 5 clear questions:

1. **What does the agent DO?** - Core functionality in one clear action verb
2. **What is the INPUT?** - Data type, format, maximum size, real example
3. **What is the OUTPUT?** - Expected structure, success example, error example
4. **What is the TOOL/API?** - Single tool, access confirmation, cost, backup alternative
5. **What is SUCCESS?** - Quantifiable metric, minimum target, measurement method, dataset availability

## How It Works

When you run `/brief`:

### Step 1: Interactive Interview (In This Command)

You'll be guided through **5 questions** one at a time:

- Clear explanation of what each question means
- Examples of **good answers** (specific, concrete)
- Examples of **bad answers** (vague, incomplete)
- Space for your detailed response

**Time**: ~15-20 minutes to answer all 5 questions

### Step 2: Review & Confirmation

After all 5 answers are collected:

- Summary of your responses
- Confirmation that everything is clear
- Option to refine any answer

### Step 3: Agent Validation & Generation

Once confirmed, this command **calls the brief-assistant agent** to:

- Validate completeness of your responses
- Ask follow-up questions if needed (pushback on vague answers)
- Generate your final README.md with Brief Minimo specification
- Provide next steps for development

**Time**: ~10 minutes for agent validation + generation

---

## Getting Started

Simply run:

```bash
/brief
```

**What to have ready**:

- 15-20 minutes of focused time
- Clear idea of what your agent should do (or existing agent to document)
- Concrete examples (not conceptual descriptions)

**Respond with**:

- Specific details and examples
- Real sample data (not generic descriptions)
- Measurable metrics (not vague goals)
- Concrete implementation details (not "we'll figure it out later")

---

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

---

## The Brief Minimo Output

After completion, you'll have:

✅ **Agent Purpose** - Clear, single-sentence description with action verb
✅ **Input Specification** - Type, format, size limits, real examples
✅ **Output Specification** - Exact structure, success cases, error handling
✅ **Tool/API Requirements** - Primary tool, auth, costs, backup plan
✅ **Success Metrics** - Quantifiable targets, measurement method, validation strategy

All packaged in a **production-ready README.md** specification.

---

## Operating Modes (Agent-Detected)

After you provide your 5 answers, the **brief-assistant** agent will:

1. **Detect your context** - New agent vs existing project
2. **Ask follow-up questions** - Clarify any vague responses
3. **Suggest improvements** - Pushback if needed for specificity
4. **Generate documentation** - Create README.md or validation report
5. **Provide next steps** - Ready for architecture/design phase

---

## Example Flow

```text
You run: /brief

Command says:
  "Let's define your AI agent with 5 fundamental questions."
  [Brief explanation of process]

Q1: What does the agent DO?
  [Explanation + good/bad examples]
  Your answer: [You type detailed response]

Q2: What is the INPUT?
  [Explanation + good/bad examples]
  Your answer: [You type detailed response]

[... Questions 3, 4, 5 follow same pattern ...]

After Q5:
  [Command summarizes all 5 answers]
  "Ready to proceed? (y/n)"

You answer: Yes

Command says:
  "Calling brief-assistant for validation and README.md generation..."

Agent takes over:
  - Validates completeness
  - Asks follow-up questions if needed
  - Generates your final README.md
  - Provides next steps
```

---

## Why This Two-Step Approach?

**Command Step** (Interactive interview):

- Provides clear structure and guidance
- Ensures all 5 questions are answered
- Collects responses efficiently
- Sets stage for agent validation

**Agent Step** (Validation + generation):

- Applies intelligent analysis to responses
- Pushes back on vague answers
- Generates production-ready documentation
- Provides contextual advice and next steps

Together: **30 minutes of focused planning** that results in a **complete agent specification**.

---

After running `/brief`, you'll have everything needed to move forward with architecture and implementation. The brief becomes your specification reference throughout development.
