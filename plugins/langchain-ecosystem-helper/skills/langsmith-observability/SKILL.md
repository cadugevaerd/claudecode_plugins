---
description: "This skill should be used when the user asks about LangSmith observability, tracing, debugging, evaluation, datasets, evaluators, prompts management, or monitoring LLM applications. Trigger on questions like 'how to trace with LangSmith', 'LLM evaluation', 'create evaluator', 'debug LangChain application'."
---

# LangSmith Observability & Evaluation Guide (2025)

## Overview

LangSmith is the observability platform for LLM applications by LangChain. It provides tracing, debugging, evaluation, and prompt management for LangChain, LangGraph, and any LLM application.

**Key Features**:
- Complete visibility into agent behavior
- Real-time monitoring and alerting
- Offline and online evaluation
- Prompt versioning and management
- Dataset creation and management

## Quick Setup

### Environment Variables
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=my-project
```

### Automatic Tracing
With LangChain/LangGraph, tracing is automatic once environment variables are set.

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
# All calls are automatically traced to LangSmith
response = model.invoke("Hello!")
```

## Tracing

### Basic Tracing
```python
from langsmith import traceable

@traceable
def my_function(input: str) -> str:
    # Your logic here
    return result
```

### Custom Run Names
```python
@traceable(run_type="chain", name="my-custom-chain")
def process_data(data: dict) -> dict:
    return processed_data
```

### Nested Traces
```python
@traceable(name="parent")
def parent_function(input: str):
    result1 = child_function_1(input)
    result2 = child_function_2(result1)
    return result2

@traceable(name="child-1")
def child_function_1(data):
    return process(data)

@traceable(name="child-2")
def child_function_2(data):
    return finalize(data)
```

### Adding Metadata
```python
from langsmith import traceable

@traceable(metadata={"version": "1.0", "environment": "production"})
def my_function(input: str):
    return result
```

### Manual Tracing
```python
from langsmith import Client

client = Client()

with client.trace(name="my-trace", project_name="my-project") as trace:
    # Your code here
    trace.add_metadata({"key": "value"})
    trace.add_outputs({"result": "success"})
```

## OpenTelemetry Support (March 2025)

### End-to-End OpenTelemetry
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from langsmith.wrappers import wrap_openai

# Initialize OpenTelemetry
provider = TracerProvider()
trace.set_tracer_provider(provider)

# LangSmith automatically exports traces via OTLP
```

## Evaluation

### Basic Evaluation Flow
```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# 1. Create dataset
dataset = client.create_dataset("my-eval-dataset")

# 2. Add examples
client.create_examples(
    inputs=[
        {"question": "What is 2+2?"},
        {"question": "What is the capital of France?"}
    ],
    outputs=[
        {"answer": "4"},
        {"answer": "Paris"}
    ],
    dataset_id=dataset.id
)

# 3. Define target function
def my_agent(inputs: dict) -> dict:
    question = inputs["question"]
    return {"answer": model.invoke(question).content}

# 4. Define evaluator
def accuracy_evaluator(run, example):
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]
    return {"score": 1.0 if predicted.lower() == expected.lower() else 0.0}

# 5. Run evaluation
results = evaluate(
    my_agent,
    data=dataset.name,
    evaluators=[accuracy_evaluator]
)
```

### Built-in Evaluators (UI - March 2025)

Available in the LangSmith UI without code:
- **Hallucination**: Detect hallucinations
- **Correctness**: Verify correctness
- **Conciseness**: Evaluate conciseness
- **Code Checker**: Validate code

### Custom Evaluators

#### Simple Evaluator
```python
def exact_match(run, example):
    return {
        "key": "exact_match",
        "score": run.outputs["answer"] == example.outputs["answer"]
    }
```

#### LLM-as-Judge Evaluator
```python
from langsmith.evaluation import evaluate
from langchain_anthropic import ChatAnthropic

def llm_judge(run, example):
    judge = ChatAnthropic(model="claude-3-5-sonnet-20241022")

    prompt = f"""
    Question: {example.inputs['question']}
    Expected: {example.outputs['answer']}
    Predicted: {run.outputs['answer']}

    Is the prediction correct? Answer 'yes' or 'no'.
    """

    result = judge.invoke(prompt).content.lower()
    return {"score": 1.0 if "yes" in result else 0.0}
```

#### Pydantic Evaluator
```python
from pydantic import BaseModel, Field

class EvalResult(BaseModel):
    score: float = Field(ge=0, le=1)
    reasoning: str

def structured_evaluator(run, example):
    # Use structured output for evaluation
    result = judge.with_structured_output(EvalResult).invoke(...)
    return {"score": result.score, "comment": result.reasoning}
```

### Async Evaluation
```python
from langsmith.evaluation import aevaluate

async def async_evaluator(run, example):
    # Async evaluation logic
    return {"score": 0.9}

results = await aevaluate(
    my_agent,
    data="my-dataset",
    evaluators=[async_evaluator]
)
```

### Pairwise Evaluation
```python
from langsmith.evaluation import evaluate_comparative

