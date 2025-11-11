---
description: Generate 5-10 user stories with BDD acceptance criteria from Brief Minimo specification
allowed-tools: Read, Write, Glob, AskUserQuestion
model: claude-sonnet-4-5
argument-hint: ''
---

# Create User Histories

Generate comprehensive user stories with BDD acceptance criteria based on Brief Minimo specification and agent scope.

## 🎯 Objective

Create 5-10 user stories following agile best practices that:

- Align with Brief Minimo specification (agent purpose, inputs, outputs, success metrics)
- Follow standard format: "As a [persona], I want [goal], so that [benefit]"
- Include BDD acceptance criteria in Given-When-Then format
- Are independently testable and deliverable
- Cover core functionality, edge cases, and error handling
- Provide clear validation criteria for each story

## 🔧 Instructions

### 1. Locate and Read Brief Minimo Specification

1.1 **Search for Brief Documentation**

- Use `Glob` to search for Brief Minimo documentation in standard locations:
  - `docs/BRIEF.md`
  - `README.md` (section with Brief Minimo)
  - `docs/README.md`
  - `BRIEF_*.md` files
- If multiple files found: Read all and combine information
- If no files found: Report error and suggest running `/brief` first

1.2 **Extract Key Information from Brief**

Extract and validate presence of all 5 Brief Minimo components:

- **Q1 - Agent Purpose**: What the agent DOES (action verb)
- **Q2 - Input Specification**: Data type, format, size, examples
- **Q3 - Output Specification**: Structure, success/error samples
- **Q4 - Tool/API Requirements**: External dependencies
- **Q5 - Success Metrics**: Quantifiable targets and measurement

1.3 **Validate Brief Completeness**

- If any component missing: Report incomplete Brief and suggest re-running `/brief`
- If all components present: Proceed to user story generation

### 2. Identify Personas and User Contexts

2.1 **Derive Primary Personas**

Based on agent purpose and inputs, identify 2-4 primary personas:

- **Technical personas**: Developer, API consumer, System integrator
- **Business personas**: Product manager, Data analyst, End user
- **Operational personas**: DevOps engineer, Support team, Admin

2.2 **Map Personas to Agent Interactions**

For each persona, identify:

- Primary goal when using the agent
- Context of interaction (when/why they use it)
- Expected outcomes and benefits

### 3. Generate User Stories (5-10 Stories)

3.1 **Story Distribution Strategy**

Generate stories covering:

- **Happy path scenarios** (3-4 stories): Core functionality with valid inputs
- **Edge cases** (2-3 stories): Boundary conditions, unusual inputs
- **Error handling** (1-2 stories): Invalid inputs, API failures, timeouts
- **Performance/Quality** (1 story): Success metrics validation

3.2 **User Story Format**

For each story, use Connextra template:

```markdown
### Story [ID]: [Short Title]

**As a** [persona]
**I want** [specific goal/action]
**So that** [clear benefit/value]

**Priority**: [HIGH | MEDIUM | LOW]
**Estimated Effort**: [1-6 hours] (precise, e.g., 2.5h)
**Impact**: [1-10] (business value)
```

3.3 **Story Quality Criteria - INVEST Framework**

Ensure EVERY story meets ALL 6 INVEST criteria (required for validation):

**I - Independent (15 points in validation):**

- Story can be developed without waiting for other stories
- If dependencies exist: MUST document them explicitly
- Avoid circular dependencies
- ✅ Good: "Classify email urgency using keywords"
- ❌ Bad: "Complete previous story first, then classify"

**N - Negotiable (10 points in validation):**

- Flexible implementation approach
- Focuses on WHAT, not HOW
- Room for technical discussion
- ✅ Good: "Extract deadline from email text"
- ❌ Bad: "Use regex pattern /\\d{2}/\\d{2}/\\d{4}/ to extract deadline"

**V - Valuable (20 points in validation):**

- **Persona (10 pts)**: MUST be specific role, not generic
  - ✅ Excellent: "Sales professional", "DevOps engineer", "API developer"
  - ⚠️ Acceptable: "Developer", "Manager" (generic but identifiable)
  - ❌ Fails validation: "User", "Person", "Someone"
