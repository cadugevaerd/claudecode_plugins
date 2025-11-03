---
name: benchmark-runner
description: Executa benchmarks comparativos de LLMs usando LangChain/LangGraph e LangSmith. Use quando comparar múltiplos modelos, criar comparative evaluation, ou executar performance testing de LLMs.
allowed-tools: Read, Write, Bash, Grep
---

name: benchmark-runner
description: Executa benchmarks comparativos de LLMs usando LangChain/LangGraph e LangSmith. Use quando comparar múltiplos modelos, criar comparative evaluation, ou executar performance testing de LLMs.
allowed-tools: Read, Write, Bash, Grep

# Benchmark Runner Skill

## Instructions

Skill para executar benchmarks comparativos de LLMs automaticamente usando **LangChain/LangGraph** e **LangSmith**.

### Step 1: Detect Benchmarking Need

Quando usuário menciona termos como:

- "comparar modelos", "benchmark LLMs"
- "qual modelo melhor", "performance comparison"
- "gpt vs claude", "model A vs model B"
- "custo x performance", "latência dos modelos"
- "comparative evaluation", "model selection"

### Step 2: Identify Benchmark Type

Determinar tipo de benchmark necessário:

**Simple Comparison** (2-3 modelos, métricas básicas):

- Usar LCEL batch
- LangSmith evaluate() API
- Evaluators nativos

**Complex Comparison** (4+ modelos, métricas avançadas):

- Usar LangGraph parallel workflows
- Custom evaluators
- Multiple evaluation rounds

**Cost-Performance Analysis**:

- Focus em cost-efficiency
- LangSmith automatic cost tracking
- Trade-off analysis

**Latency Testing**:

- Custom callbacks para P95/P99
- TTFT tracking
- SLA validation

### Step 3: Configure Benchmark

Coletar informações necessárias:

1. **Models to compare**:

   - Providers: OpenAI, Anthropic, Google
   - Models: gpt-4o, claude-3.5-sonnet, gemini-1.5-pro, etc.
   - Configurations: temperature, max_tokens

1. **Dataset**:

   - LangSmith dataset (preferred)
   - MMLU, HumanEval, TruthfulQA
   - Custom local dataset

1. **Metrics**:

   - **Quality**: accuracy, relevance, hallucination (LangSmith evaluators)
   - **Performance**: latency P95/P99, TTFT (callbacks)
   - **Cost**: token usage, costs (LangSmith tracking)

1. **Execution mode**:

   - Parallel (LCEL batch ou LangGraph)
   - Sequential (menor custo)

### Step 4: Generate Benchmark Code

Gerar código completo usando template apropriado:

#### Template 1: LCEL Batch Benchmark (Simple)

````python
"""
Simple Benchmark usando LCEL Batch
Compara múltiplos modelos em paralelo.
"""

import asyncio
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.callbacks import BaseCallbackHandler
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
import numpy as np
import time

class LatencyCallback(BaseCallbackHandler):
    """Track latency metrics"""
    def __init__(self):
        self.latencies = []
        self.start = None

    def on_llm_start(self, *args, **kwargs):
        self.start = time.perf_counter()

    def on_llm_end(self, *args, **kwargs):
        if self.start:
            self.latencies.append((time.perf_counter() - self.start) * 1000)

    def get_p95(self):
        return np.percentile(self.latencies, 95) if self.latencies else 0


async def benchmark_model(provider, model_name, dataset_name, project_name):
    """Benchmark individual model"""

    # Create chain
    if provider == "openai":
        llm = ChatOpenAI(model=model_name)
    elif provider == "anthropic":
        llm = ChatAnthropic(model=model_name)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()

    # Callback for latency
    latency_cb = LatencyCallback()

    # Target function
    def predict(inputs):
        config = RunnableConfig(callbacks=[latency_cb])
        result = chain.invoke(inputs, config=config)
        return {"output": result}

    # Evaluate using LangSmith
    results = evaluate(
        predict,
        data=dataset_name,
        evaluators=[LangChainStringEvaluator("qa")],
        experiment_prefix=f"benchmark-{model_name}",
        project_name=project_name,
        max_concurrency=10
    )

    return {
        "model": f"{provider}:{model_name}",
        "accuracy": results["qa"]["mean"],
        "p95_latency_ms": latency_cb.get_p95(),
        "url": results.experiment_url
    }


