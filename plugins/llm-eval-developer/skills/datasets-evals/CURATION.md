# Dataset Curation - Sourcing and Quality Strategies

Comprehensive guide on curation strategies for Golden Datasets (manual curation) and Production Datasets (backtesting, HITL workflows).

## 🎯 Curation Overview

**Curation** = Where examples come from + How they're selected/enriched

Two fundamentally different approaches:

| Aspect | Golden Dataset | Production Dataset |
|--------|----------------|-------------------|
| **Goal** | Define "good" behavior | Prevent regressions |
| **Source** | Manual curation | Production traces |
| **Size** | Small (50-200) | Large (100s-1000s) |
| **Quality** | High-quality, curated | Real-world, messy |
| **Use** | Quick Evals, A/B Testing | Regression Tests, HITL |

## 🏆 Golden Dataset Curation

### Purpose

Golden datasets define **expected behavior** through carefully selected examples. They serve as the "gold standard" for evaluation.

### Curation Process

#### Step 1: Define Scope and Coverage

Before creating examples, define:

1. **Use case boundaries**

   - What functionality are you testing?
   - What inputs are in-scope vs out-of-scope?

1. **Coverage dimensions**

   - Common cases (80% of real usage)
   - Edge cases (20% of critical but rare scenarios)
   - Error cases (invalid inputs, boundary conditions)

1. **Target size**

   - Start: 10-20 examples (MVP)
   - Quick Eval: 50-100 examples
   - Comprehensive: 100-200 examples

**Rule of thumb**: Each example should test a distinct scenario. Avoid redundancy.

#### Step 2: Create Example Categories

Organize examples into categories for balanced coverage:

**Common case categories** (70-80% of dataset):

```python
# Category: Basic Q&A
{
    "inputs": {"question": "What is LangChain?"},
    "outputs": {"answer": "LangChain is a framework for building LLM applications"},
    "metadata": {"category": "basic_qa", "difficulty": "easy"}
}

# Category: Factual retrieval
{
    "inputs": {"question": "What is the capital of France?"},
    "outputs": {"answer": "Paris"},
    "metadata": {"category": "factual", "difficulty": "easy"}
}
```

**Edge case categories** (20-30% of dataset):

```python
# Edge case: Ambiguous input
{
    "inputs": {"question": "What is it?"},
    "outputs": {"answer": "I need more context. What are you referring to?"},
    "metadata": {"category": "ambiguous", "difficulty": "medium", "is_edge_case": true}
}

# Edge case: Multi-part question
{
    "inputs": {"question": "What is LangChain and how do I install it?"},
    "outputs": {
        "answer": "LangChain is a framework... To install: pip install langchain",
        "must_address": ["definition", "installation"]
    },
    "metadata": {"category": "multi_part", "difficulty": "medium", "is_edge_case": true}
}

# Edge case: Out-of-scope request
{
    "inputs": {"question": "Write me a poem about cats"},
    "outputs": {"answer": "I'm designed for technical Q&A, not creative writing"},
    "metadata": {"category": "out_of_scope", "difficulty": "easy", "is_edge_case": true}
}
```

#### Step 3: Manual Curation Best Practices

**Who should curate**:

- ✅ Domain experts / Subject Matter Experts (SMEs)
- ✅ Product managers (understand user needs)
- ✅ Engineers (understand edge cases)

**Quality guidelines**:

1. **Inputs should be realistic**

   - Use actual user queries if available
   - Avoid overly synthetic or contrived examples
   - Include typos/variations for robustness testing

1. **Reference outputs should be verifiable**

   - Fact-check answers (for factual domains)
   - Get SME review (for specialized domains)
   - Include reasoning/justification if needed

1. **Balance is critical**

   - Don't over-index on any single category
   - Include positive and negative examples
   - Test both success and failure modes

**Curation workflow**:

```
1. Draft examples (engineer/PM)
   ↓
2. SME review (domain expert)
   ↓
3. Pilot test (run eval on 10-20 examples)
   ↓
4. Refine based on results
   ↓
5. Expand to target size (50-200)
   ↓
6. Periodic review (quarterly)
```

#### Step 4: Edge Case Identification

Edge cases are **critical for golden datasets**. Techniques to identify:

**Technique 1: Boundary Analysis**

- Test limits of input parameters
- Example: "What if question is 1 word? 1000 words?"

**Technique 2: Negative Testing**

- What should NOT work?
- Example: "Ask about unrelated topics"

**Technique 3: User Feedback Mining**

- Review support tickets
- Analyze user complaints
- Example: "Users often ask X, but system fails"

**Technique 4: Adversarial Examples**

- Try to break the system
- Example: "Inject malicious prompts", "Ask contradictory questions"

**Edge case template**:

