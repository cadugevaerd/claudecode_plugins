# LangGraph Architecture Patterns

Padrões arquiteturais e best practices para construir sistemas complexos com LangGraph 1.0.

## 📐 Multi-Agent Patterns

### Pattern 1: Supervisor Architecture

**Quando usar**: Coordenar múltiplos agentes especializados com um supervisor central.

**Estrutura**:

```
        Supervisor (LLM)
            ↓
    ┌───────┼───────┐
    ↓       ↓       ↓
Research  Code   Writing
 Agent   Agent   Agent
```

**Implementação**:

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages

class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

# Agentes especializados
def research_agent(state):
    """Agente especializado em pesquisa"""
    return {"messages": [AIMessage(content="Research findings...")]}

def code_agent(state):
    """Agente especializado em código"""
    return {"messages": [AIMessage(content="Code implementation...")]}

def writing_agent(state):
    """Agente especializado em escrita"""
    return {"messages": [AIMessage(content="Written content...")]}

# Supervisor decide qual agente chamar
def supervisor(state) -> Literal["research", "code", "writing", "end"]:
    """LLM supervisor que roteia tarefas"""
    # Simulação - em produção, LLM analisa messages e decide
    last_msg = state["messages"][-1].content
    if "research" in last_msg.lower():
        return "research"
    elif "code" in last_msg.lower():
        return "code"
    elif "write" in last_msg.lower():
        return "writing"
    return "end"

# Construir grafo
builder = StateGraph(MultiAgentState)
builder.add_node("supervisor_node", lambda s: s)  # Pass-through
builder.add_node("research", research_agent)
builder.add_node("code", code_agent)
builder.add_node("writing", writing_agent)

builder.add_edge(START, "supervisor_node")
builder.add_conditional_edges(
    "supervisor_node",
    supervisor,
    {
        "research": "research",
        "code": "code",
        "writing": "writing",
        "end": END
    }
)

# Agents podem voltar para supervisor
builder.add_edge("research", "supervisor_node")
builder.add_edge("code", "supervisor_node")
builder.add_edge("writing", "supervisor_node")

graph = builder.compile()
```

**Vantagens**:

- ✅ Especialização clara de responsabilidades
- ✅ Supervisor controla fluxo
- ✅ Fácil adicionar novos agentes

**Desvantagens**:

- ⚠️ Supervisor é single point of failure
- ⚠️ Pode ter overhead de routing

______________________________________________________________________

### Pattern 2: Hierarchical Agents (Nested Subgraphs)

**Quando usar**: Agentes complexos que precisam de sub-workflows.

**Estrutura**:

```
Main Agent
├── Subgraph: Data Processing
│   ├── Extract
│   ├── Transform
│   └── Load
└── Subgraph: Analysis
    ├── Analyze
    └── Report
```

**Implementação**:

```python
from langgraph.graph import StateGraph, START, END

# Subgraph 1: Data Processing
def build_data_pipeline():
    class PipelineState(TypedDict):
        data: str
        processed: bool

    builder = StateGraph(PipelineState)
    builder.add_node("extract", lambda s: {"data": "extracted"})
    builder.add_node("transform", lambda s: {"data": s["data"] + " transformed"})
    builder.add_node("load", lambda s: {"processed": True})

    builder.add_edge(START, "extract")
    builder.add_edge("extract", "transform")
    builder.add_edge("transform", "load")
    builder.add_edge("load", END)

    return builder.compile()

# Subgraph 2: Analysis
def build_analysis_pipeline():
    class AnalysisState(TypedDict):
        data: str
        insights: str

    builder = StateGraph(AnalysisState)
    builder.add_node("analyze", lambda s: {"insights": "analyzed"})
    builder.add_node("report", lambda s: {"insights": s["insights"] + " reported"})

    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "report")
    builder.add_edge("report", END)

    return builder.compile()

# Main graph usando subgraphs
class MainState(TypedDict):
    request: str
    result: str

builder = StateGraph(MainState)

# Add subgraphs como nodes
data_pipeline = build_data_pipeline()
analysis_pipeline = build_analysis_pipeline()

builder.add_node("process_data", data_pipeline)
builder.add_node("analyze_data", analysis_pipeline)

builder.add_edge(START, "process_data")
builder.add_edge("process_data", "analyze_data")
builder.add_edge("analyze_data", END)

