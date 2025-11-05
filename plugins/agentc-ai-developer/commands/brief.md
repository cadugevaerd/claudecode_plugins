---
description: "Interactive Brief Minimo interview - answer 5 fundamental questions to define your AI agent's scope and generate production-ready README.md specification"
allowed-tools: Read, Write, AskUserQuestion, Glob, Grep
argument-hint: ""
---

# Brief Minimo - Agent Planning Session

Run a complete, structured Brief Minimo planning session to define your AI agent's scope with precision.

## Core Questions Framework

The Brief Minimo process revolves around 5 fundamental questions that establish precise scope:

### Question 1: What does the agent DO?

Core functionality as single action verb (e.g., "Extract", "Validate", "Transform")

- **Request**: Concrete description with one clear responsibility
- **Validate**: Must be action-oriented, not conceptual

### Question 2: What is the INPUT?

Complete input specification

- **Request**: Data type, exact format, maximum size, real example
- **Validate**: Must include specific data structure or sample

### Question 3: What is the OUTPUT?

Complete output specification

- **Request**: Expected structure, success example, error example
- **Validate**: Must show concrete output samples, not descriptions

### Question 4: What is the TOOL/API?

Primary external tool or API dependency

- **Request**: Single tool name, access requirements, costs, backup alternative
- **Validate**: Must have confirmation of tool access availability

### Question 5: What is SUCCESS?

Quantifiable success metrics

- **Request**: Specific metric, minimum acceptable target, measurement method, dataset for validation
- **Validate**: Must be measurable, not subjective

## Execution Workflow

### Phase 1: Discovery & Validation

**Steps 1-2**: Quick-path if brief already defined

1. Search the repository for existing Brief Minimo documentation (BRIEF.md, README.md, docs/)
2. If all 5 questions are found and documented:
   - Confirm understanding with user
   - If confirmed → Skip to Phase 3 (Generation)
   - If not confirmed → Proceed to Phase 2

### Phase 2: Interactive Interview

**Steps 3-4**: Detailed planning session if starting fresh

3. Interview user to collect all 5 questions:
   - Ask each question sequentially
   - After each response:
     - Provide feedback on specificity level
     - Flag vague or conceptual responses as needing more detail
     - Request real examples if description is too generic
     - Continue to next question only when response meets specificity threshold

4. Set clear expectations during interview:
   - All metrics must be measurable (not subjective)
   - All examples must be concrete (not generic)
   - Answers define the entire architecture going forward

### Phase 3: Documentation Generation

**Steps 5-6**: Create official Brief Minimo specification

5. Generate official Brief Minimo documentation:
   - **Location**: Create `docs/BRIEF.md` (or update `README.md` in project root)
   - **Sections**:
     - **Agent Purpose**: Single sentence with action verb from Q1
     - **Input Specification**: Complete details from Q2 with real examples
     - **Output Specification**: Structure and samples from Q3 (both success & error cases)
     - **Tool/API Requirements**: Details from Q4 with access confirmation
     - **Success Metrics**: Quantifiable targets from Q5 with measurement method
     - **Next Steps**: Reference to `/setup-local-observability` for environment setup
   - **Quality Assurance**:
     - Ensure all examples use real, specific data (not generic placeholders)
     - Verify all metrics are measurable and achievable
     - Confirm all responses are concrete and action-oriented

6. Post-Generation Review (final step):
   - Display generated documentation to user for review
   - Offer option to refine any section
   - Confirm file is saved to project repository
   - Provide reference: *"Brief Minimo specification is now your source of truth for architecture and development"*
   - Suggest next step: `/setup-local-observability` to configure local environment

## Quality Checkpoints

| Question | Specificity Check | Real Data | Example Required |
|----------|------------------|-----------|------------------|
| Q1 (DO) | Action verb present | Yes | Responsibility statement |
| Q2 (INPUT) | Data structure defined | Yes | Sample data |
| Q3 (OUTPUT) | Both success & error | Yes | Sample outputs |
| Q4 (TOOL/API) | Access confirmed | Yes | Tool requirements |
| Q5 (SUCCESS) | Measurable metric | Yes | Measurement method |

## Integration

- **Previous step**: Project initialization or architecture planning
- **Next step**: `/setup-local-observability` for local environment configuration
- **Related**: `/spike-agentic` to implement agent with agentic loop based on Brief Minimo