async def main():
    """Run benchmark"""

    models = [
        ("openai", "gpt-4o"),
        ("anthropic", "claude-3-5-sonnet-20241022")
    ]

    results = await asyncio.gather(*[
        benchmark_model(p, m, "my-dataset", "llm-benchmark")
        for p, m in models
    ])

    # Print results
    for r in sorted(results, key=lambda x: x["accuracy"], reverse=True):
        print(f"{r['model']}: {r['accuracy']:.2%} acc, {r['p95_latency_ms']:.0f}ms P95")

if __name__ == "__main__":
    asyncio.run(main())

```text

#### Template 2: LangGraph Parallel Benchmark (Complex)

```python
"""
LangGraph Parallel Benchmark
Executa múltiplos modelos em paralelo com state management.
"""

from typing import TypedDict, Annotated, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import time

class BenchmarkState(TypedDict):
    input: str
    responses: Annotated[Dict[str, str], "Responses"]
    latencies: Annotated[Dict[str, float], "Latencies"]
    scores: Annotated[Dict[str, float], "Scores"]


def create_model_node(model_name, llm):
    def node(state):
        start = time.perf_counter()
        response = llm.invoke(state["input"])
        latency = (time.perf_counter() - start) * 1000

        return {
            "responses": {**state.get("responses", {}), model_name: response.content},
            "latencies": {**state.get("latencies", {}), model_name: latency}
        }
    return node


def evaluate_node(state):
    """LLM-as-judge evaluation"""
    from langchain_openai import ChatOpenAI
    import json

    evaluator = ChatOpenAI(model="gpt-4o-mini")
    scores = {}

    for model, response in state["responses"].items():
        eval_prompt = f"""Rate 1-10:
Question: {state['input']}
Answer: {response}
Return JSON: {{"score": N}}"""

        result = evaluator.invoke(eval_prompt)
        try:
            scores[model] = json.loads(result.content)["score"] / 10.0
        except:
            scores[model] = 0.5

    return {"scores": scores}


def create_graph():
    workflow = StateGraph(BenchmarkState)

    # Models
    llms = {
        "gpt-4o": ChatOpenAI(model="gpt-4o"),
        "claude": ChatAnthropic(model="claude-3-5-sonnet-20241022")
    }

    for name, llm in llms.items():
        workflow.add_node(name, create_model_node(name, llm))

    workflow.add_node("evaluate", evaluate_node)
    workflow.set_entry_point("gpt-4o")

    for name in llms.keys():
        workflow.add_edge(name, "evaluate")

    workflow.add_edge("evaluate", END)
    return workflow.compile()


# Run
graph = create_graph()
result = graph.invoke({"input": "Explain quantum computing"})

for model in result["responses"].keys():
    print(f"{model}: score={result['scores'][model]:.2f}, latency={result['latencies'][model]:.0f}ms")