```python
# Template for edge cases
{
    "inputs": {
        "question": "[Edge case scenario]"
    },
    "outputs": {
        "answer": "[Expected handling]",
        "behavior_note": "[Why this is correct]"
    },
    "metadata": {
        "category": "[Category]",
        "difficulty": "medium|hard",
        "is_edge_case": true,
        "edge_type": "boundary|negative|adversarial|ambiguous"
    }
}
```

#### Step 5: Validation Before Upload

Before uploading golden dataset:

- [ ] All examples reviewed by SME
- [ ] Categories balanced (not all easy, not all edge cases)
- [ ] Reference outputs verified for correctness
- [ ] Metadata consistent across examples
- [ ] Size appropriate (50-200 for Quick Eval)
- [ ] No sensitive/proprietary information
- [ ] Pilot evaluation completed successfully

### Golden Dataset Sizing Strategy

**Start small, expand deliberately**:

```
Week 1: 10-20 examples (critical paths)
  ↓
Week 2: 30-50 examples (+ common variations)
  ↓
Month 1: 50-100 examples (+ edge cases)
  ↓
Quarter 1: 100-200 examples (comprehensive coverage)
```

**When to stop growing**:

- ✅ Coverage of all known scenarios
- ✅ Evaluation time < 5 minutes (for Quick Eval)
- ✅ Diminishing returns on new examples

## 🏭 Production Dataset Curation

### Purpose

Production datasets capture **real-world failures** to prevent regressions and improve robustness.

### Curation Process

#### Step 1: Trace Sampling

**Source**: LangSmith production traces (logged interactions)

**Filtering criteria**:

```python
from langsmith import Client

client = Client()

# Filter 1: Error traces
error_traces = client.list_runs(
    project_name="prod-qa-system",
    filter="error = true",
    limit=500
)

# Filter 2: Low user feedback
low_feedback_traces = client.list_runs(
    project_name="prod-qa-system",
    filter="feedback_score < 3",
    limit=500
)

# Filter 3: High latency
slow_traces = client.list_runs(
    project_name="prod-qa-system",
    filter="latency > 5000",  # > 5 seconds
    limit=200
)

# Filter 4: Specific error types
specific_errors = client.list_runs(
    project_name="prod-qa-system",
    filter="error_type = 'RateLimitError'",
    limit=100
)
```

**Sampling strategies**:

1. **Random sampling** - Representative cross-section

   - Use when: Understanding overall performance
   - Sample size: 1-5% of production traffic

1. **Stratified sampling** - Balanced across categories

   - Use when: Ensuring coverage of all use cases
   - Example: 20% from each user segment

1. **Failure-focused sampling** - Only failures

   - Use when: Building regression test suite
   - Rationale: Prevent known failures from recurring

#### Step 2: Example Conversion

Convert production traces to dataset examples:

```python
def trace_to_example(trace):
    """Convert LangSmith trace to dataset example."""
    return {
        "inputs": trace.inputs,
        "outputs": None,  # To be filled by HITL
        "metadata": {
            "source": "production",
            "trace_id": str(trace.id),
            "timestamp": trace.start_time.isoformat(),
            "error_type": trace.error if trace.error else None,
            "latency_ms": trace.latency,
            "user_feedback_score": trace.feedback_score if hasattr(trace, "feedback_score") else None,
            "needs_annotation": True
        }
    }

# Convert all filtered traces
examples = [trace_to_example(t) for t in error_traces]
```

**Key decisions**:

- **Reference outputs**: Set to `None` initially (filled by HITL)
- **Metadata**: Include trace context for debugging
- **Flag for annotation**: `needs_annotation: true`

#### Step 3: Human-in-the-Loop (HITL) Annotation

**Purpose**: Enrich production examples with ground truth reference outputs.

**Workflow**:

```
1. Upload examples to LangSmith (outputs = None)
   ↓
2. Create Annotation Queue
   ↓
3. SMEs review and provide reference outputs
   ↓
4. Approved examples added to dataset
   ↓
5. Dataset version incremented
```

**LangSmith Annotation Queue setup**:

```python
from langsmith import Client

client = Client()

# Create dataset with partial examples
dataset = client.create_dataset(
    dataset_name="prod-regression_v2.0.0_pending-annotation",
    description="Production failures awaiting SME annotation"
)

# Upload examples (outputs = None)
client.create_examples(dataset_id=dataset.id, examples=examples)

# SMEs will review in LangSmith UI:
# 1. Navigate to dataset
# 2. Click "Annotate"
# 3. Review each example
# 4. Provide reference output
# 5. Approve or reject
```

**Annotation guidelines for SMEs**:

- ✅ Provide ideal response (not just "correct/incorrect")
- ✅ Explain reasoning if non-obvious
- ✅ Flag examples that need product changes
- ✅ Mark confidence level (high/medium/low)

**Annotation UI fields** (LangSmith):

