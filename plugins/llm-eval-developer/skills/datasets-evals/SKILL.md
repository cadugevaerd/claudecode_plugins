---
name: datasets-evals
description: LangSmith dataset creation and management expertise - structure (inputs/outputs/metadata), curation strategies (golden vs production data), versioning, and SDK usage. Use when creating evaluation datasets, managing test data for LLM evaluations, designing golden datasets, curating production datasets for regression testing, or versioning evaluation data. Essential for Quick Evals, A/B testing, regression tests, and HITL workflows.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
---

# LangSmith Datasets for Evaluation

Expertise in creating effective evaluation datasets for LangSmith across different evaluation types: structure, curation strategies, and lifecycle management.

## 📋 When to Use Me

Invoke this skill when you need to:

- **Create evaluation datasets** for LLM applications using LangSmith
- **Design golden datasets** for Quick Evals or A/B testing
- **Curate production datasets** for regression testing
- **Version datasets** for reproducibility in CI/CD pipelines
- **Structure inputs/outputs** for different evaluation scenarios
- **Implement HITL workflows** with Annotation Queues
- **Manage dataset lifecycle** (creation, updates, versioning)
- **Use LangSmith SDK** for programmatic dataset creation

**Trigger terms**: "create dataset", "golden dataset", "evaluation data", "test cases", "ground truth", "dataset versioning", "regression testing", "LangSmith examples"

## 🎓 Core Knowledge

### What is an Evaluation Dataset?

A Dataset in LangSmith is a **stable, versioned collection of test/validation examples**. It is NOT used for training models, but as **immutable reference data** to measure performance.

Think of it as a **calibrated ruler** - it must be:

- ✅ Structured correctly (proper inputs/outputs)
- ✅ Measuring what matters (domain-specific)
- ✅ Versioned and immutable during measurement

### Fundamental Anatomy of an Example

Each evaluation example consists of:

```python
{
    "inputs": {"question": "What is LangChain?"},           # Required
    "outputs": {"answer": "LangChain is a framework..."},   # Reference/ground truth
    "metadata": {                                            # Optional but recommended
        "source": "docs",
        "difficulty": "easy",
        "created_at": "2025-01-08"
    }
}
```

**Key components**:

1. **Inputs**: Dictionary passed to the Target Function (application under test)
1. **Reference Outputs**: Ground truth/expected outputs used by Evaluators for scoring
1. **Metadata**: Additional data for filtering and stratification of results

### Two Main Dataset Types

| Type | Purpose | Size | Source | Evaluation Focus |
|------|---------|------|--------|-----------------|
| **Golden Dataset** | Correctness & Model Engineering | Small (50-200) | Manual curation | Quick Evals, A/B Testing |
| **Production Dataset** | Robustness & Regression | Large (100s-1000s) | Real-world traces | Regression Tests, HITL |

### Dataset Size Guidelines

Based on industry best practices:

- **Initial/MVP**: 10-20 examples (rapid iteration)
- **Quick Evals**: 50-200 examples (< 5 min feedback)
- **Comprehensive**: 100-500 examples (production-ready)
- **Regression Suite**: 500+ examples (ongoing monitoring)

**Trade-off**: Smaller = faster feedback, Larger = better coverage

### Golden Dataset vs Production Dataset

**Golden Dataset** (Curated for Correctness):

- ✅ Hand-selected high-quality examples
- ✅ Define "good" expected behavior
- ✅ Include both standard cases and critical edge cases
- ✅ Small enough for quick iteration (< 5 min evaluation)
- 🎯 **Use for**: Quick Evals, Model A/B Testing, Prompt Engineering

**Production Dataset** (Curated for Robustness):

- ✅ Sampled from real-world production traces
- ✅ Focus on failures and negative user feedback
- ✅ Enriched via Human-in-the-Loop (HITL) annotation
- ✅ Larger scale for comprehensive regression coverage
- 🎯 **Use for**: Regression Tests, Backtesting, Continuous Monitoring

### Versioning Best Practices

Datasets must be treated as **software artifacts** with explicit versioning:

**Versioning Strategies**:

1. **Semantic Versioning**: `v2.1.0` (MAJOR.MINOR.PATCH)

   - MAJOR: Breaking schema changes
   - MINOR: New examples added
   - PATCH: Fixes to existing examples

1. **Branch-based**: `qa-system_feature-improved-qa`

   - Tie to git branch/feature
   - Easier to track feature development

**When to Create New Version**:

- ✅ End of sprint (significant changes)
- ✅ Before major deployment
- ✅ When schema changes

**When to Update Existing**:

- ✅ During active sprint (iterative improvements)
- ✅ Minor example corrections
- ✅ Metadata enrichment

### LangSmith SDK Essentials

**Basic workflow**:

```python
from langsmith import Client
import os

# 1. Initialize client
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
client = Client()

# 2. Create dataset
dataset = client.create_dataset(
    dataset_name="qa-system_v1.0.0",
    description="Golden dataset for Q&A evaluation"
)

# 3. Add examples
examples = [
    {
        "inputs": {"question": "What is LangChain?"},
        "outputs": {"answer": "LangChain is a framework..."}
    },
    # ... more examples
]

client.create_examples(
    dataset_id=dataset.id,
    examples=examples
)
```

**Key SDK functions**:

- `client.create_dataset()` - Create new dataset
- `client.create_examples()` - Bulk upload examples
- `client.create_example()` - Add single example
- `client.update_example()` - Modify existing example
- `client.read_dataset()` - Fetch dataset by name/ID

## 📚 Reference Files

For detailed information, consult:

- **STRUCTURE.md** - Deep dive into dataset anatomy, schema design, input/output patterns, and metadata strategies
- **CURATION.md** - Comprehensive curation strategies for Golden Datasets (manual curation, edge cases) and Production Datasets (backtesting, HITL workflows, Annotation Queues)
- **LIFECYCLE.md** - Complete lifecycle management: versioning patterns, creation vs update decisions, local storage organization, CI/CD integration

## 💡 Quick Examples

### Example 1: Create Simple Golden Dataset

```python
from langsmith import Client

client = Client()

# Create dataset
dataset = client.create_dataset(
    dataset_name="customer-support_v1.0.0",
    description="Golden dataset for customer support Q&A"
)

# Define examples with edge cases
examples = [
    # Standard case
    {
        "inputs": {"query": "How do I reset my password?"},
        "outputs": {"response": "Click 'Forgot Password' on login page..."},
        "metadata": {"category": "authentication", "difficulty": "easy"}
    },
    # Edge case: ambiguous query
    {
        "inputs": {"query": "I can't login"},
        "outputs": {"response": "There could be several reasons..."},
        "metadata": {"category": "authentication", "difficulty": "medium"}
    },
    # Edge case: multiple topics
    {
        "inputs": {"query": "Reset password and delete account"},
        "outputs": {"response": "These are two separate actions..."},
        "metadata": {"category": "authentication,account", "difficulty": "hard"}
    }
]

# Upload examples
client.create_examples(dataset_id=dataset.id, examples=examples)
```

### Example 2: Curate Production Dataset from Traces

```python
from langsmith import Client

client = Client()

# 1. Query production traces that failed
traces = client.list_runs(
    project_name="customer-support-prod",
    filter="error = true OR feedback_score < 3",
    limit=100
)

# 2. Convert traces to examples
examples = []
for trace in traces:
    examples.append({
        "inputs": trace.inputs,
        "outputs": None,  # To be filled by SME via HITL
        "metadata": {
            "source": "production",
            "trace_id": str(trace.id),
            "error_type": trace.error,
            "user_feedback_score": trace.feedback_score
        }
    })

# 3. Create regression dataset
dataset = client.create_dataset(
    dataset_name="customer-support_regression_v2.0.0",
    description="Regression dataset from production failures (Jan 2025)"
)

client.create_examples(dataset_id=dataset.id, examples=examples)

# 4. SMEs will review via Annotation Queues and add reference outputs
```

### Example 3: Version Dataset by Feature Branch

```python
from langsmith import Client

client = Client()

# Semantic versioning tied to git branch
BRANCH = "feature/improved-rag"
VERSION = "v1.1.0"

dataset_name = f"rag-system_{BRANCH}_{VERSION}"

dataset = client.create_dataset(
    dataset_name=dataset_name,
    description=f"Dataset for RAG improvements ({BRANCH})"
)

# Load examples from local versioned JSON
import json

with open(f"datasets/{dataset_name}.json", "r") as f:
    examples = json.load(f)

client.create_examples(dataset_id=dataset.id, examples=examples)
```

## ✅ Quick Validation Checklist

Before creating a dataset, verify:

- [ ] **Clear purpose** defined (Quick Eval, Regression, A/B Test)?
- [ ] **Type determined** (Golden or Production)?
- [ ] **Size appropriate** for purpose (50-200 for golden, 100+ for production)?
- [ ] **Inputs match** application's expected input schema?
- [ ] **Reference outputs** are accurate and complete?
- [ ] **Metadata included** for filtering/stratification?
- [ ] **Version naming** follows convention (semantic or branch-based)?
- [ ] **Examples balanced** (standard cases + edge cases)?
- [ ] **SDK configured** (LANGCHAIN_API_KEY set)?

## 🎯 Decision Tree: Which Dataset Strategy?

```
Need evaluation dataset?
│
├─ For rapid iteration during development?
│  └─ → Golden Dataset (50-200 examples, manual curation)
│     └─ See: CURATION.md > Golden Dataset Creation
│
├─ For preventing regressions from production issues?
│  └─ → Production Dataset (100+ examples, trace sampling)
│     └─ See: CURATION.md > Production Dataset Creation
│
└─ For both?
   └─ → Maintain separate datasets with clear versioning
      └─ See: LIFECYCLE.md > Multi-Dataset Management
```

## 🔗 Integration Points

This skill integrates with:

- **Evaluators/Metrics** - Datasets feed into evaluation pipelines
- **LangSmith Tracing** - Production datasets sourced from traces
- **Annotation Queues** - HITL enrichment of datasets
- **CI/CD Pipelines** - Versioned datasets for regression tests
- **A/B Testing** - Golden datasets for model comparison

## 📖 Key Principles

Remember these core principles:

1. **Datasets are not for training** - They're immutable reference data for evaluation
1. **Versioning is critical** - Enable reproducibility and CI/CD integration
1. **Small golden datasets** - Enable fast feedback loops (< 5 min evals)
1. **Production datasets capture reality** - Real failures inform robustness
1. **Metadata enables insights** - Stratify results by difficulty, source, category
1. **HITL closes the loop** - SME annotation enriches datasets over time

## 🚀 Getting Started

**Step 1**: Determine evaluation type (Quick Eval vs Regression)

**Step 2**: Choose dataset strategy (Golden vs Production)

**Step 3**: Consult reference files:

- STRUCTURE.md for schema design
- CURATION.md for sourcing strategies
- LIFECYCLE.md for versioning approach

**Step 4**: Implement with LangSmith SDK

**Step 5**: Integrate into evaluation pipeline