graph = builder.compile()
```

**Vantagens**:

- ✅ Encapsulação de lógica complexa
- ✅ Reutilização de subgraphs
- ✅ Testing isolado

**Desvantagens**:

- ⚠️ State mapping entre parent/subgraph pode ser complexo
- ⚠️ Debugging mais difícil

______________________________________________________________________

## 🔄 Loop Patterns

### Pattern 3: Retry with Backoff

**Quando usar**: Node pode falhar, precisa retry com backoff.

```python
from typing import TypedDict
import time

class RetryState(TypedDict):
    attempt: int
    max_attempts: int
    result: str
    error: str

def risky_operation(state: RetryState) -> dict:
    """Operação que pode falhar"""
    import random
    if random.random() < 0.7:  # 70% chance de falha
        return {
            "attempt": state["attempt"] + 1,
            "error": "Operation failed"
        }
    return {
        "result": "Success!",
        "error": ""
    }

def should_retry(state: RetryState) -> Literal["retry", "success", "failed"]:
    """Decide se tenta novamente"""
    if state.get("result"):
        return "success"
    if state["attempt"] >= state["max_attempts"]:
        return "failed"
    return "retry"

def apply_backoff(state: RetryState) -> dict:
    """Aplica backoff exponencial"""
    backoff = 2 ** state["attempt"]
    time.sleep(min(backoff, 10))  # Max 10s
    return {}

builder = StateGraph(RetryState)
builder.add_node("operation", risky_operation)
builder.add_node("backoff", apply_backoff)

builder.add_edge(START, "operation")
builder.add_conditional_edges(
    "operation",
    should_retry,
    {
        "retry": "backoff",
        "success": END,
        "failed": END
    }
)
builder.add_edge("backoff", "operation")  # Loop

graph = builder.compile()

result = graph.invoke({"attempt": 0, "max_attempts": 5, "result": "", "error": ""})
print(result)
```

______________________________________________________________________

### Pattern 4: Iterative Refinement

**Quando usar**: Melhorar output iterativamente até critério de qualidade.

```python
class RefinementState(TypedDict):
    draft: str
    score: float
    iterations: int
    max_iterations: int

def generate_draft(state: RefinementState) -> dict:
    """Gera versão inicial"""
    return {"draft": "Initial draft"}

def evaluate_quality(state: RefinementState) -> dict:
    """Avalia qualidade (simulado)"""
    import random
    score = random.random()
    return {"score": score, "iterations": state["iterations"] + 1}

def refine_draft(state: RefinementState) -> dict:
    """Refina draft"""
    return {"draft": state["draft"] + " (refined)"}

def should_refine(state: RefinementState) -> Literal["refine", "done"]:
    """Decide se refina ou está bom"""
    if state["score"] >= 0.8:
        return "done"
    if state["iterations"] >= state["max_iterations"]:
        return "done"
    return "refine"

builder = StateGraph(RefinementState)
builder.add_node("generate", generate_draft)
builder.add_node("evaluate", evaluate_quality)
builder.add_node("refine", refine_draft)

builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")
builder.add_conditional_edges(
    "evaluate",
    should_refine,
    {
        "refine": "refine",
        "done": END
    }
)
builder.add_edge("refine", "evaluate")  # Loop

graph = builder.compile()

result = graph.invoke({
    "draft": "",
    "score": 0.0,
    "iterations": 0,
    "max_iterations": 5
})
print(f"Final draft: {result['draft']} (score: {result['score']:.2f})")
```

______________________________________________________________________

## 🌊 Parallel Execution Patterns

### Pattern 5: Map-Reduce

**Quando usar**: Processar múltiplos itens em paralelo e agregar resultados.

```python
from typing import List, Annotated
import operator

class MapReduceState(TypedDict):
    items: List[str]
    results: Annotated[List[str], operator.add]
    final_result: str

def map_node(item: str) -> str:
    """Processa um item individual"""
    return f"Processed: {item}"

def reduce_node(state: MapReduceState) -> dict:
    """Agrega todos os resultados"""
    combined = " | ".join(state["results"])
    return {"final_result": combined}

# LangGraph suporta Send API para parallel execution
from langgraph.graph import Send

def fan_out(state: MapReduceState):
    """Cria múltiplas execuções paralelas"""
    return [Send("process_item", {"item": item}) for item in state["items"]]

