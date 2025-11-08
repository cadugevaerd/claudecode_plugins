# Quick Evals - Implementation Patterns

**Common implementation patterns for Quick Evaluation across different frameworks**

## 📖 Pattern Catalog

1. [LangSmith Quick Eval Pattern](#langsmith-quick-eval-pattern)
1. [LangChain LCEL Quick Eval](#langchain-lcel-quick-eval)
1. [Custom Framework Pattern](#custom-framework-pattern)
1. [Multi-Framework Comparison Pattern](#multi-framework-comparison-pattern)
1. [Golden Dataset Management Pattern](#golden-dataset-management-pattern)
1. [CI/CD Integration Pattern](#cicd-integration-pattern)

______________________________________________________________________

## LangSmith Quick Eval Pattern

### Basic Pattern

```python
from langsmith import Client
from langsmith.evaluation import evaluate

def run_quick_eval_langsmith(
    target_function,
    golden_dataset,
    evaluators,
    experiment_name="quick-eval"
):
    """
    Standard Quick Eval pattern with LangSmith
    """
    client = Client()

    results = evaluate(
        target_function,
        data=golden_dataset,
        evaluators=evaluators,
        experiment_prefix=experiment_name,
        upload_results=False,  # Local only
        max_concurrency=5,
    )

    return results

# Usage
results = run_quick_eval_langsmith(
    target_function=my_chatbot,
    golden_dataset=load_golden_dataset(),
    evaluators=[correctness, latency, format_check],
)
```

### Advanced Pattern with Alerts

```python
from langsmith import Client
from langsmith.evaluation import evaluate

class QuickEvalRunner:
    def __init__(self, thresholds):
        self.client = Client()
        self.thresholds = thresholds
        self.alerts = []

    def run(self, target, dataset, evaluators):
        # Execute evaluation
        results = evaluate(
            target,
            data=dataset,
            evaluators=evaluators,
            upload_results=False,
            max_concurrency=5,
        )

        # Check thresholds
        self._check_thresholds(results)

        return results, self.alerts

    def _check_thresholds(self, results):
        """Check all thresholds and generate alerts"""
        results_list = list(results)

        # Pass rate
        total = len(results_list)
        passed = sum(1 for r in results_list if r.passed)
        pass_rate = passed / total if total > 0 else 0

        if pass_rate < self.thresholds["pass_rate"]:
            self.alerts.append(
                f"⚠️ Pass rate {pass_rate:.2%} below {self.thresholds['pass_rate']:.2%}"
            )

        # Latency
        latencies = [r.metadata.get("latency", 0) for r in results_list]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0

        if avg_latency > self.thresholds["latency"]:
            self.alerts.append(
                f"⚠️ Avg latency {avg_latency:.2f}ms exceeds {self.thresholds['latency']}ms"
            )

# Usage
runner = QuickEvalRunner(thresholds={
    "pass_rate": 0.90,
    "latency": 500,
})

results, alerts = runner.run(
    target=my_chatbot,
    dataset=golden_dataset,
    evaluators=[correctness, latency],
)

if alerts:
    print("🚨 Alerts triggered:")
    for alert in alerts:
        print(f"  {alert}")
```

______________________________________________________________________

## LangChain LCEL Quick Eval

### Pattern for LCEL Chains

```python
from langchain_core.runnables import RunnablePassthrough
from langsmith import Client
from langsmith.evaluation import evaluate

def quick_eval_lcel_chain(chain, golden_dataset):
    """
    Quick Eval for LangChain LCEL chains
    """

    # Define evaluators
    def correctness_evaluator(run, example):
        """Check if chain output matches expected"""
        output = run.outputs.get("output", "")
        expected = example.get("expected", "")

        score = 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

        return {
            "key": "correctness",
            "score": score,
        }

    def latency_evaluator(run, example):
        """Check chain latency"""
        latency_ms = run.execution_time_ms

        score = 1.0 if latency_ms < 500 else 0.0

        return {
            "key": "latency",
            "score": score,
            "comment": f"Latency: {latency_ms:.2f}ms",
        }

    # Run evaluation
    client = Client()
    results = evaluate(
        lambda inputs: {"output": chain.invoke(inputs)},
        data=golden_dataset,
        evaluators=[correctness_evaluator, latency_evaluator],
        upload_results=False,
    )

    return results

# Usage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chain = (
    ChatPromptTemplate.from_template("Answer: {question}")
    | ChatOpenAI(model="gpt-4")
)

results = quick_eval_lcel_chain(chain, golden_dataset)
```

### Pattern for RAG Chains

```python
from langchain.chains import RetrievalQA
from langsmith.evaluation import evaluate

def quick_eval_rag_chain(retrieval_qa_chain, golden_dataset):
    """
    Quick Eval specialized for RAG chains
    """

    # RAG-specific evaluators
    def retrieval_relevance_evaluator(run, example):
        """Check if retrieved docs are relevant"""
        retrieved_docs = run.outputs.get("source_documents", [])

        # Check if any doc contains expected keywords
        expected_keywords = example.get("expected_keywords", [])
        found = any(
            keyword in doc.page_content.lower()
            for doc in retrieved_docs
            for keyword in expected_keywords
        )

        return {
            "key": "retrieval_relevance",
            "score": 1.0 if found else 0.0,
        }

    def answer_correctness_evaluator(run, example):
        """Check if answer is correct"""
        answer = run.outputs.get("result", "")
        expected = example.get("expected", "")

        # Simple substring match for Quick Eval
        score = 1.0 if expected.lower() in answer.lower() else 0.0

        return {
            "key": "answer_correctness",
            "score": score,
        }

    # Run evaluation
    results = evaluate(
        retrieval_qa_chain.invoke,
        data=golden_dataset,
        evaluators=[retrieval_relevance_evaluator, answer_correctness_evaluator],
        upload_results=False,
        max_concurrency=3,  # Lower for RAG to avoid rate limits
    )

    return results

# Usage
rag_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vector_store.as_retriever(),
)

results = quick_eval_rag_chain(rag_chain, golden_dataset)
```

______________________________________________________________________

## Custom Framework Pattern

### Generic Quick Eval Framework

```python
import time
from typing import Callable, List, Dict, Any

class QuickEvalFramework:
    """
    Framework-agnostic Quick Eval implementation
    """

    def __init__(self, time_limit_seconds=300):
        self.time_limit = time_limit_seconds
        self.results = []

    def run(
        self,
        target_func: Callable,
        dataset: List[Dict],
        evaluators: List[Callable],
    ):
        """
        Run Quick Eval on any target function
        """
        start_time = time.time()

        for example in dataset:
            # Check time limit
            if time.time() - start_time > self.time_limit:
                print(f"⚠️ Time limit exceeded ({self.time_limit}s)")
                break

            # Run target
            try:
                output = target_func(example["input"])
                success = True
                error = None
            except Exception as e:
                output = None
                success = False
                error = str(e)

            # Run evaluators
            eval_results = {}
            for evaluator in evaluators:
                eval_name = evaluator.__name__
                try:
                    eval_results[eval_name] = evaluator(
                        input=example["input"],
                        output=output,
                        expected=example.get("expected"),
                    )
                except Exception as e:
                    eval_results[eval_name] = {
                        "score": 0.0,
                        "error": str(e),
                    }

            # Store result
            self.results.append({
                "input": example["input"],
                "output": output,
                "expected": example.get("expected"),
                "success": success,
                "error": error,
                "evaluations": eval_results,
            })

        return self.results

    def summary(self):
        """Generate summary statistics"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])

        # Aggregate evaluator scores
        eval_scores = {}
        for result in self.results:
            for eval_name, eval_result in result["evaluations"].items():
                if eval_name not in eval_scores:
                    eval_scores[eval_name] = []
                eval_scores[eval_name].append(eval_result.get("score", 0.0))

        avg_scores = {
            name: sum(scores) / len(scores)
            for name, scores in eval_scores.items()
        }

        return {
            "total": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0,
            "average_scores": avg_scores,
        }

# Usage
def my_llm_function(input_text):
    # Your custom LLM logic
    return f"Response to: {input_text}"

def correctness_evaluator(input, output, expected):
    score = 1.0 if expected in output else 0.0
    return {"score": score}

framework = QuickEvalFramework(time_limit_seconds=300)
results = framework.run(
    target_func=my_llm_function,
    dataset=golden_dataset,
    evaluators=[correctness_evaluator],
)

summary = framework.summary()
print(f"Success rate: {summary['success_rate']:.2%}")
```

______________________________________________________________________

## Multi-Framework Comparison Pattern

### Compare Multiple Models/Chains

```python
from typing import Dict, List, Callable
from langsmith.evaluation import evaluate

def compare_multiple_targets(
    targets: Dict[str, Callable],
    dataset: List[Dict],
    evaluators: List[Callable],
):
    """
    Run Quick Eval on multiple targets for comparison
    """
    results_by_target = {}

    for target_name, target_func in targets.items():
        print(f"Evaluating {target_name}...")

        results = evaluate(
            target_func,
            data=dataset,
            evaluators=evaluators,
            experiment_prefix=f"quick-eval-{target_name}",
            upload_results=False,
        )

        # Calculate metrics
        results_list = list(results)
        total = len(results_list)
        passed = sum(1 for r in results_list if r.passed)

        results_by_target[target_name] = {
            "total": total,
            "passed": passed,
            "pass_rate": passed / total if total > 0 else 0,
        }

    # Print comparison
    print("\n📊 Comparison Results:")
    print(f"{'Target':<30} {'Pass Rate':<15} {'Total':<10}")
    print("-" * 55)

    for target_name, metrics in results_by_target.items():
        print(
            f"{target_name:<30} "
            f"{metrics['pass_rate']:.2%:<15} "
            f"{metrics['total']:<10}"
        )

    return results_by_target

# Usage
targets = {
    "gpt-4-baseline": lambda x: gpt4_chain.invoke(x),
    "gpt-3.5-optimized": lambda x: gpt35_optimized_chain.invoke(x),
    "claude-3-sonnet": lambda x: claude_chain.invoke(x),
}

comparison = compare_multiple_targets(
    targets=targets,
    dataset=golden_dataset,
    evaluators=[correctness, latency],
)
```

______________________________________________________________________

## Golden Dataset Management Pattern

### Versioned Golden Dataset Manager

```python
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class GoldenDatasetManager:
    """
    Manage versioned Golden Datasets
    """

    def __init__(self, base_path="golden_datasets"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def create(
        self,
        examples: List[Dict],
        version: str,
        metadata: Dict = None,
    ):
        """Create new versioned Golden Dataset"""
        dataset = {
            "version": version,
            "created_at": datetime.now().isoformat(),
            "num_examples": len(examples),
            "metadata": metadata or {},
            "examples": examples,
        }

        filepath = self.base_path / f"golden_dataset_v{version}.json"
        with open(filepath, "w") as f:
            json.dump(dataset, f, indent=2)

        print(f"✅ Created Golden Dataset v{version} with {len(examples)} examples")
        return filepath

    def load(self, version: str = "latest"):
        """Load Golden Dataset by version"""
        if version == "latest":
            # Find latest version
            files = list(self.base_path.glob("golden_dataset_v*.json"))
            if not files:
                raise FileNotFoundError("No Golden Datasets found")

            filepath = max(files, key=lambda p: p.stat().st_mtime)
        else:
            filepath = self.base_path / f"golden_dataset_v{version}.json"

        with open(filepath) as f:
            dataset = json.load(f)

        print(f"📁 Loaded Golden Dataset v{dataset['version']} ({dataset['num_examples']} examples)")
        return dataset["examples"]

    def update(
        self,
        current_version: str,
        new_examples: List[Dict],
        new_version: str,
    ):
        """Update existing dataset with new examples"""
        # Load current
        current_examples = self.load(current_version)

        # Merge
        merged = current_examples + new_examples

        # Create new version
        self.create(merged, new_version, metadata={
            "updated_from": current_version,
            "added_examples": len(new_examples),
        })

    def list_versions(self):
        """List all available versions"""
        files = list(self.base_path.glob("golden_dataset_v*.json"))

        versions = []
        for filepath in sorted(files):
            with open(filepath) as f:
                dataset = json.load(f)

            versions.append({
                "version": dataset["version"],
                "created_at": dataset["created_at"],
                "num_examples": dataset["num_examples"],
            })

        return versions

# Usage
manager = GoldenDatasetManager()

# Create v1.0.0
manager.create(
    examples=initial_100_examples,
    version="1.0.0",
    metadata={"creator": "team", "purpose": "initial release"},
)

# Load latest
golden_dataset = manager.load(version="latest")

# Update to v1.1.0
manager.update(
    current_version="1.0.0",
    new_examples=additional_50_examples,
    new_version="1.1.0",
)

# List all versions
versions = manager.list_versions()
for v in versions:
    print(f"v{v['version']}: {v['num_examples']} examples (created {v['created_at']})")
```

______________________________________________________________________

## CI/CD Integration Pattern

### Complete CI/CD Pattern with GitHub Actions

```python
# scripts/run_quick_eval.py

import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    """
    Run Quick Eval in CI/CD pipeline
    """
    print("🚀 Starting Quick Eval...")

    # Load Golden Dataset
    with open("golden_dataset_latest.json") as f:
        dataset = json.load(f)["examples"]

    print(f"📊 Loaded {len(dataset)} examples from Golden Dataset")

    # Run evaluation
    from langsmith import Client
    from langsmith.evaluation import evaluate

    client = Client()
    results = evaluate(
        target_function,
        data=dataset,
        evaluators=[correctness, latency, format_check],
        upload_results=False,
        max_concurrency=5,
    )

    # Analyze results
    results_list = list(results)
    total = len(results_list)
    passed = sum(1 for r in results_list if r.passed)
    pass_rate = passed / total if total > 0 else 0

    # Check thresholds
    PASS_RATE_THRESHOLD = 0.90  # 90%

    print(f"\n📈 Results:")
    print(f"  Total: {total}")
    print(f"  Passed: {passed}")
    print(f"  Pass Rate: {pass_rate:.2%}")

    # Save results for artifact
    results_file = Path("results") / f"quick_eval_{datetime.now().isoformat()}.json"
    results_file.parent.mkdir(exist_ok=True)

    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "passed": passed,
            "pass_rate": pass_rate,
            "threshold": PASS_RATE_THRESHOLD,
        }, f, indent=2)

    # Exit with appropriate code
    if pass_rate >= PASS_RATE_THRESHOLD:
        print(f"✅ Quick Eval PASSED ({pass_rate:.2%} >= {PASS_RATE_THRESHOLD:.2%})")
        sys.exit(0)
    else:
        print(f"❌ Quick Eval FAILED ({pass_rate:.2%} < {PASS_RATE_THRESHOLD:.2%})")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### GitHub Actions Workflow

```yaml
# .github/workflows/quick-eval.yml

name: Quick Eval

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quick-eval:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Quick Eval
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/run_quick_eval.py
        timeout-minutes: 5

      - name: Upload results on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: quick-eval-results
          path: results/*.json

      - name: Comment on PR (on failure)
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Quick Eval failed. Please review the results.'
            })
```

______________________________________________________________________

## Summary

This document provides implementation patterns for:

1. **LangSmith** - Standard and advanced patterns with alerts
1. **LangChain LCEL** - Chain and RAG-specific patterns
1. **Custom Framework** - Framework-agnostic implementation
1. **Multi-Framework Comparison** - Compare multiple targets
1. **Golden Dataset Management** - Versioning and updates
1. **CI/CD Integration** - Complete pipeline integration

Choose the pattern that best fits your framework and use case. All patterns follow the core Quick Eval principles: **< 5 minutes, local execution, fast feedback**.
