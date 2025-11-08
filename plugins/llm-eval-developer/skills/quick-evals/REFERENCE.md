# Quick Evals - Technical Reference

**Complete technical documentation for implementing Quick Evaluation strategies**

## 📖 Table of Contents

1. [Evaluation Rhythms Deep Dive](#evaluation-rhythms-deep-dive)
1. [Golden Dataset Creation](#golden-dataset-creation)
1. [LangSmith Local Execution](#langsmith-local-execution)
1. [Subset Strategies](#subset-strategies)
1. [Technical Metrics Implementation](#technical-metrics-implementation)
1. [Alert Systems](#alert-systems)
1. [Node-Level Metrics (LangGraph)](#node-level-metrics-langgraph)
1. [Integration with CI/CD](#integration-with-cicd)

______________________________________________________________________

## Evaluation Rhythms Deep Dive

### The Three-Tier Strategy

#### Quick Eval (Tier 1)

- **Frequency**: On every commit or significant code change
- **Duration**: < 5 minutes (hard limit)
- **Dataset**: 1-5% of full dataset OR Golden Dataset (50-200 examples)
- **Execution**: Local only (`upload_results=False`)
- **Metrics**: Technical/deterministic only
- **Purpose**: Immediate feedback to catch regressions early

**When to trigger**:

```bash
# Git hook example
.git/hooks/pre-commit
#!/bin/bash
python scripts/run_quick_eval.py
```

#### Continuous Eval (Tier 2)

- **Frequency**: Hourly or daily (scheduled)
- **Duration**: 15-30 minutes
- **Dataset**: 10-20% of full dataset (stratified sampling)
- **Execution**: Can upload to cloud for trend tracking
- **Metrics**: Technical + basic quality metrics
- **Purpose**: Ongoing validation and trend monitoring

**When to trigger**:

```yaml
# GitHub Actions example
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

#### Formal Eval (Tier 3)

- **Frequency**: End of sprint or before deployment
- **Duration**: 30-60+ minutes
- **Dataset**: 100% full dataset (10k+ examples)
- **Execution**: Upload to cloud, comprehensive tracking
- **Metrics**: All metrics (technical, quality, business)
- **Purpose**: Quality gate before production deployment

**When to trigger**:

```yaml
# On release branch or tag
on:
  push:
    tags:
      - 'v*'
```

### Choosing the Right Rhythm

| Scenario | Recommended Rhythm |
|----------|-------------------|
| Testing new prompt variation | Quick Eval |
| Validating refactored code | Quick Eval |
| Daily health check | Continuous Eval |
| Weekly performance review | Continuous Eval |
| Pre-deployment validation | Formal Eval |
| Quarterly model comparison | Formal Eval |

______________________________________________________________________

## Golden Dataset Creation

### Step-by-Step Creation Process

#### Step 1: Define Coverage Requirements

```python
coverage_requirements = {
    "standard_cases": 0.60,      # 60% standard use cases
    "edge_cases": 0.25,          # 25% edge cases
    "failure_modes": 0.15,       # 15% known failure scenarios
}
```

#### Step 2: Manual Curation vs Automated Generation

**Manual Curation (Preferred)**:

```python
def manually_curate_example(input_text, expected_output, metadata):
    """
    Human expert reviews and validates each example
    """
    return {
        "input": input_text,
        "expected": expected_output,
        "metadata": {
            "category": metadata.get("category"),
            "difficulty": metadata.get("difficulty"),
            "edge_case": metadata.get("edge_case", False),
            "curator": metadata.get("curator"),
            "date": datetime.now().isoformat(),
        }
    }
```

**Automated Generation (With Human Review)**:

```python
from langsmith import Client

def generate_golden_examples_with_llm(doc_corpus, num_examples=100):
    """
    Use LLM to generate candidates, then human reviews/filters
    """
    client = Client()

    # Generate candidates
    candidates = client.generate_examples(
        corpus=doc_corpus,
        num_examples=num_examples * 2,  # Generate 2x, filter to best
        diversity_threshold=0.7,
    )

    # Human review step
    reviewed = []
    for candidate in candidates:
        if human_approves(candidate):  # Manual review
            reviewed.append(candidate)

    return reviewed[:num_examples]
```

#### Step 3: Dataset Size Progression

```python
# Phase 1: Initial Development
golden_dataset_v1 = create_dataset(size=10)  # Smoke test only

# Phase 2: Active Development
golden_dataset_v2 = create_dataset(size=50)  # Iterative improvements

# Phase 3: Pre-Production
golden_dataset_v3 = create_dataset(size=100)  # Comprehensive testing

# Phase 4: Production
golden_dataset_v4 = create_dataset(size=200)  # Full coverage
```

#### Step 4: Version Control and Updates

```python
# Store Golden Dataset in version control
# golden_dataset_v1.0.0.json

{
  "version": "1.0.0",
  "created_at": "2025-01-15T10:30:00Z",
  "num_examples": 100,
  "coverage": {
    "standard": 60,
    "edge_cases": 25,
    "failures": 15
  },
  "examples": [
    {
      "id": "ex_001",
      "input": "...",
      "expected": "...",
      "metadata": {...}
    }
  ]
}
```

**Update strategy**:

- **Patch (1.0.1)**: Fix typos, update metadata
- **Minor (1.1.0)**: Add new examples, expand coverage
- **Major (2.0.0)**: Complete restructure, change format

______________________________________________________________________

## LangSmith Local Execution

### Core Pattern: upload_results=False

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Local Quick Eval
results = client.evaluate(
    target=my_llm_function,
    data=golden_dataset,
    evaluators=[correctness, latency, format_check],
    experiment_prefix="quick-eval-local",
    upload_results=False,  # ← Critical parameter
    max_concurrency=5,     # Parallel execution for speed
)

# Results available in-memory only
print(f"Pass rate: {results.pass_rate}")
print(f"Avg latency: {results.avg_latency}")
```

### Analyzing Local Results

```python
# Convert to list for filtering
results_list = list(results)

# Filter by evaluator
correctness_results = [
    r for r in results_list
    if r.evaluator_name == "correctness"
]

# Analyze failures only
failures = [r for r in results_list if not r.passed]
for failure in failures:
    print(f"Failed: {failure.input}")
    print(f"Reason: {failure.feedback}")
```

### Async Pattern for Speed

```python
from langsmith.evaluation import aevaluate

# Async version for faster execution
async def run_quick_eval_async():
    results = await aevaluate(
        target=my_async_llm_function,
        data=golden_dataset,
        evaluators=[async_evaluator_1, async_evaluator_2],
        upload_results=False,
        max_concurrency=10,  # Higher concurrency with async
    )
    return results

# Run
import asyncio
results = asyncio.run(run_quick_eval_async())
```

### When to Upload vs Local

| Scenario | upload_results |
|----------|---------------|
| Active development iteration | False |
| Smoke testing new feature | False |
| Validating refactor | False |
| CI/CD pipeline (monitoring) | True |
| Scheduled health checks | True |
| Pre-deployment validation | True |

______________________________________________________________________

## Subset Strategies

### Strategy 1: Percentage Sampling

```python
import random

def create_subset_percentage(full_dataset, percentage=0.05):
    """
    Sample X% of full dataset randomly
    """
    sample_size = int(len(full_dataset) * percentage)
    return random.sample(full_dataset, sample_size)

# Usage
quick_eval_data = create_subset_percentage(full_10k_dataset, 0.01)  # 1%
# Result: 100 examples from 10,000
```

### Strategy 2: Stratified Sampling

```python
from collections import defaultdict
import random

def create_subset_stratified(full_dataset, percentage=0.05):
    """
    Sample evenly across categories to maintain distribution
    """
    # Group by category
    by_category = defaultdict(list)
    for example in full_dataset:
        category = example.get("metadata", {}).get("category", "default")
        by_category[category].append(example)

    # Sample from each category
    subset = []
    for category, examples in by_category.items():
        sample_size = max(1, int(len(examples) * percentage))
        subset.extend(random.sample(examples, sample_size))

    return subset

# Usage
quick_eval_data = create_subset_stratified(full_10k_dataset, 0.05)  # 5%
# Result: 500 examples, distributed across all categories
```

### Strategy 3: Fixed Golden Dataset

```python
def load_golden_dataset(version="latest"):
    """
    Load fixed Golden Dataset (50-200 examples)
    """
    with open(f"golden_dataset_{version}.json") as f:
        return json.load(f)["examples"]

# Usage - always same examples for consistency
quick_eval_data = load_golden_dataset(version="1.0.0")
```

### Strategy 4: Hybrid Approach

```python
def create_hybrid_subset(full_dataset, golden_dataset):
    """
    Combine Golden Dataset with random sampling
    """
    # Always include Golden Dataset
    subset = golden_dataset.copy()

    # Add random samples from full dataset
    remaining = [ex for ex in full_dataset if ex not in golden_dataset]
    additional = random.sample(remaining, min(50, len(remaining)))

    subset.extend(additional)
    return subset

# Usage
quick_eval_data = create_hybrid_subset(full_10k_dataset, golden_100)
# Result: 100 (golden) + 50 (random) = 150 examples
```

______________________________________________________________________

## Technical Metrics Implementation

### Latency Measurement

```python
import time

def measure_latency(func, input_data):
    """
    Measure execution latency in milliseconds
    """
    start = time.time()
    result = func(input_data)
    end = time.time()

    latency_ms = (end - start) * 1000
    return latency_ms, result

# Usage in evaluator
def latency_evaluator(run, example):
    latency, _ = measure_latency(target_func, example["input"])

    return {
        "key": "latency",
        "score": 1.0 if latency < 500 else 0.0,  # Pass if < 500ms
        "comment": f"Latency: {latency:.2f}ms"
    }
```

### Memory Usage Tracking

```python
import tracemalloc

def measure_memory(func, input_data):
    """
    Measure memory usage in MB
    """
    tracemalloc.start()

    result = func(input_data)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / 1024 / 1024
    return peak_mb, result

# Usage in evaluator
def memory_evaluator(run, example):
    memory_mb, _ = measure_memory(target_func, example["input"])

    return {
        "key": "memory",
        "score": 1.0 if memory_mb < 100 else 0.0,  # Pass if < 100MB
        "comment": f"Peak memory: {memory_mb:.2f}MB"
    }
```

### Regression Detection

```python
def regression_evaluator(run, example, baseline_results):
    """
    Compare current run with baseline
    """
    current_score = run.outputs["score"]
    baseline_score = baseline_results.get(example["id"], {}).get("score", 0)

    is_regression = current_score < baseline_score - 0.05  # 5% tolerance

    return {
        "key": "regression",
        "score": 0.0 if is_regression else 1.0,
        "comment": f"Current: {current_score:.2f} vs Baseline: {baseline_score:.2f}"
    }
```

### Format Validation

```python
import json
from jsonschema import validate, ValidationError

def format_evaluator(run, example):
    """
    Validate output format against schema
    """
    expected_schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["answer", "confidence"]
    }

    try:
        validate(instance=run.outputs, schema=expected_schema)
        return {
            "key": "format",
            "score": 1.0,
            "comment": "Valid format"
        }
    except ValidationError as e:
        return {
            "key": "format",
            "score": 0.0,
            "comment": f"Invalid format: {e.message}"
        }
```

______________________________________________________________________

## Alert Systems

### Threshold-Based Alerts

```python
class QuickEvalAlerts:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.alerts = []

    def check_latency(self, avg_latency):
        if avg_latency > self.thresholds["latency"]:
            alert = f"⚠️ LATENCY ALERT: {avg_latency:.2f}ms exceeds {self.thresholds['latency']}ms"
            self.alerts.append(alert)
            print(alert)

    def check_pass_rate(self, pass_rate):
        if pass_rate < self.thresholds["pass_rate"]:
            alert = f"⚠️ PASS RATE ALERT: {pass_rate:.2%} below {self.thresholds['pass_rate']:.2%}"
            self.alerts.append(alert)
            print(alert)

    def check_regressions(self, num_regressions):
        if num_regressions > self.thresholds["max_regressions"]:
            alert = f"⚠️ REGRESSION ALERT: {num_regressions} regressions detected (max: {self.thresholds['max_regressions']})"
            self.alerts.append(alert)
            print(alert)

# Usage
alerts = QuickEvalAlerts(thresholds={
    "latency": 500,        # ms
    "pass_rate": 0.90,     # 90%
    "max_regressions": 5,
})

alerts.check_latency(results.avg_latency)
alerts.check_pass_rate(results.pass_rate)
alerts.check_regressions(len(regressions))

if alerts.alerts:
    print("\n🚨 Quick Eval FAILED with alerts:")
    for alert in alerts.alerts:
        print(f"  - {alert}")
    sys.exit(1)  # Fail CI/CD pipeline
```

### Slack/Email Integration

```python
import requests

def send_alert_to_slack(alerts, webhook_url):
    """
    Send alerts to Slack channel
    """
    if not alerts:
        return

    message = {
        "text": "🚨 Quick Eval Alerts",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(alerts)
                }
            }
        ]
    }

    requests.post(webhook_url, json=message)

# Usage
if alerts.alerts:
    send_alert_to_slack(alerts.alerts, SLACK_WEBHOOK_URL)
```

______________________________________________________________________

## Node-Level Metrics (LangGraph)

### Collecting Per-Node Metrics

```python
from langsmith import traceable

@traceable(name="agent_node")
def agent_node(state, node_name):
    """
    Wrap each node to collect metrics
    """
    start = time.time()
    tracemalloc.start()

    # Execute node logic
    result = execute_node_logic(state)

    # Collect metrics
    latency = (time.time() - start) * 1000
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Store metrics in state
    state.setdefault("node_metrics", {})[node_name] = {
        "latency_ms": latency,
        "memory_peak_mb": memory_peak / 1024 / 1024,
        "tokens": result.get("tokens", 0),
        "cost": result.get("cost", 0),
    }

    return result

# Analyze node metrics after evaluation
def analyze_node_metrics(results):
    for result in results:
        node_metrics = result.state.get("node_metrics", {})

        print("\n📊 Node-Level Metrics:")
        for node_name, metrics in node_metrics.items():
            print(f"  {node_name}:")
            print(f"    Latency: {metrics['latency_ms']:.2f}ms")
            print(f"    Memory: {metrics['memory_peak_mb']:.2f}MB")
            print(f"    Tokens: {metrics['tokens']}")
            print(f"    Cost: ${metrics['cost']:.4f}")
```

______________________________________________________________________

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Quick Eval on Commit

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quick-eval:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Hard limit for Quick Eval

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Quick Eval
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
        run: |
          python scripts/run_quick_eval.py
        timeout-minutes: 5  # Must complete in 5 minutes

      - name: Upload results (on failure)
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: quick-eval-results
          path: results/quick_eval_*.json
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🚀 Running Quick Eval before commit..."

# Run Quick Eval with timeout
timeout 300 python scripts/run_quick_eval.py

if [ $? -eq 0 ]; then
    echo "✅ Quick Eval passed!"
    exit 0
else
    echo "❌ Quick Eval failed! Commit blocked."
    echo "Fix issues or run: git commit --no-verify"
    exit 1
fi
```

______________________________________________________________________

## Summary

This reference provides complete technical details for implementing Quick Eval strategies. Key takeaways:

- **Three evaluation rhythms** with clear distinctions
- **Golden Dataset creation** with curation and versioning
- **Local execution patterns** using LangSmith
- **Subset strategies** for speed optimization
- **Technical metrics** with code implementations
- **Alert systems** for immediate feedback
- **Node-level metrics** for complex agents
- **CI/CD integration** for automated validation

For implementation patterns and code examples, see **PATTERNS.md** and **EXAMPLES.md**.