builder = StateGraph(MapReduceState)

# Map phase (parallel)
builder.add_node("process_item", lambda s: {"results": [map_node(s["item"])]})

# Reduce phase
builder.add_node("aggregate", reduce_node)

builder.add_conditional_edges(START, fan_out)
builder.add_edge("process_item", "aggregate")
builder.add_edge("aggregate", END)

graph = builder.compile()

result = graph.invoke({
    "items": ["A", "B", "C", "D"],
    "results": [],
    "final_result": ""
})
print(result["final_result"])
# Output: "Processed: A | Processed: B | Processed: C | Processed: D"
```

______________________________________________________________________

## 🎯 Specialized Patterns

### Pattern 6: RAG (Retrieval Augmented Generation)

**Quando usar**: Responder perguntas usando documentos externos.

```python
class RAGState(TypedDict):
    question: str
    documents: List[str]
    context: str
    answer: str

def retrieve_documents(state: RAGState) -> dict:
    """Busca documentos relevantes"""
    # Simulação - em produção, usa vector store
    docs = ["Doc1: Python is great", "Doc2: LangGraph is powerful"]
    return {"documents": docs}

def decide_retrieval(state: RAGState) -> Literal["retrieve", "answer"]:
    """Decide se precisa buscar docs ou já pode responder"""
    # Simulação - LLM decide se tem contexto suficiente
    if "what is" in state["question"].lower():
        return "retrieve"
    return "answer"

def build_context(state: RAGState) -> dict:
    """Constrói contexto a partir dos docs"""
    context = "\n".join(state["documents"])
    return {"context": context}

def generate_answer(state: RAGState) -> dict:
    """Gera resposta usando contexto (ou não)"""
    if state.get("context"):
        answer = f"Based on context: {state['context']}, the answer is..."
    else:
        answer = "Direct answer without retrieval"
    return {"answer": answer}

builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve_documents)
builder.add_node("contextualize", build_context)
builder.add_node("answer", generate_answer)

