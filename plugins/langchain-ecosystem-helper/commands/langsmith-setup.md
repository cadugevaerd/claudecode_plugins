---
description: Set up LangSmith tracing and evaluation for your project
arguments:
  - name: action
    description: "Action: trace (setup tracing), evaluate (create evaluator), dataset (create dataset)"
    required: true
allowed_tools:
  - mcp__langchain-docs__SearchDocsByLangChain
  - Write
  - Read
  - Bash
---

# LangSmith Setup Helper

Set up LangSmith observability and evaluation for your LLM application.

## Action: $ARGUMENTS.action

## Instructions

### Tracing Setup (`trace`)

1. **Environment Variables**
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=my-project
```

2. **Python .env file**
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-api-key
LANGCHAIN_PROJECT=my-project
```

3. **Automatic Tracing** (LangChain/LangGraph)
```python
# No code changes needed - tracing is automatic
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
response = model.invoke("Hello!")  # Automatically traced
```

4. **Custom Function Tracing**
```python
from langsmith import traceable

@traceable(name="my-function", metadata={"version": "1.0"})
def my_function(input: str) -> str:
    # Your logic
    return result
```

### Evaluation Setup (`evaluate`)

1. **Basic Evaluator**
```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

def my_evaluator(run, example):
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]
    return {"score": 1.0 if predicted == expected else 0.0}

results = evaluate(
    my_agent,
    data="my-dataset",
    evaluators=[my_evaluator]
)
```

2. **LLM-as-Judge Evaluator**
```python
from langchain_anthropic import ChatAnthropic

def llm_judge(run, example):
    judge = ChatAnthropic(model="claude-3-5-sonnet-20241022")

    prompt = f"""
    Evaluate the response quality.

    Question: {example.inputs['question']}
    Expected: {example.outputs['answer']}
    Predicted: {run.outputs['answer']}

    Score from 0 to 1:
    """

    result = judge.invoke(prompt)
    score = float(result.content.strip())
    return {"score": score}
```

3. **Async Evaluation**
```python
from langsmith.evaluation import aevaluate

async def async_evaluator(run, example):
    return {"score": 0.9}

results = await aevaluate(my_agent, data="dataset", evaluators=[async_evaluator])
```

### Dataset Creation (`dataset`)

1. **Create Empty Dataset**
```python
from langsmith import Client

client = Client()

dataset = client.create_dataset(
    dataset_name="my-dataset",
    description="Dataset for testing my agent"
)
```

2. **Add Examples**
```python
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
```

3. **From CSV**
```python
client.create_dataset_from_csv(
    csv_file="data.csv",
    input_keys=["question"],
    output_keys=["answer"],
    name="csv-dataset"
)
```

4. **From Production Traces** (UI)
```
1. Go to LangSmith UI
2. Filter runs by project
3. Select traces
4. Click "Add to Dataset"
```

## Complete Example

Generate a complete setup based on the action requested, with:
1. All necessary imports
2. Environment configuration
3. Working code examples
4. Best practices and tips