```python
# Example annotation
{
    "inputs": {"question": "How do I reset password?"},
    "outputs": {
        "answer": "[SME provides correct answer]",
        "annotation_note": "[Why this is the right answer]"
    },
    "metadata": {
        "annotator": "expert@company.com",
        "annotation_date": "2025-01-09",
        "confidence": "high",
        "approved": true
    }
}
```

#### Step 4: Backtesting Strategy

**Backtesting** = Testing current system against past failures.

**Process**:

1. **Collect failures** from past weeks/months
1. **Annotate** with correct responses (HITL)
1. **Run evaluation** on current model
1. **Measure improvement** vs historical baseline

**Metrics to track**:

```python
# Regression prevention metrics
metrics = {
    "total_past_failures": 150,
    "current_passing": 120,
    "regression_prevention_rate": 0.80,  # 80% of past failures now pass
    "new_failures": 5,  # New issues introduced
    "net_improvement": 115  # 120 - 5
}
```

**Backtesting frequency**:

- 🟢 **Weekly**: For high-velocity teams
- 🟡 **Bi-weekly**: Standard cadence
- 🔴 **Monthly**: Minimum for regression prevention

#### Step 5: Dataset Maintenance

Production datasets require ongoing maintenance:

**Quarterly review**:

- Remove outdated examples (product changes)
- Add new failure patterns
- Re-annotate ambiguous examples
- Prune redundant examples

**Versioning after maintenance**:

```python
# Before maintenance
dataset_name = "prod-regression_v2.3.0"

# After quarterly review (MINOR bump)
dataset_name = "prod-regression_v2.4.0"
```

## 🔄 Hybrid Approach: Golden + Production

Many teams maintain **both** datasets:

| Dataset Type | Purpose | Update Frequency |
|--------------|---------|------------------|
| Golden | Quick iteration feedback | Monthly |
| Production | Regression prevention | Weekly |

**Workflow**:

```
Development:
  → Run Quick Eval on Golden Dataset (50 examples, < 2 min)
  → Iterate on prompts/model
  ↓
Pre-deployment:
  → Run full eval on Production Dataset (500 examples, 10 min)
  → Ensure no regressions
  ↓
Post-deployment:
  → Monitor production traces
  → Sample failures for next Production Dataset version
```

## 📊 Curation Quality Metrics

**For Golden Datasets**:

- Coverage: % of scenarios represented
- Balance: Distribution across categories
- Edge case ratio: 20-30% is ideal
- SME approval rate: > 95%

**For Production Datasets**:

- Annotation completion rate: > 90%
- Annotator agreement: > 85% (if multiple annotators)
- Regression prevention rate: > 80%
- Time to annotation: < 2 weeks

## 🎯 Curation Anti-Patterns

### ❌ Golden Dataset Anti-Patterns

1. **Over-curating** - Too much time perfecting examples

   - Impact: Slow iteration, analysis paralysis
   - Fix: Start with 10-20 "good enough" examples, iterate

1. **Ignoring edge cases** - Only testing happy paths

   - Impact: System breaks in production
   - Fix: Allocate 20-30% of examples to edge cases

1. **One-person curation** - No SME review

   - Impact: Biased or incorrect reference outputs
   - Fix: Always get domain expert review

### ❌ Production Dataset Anti-Patterns

1. **Sampling bias** - Only sampling easy errors

   - Impact: Missing hard failures
   - Fix: Stratified sampling across error types

1. **Annotation backlog** - Traces never annotated

   - Impact: Dataset never updated
   - Fix: Set SLA for annotation (e.g., 2 weeks)

1. **Forgetting to version** - Overwriting dataset

   - Impact: Lost reproducibility
   - Fix: Always increment version after changes

## ✅ Curation Checklist

**Golden Dataset**:

- [ ] SME involvement confirmed
- [ ] Coverage dimensions defined
- [ ] 70% common cases, 30% edge cases
- [ ] All examples reviewed for correctness
- [ ] Size appropriate for Quick Eval (50-200)
- [ ] Pilot evaluation completed

**Production Dataset**:

- [ ] Trace sampling strategy defined
- [ ] HITL annotation workflow established
- [ ] SME annotators assigned
- [ ] Annotation SLA set (e.g., 2 weeks)
- [ ] Backtesting metrics defined
- [ ] Maintenance cadence planned (quarterly)

## 📚 Additional Resources

- **LangSmith Annotation Queues**: https://docs.smith.langchain.com/evaluation/how_to_guides/annotation_queues
- **Dataset Curation Best Practices**: https://www.deepchecks.com/question/how-important-is-a-golden-dataset-for-llm-evaluation/
- **Synthetic Data for Bootstrapping**: https://phoenix.arize.com/creating-and-validating-synthetic-datasets-for-llm-evaluation-experimentation/