builder.add_conditional_edges(
    START,
    decide_retrieval,
    {
        "retrieve": "retrieve",
        "answer": "answer"
    }
)
builder.add_edge("retrieve", "contextualize")
builder.add_edge("contextualize", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

result = graph.invoke({
    "question": "What is LangGraph?",
    "documents": [],
    "context": "",
    "answer": ""
})
print(result["answer"])
```

______________________________________________________________________

### Pattern 7: Self-Correction Loop

**Quando usar**: Agent revisa e corrige seu próprio output.

```python
class SelfCorrectionState(TypedDict):
    task: str
    draft: str
    feedback: str
    iterations: int
    max_iterations: int
    approved: bool

def generate_solution(state: SelfCorrectionState) -> dict:
    """Gera solução inicial ou revisada"""
    if state.get("feedback"):
        draft = f"{state['draft']} [Revised based on: {state['feedback']}]"
    else:
        draft = "Initial solution"
    return {"draft": draft, "iterations": state["iterations"] + 1}

def self_critique(state: SelfCorrectionState) -> dict:
    """Agent critica seu próprio trabalho"""
    # Simulação - em produção, outro LLM ou mesmo LLM avalia
    import random
    if random.random() > 0.6:
        return {"approved": True, "feedback": ""}
    else:
        return {
            "approved": False,
            "feedback": "Needs improvement in clarity"
        }

def should_revise(state: SelfCorrectionState) -> Literal["revise", "done"]:
    """Decide se precisa revisar"""
    if state["approved"]:
        return "done"
    if state["iterations"] >= state["max_iterations"]:
        return "done"
    return "revise"

builder = StateGraph(SelfCorrectionState)
builder.add_node("generate", generate_solution)
builder.add_node("critique", self_critique)

builder.add_edge(START, "generate")
builder.add_edge("generate", "critique")
builder.add_conditional_edges(
    "critique",
    should_revise,
    {
        "revise": "generate",  # Loop
        "done": END
    }
)

graph = builder.compile()

result = graph.invoke({
    "task": "Write a summary",
    "draft": "",
    "feedback": "",
    "iterations": 0,
    "max_iterations": 3,
    "approved": False
})
print(f"Final draft: {result['draft']}")
print(f"Approved: {result['approved']}, Iterations: {result['iterations']}")
```

______________________________________________________________________

## 🔒 Production Patterns

### Pattern 8: Error Handling & Fallbacks

```python
class RobustState(TypedDict):
    input: str
    result: str
    error: str
    fallback_used: bool

def primary_node(state: RobustState) -> dict:
    """Node principal que pode falhar"""
    try:
        # Operação que pode dar erro
        result = risky_operation(state["input"])
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def fallback_node(state: RobustState) -> dict:
    """Fallback se primary falhar"""
    return {
        "result": f"Fallback result for: {state['input']}",
        "fallback_used": True
    }

def route_on_error(state: RobustState) -> Literal["success", "fallback"]:
    """Roteia baseado em erro"""
    if state.get("error"):
        return "fallback"
    return "success"

builder = StateGraph(RobustState)
builder.add_node("primary", primary_node)
builder.add_node("fallback", fallback_node)

builder.add_edge(START, "primary")
builder.add_conditional_edges(
    "primary",
    route_on_error,
    {
        "success": END,
        "fallback": "fallback"
    }
)
builder.add_edge("fallback", END)

graph = builder.compile()
```

______________________________________________________________________

### Pattern 9: Rate Limiting & Throttling

```python
import time
from collections import deque
from typing import Deque

class ThrottledState(TypedDict):
    requests: Annotated[Deque, lambda x, y: x]  # Custom reducer
    result: str

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def allow_request(self) -> bool:
        now = time.time()
        # Remove requests fora da janela
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

rate_limiter = RateLimiter(max_requests=5, time_window=60)

def throttled_api_call(state: ThrottledState) -> dict:
    """API call com rate limiting"""
    if not rate_limiter.allow_request():
        return {"result": "Rate limit exceeded, retrying..."}

    # Faz chamada
    return {"result": "API call successful"}

def should_retry(state: ThrottledState) -> Literal["retry", "done"]:
    if "exceeded" in state["result"]:
        time.sleep(1)  # Backoff
        return "retry"
    return "done"

builder = StateGraph(ThrottledState)
builder.add_node("api_call", throttled_api_call)

builder.add_edge(START, "api_call")
builder.add_conditional_edges(
    "api_call",
    should_retry,
    {
        "retry": "api_call",
        "done": END
    }
)

graph = builder.compile()
```

______________________________________________________________________

## 📊 Pattern Selection Guide

| Pattern | Complexity | Use Case | Best For |
|---------|-----------|----------|----------|
| Supervisor | Medium | Multi-agent coordination | Task delegation |
| Hierarchical | High | Complex workflows | Modular systems |
| Retry/Backoff | Low | Unreliable operations | API calls |
| Iterative Refinement | Medium | Quality improvement | Content generation |
| Map-Reduce | Medium | Parallel processing | Batch operations |
| RAG | High | Knowledge-based QA | Document retrieval |
| Self-Correction | High | Quality assurance | Self-improvement |
| Error Handling | Low | Robustness | Production systems |
| Rate Limiting | Medium | API constraints | External services |

## ✅ Best Practices

### State Design

1. **Keep State Minimal**: Apenas campos necessários
1. **Use Reducers**: Para acumulação (add_messages, operator.add)
1. **Type Safety**: TypedDict sempre

### Node Design

1. **Pure Functions**: Evite side effects quando possível
1. **Single Responsibility**: Um node = uma tarefa
1. **Error Handling**: Try/catch dentro de nodes críticos

### Edge Design

1. **Explicit Routing**: Conditional edges com Literal types
1. **Avoid Infinite Loops**: Sempre tenha condição de parada
1. **Clear Decisions**: Router functions com lógica clara

### Performance

1. **Parallel When Possible**: Use Send API
1. **Lazy Loading**: Carregue recursos sob demanda
1. **Caching**: Cache resultados de operations caras

### Production

1. **Checkpointing**: Sempre em produção
1. **Observability**: Log state transitions
1. **Testing**: Unit tests para nodes, integration tests para graphs
1. **Monitoring**: Track execution time, errors, retry rates

## 🚀 Advanced Patterns

Para padrões mais avançados:

- **Multi-tenant**: Isolamento de state por tenant
- **A/B Testing**: Routing baseado em feature flags
- **Circuit Breaker**: Proteção contra cascading failures
- **Saga Pattern**: Transações distribuídas com compensação

Consulte LangGraph documentation para implementações detalhadas.
