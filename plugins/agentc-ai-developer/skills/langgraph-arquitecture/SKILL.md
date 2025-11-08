---
name: langgraph-arquitecture
description: LangGraph 1.0 architecture patterns with real code examples - StateGraph, nodes, edges, agentic loops, persistence. Use when building LangGraph agents, implementing state machines, designing agentic workflows, working with LangGraph 1.0 API. Always invoke when analyzing or creating LangGraph code.
version: 1.0.1
allowed-tools:
  - Read
  - Grep
  - WebFetch
---

# LangGraph Architecture

**Conhecimento especializado em arquitetura LangGraph 1.0 com exemplos de código real**

## 📋 When to Use Me

Invoque esta skill quando:

- Construir agentes com LangGraph 1.0
- Implementar StateGraph e state machines
- Desenhar agentic loops (Pensar→Agir→Observar→Pensar)
- Trabalhar com nodes, edges e conditional routing
- Implementar persistence com checkpointers
- Adicionar human-in-the-loop workflows
- Analisar ou revisar código LangGraph existente
- Migrar de versões anteriores para LangGraph 1.0
- Debugar grafos complexos ou multi-agent systems

**Palavras-chave**: LangGraph, StateGraph, agentic loop, nodes, edges, conditional edges, persistence, checkpointer, human-in-the-loop, streaming

## 🎓 Core Knowledge

### Conceitos Fundamentais

LangGraph representa **workflows como grafos** onde:

1. **State** = Dados compartilhados fluindo entre nodes
1. **Nodes** = Funções Python que processam e atualizam state
1. **Edges** = Conexões que definem fluxo de execução
1. **Graph** = Combinação compiled de state + nodes + edges

### Primitivos Principais (LangGraph 1.0)

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 1. State - estrutura de dados compartilhada
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Reducer automático

# 2. Graph Builder
builder = StateGraph(State)

# 3. Nodes - funções que processam state
builder.add_node("node_name", function)

# 4. Edges - conexões entre nodes
builder.add_edge(START, "first_node")
builder.add_edge("node_a", "node_b")
builder.add_edge("last_node", END)

# 5. Conditional Edges - routing baseado em lógica
builder.add_conditional_edges("node", decide_function)

# 6. Compilation
graph = builder.compile()
```

**Mudança LangGraph 1.0**: API estável sem breaking changes. Core primitives (state, nodes, edges) **não mudaram**.

### State Management

**State é um TypedDict** que define schema compartilhado:

```python
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    # Simples override
    input: str
    output: str

    # Acumulação via reducer
    all_actions: Annotated[List[str], operator.add]
    messages: Annotated[list, add_messages]  # Reducer built-in
```

**Reducers**: Definem como múltiplas atualizações são combinadas.

### Node Functions

Nodes são **funções Python puras**:

```python
def my_node(state: State) -> dict:
    """
    - Recebe: state dict conforme State schema
    - Processa: lógica customizada
    - Retorna: dict com keys do State para atualizar
    """
    return {"messages": [AIMessage(content="Hello")]}
```

**Regra de Ouro**: Nodes retornam dicts com partial state updates.

### Edge Types

**1. Direct Edges** (transição fixa):

```python
builder.add_edge("node_a", "node_b")
```

**2. Conditional Edges** (routing dinâmico):

```python
from typing import Literal

def router(state) -> Literal["path_a", "path_b", "__end__"]:
    if condition:
        return "path_a"
    return "__end__"

builder.add_conditional_edges("node", router)
```

**3. Special Edges**:

- `START`: Entry point do grafo
- `END`: Terminal node (finaliza execução)

### LLM vs Tools - Distinção Crítica ⚠️

**ERRO COMUM**: Confundir "LLM calls" com "tools" em LangGraph.

**Conceitos fundamentais**:

1. **LLM é o CORE do agente**, não uma ferramenta

   - LLM node: Node que invoca o modelo de linguagem
   - Responsabilidade: Raciocinar, decidir próximas ações
   - É o "cérebro" do agente
   - Executado repetidamente no loop

1. **Tools são FUNÇÕES que o agente invoca dinamicamente**

   - Exemplos: buscar em database, fazer API call, calcular, etc
   - Executadas em nodes separados (tool_executor node)
   - NÃO são chamadas diretas ao LLM
   - O LLM decide SE usar uma tool e QUAL usar

**Padrão correto**:

```python
# ❌ ERRADO - Tratando LLM como tool
tools = [llm_model]  # Isto é INCORRETO

# ✅ CORRETO - LLM é o core, tools são funções
def llm_node(state):
    """LLM decide qual tool usar"""
    return {"messages": [llm_call]}

def tool_executor_node(state):
    """Executa a tool que o LLM escolheu"""
    tool_name = extract_tool_name(state)
    return {"messages": [execute_tool(tool_name)]}

builder.add_node("llm", llm_node)  # Core
builder.add_node("tools", tool_executor_node)  # Funções executáveis
```

**Arquitetura típica**:

```text
┌─────────────────────┐
│   LLM Node (Core)   │ ← Raciocina, decide
└──────────┬──────────┘
           │ "use_tool: search"
           ↓
┌─────────────────────┐
│  Tool Executor      │ ← Executa função
└──────────┬──────────┘
           │ resultado
           ↓