- **Benefit (10 pts)**: MUST be clear WHY (>10 characters)
  - ✅ Excellent: "Not lose critical proposal deadlines" (36 chars)
  - ⚠️ Acceptable: "Save time" (10 chars - minimum)
  - ❌ Fails validation: "To work" (7 chars), "Funciona" (8 chars)

**E - Estimable (15 points in validation):**

- MUST have precise estimate in hours
- ✅ Excellent: "2.5h", "4h" (precise)
- ⚠️ Acceptable: "2-3h" (range)
- ❌ Fails validation: "~5h?", "few hours", no estimate

**S - Small (15 points in validation):**

- MUST fit in 1-6 hours (ideal: 2-3h)
- ✅ Excellent: 2-3 hours
- ⚠️ Warning: 0.5-1h (too small - consider grouping)
- ⚠️ Warning: 6-8h (large - consider splitting)
- ❌ Fails validation: >8 hours (must split into 2-3 stories)

**T - Testable (25 points in validation):**

- **AC Count (5 pts)**: MUST have 3-5 acceptance criteria
  - ✅ Optimal: 3-5 ACs
  - ⚠️ Acceptable: 2 ACs
  - ❌ Fails validation: \<2 ACs or >5 ACs
- **AC Specificity (20 pts)**: ALL ACs MUST be measurable
  - ✅ Excellent: "success_rate >= 80%", "latency < 2s", "HTTP 200 response"
  - ⚠️ Acceptable: "Returns valid JSON structure" (somewhat specific)
  - ❌ Fails validation: "Works correctly", "Functions well", "Is ok"

3.4 **Impact/Hours Ratio Calculation**

For prioritization, calculate ratio for each story:

```
Ratio = Impact (1-10) / Estimated Hours
```

Target ratios (will be validated):

- 🔥 Excellent: > 3.0 (high value, low effort)
- ✅ Good: 1.5-3.0 (balanced)
- ⚠️ Medium: 1.0-1.5 (consider refining)
- ❌ Poor: < 1.0 (may not be worth implementing)

**Example:**

- Story: Impact=8, Hours=2.5 → Ratio=3.2 🔥 EXCELLENT
- Story: Impact=5, Hours=8 → Ratio=0.625 ❌ POOR (reconsider)

### 4. Write BDD Acceptance Criteria (Given-When-Then)

4.1 **Acceptance Criteria Format**

For each story, define 2-5 scenarios using Given-When-Then:

```markdown
**Acceptance Criteria:**

**Scenario 1: [Descriptive scenario name]**
- **Given** [initial context/preconditions]
- **When** [action or event occurs]
- **Then** [expected outcome with observable behavior]

**Scenario 2: [Descriptive scenario name]**
- **Given** [initial context/preconditions]
- **When** [action or event occurs]
- **Then** [expected outcome with observable behavior]
```

4.2 **Criteria Quality Guidelines**

- **Given**: Describe system state and preconditions (use concrete examples from Q2-Input)
- **When**: Single, specific action (use agent action from Q1)
- **Then**: Observable, testable outcome (reference Q3-Output and Q5-Success Metrics)
- Use exact data samples from Brief Minimo examples
- Include both positive and negative test scenarios
- Make criteria specific enough to be automated with pytest/behave

### 5. Organize and Save User Stories

5.1 **Create User Stories Document**

Generate `docs/USER_STORIES.md` with structure:

```markdown
# User Stories - [Agent Name]

**Brief**: [One-line agent purpose from Q1]
**Success Metric**: [From Q5]

## Stories Overview

| ID | Title | Persona | Priority | Effort |
|----|-------|---------|----------|--------|
| US-01 | [Title] | [Persona] | HIGH | 3 |
| US-02 | [Title] | [Persona] | MEDIUM | 2 |
| ... | ... | ... | ... | ... |

## Detailed Stories

[Individual stories with acceptance criteria]
```

5.2 **Link to Brief Minimo**

- Reference Brief Minimo components in each story
- Include traceability matrix showing which stories cover which Q1-Q5 components
- Validate that all Brief components are covered by at least one story

5.3 **Final Validation Checklist**

Before saving:

