---
description: 100% interactive Brief Minimo interview - 5 fundamental questions to define your AI agent's scope. Collects structured responses, validates completeness, and generates production-ready README.md specification. No agent delegation - complete process in single command.
---

# Brief Minimo - AI Agent Planning

**INTERACTIVE**: Guides you through a complete 30-minute Brief Minimo planning session - no agent delegation.

Fully interactive command that asks 5 fundamental questions, validates your responses for specificity, and generates a production-ready README.md specification document.

## TL;DR

`/brief` → Answer 5 questions → Validation → README.md specification

**Time**: ~30 minutes
**Result**: Complete Brief Minimo specification ready for architecture & development

## ⚠️ Prerequisites

- ✅ 15-20 minutes of focused time
- ✅ Clear idea of what your agent should do (or existing agent to update/document)
- ✅ Concrete examples ready (not conceptual descriptions)
- ✅ Be prepared to think about specific metrics and tools

## The 5 Fundamental Questions

The Brief Minimo methodology asks you to answer these 5 clear questions:

1. **What does the agent DO?** - Core functionality in one clear action verb
1. **What is the INPUT?** - Data type, format, maximum size, real example
1. **What is the OUTPUT?** - Expected structure, success example, error example
1. **What is the TOOL/API?** - Single tool, access confirmation, cost, backup alternative
1. **What is SUCCESS?** - Quantifiable metric, minimum target, measurement method, dataset availability

## How It Works

When you run `/brief`, you engage in a **fully self-contained interactive interview**:

### Step 1: Initial Context Detection

Command checks:

- Are you in a new project or existing project with agents?
- This determines if you're creating new agent or updating existing

### Step 2: Interactive Interview (Single Command)

You'll be guided through **5 questions** one at a time, in conversation:

- Clear explanation of what each question means
- Examples of **good answers** (specific, concrete, measurable)
- Examples of **bad answers** (vague, incomplete, wishful thinking)
- Space for your detailed response
- **If your answer is vague**: The command pushes back gently with follow-up questions
  - "Can you show me a concrete example?"
  - "What specific percentage or number?"
  - "Which ONE tool would you start with?"

**Time**: ~30 minutes for complete interview + validation + generation

### Step 3: Review & Confirmation

After all 5 answers are collected:

- Full summary of your responses
- Validation check: Are all answers specific? (not vague)
- Option to refine any answer before proceeding
- Confirmation that everything is clear

### Step 4: README.md Generation

Once confirmed, command **generates your production-ready specification** including:

- Your agent's complete Brief Minimo specification
- Input/output examples
- Tool/API requirements
- Success metrics and measurement strategy
- Next steps for development
- Everything you need to move to architecture and design phase

## Getting Started

Simply run:

````bash
/brief

```text

**What to have ready**:

- 15-20 minutes of focused time
- Clear idea of what your agent should do (or existing agent to document)
- Concrete examples (not conceptual descriptions)

**Respond with**:

- Specific details and examples
- Real sample data (not generic descriptions)
- Measurable metrics (not vague goals)
- Concrete implementation details (not "we'll figure it out later")


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


## The Brief Minimo Output

After completion, you'll have:

✅ **Agent Purpose** - Clear, single-sentence description with action verb
✅ **Input Specification** - Type, format, size limits, real examples
✅ **Output Specification** - Exact structure, success cases, error handling
✅ **Tool/API Requirements** - Primary tool, auth, costs, backup plan
✅ **Success Metrics** - Quantifiable targets, measurement method, validation strategy

All packaged in a **production-ready README.md** specification.


## Complete Interview Flow (All in This Command)

When you run `/brief`, you go through this complete flow:

```text
Step 1: Context Detection
  ✓ Are you in new project or existing project?
  ✓ Adjust questions accordingly

Step 2: Interactive Interview (5 Questions)
  Q1: What does the agent DO?
      [Explanation + good/bad examples]
      Your answer: [You provide detailed response]
      Command validates specificity - if vague, asks follow-ups

  Q2: What is the INPUT?
      [Explanation + good/bad examples]
      Your answer: [You provide detailed response]
      Command validates format and size details

  Q3: What is the OUTPUT?
      [Explanation + good/bad examples]
      Your answer: [You provide detailed response]
      Command validates structure clarity

  Q4: What is the TOOL/API?
      [Explanation + good/bad examples]
      Your answer: [You provide detailed response]
      Command validates single tool focus, not multiple

  Q5: What is SUCCESS?
      [Explanation + good/bad examples]
      Your answer: [You provide detailed response]
      Command validates quantifiable metrics

Step 3: Review & Validation
  [Command summarizes all 5 answers]
  [Checks for vagueness - asks follow-ups if needed]
  "Everything clear? Ready to generate README.md? (y/n)"

Step 4: README.md Generation
  Command generates:
  ✅ Complete Brief Minimo specification
  ✅ Formatted and ready for production
  ✅ Next steps for architecture & development
  ✅ Saved to your project directory

```text

**Total time**: ~30 minutes from start to finished README.md


## Red Flags - Command Will Push Back

If you answer vaguely, the command will gently push back:

| If you say | Command pushes back |
|-----------|-------------------|
| "We'll figure it out later" | "Let's nail this now while thinking through requirements. This takes 2 minutes." |
| "Maybe multiple tools" | "Let's start with ONE primary tool. You can add complexity later. Which one matters most?" |
| "It should be accurate" | "What does accurate mean? 80%? 95%? How will you measure it?" |
| "The input can be anything" | "What's the most common format? What's the maximum size? Let's be specific." |
| "Success is when it works" | "Perfect. What does 'works' mean numerically? How many out of 100?" |

This ensures your brief is **complete and specific**, not wishful thinking.


After running `/brief`, you'll have:

✅ Complete Brief Minimo specification in README.md
✅ Everything needed for architecture and design
✅ Crystal-clear input/output examples
✅ Quantifiable success metrics
✅ Tool/API requirements validated
✅ Ready for Microprocesso 1.2 (`/setup-local-observability`)

The brief becomes your specification reference throughout development.
````