┌─────────────────────┐
│   LLM Node (Core)   │ ← Processa resultado
└─────────────────────┘
```

**Resumo**:

- LLM = Inteligência (raciocina e decide)
- Tools = Capacidades (fazem coisas específicas)
- Agente = Orquestração (graph definindo fluxo)

### Agentic Loop Pattern

Padrão central para agentes autônomos:

```
START → Think (LLM) → Decide → Act (Tool) → Observe → Think → ...
                          ↓
                         END
```

Implementação típica:

```python
builder.add_node("think", llm_node)
builder.add_node("act", tool_executor)
builder.add_conditional_edges("think", should_continue)
builder.add_edge("act", "think")  # Loop back
```

### Persistence & Checkpointing

**Checkpointer** salva state em cada super-step:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Invoke com thread_id
config = {"configurable": {"thread_id": "user-123"}}
graph.invoke(input_data, config=config)
```

**Benefícios**:

- Memory entre invocações
- Pause/resume execution
- Time-travel debugging
- Human-in-the-loop

### Human-in-the-Loop

**interrupt()** pausa execução para input humano:

```python
from langgraph.types import interrupt

def human_review_node(state):
    # Pause e solicita input
    human_input = interrupt("Approve this action?")
    return {"approved": human_input}
```

**Workflow típico**:

1. Graph executa até interrupt()
1. State é salvo (checkpointer)
1. Humano fornece input
1. Execução resume do ponto exato

### Streaming

LangGraph 1.0 **streams tudo**:

```python
for chunk in graph.stream(input_data):
    print(chunk)  # State updates, tokens, node transitions
```

**Modos de streaming**:

- `values`: Full state após cada node
- `updates`: Partial updates de cada node
- `messages`: Stream de tokens LLM
- `custom`: Dados customizados

## 📚 Reference Files

Para conhecimento detalhado, consulte:

- **EXAMPLES.md** - Exemplos completos de código LangGraph 1.0
- **PATTERNS.md** - Padrões arquiteturais e best practices

## 💡 Quick Examples

### Exemplo 1: Simple Sequential Flow

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    text: str

def node_1(state):
    return {"text": state["text"] + " processed"}

def node_2(state):
    return {"text": state["text"] + " finalized"}

builder = StateGraph(State)
builder.add_node("step1", node_1)
builder.add_node("step2", node_2)
builder.add_edge(START, "step1")
builder.add_edge("step1", "step2")
builder.add_edge("step2", END)

graph = builder.compile()
result = graph.invoke({"text": "initial"})
# result: {"text": "initial processed finalized"}
```

### Exemplo 2: Conditional Routing

```python
from typing import Literal

def decide_path(state) -> Literal["happy", "sad"]:
    if state["score"] > 0.5:
        return "happy"
    return "sad"

builder.add_conditional_edges(
    "evaluator",
    decide_path,
    {"happy": "celebrate", "sad": "retry"}
)
```

### Exemplo 3: ReAct Agent

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[search_tool, calculator_tool],
    prompt="You are a helpful assistant"
)

# Usage
result = agent.invoke({"messages": [("user", "What's 2+2?")]})
```

## ✅ Checklist Rápido

Ao criar LangGraph agent:

- [ ] State schema definido com TypedDict
- [ ] Reducers configurados para fields acumulados (Annotated)
- [ ] Nodes implementados como funções puras retornando dicts
- [ ] Entry point configurado (add_edge(START, ...))
- [ ] Terminal points configurados (add_edge(..., END))
- [ ] Conditional edges com type hints corretos (Literal)
- [ ] Checkpointer adicionado se precisar persistence
- [ ] Config com thread_id se usar checkpointer
- [ ] interrupt() adicionado para human-in-the-loop
- [ ] Streaming configurado se precisar real-time updates

## 🔍 Quick Reference

| Conceito | Import | Exemplo |
|---------|--------|---------|
| StateGraph | `from langgraph.graph import StateGraph` | `StateGraph(State)` |
| START/END | `from langgraph.graph import START, END` | `add_edge(START, "node")` |
| Messages Reducer | `from langgraph.graph.message import add_messages` | `Annotated[list, add_messages]` |
| Memory | `from langgraph.checkpoint.memory import MemorySaver` | `compile(checkpointer=MemorySaver())` |
| Interrupt | `from langgraph.types import interrupt` | `interrupt("message")` |
| ReAct Agent | `from langgraph.prebuilt import create_react_agent` | `create_react_agent(model, tools)` |

## 🎯 Princípios de Design

1. **State é Central**: Todo o sistema gira em torno do state compartilhado
1. **Nodes são Puros**: Funções sem side-effects complexos
1. **Edges Definem Lógica**: Routing é explícito via edges
1. **Persistence é Opcional**: Adicione checkpointer quando precisar memory
1. **Streaming é Default**: Tudo pode ser streamed em real-time
1. **Type Safety**: Use TypedDict e Literal para robustez

## 📖 Next Steps

- Consulte **EXAMPLES.md** para ver 5+ exemplos completos de código real
- Consulte **PATTERNS.md** para padrões como multi-agent, supervisor, subgraphs
- Teste localmente com `pip install langgraph` e execute os exemplos
- Para deployment, veja LangGraph Platform documentation
