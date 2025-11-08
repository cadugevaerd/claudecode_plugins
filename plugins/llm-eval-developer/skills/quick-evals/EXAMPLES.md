# Quick Evals - Practical Examples

**Real-world scenarios and complete code examples for Quick Evaluation implementation**

## 📖 Example Catalog

1. [Chatbot Quick Eval](#chatbot-quick-eval)
1. [RAG Application Quick Eval](#rag-application-quick-eval)
1. [LangGraph Agent Quick Eval](#langgraph-agent-quick-eval)
1. [Multi-Model Comparison](#multi-model-comparison)
1. [Pre-Commit Hook Integration](#pre-commit-hook-integration)
1. [Complete CI/CD Pipeline](#complete-cicd-pipeline)

______________________________________________________________________

## Chatbot Quick Eval

### Scenario

You're developing a customer support chatbot and want to validate each code change doesn't introduce regressions.

### Golden Dataset

```python
# golden_dataset_chatbot.json
{
  "version": "1.0.0",
  "created_at": "2025-01-15T10:00:00Z",
  "num_examples": 50,
  "examples": [
    {
      "id": "ex_001",
      "input": "What are your business hours?",
      "expected": "9 AM to 5 PM",
      "metadata": {
        "category": "business_info",
        "difficulty": "easy"
      }
    },
    {
      "id": "ex_002",
      "input": "How do I reset my password?",
      "expected": "Click 'Forgot Password' on the login page",
      "metadata": {
        "category": "technical_support",
        "difficulty": "medium"
      }
    },
    {
      "id": "ex_003",
      "input": "asdfghjkl",
      "expected": "I don't understand",
      "metadata": {
        "category": "edge_case",
        "difficulty": "hard",
        "edge_case": true
      }
    }
    // ... 47 more examples
  ]
}
```

### Implementation

```python
# quick_eval_chatbot.py

import json
import time
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Load Golden Dataset
with open("golden_dataset_chatbot.json") as f:
    dataset_config = json.load(f)
    golden_dataset = dataset_config["examples"]

print(f"📊 Loaded {len(golden_dataset)} examples from Golden Dataset v{dataset_config['version']}")

# 2. Define chatbot
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support assistant. Be concise."),
    ("human", "{input}"),
])

chatbot = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define evaluators
def correctness_evaluator(run, example):
    """Check if expected keywords are in output"""
    output = run.outputs.get("content", "").lower()
    expected = example["expected"].lower()

    # Simple substring matching for Quick Eval
    score = 1.0 if expected in output else 0.0

    return {
        "key": "correctness",
        "score": score,
        "comment": f"Expected '{expected}' in output",
    }

def latency_evaluator(run, example):
    """Check latency is under 2 seconds"""
    latency_ms = run.execution_time_ms

    score = 1.0 if latency_ms < 2000 else 0.0

    return {
        "key": "latency",
        "score": score,
        "comment": f"Latency: {latency_ms:.2f}ms (threshold: 2000ms)",
    }

def conciseness_evaluator(run, example):
    """Check response is concise (< 100 words)"""
    output = run.outputs.get("content", "")
    word_count = len(output.split())

    score = 1.0 if word_count < 100 else 0.0

    return {
        "key": "conciseness",
        "score": score,
        "comment": f"Word count: {word_count} (threshold: 100)",
    }

# 4. Run Quick Eval
print("\n🚀 Running Quick Eval...")
start_time = time.time()

client = Client()
results = evaluate(
    lambda x: chatbot.invoke({"input": x["input"]}),
    data=golden_dataset,
    evaluators=[correctness_evaluator, latency_evaluator, conciseness_evaluator],
    experiment_prefix="quick-eval-chatbot",
    upload_results=False,  # Local only
    max_concurrency=5,
)

duration = time.time() - start_time

# 5. Analyze results
results_list = list(results)
total = len(results_list)
passed = sum(1 for r in results_list if r.passed)
pass_rate = passed / total if total > 0 else 0

print(f"\n⏱️  Duration: {duration:.2f}s")
print(f"📈 Results:")
print(f"  Total: {total}")
print(f"  Passed: {passed}")
print(f"  Pass Rate: {pass_rate:.2%}")

# 6. Check threshold
PASS_RATE_THRESHOLD = 0.85  # 85%

if pass_rate >= PASS_RATE_THRESHOLD:
    print(f"✅ Quick Eval PASSED ({pass_rate:.2%} >= {PASS_RATE_THRESHOLD:.2%})")
else:
    print(f"❌ Quick Eval FAILED ({pass_rate:.2%} < {PASS_RATE_THRESHOLD:.2%})")

    # Show failures
    print("\n❌ Failed examples:")
    for result in results_list:
        if not result.passed:
            print(f"  - Input: {result.example['input']}")
            print(f"    Reason: {result.feedback}")

# 7. Check duration
if duration > 300:  # 5 minutes
    print(f"⚠️ WARNING: Quick Eval exceeded 5 minutes ({duration:.2f}s)")
```

### Output Example

```
📊 Loaded 50 examples from Golden Dataset v1.0.0

🚀 Running Quick Eval...

⏱️  Duration: 142.35s
📈 Results:
  Total: 50
  Passed: 45
  Pass Rate: 90.00%

✅ Quick Eval PASSED (90.00% >= 85.00%)
```

______________________________________________________________________

## RAG Application Quick Eval

### Scenario

You have a RAG application for internal documentation and want to ensure retrieval quality on each commit.

### Golden Dataset

```python
# golden_dataset_rag.json
{
  "version": "1.0.0",
  "num_examples": 30,
  "examples": [
    {
      "id": "ex_001",
      "input": "How do I deploy to production?",
      "expected": "deployment guide",
      "expected_keywords": ["deployment", "production", "CI/CD"],
      "metadata": {
        "category": "deployment",
        "difficulty": "medium"
      }
    },
    {
      "id": "ex_002",
      "input": "What is our API rate limit?",
      "expected": "1000 requests per minute",
      "expected_keywords": ["rate limit", "1000", "API"],
      "metadata": {
        "category": "api_docs",
        "difficulty": "easy"
      }
    }
    // ... 28 more examples
  ]
}
```

### Implementation

```python
# quick_eval_rag.py

import json
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load Golden Dataset
with open("golden_dataset_rag.json") as f:
    golden_dataset = json.load(f)["examples"]

print(f"📊 Loaded {len(golden_dataset)} examples")

# 2. Setup RAG chain
embeddings = OpenAIEmbeddings()
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

rag_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
)

# 3. Define RAG-specific evaluators
def retrieval_quality_evaluator(run, example):
    """Check if retrieved docs contain expected keywords"""
    source_docs = run.outputs.get("source_documents", [])

    expected_keywords = example.get("expected_keywords", [])

    # Check if any keyword appears in retrieved docs
    found_keywords = []
    for doc in source_docs:
        content = doc.page_content.lower()
        for keyword in expected_keywords:
            if keyword.lower() in content:
                found_keywords.append(keyword)

    coverage = len(found_keywords) / len(expected_keywords) if expected_keywords else 0

    score = 1.0 if coverage >= 0.7 else 0.0  # 70% keyword coverage

    return {
        "key": "retrieval_quality",
        "score": score,
        "comment": f"Found {len(found_keywords)}/{len(expected_keywords)} keywords",
    }

def answer_relevance_evaluator(run, example):
    """Check if answer contains expected content"""
    answer = run.outputs.get("result", "").lower()
    expected = example["expected"].lower()

    score = 1.0 if expected in answer else 0.0

    return {
        "key": "answer_relevance",
        "score": score,
    }

def num_sources_evaluator(run, example):
    """Check if at least 2 sources were retrieved"""
    source_docs = run.outputs.get("source_documents", [])

    score = 1.0 if len(source_docs) >= 2 else 0.0

    return {
        "key": "num_sources",
        "score": score,
        "comment": f"Retrieved {len(source_docs)} sources",
    }

# 4. Run Quick Eval
print("\n🚀 Running Quick Eval for RAG...")

client = Client()
results = evaluate(
    lambda x: rag_chain.invoke({"query": x["input"]}),
    data=golden_dataset,
    evaluators=[
        retrieval_quality_evaluator,
        answer_relevance_evaluator,
        num_sources_evaluator,
    ],
    upload_results=False,
    max_concurrency=3,  # Lower for RAG to avoid rate limits
)

# 5. Analyze results
results_list = list(results)

# Calculate per-evaluator pass rates
evaluator_scores = {}
for result in results_list:
    for eval_result in result.results:
        eval_name = eval_result.key
        if eval_name not in evaluator_scores:
            evaluator_scores[eval_name] = []
        evaluator_scores[eval_name].append(eval_result.score)

print("\n📊 Per-Evaluator Results:")
for eval_name, scores in evaluator_scores.items():
    avg_score = sum(scores) / len(scores)
    print(f"  {eval_name}: {avg_score:.2%}")

# 6. Overall pass rate
total = len(results_list)
passed = sum(1 for r in results_list if r.passed)
pass_rate = passed / total if total > 0 else 0

print(f"\n📈 Overall Pass Rate: {pass_rate:.2%}")

if pass_rate >= 0.80:
    print("✅ Quick Eval PASSED")
else:
    print("❌ Quick Eval FAILED")
```

______________________________________________________________________

## LangGraph Agent Quick Eval

### Scenario

You have a LangGraph agent with multiple nodes and want to track per-node performance.

### Implementation

```python
# quick_eval_langgraph_agent.py

import time
import tracemalloc
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langsmith import Client, traceable
from langsmith.evaluation import evaluate

# 1. Define state
class AgentState(TypedDict):
    input: str
    plan: str
    execution: str
    output: str
    node_metrics: dict

# 2. Define nodes with metric collection
@traceable(name="planner_node")
def planner_node(state: AgentState):
    """Node that creates a plan"""
    start = time.time()
    tracemalloc.start()

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    plan = llm.invoke(f"Create a plan to answer: {state['input']}")

    latency = (time.time() - start) * 1000
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Store metrics
    if "node_metrics" not in state:
        state["node_metrics"] = {}

    state["node_metrics"]["planner"] = {
        "latency_ms": latency,
        "memory_peak_mb": memory_peak / 1024 / 1024,
    }

    state["plan"] = plan.content
    return state

@traceable(name="executor_node")
def executor_node(state: AgentState):
    """Node that executes the plan"""
    start = time.time()
    tracemalloc.start()

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    execution = llm.invoke(f"Execute this plan: {state['plan']}")

    latency = (time.time() - start) * 1000
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    state["node_metrics"]["executor"] = {
        "latency_ms": latency,
        "memory_peak_mb": memory_peak / 1024 / 1024,
    }

    state["execution"] = execution.content
    return state

@traceable(name="synthesizer_node")
def synthesizer_node(state: AgentState):
    """Node that synthesizes the final output"""
    start = time.time()
    tracemalloc.start()

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    output = llm.invoke(f"Synthesize final answer: {state['execution']}")

    latency = (time.time() - start) * 1000
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    state["node_metrics"]["synthesizer"] = {
        "latency_ms": latency,
        "memory_peak_mb": memory_peak / 1024 / 1024,
    }

    state["output"] = output.content
    return state

# 3. Build graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("synthesizer", synthesizer_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "synthesizer")
workflow.add_edge("synthesizer", END)

agent = workflow.compile()

# 4. Golden Dataset
golden_dataset = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
    },
    {
        "input": "How many days in a week?",
        "expected": "7",
    },
    # ... more examples
]

# 5. Define evaluators
def correctness_evaluator(run, example):
    output = run.outputs.get("output", "").lower()
    expected = example["expected"].lower()

    score = 1.0 if expected in output else 0.0

    return {"key": "correctness", "score": score}

def node_latency_evaluator(run, example):
    """Check per-node latency"""
    node_metrics = run.outputs.get("node_metrics", {})

    # Check each node is under threshold
    alerts = []
    all_pass = True

    for node_name, metrics in node_metrics.items():
        latency = metrics.get("latency_ms", 0)
        if latency > 2000:  # 2s per node
            alerts.append(f"{node_name}: {latency:.2f}ms")
            all_pass = False

    score = 1.0 if all_pass else 0.0

    return {
        "key": "node_latency",
        "score": score,
        "comment": f"Alerts: {', '.join(alerts)}" if alerts else "All nodes OK",
    }

def total_latency_evaluator(run, example):
    """Check total latency across all nodes"""
    node_metrics = run.outputs.get("node_metrics", {})

    total_latency = sum(
        metrics.get("latency_ms", 0)
        for metrics in node_metrics.values()
    )

    score = 1.0 if total_latency < 5000 else 0.0  # 5s total

    return {
        "key": "total_latency",
        "score": score,
        "comment": f"Total: {total_latency:.2f}ms",
    }

# 6. Run Quick Eval
print("🚀 Running Quick Eval for LangGraph Agent...")

client = Client()
results = evaluate(
    lambda x: agent.invoke({"input": x["input"]}),
    data=golden_dataset,
    evaluators=[
        correctness_evaluator,
        node_latency_evaluator,
        total_latency_evaluator,
    ],
    upload_results=False,
)

# 7. Analyze node-level metrics
results_list = list(results)

print("\n📊 Per-Node Metrics (Average):")
node_metrics_aggregated = {}

for result in results_list:
    node_metrics = result.outputs.get("node_metrics", {})
    for node_name, metrics in node_metrics.items():
        if node_name not in node_metrics_aggregated:
            node_metrics_aggregated[node_name] = []
        node_metrics_aggregated[node_name].append(metrics)

for node_name, metrics_list in node_metrics_aggregated.items():
    avg_latency = sum(m["latency_ms"] for m in metrics_list) / len(metrics_list)
    avg_memory = sum(m["memory_peak_mb"] for m in metrics_list) / len(metrics_list)

    print(f"  {node_name}:")
    print(f"    Avg Latency: {avg_latency:.2f}ms")
    print(f"    Avg Memory: {avg_memory:.2f}MB")

# 8. Overall pass rate
total = len(results_list)
passed = sum(1 for r in results_list if r.passed)
pass_rate = passed / total if total > 0 else 0

print(f"\n📈 Overall Pass Rate: {pass_rate:.2%}")
```

______________________________________________________________________

## Multi-Model Comparison

### Scenario

Compare GPT-4, GPT-3.5, and Claude 3 Sonnet on the same Golden Dataset to pick the best model for production.

### Implementation

```python
# quick_eval_multi_model.py

from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 1. Golden Dataset
golden_dataset = [
    {"input": "What is 2+2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
    # ... 48 more examples
]

# 2. Define models
models = {
    "GPT-4": ChatOpenAI(model="gpt-4", temperature=0),
    "GPT-3.5-Turbo": ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    "Claude-3-Sonnet": ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0),
}

# 3. Define evaluator
def correctness_evaluator(run, example):
    output = run.outputs.get("content", "").lower()
    expected = example["expected"].lower()

    score = 1.0 if expected in output else 0.0

    return {"key": "correctness", "score": score}

# 4. Run Quick Eval for each model
client = Client()
results_by_model = {}

for model_name, model in models.items():
    print(f"\n🔍 Evaluating {model_name}...")

    results = evaluate(
        lambda x: model.invoke(x["input"]),
        data=golden_dataset,
        evaluators=[correctness_evaluator],
        experiment_prefix=f"quick-eval-{model_name}",
        upload_results=False,
    )

    # Calculate metrics
    results_list = list(results)
    total = len(results_list)
    passed = sum(1 for r in results_list if r.passed)
    pass_rate = passed / total if total > 0 else 0

    # Collect latency
    latencies = [r.execution_time_ms for r in results_list if hasattr(r, "execution_time_ms")]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    results_by_model[model_name] = {
        "pass_rate": pass_rate,
        "avg_latency_ms": avg_latency,
        "total": total,
        "passed": passed,
    }

# 5. Print comparison table
print("\n" + "="*80)
print("📊 MULTI-MODEL COMPARISON RESULTS")
print("="*80)

print(f"\n{'Model':<25} {'Pass Rate':<15} {'Avg Latency':<20} {'Passed/Total':<15}")
print("-"*80)

for model_name, metrics in results_by_model.items():
    print(
        f"{model_name:<25} "
        f"{metrics['pass_rate']:.2%:<15} "
        f"{metrics['avg_latency_ms']:.2f}ms{'':<10} "
        f"{metrics['passed']}/{metrics['total']:<10}"
    )

# 6. Recommend best model
best_model = max(results_by_model.items(), key=lambda x: x[1]["pass_rate"])

print(f"\n✅ RECOMMENDED: {best_model[0]} with {best_model[1]['pass_rate']:.2%} pass rate")
```

### Output Example

```
================================================================================
📊 MULTI-MODEL COMPARISON RESULTS
================================================================================

Model                     Pass Rate       Avg Latency          Passed/Total
--------------------------------------------------------------------------------
GPT-4                     96.00%          1850.45ms            48/50
GPT-3.5-Turbo             88.00%          950.23ms             44/50
Claude-3-Sonnet           92.00%          1450.67ms            46/50

✅ RECOMMENDED: GPT-4 with 96.00% pass rate
```

______________________________________________________________________

## Pre-Commit Hook Integration

### Scenario

Run Quick Eval automatically before every git commit to catch regressions.

### Implementation

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🚀 Running Quick Eval before commit..."

# Set timeout (5 minutes)
timeout 300 python scripts/run_quick_eval.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Quick Eval PASSED - commit allowed"
    exit 0
elif [ $EXIT_CODE -eq 124 ]; then
    echo "⏱️  Quick Eval TIMEOUT (exceeded 5 minutes)"
    echo "❌ Commit blocked"
    exit 1
else
    echo "❌ Quick Eval FAILED - commit blocked"
    echo ""
    echo "To bypass this check (not recommended):"
    echo "  git commit --no-verify"
    exit 1
fi
```

```python
# scripts/run_quick_eval.py

import sys
import json
from langsmith import Client
from langsmith.evaluation import evaluate

def main():
    # Load dataset
    with open("golden_dataset_latest.json") as f:
        dataset = json.load(f)["examples"]

    # Run eval
    client = Client()
    results = evaluate(
        target_function,
        data=dataset,
        evaluators=[correctness, latency],
        upload_results=False,
    )

    # Check threshold
    results_list = list(results)
    total = len(results_list)
    passed = sum(1 for r in results_list if r.passed)
    pass_rate = passed / total if total > 0 else 0

    THRESHOLD = 0.90

    if pass_rate >= THRESHOLD:
        print(f"✅ Pass rate: {pass_rate:.2%}")
        sys.exit(0)
    else:
        print(f"❌ Pass rate: {pass_rate:.2%} (threshold: {THRESHOLD:.2%})")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

______________________________________________________________________

## Complete CI/CD Pipeline

### Scenario

Full GitHub Actions pipeline with Quick Eval, results artifacts, and PR comments.

### Implementation

```yaml
# .github/workflows/quick-eval.yml

name: Quick Eval Pipeline

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main ]

jobs:
  quick-eval:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Quick Eval
        id: quick_eval
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/run_quick_eval.py | tee quick_eval_output.txt
        continue-on-error: true
        timeout-minutes: 5

      - name: Parse results
        id: parse_results
        if: always()
        run: |
          if [ -f "results/quick_eval_latest.json" ]; then
            PASS_RATE=$(jq -r '.pass_rate' results/quick_eval_latest.json)
            echo "pass_rate=$PASS_RATE" >> $GITHUB_OUTPUT
          fi

      - name: Upload results artifact
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: quick-eval-results
          path: |
            results/*.json
            quick_eval_output.txt

      - name: Comment on PR
        if: always() && github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');

            let comment = '## 🚀 Quick Eval Results\n\n';

            if (fs.existsSync('results/quick_eval_latest.json')) {
              const results = JSON.parse(fs.readFileSync('results/quick_eval_latest.json'));

              comment += `- **Pass Rate**: ${(results.pass_rate * 100).toFixed(2)}%\n`;
              comment += `- **Passed**: ${results.passed}/${results.total}\n`;
              comment += `- **Threshold**: ${(results.threshold * 100).toFixed(2)}%\n\n`;

              if (results.pass_rate >= results.threshold) {
                comment += '✅ **Status**: PASSED\n';
              } else {
                comment += '❌ **Status**: FAILED\n';
              }
            } else {
              comment += '❌ Quick Eval did not complete successfully.\n';
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });

      - name: Fail if Quick Eval failed
        if: steps.quick_eval.outcome != 'success'
        run: exit 1
```

______________________________________________________________________

## Summary

These examples demonstrate real-world Quick Eval implementations for:

1. **Chatbot** - Customer support with correctness, latency, and conciseness checks
1. **RAG Application** - Retrieval quality and answer relevance evaluation
1. **LangGraph Agent** - Per-node metrics collection and analysis
1. **Multi-Model Comparison** - Side-by-side model evaluation
1. **Pre-Commit Hook** - Automatic validation before commits
1. **CI/CD Pipeline** - Complete GitHub Actions integration

All examples follow Quick Eval principles: **< 5 minutes, local execution, fast feedback**.