def pairwise_judge(runs, example):
    # Compare two model outputs
    run_a, run_b = runs
    # Return which is better
    return {"preference": "a" if better(run_a) else "b"}

results = evaluate_comparative(
    experiments=["experiment-1", "experiment-2"],
    evaluators=[pairwise_judge]
)
```

## Datasets

### Create Dataset
```python
from langsmith import Client

client = Client()

# Create empty dataset
dataset = client.create_dataset(
    dataset_name="my-dataset",
    description="Dataset for testing"
)

# Add examples
client.create_examples(
    inputs=[{"input": "..."}],
    outputs=[{"output": "..."}],
    dataset_id=dataset.id
)
```

### From CSV
```python
import pandas as pd

df = pd.read_csv("data.csv")
client.create_dataset_from_csv(
    csv_file="data.csv",
    input_keys=["question"],
    output_keys=["answer"],
    name="csv-dataset"
)
```

### From Production Traces
```python
# In LangSmith UI:
# 1. Filter runs
# 2. Select traces
# 3. "Add to Dataset"
```

### Split Datasets
```python
from langsmith import Client

client = Client()
examples = list(client.list_examples(dataset_name="my-dataset"))

# Split 80/20
train_size = int(len(examples) * 0.8)
train_examples = examples[:train_size]
test_examples = examples[train_size:]
```

## Prompt Management

### Create and Version Prompts
```python
from langchain import hub

# Push prompt to hub
hub.push("my-org/my-prompt", prompt_template)

# Pull specific version
prompt = hub.pull("my-org/my-prompt:v2")
```

### Prompt in Code
```python
from langsmith import Client

client = Client()

# List prompts
prompts = client.list_prompts()

# Get prompt by name
prompt = client.pull_prompt("my-prompt")
```

## Monitoring & Alerting

### Real-time Monitoring
- Latency tracking per step
- Token usage monitoring
- Error rate tracking
- Cost estimation

### Setting Up Alerts
```python
# In LangSmith UI:
# 1. Go to Settings > Alerts
# 2. Create alert rule:
#    - Condition: error_rate > 5%
#    - Action: Send notification
```

### Custom Metrics
```python
from langsmith import traceable

@traceable
def my_function(input: str):
    start = time.time()
    result = process(input)

    # Log custom metrics
    client.log_metric(
        run_id=current_run_id,
        key="processing_time",
        value=time.time() - start
    )
    return result
```

## Online Evaluation

### Evaluate Production Traffic
```python
from langsmith import Client

client = Client()

# Create online evaluator rule
client.create_feedback_rule(
    project_name="production",
    evaluator_name="relevance-check",
    # Runs automatically on new traces
)
```

### Feedback Collection
```python
from langsmith import Client

client = Client()

# Add feedback to a run
client.create_feedback(
    run_id="run-uuid",
    key="user-rating",
    score=0.9,
    comment="Great response!"
)
```

## LangSmith MCP Server

### Available Tools
- `list_prompts` - Retrieve prompts
- `get_prompt_by_name` - Fetch specific prompt
- `fetch_runs` - Query runs with filtering
- `list_projects` - View projects
- `list_experiments` - Access experiment data
- `list_datasets` - View datasets
- `list_examples` - View dataset examples

### Configuration
```bash
export LANGSMITH_API_KEY=your-api-key
export LANGSMITH_WORKSPACE_ID=your-workspace  # Optional
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com  # Default
```

## Pricing & Tiers

| Tier | Traces/Month | Price |
|------|--------------|-------|
| Free | 5,000 | $0 |
| Plus | 50,000 | $39/month |
| Enterprise | Custom | Contact |

## Best Practices

### 1. Always Trace in Production
```bash
export LANGCHAIN_TRACING_V2=true
```

### 2. Use Meaningful Project Names
```bash
export LANGCHAIN_PROJECT=my-app-production
```

### 3. Add Metadata for Filtering
```python
@traceable(metadata={"user_id": user_id, "version": "1.0"})
def my_function():
    pass
```

### 4. Create Datasets from Edge Cases
When you find problematic traces, add them to datasets for regression testing.

### 5. Automate Evaluation
Run evaluations in CI/CD pipeline:
```python
results = evaluate(my_agent, data="regression-tests")
assert results.aggregate_score > 0.9
```

### 6. Use Pairwise Evaluation for Model Comparison
Compare model versions before deploying:
```python
evaluate_comparative(
    experiments=["model-v1", "model-v2"],
    evaluators=[preference_evaluator]
)
```

## Integration with LangGraph Platform

Every deployed LangGraph agent exposes an MCP endpoint automatically, enabling:
- Remote tracing
- Cross-system observability
- Unified evaluation

## References

- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation)
- [LangSmith API Reference](https://api.smith.langchain.com/redoc)
- [LangSmith GitHub](https://github.com/langchain-ai/langsmith-sdk)

---

**Use the MCP tool `SearchDocsByLangChain` to find specific documentation and examples.**