- [ ] 5-10 user stories generated (not fewer, not more)
- [ ] All stories follow "As a... I want... So that..." format
- [ ] Each story has 2-5 BDD acceptance criteria scenarios
- [ ] All acceptance criteria use Given-When-Then format
- [ ] Stories cover happy path, edge cases, and errors
- [ ] All Brief Minimo components (Q1-Q5) are covered
- [ ] Personas are clearly defined and relevant
- [ ] Priority and effort estimates assigned
- [ ] Output file saved to `docs/USER_STORIES.md`
- [ ] Traceability to Brief components documented

### 6. Report Completion

Display summary:

```text
✅ User Stories created successfully!
📁 Location: docs/USER_STORIES.md
📊 Stories generated: [X]
👥 Personas: [List]
🎯 Coverage: [% of Brief components covered]
🔗 Next step: Use stories to guide `/backlog` or `/spike-agentic`
```

## 📊 Output Format

### Document Structure: `docs/USER_STORIES.md`

```markdown
# User Stories - [Agent Name from Brief]

**Agent Purpose**: [From Q1 - What agent DOES]
**Success Metric**: [From Q5 - Quantifiable target]
**Last Updated**: [Date]

---

## 📋 Stories Overview

| ID | Story Title | Persona | Priority | Effort | Impact | Ratio | Brief Component |
|----|-------------|---------|----------|--------|--------|-------|-----------------|
| US-01 | Process valid input successfully | API Consumer | HIGH | 2.5h | 8 | 3.2 🔥 | Q1, Q2, Q3 |
| US-02 | Handle malformed input gracefully | Developer | HIGH | 2h | 7 | 3.5 🔥 | Q2, Q3 |
| US-03 | Validate edge case boundary | Data Analyst | MEDIUM | 2h | 5 | 2.5 ✅ | Q2, Q5 |
| US-04 | Recover from API timeout | System Integrator | MEDIUM | 3h | 6 | 2.0 ✅ | Q4 |
| US-05 | Meet performance success metric | Product Manager | HIGH | 3h | 9 | 3.0 🔥 | Q5 |

**Total Stories**: 5
**Personas**: 4 unique personas (all specific, not generic "user")
**Brief Coverage**: 100% (all Q1-Q5 components covered)
**Average Ratio**: 2.84 (Excellent - all stories > 1.5)
**Estimated Validation Score**: 95/100 (INVEST compliant)

---

## 📖 Detailed User Stories

### Story US-01: Process valid input successfully

**As a** API Consumer
**I want** to submit a valid request and receive processed output
**So that** I can integrate the agent into my production workflow

**Priority**: HIGH
**Estimated Effort**: 2.5h (precise)
**Impact**: 8/10 (high business value)
**Ratio**: 8 / 2.5 = 3.2 🔥 EXCELLENT
**Brief Components**: Q1 (Agent Purpose), Q2 (Input), Q3 (Output)

**INVEST Validation:**
- ✅ Independent: No dependencies
- ✅ Negotiable: Flexible implementation
- ✅ Valuable: Specific persona "API Consumer" (not generic), clear benefit >10 chars
- ✅ Estimable: Precise 2.5h estimate
- ✅ Small: Within 1-6h range
- ✅ Testable: 3 specific, measurable ACs

**Acceptance Criteria:**

**Scenario 1: Valid input returns successful output**
- **Given** an input matching the exact format from Brief Q2 (e.g., JSON with required fields)
- **When** I invoke the agent with this valid input
- **Then** I receive output in the format specified in Brief Q3 with HTTP 200 status

**Scenario 2: Output matches expected structure**
- **Given** a successful agent invocation
- **When** I inspect the returned output
- **Then** the output contains all required fields from Brief Q3 success example

**Scenario 3: Processing completes within performance target**
- **Given** a valid input request
- **When** the agent processes the request
- **Then** response time is <= [value from Q5 success metric]

**Expected Validation Score**: 95-100/100 ✅

---

### Story US-02: Handle malformed input gracefully

**As a** Developer
**I want** to receive clear error messages for invalid inputs
**So that** I can debug integration issues quickly

**Priority**: HIGH
**Estimated Effort**: 2 story points
**Brief Components**: Q2 (Input), Q3 (Output - error example)

**Acceptance Criteria:**

**Scenario 1: Missing required field returns descriptive error**
- **Given** an input missing a required field from Brief Q2 specification
- **When** I submit the malformed input to the agent
- **Then** I receive an error response matching Q3 error example with specific field name

**Scenario 2: Invalid data type returns validation error**
- **Given** an input with incorrect data type (e.g., string instead of integer)
- **When** I submit the invalid input
- **Then** I receive HTTP 400 with error message specifying expected vs actual type

---

[Additional stories US-03 through US-05...]

---

## 🔗 Traceability Matrix

| Brief Component | Covered by Stories |
|-----------------|-------------------|
| Q1 - Agent Purpose | US-01, US-05 |
| Q2 - Input Specification | US-01, US-02, US-03 |
| Q3 - Output Specification | US-01, US-02, US-05 |
| Q4 - Tool/API Requirements | US-04 |
| Q5 - Success Metrics | US-03, US-05 |

**Coverage**: 100% - All Brief Minimo components have associated user stories

---

## 📝 Notes

- All scenarios use concrete examples from Brief Minimo specification
- BDD format enables direct automation with pytest-bdd or behave
- Story priorities align with Brief success metrics (Q5)
- Estimated effort based on complexity of acceptance criteria

## 🎯 Next Steps

1. **Review stories with stakeholders** for completeness and clarity
1. **Use stories to create backlog** via `/backlog` command
1. **Implement spike** via `/spike-agentic` referencing these stories
1. **Create acceptance tests** using `/python-test-generator:create-acceptance-tests`
```