```text

### Step 5: Execute and Report

Após gerar código:

1. **Executar benchmark**:
   - Criar arquivo Python com código
   - Configurar env vars (API keys, LangSmith)
   - Executar script

2. **Analisar resultados**:
   - Comparar métricas
   - Identificar winners por categoria
   - Gerar recommendations

3. **Gerar relatório**:
   - Markdown comparativo
   - JSON para análise
   - Link para LangSmith UI

### Step 6: Provide Recommendations

Baseado nos resultados, gerar recommendations:

**For Production**:
- Best overall (balanceado)
- Budget-conscious (custo-eficiência)
- Highest quality (accuracy)
- Fastest (latência)

**For Specific Use Cases**:
- Real-time applications → Fastest model
- Batch processing → Cost-efficient model
- High-stakes decisions → Highest quality

## When to Use

Esta skill é invocada quando:

- Usuário quer **comparar múltiplos LLMs**
- Precisa decidir qual modelo usar
- Quer medir performance/custo
- Menciona "benchmark", "compare models"
- Pergunta "qual modelo melhor para X?"

**Trigger terms**:
- "comparar modelos", "benchmark"
- "gpt vs claude", "openai vs anthropic"
- "qual modelo mais rápido/barato/preciso"
- "performance comparison", "model evaluation"
- "custo x qualidade", "latência dos modelos"

## Examples

### Example 1: Simple Comparison

**User**: "Qual modelo é melhor para chatbot: gpt-4o ou claude-3.5-sonnet?"

**Skill**:
1. Detecta: comparison de 2 modelos
2. Gera benchmark LCEL batch
3. Usa LangSmith evaluators (qa, helpfulness)
4. Executa em dataset de chatbot
5. Reporta winner baseado em accuracy + latência + custo

### Example 2: Cost-Performance Analysis

**User**: "Preciso do modelo mais cost-efficient para resumos"

**Skill**:
1. Detecta: focus em cost-efficiency
2. Compara modelos small/medium (gpt-4o-mini, claude-haiku, gemini-flash)
3. Usa ROUGE evaluator para summaries
4. Calcula cost per summary
5. Reporta melhor custo-benefício

### Example 3: Latency Testing

**User**: "Qual modelo atende SLA de P95 < 1000ms?"

**Skill**:
1. Detecta: focus em latência P95
2. Gera benchmark com custom callback
3. Testa múltiplos modelos
4. Calcula P95 de cada
5. Reporta quais atendem SLA

## Key Patterns

### Pattern 1: Always Use LangSmith

**Vantagens**:
- Tracking automático (tokens, custos, traces)
- Evaluators prontos
- Comparison view no UI
- Dataset management

```python
from langsmith.evaluation import evaluate

# LangSmith automaticamente trackeia TUDO
results = evaluate(
    your_app,
    data="dataset-name",
    evaluators=[...],
    project_name="benchmark-project"
)

```text

### Pattern 2: Custom Callbacks for Latency

**LangSmith não trackeia P95/P99 automaticamente**:

```python
from langchain_core.callbacks import BaseCallbackHandler

class LatencyCallback(BaseCallbackHandler):
    def on_llm_start(self, *args, **kwargs):
        self.start = time.perf_counter()

    def on_llm_end(self, *args, **kwargs):
        latency = (time.perf_counter() - self.start) * 1000
        self.latencies.append(latency)

```text

### Pattern 3: Parallel Execution

**LCEL batch para I/O-bound**:

```python
results = chain.batch(
    inputs,
    config=RunnableConfig(max_concurrency=10)
)

```text

**LangGraph para complex workflows**:

```python
workflow = StateGraph(State)

# Add parallel nodes

# All execute concurrently

```text

### Pattern 4: Winner Analysis

Sempre reportar winners por categoria:

```text

🏆 Winners:
  Best Accuracy: gpt-4o (0.872)
  Fastest: claude-3.5-sonnet (891ms P95)
  Best Value: gemini-1.5-pro (196 acc/$)

```text

## Integration with LangSmith

### Upload Dataset

```python
from langsmith import Client

client = Client()
dataset = client.create_dataset("my-benchmark")

client.create_examples(
    inputs=[{"input": "..."}],
    outputs=[{"output": "..."}],
    dataset_id=dataset.id
)

```text

### Configure Cost Tracking

Via LangSmith UI:
- Settings > Model Pricing
- Adicionar pricing por modelo
- Tracking automático em evaluate()

### Access Results

```python

# Via API
project = client.read_project("benchmark-project")
print(f"Total Cost: ${project.total_cost}")

# Via UI

# https://smith.langchain.com/o/org/projects/p/benchmark-project

```text

## References

- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation)
- [LCEL Batch](https://python.langchain.com/docs/how_to/parallel/)
- [LangGraph Parallel](https://langchain-ai.github.io/langgraph/how-tos/)
- [LangChain Callbacks](https://python.langchain.com/docs/integrations/callbacks/)
````
