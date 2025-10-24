---
description: Ajuda rápida e referência sobre LangGraph v1 - grafos, state management, agentes e padrões multi-agent
---

# LangGraph Help - Assistência Rápida LangGraph v1

Forneço ajuda rápida e referência sobre LangGraph v1, incluindo construção de grafos, state management, agentes e padrões de multi-agent workflows.

## Como usar:

```bash
/langgraph-help [tópico opcional]
```

**Tópicos disponíveis**:
- `graphs` - Construção de grafos (nodes, edges, state)
- `state` - State management e reducers
- `agents` - Padrões de agentes (ReAct, multi-agent)
- `patterns` - Padrões comuns (branching, loops, subgraphs)
- `persistence` - Checkpointing e memória persistente

## O que faço:

### 1. Construção de Grafos
Explico os componentes fundamentais:
- **Nodes**: Funções que processam estado
- **Edges**: Conexões entre nodes (condicionais ou diretas)
- **State**: Shared memory object (TypedDict)
- **Compilation**: Transformar grafo em runnable

### 2. State Management
Ajudo com gerenciamento de estado:
- TypedDict para estrutura de estado
- Annotated types para reducers customizados
- State updates (override vs additive)
- Concurrent execution com reducers
- Memory: checkpointing e thread-local storage

### 3. Padrões de Agentes
Demonstro padrões comuns:
- **ReAct Pattern**: Reasoning + Acting
- **Multi-Agent Collaboration**: Shared scratchpad
- **Multi-Agent Hierarchical**: Private scratchpads
- **Human-in-the-Loop**: Aprovação manual

### 4. Control Flow Avançado
- Conditional branching
- Loops e cycles
- Subgraphs
- Error handling e fallbacks

## Exemplos:

### Basic Graph
```python
from langgraph.graph import StateGraph
from typing import TypedDict

# Definir estado
class AgentState(TypedDict):
    messages: list[str]
    context: dict

# Criar grafo
graph = StateGraph(AgentState)

# Adicionar nodes
graph.add_node("process", process_node)
graph.add_node("analyze", analyze_node)

# Adicionar edges
graph.add_edge("process", "analyze")
graph.set_entry_point("process")
graph.set_finish_point("analyze")

# Compilar
app = graph.compile()
```

### State com Reducers
```python
from typing import Annotated
from operator import add

class State(TypedDict):
    # Override: último valor prevalece
    current_step: str

    # Additive: acumula valores (reducer=add)
    messages: Annotated[list[str], add]

    # Custom reducer
    scores: Annotated[list[int], lambda x, y: x + y]
```

### Conditional Branching
```python
def route_decision(state: AgentState) -> str:
    """Decide qual node executar próximo"""
    if state["score"] > 0.8:
        return "high_quality"
    return "needs_improvement"

# Adicionar edge condicional
graph.add_conditional_edges(
    "analyze",
    route_decision,
    {
        "high_quality": "finalize",
        "needs_improvement": "revise"
    }
)
```

### Multi-Agent Pattern
```python
from langgraph.prebuilt import ToolExecutor

# Agent 1: Research
def research_agent(state):
    # Adiciona ao scratchpad compartilhado
    state["messages"].append({"role": "research", "content": "..."})
    return state

# Agent 2: Writer
def writer_agent(state):
    # Lê do scratchpad compartilhado
    research_data = [m for m in state["messages"] if m["role"] == "research"]
    # Adiciona resultado
    state["messages"].append({"role": "writer", "content": "..."})
    return state

graph.add_node("research", research_agent)
graph.add_node("write", writer_agent)
graph.add_edge("research", "write")
```

### Checkpointing (Persistence)
```python
from langgraph.checkpoint.memory import MemorySaver

# Criar checkpointer
memory = MemorySaver()

# Compilar com checkpointing
app = graph.compile(checkpointer=memory)

# Executar com thread_id para persistência
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke(input_data, config=config)

# Retomar conversação
result2 = app.invoke(new_input, config=config)  # Mantém histórico
```

## Quando me usar:

- ✅ Construir grafos complexos com LangGraph
- ✅ Implementar state management robusto
- ✅ Criar padrões multi-agent
- ✅ Adicionar branching condicional e loops
- ✅ Implementar checkpointing e persistência
- ✅ Migrar de AgentExecutor (LangChain legado)

## Quando usar LangGraph (vs LCEL):

**Use LangGraph quando**:
- ✅ State management complexo necessário
- ✅ Branching condicional ou loops
- ✅ Multi-agent orchestration
- ✅ Persistência de estado (checkpointing)
- ✅ Human-in-the-loop workflows
- ✅ Subgraphs e composição hierárquica

**Use LCEL quando**:
- ✅ Orquestração simples e linear
- ✅ Composição de chains básicas
- ✅ Menos de ~100 steps
- ✅ Sem necessidade de state complexo

## Notas Importantes:

**Best Practices**:
- Design estado enxuto (evite crescimento descontrolado)
- Use reducers apropriados para concurrent execution
- Implemente error handling em nodes críticos
- Considere memory management em multi-agent systems
- Use checkpointing para conversações longas

**Padrões de Comunicação Multi-Agent**:
1. **Shared Scratchpad**: Todos agentes veem todo trabalho
   - Bom para: colaboração estreita, poucos agentes

2. **Private Scratchpads**: Agentes compartilham apenas resultado final
   - Bom para: muitos agentes, agentes complexos

**Recursos Oficiais**:
- Docs: https://langchain-ai.github.io/langgraph/
- Tutorials: https://langchain-ai.github.io/langgraph/tutorials/
- GitHub: https://github.com/langchain-ai/langgraph