## ✅ Success Criteria

- [ ] Brief Minimo documentation located and read successfully
- [ ] All 5 Brief components (Q1-Q5) extracted and validated
- [ ] 2-4 relevant personas identified based on agent purpose
- [ ] Exactly 5-10 user stories generated (not more, not less)
- [ ] Every story follows "As a... I want... So that..." format
- [ ] Each story has 2-5 BDD acceptance criteria scenarios (3-5 optimal)
- [ ] All acceptance criteria use Given-When-Then format
- [ ] Stories distributed across happy path (3-4), edge cases (2-3), errors (1-2), performance (1)
- [ ] All Brief Minimo components covered by at least one story
- [ ] Traceability matrix shows 100% Brief coverage
- [ ] Acceptance criteria reference concrete examples from Brief
- [ ] Document saved to `docs/USER_STORIES.md`
- [ ] Summary report displayed with statistics
- [ ] Next steps suggested (backlog, spike, acceptance tests)

### 📊 INVEST Validation Criteria (For `/validate-user-histories`)

Every generated story MUST meet these criteria to pass validation (target: 90/100 score):

**Mandatory Requirements:**

- [ ] Specific persona (not "user", "person", "someone") - 10 pts
- [ ] Clear benefit >10 characters explaining WHY - 10 pts
- [ ] Precise effort estimate in hours (1-6h range) - 15 pts
- [ ] Impact value assigned (1-10 scale) - Required for ratio
- [ ] Impact/Hours ratio calculated and >1.5 - Priority metric
- [ ] 3-5 acceptance criteria per story - 5 pts
- [ ] ALL ACs specific and measurable (no "works", "functions") - 20 pts
- [ ] No undocumented dependencies - 15 pts
- [ ] Focuses on WHAT not HOW (negotiable) - 10 pts
- [ ] Story fits in 1-6 hours (not >8h) - 15 pts

**Expected Outcome:**

- Minimum 90/100 validation score
- No stories below 75/100 (blocking threshold)
- Average Impact/Hours ratio >1.5
- All personas specific (no generic terms)
- All ACs measurable with numbers/thresholds

## 📝 Examples

### Example 1: Generate user stories for email prioritizer agent

**Context**: Brief defines agent that classifies emails as HIGH/MEDIUM/LOW priority

**Command**:

```bash
/create-user-histories
```

**Process**:

1. Reads `docs/BRIEF.md` with email classifier specification
1. Extracts Q1 (classify emails), Q2 (email JSON), Q3 (priority label), Q4 (LLM API), Q5 (90% accuracy)
1. Identifies personas: Email user, System admin, API developer
1. Generates 7 stories:
   - US-01: Classify urgent email as HIGH (happy path)
   - US-02: Classify newsletter as LOW (happy path)
   - US-03: Handle missing subject line (edge case)
   - US-04: Process email with max character limit (edge case)
   - US-05: Return error for malformed JSON (error handling)
   - US-06: Recover from LLM API timeout (error handling)
   - US-07: Achieve 90% classification accuracy (performance)
1. Writes BDD criteria with concrete email examples from Brief
1. Saves `docs/USER_STORIES.md` with traceability matrix
1. Reports: 7 stories, 3 personas, 100% Brief coverage

### Example 2: Generate stories for data transformation agent

**Context**: Brief defines agent that converts CSV to Parquet with schema validation

**Command**:

```bash
/create-user-histories
```

**Process**:

1. Reads `README.md` section with Brief Minimo
1. Extracts transformation logic, CSV schema, Parquet output format, PyArrow dependency, 95% success rate
1. Identifies personas: Data engineer, Analytics user, ETL developer
1. Generates 6 stories covering format validation, schema enforcement, error handling, performance
1. Each story includes Given-When-Then scenarios with actual CSV samples from Brief
1. Creates traceability showing all Q1-Q5 covered
1. Saves and reports completion

## ❌ Anti-Patterns

### ❌ Error 1: Generic Stories Without Brief Context

Don't create stories disconnected from Brief Minimo specification:

```markdown
# ❌ Wrong - No connection to Brief
**As a** user
**I want** the system to work
**So that** I can use it

# ✅ Correct - References Brief Q1, Q2, Q3
**As a** API consumer
**I want** to submit email JSON (from Brief Q2 format) and receive priority classification (Brief Q3 output)
**So that** I can automate email triage in my support system (Brief Q1 purpose)
```

### ❌ Error 2: Missing Given-When-Then Format

Don't write acceptance criteria as simple checklists:

```markdown
# ❌ Wrong - No BDD structure
**Acceptance Criteria:**
- System accepts input
- Output is generated
- No errors occur

# ✅ Correct - BDD format with concrete examples
**Scenario 1: Valid email classification**
- **Given** an email JSON with subject "URGENT: Server down" (from Brief Q2 example)
- **When** I invoke the classifier agent
- **Then** I receive classification {"priority": "HIGH", "confidence": 0.95} (from Brief Q3 success output)
```

### ❌ Error 3: Too Few or Too Many Stories

Don't generate fewer than 5 or more than 10 stories:

```markdown
# ❌ Wrong - Only 3 stories (insufficient coverage)
US-01: Happy path
US-02: Error case
US-03: Edge case

# ❌ Wrong - 15 stories (too granular)
US-01 through US-15: Overly detailed micro-scenarios

# ✅ Correct - 5-10 stories with balanced coverage
US-01: Core happy path
US-02: Secondary happy path
US-03: Boundary condition
US-04: Invalid input handling
US-05: API failure recovery
US-06: Performance validation
(6 stories total - within range)
```

### ❌ Error 4: Vague Personas

Don't use generic personas without context:

```markdown
# ❌ Wrong - Too vague
**As a** user
**As a** person
**As a** someone

# ✅ Correct - Specific personas from agent context
**As a** customer support agent using email classification
**As a** DevOps engineer integrating the API
**As a** data analyst validating classification accuracy
```

### ❌ Error 5: Stories Without Brief Coverage Validation

Don't skip validation that all Brief components are covered:

```markdown
# ❌ Wrong - No traceability, missing Q4 and Q5 coverage
5 stories created but only cover Q1-Q3

# ✅ Correct - Traceability matrix showing 100% coverage
| Brief Component | Covered by Stories |
|-----------------|-------------------|
| Q1 - Purpose    | US-01, US-06      |
| Q2 - Input      | US-01, US-02, US-03 |
| Q3 - Output     | US-01, US-02, US-06 |
| Q4 - Tool/API   | US-04, US-05      |
| Q5 - Metrics    | US-06             |

Coverage: 100% ✅
```
