---
name: langgraph-state-manager
description: Gerencia estado em grafos LangGraph com TypedDict, reducers customizados e state updates corretos. Use quando criar grafos LangGraph, definir state schema, implementar reducers, ou trabalhar com multi-agent state management.
allowed-tools: Read, Write, Edit, Grep, Glob
---

name: langgraph-state-manager
description: Gerencia estado em grafos LangGraph com TypedDict, reducers customizados e state updates corretos. Use quando criar grafos LangGraph, definir state schema, implementar reducers, ou trabalhar com multi-agent state management.
allowed-tools: Read, Write, Edit, Grep, Glob

# LangGraph State Manager

Skill para gerenciar estado em grafos LangGraph v1 com TypedDict, Annotated reducers e padrões de state updates.

## Instructions

### STEP 0: Consultar Documentação via MCP (OBRIGATÓRIO)

**SEMPRE use MCP para validar padrões de state management**:

- Use `fetch_docs` para buscar "StateGraph reducers", "Annotated state", ou "state management"
- Busque exemplos oficiais de padrões similares ao caso de uso
- Valide sintaxe de reducers (add, custom reducers)
- Verifique padrões multi-agent state se aplicável

**Exemplo**:

````text

User: "Criar state para multi-agent system"
→ ANTES: Use fetch_docs para buscar "multi-agent state" ou "shared scratchpad"
→ Analise padrões oficiais (shared vs private scratchpads)
→ ENTÃO implemente state schema baseado em docs oficiais

```text

### STEP 1: Analisar necessidades de estado

- Identificar dados que precisam ser compartilhados entre nodes
- Determinar se valores devem ser substituídos ou acumulados
- Verificar se há execução concorrente (precisa de reducers)

### STEP 2: Design do State Schema
   - Use `TypedDict` para estrutura de estado
   - Use `Annotated[type, reducer]` para campos que acumulam
   - Campos sem Annotated: override (último valor prevalece)

3. **Implementar State Updates**:
   - Override: `state["field"] = new_value`
   - Additive: Usar reducer apropriado (add, custom)
   - Concurrent: Garantir reducer thread-safe

4. **Validar**:
   - State schema completo (todos campos necessários)
   - Reducers apropriados para padrão de uso
   - Type hints corretos

## When to Use

Use esta skill quando:
- Criar novo grafo LangGraph
- Definir structure de estado para agents
- Implementar reducers customizados
- Trabalhar com multi-agent state management
- Adicionar campos ao estado existente
- Debugar state corruption
- Usuário menciona: "LangGraph state", "TypedDict", "reducer", "state management", "compartilhar dados entre nodes"

## State Patterns

### Pattern 1: Basic State (Override)

```python
from typing import TypedDict

class BasicState(TypedDict):
    current_step: str    # Override: último valor prevalece
    user_input: str      # Override
    result: dict         # Override

```text

### Pattern 2: Additive State (Reducer)

```python
from typing import TypedDict, Annotated
from operator import add

class AdditiveState(TypedDict):
    # Additive: acumula valores
    messages: Annotated[list[str], add]
    scores: Annotated[list[int], add]

```text

### Pattern 3: Custom Reducer

```python
from typing import Annotated

def merge_dicts(left: dict, right: dict) -> dict:
    """Custom reducer que faz merge de dicts"""
    return {**left, **right}

class CustomState(TypedDict):
    metadata: Annotated[dict, merge_dicts]

```text

### Pattern 4: Mixed State

```python
from typing import TypedDict, Annotated
from operator import add

class MixedState(TypedDict):
    # Override fields
    current_agent: str
    iteration: int

    # Additive fields
    messages: Annotated[list[dict], add]
    intermediate_steps: Annotated[list[tuple], add]

    # Custom reducer
    config: Annotated[dict, merge_dicts]

```text

## Common Reducers

### Built-in Reducers
- `add` (operator.add): Concatena listas/soma números
- `or_` (operator.or_): OR lógico
- `and_` (operator.and_): AND lógico

### Custom Reducer Examples

```python

# Merge dicts
def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

# Keep last N items
def keep_last_n(n: int):
    def reducer(left: list, right: list) -> list:
        combined = left + right
        return combined[-n:]
    return reducer

# Deduplicate list
def dedupe_list(left: list, right: list) -> list:
    return list(set(left + right))

```text

## State Update Methods

### Method 1: Override (No Reducer)

```python
def node_function(state: State):
    # Substitui valor completamente
    state["current_step"] = "processing"
    state["iteration"] += 1
    return state

```text

### Method 2: Additive (With Reducer)

```python
def node_function(state: State):
    # Adiciona à lista existente (reducer=add)
    state["messages"].append("New message")

    # Ou retorna partial state (é merged automaticamente)
    return {"messages": ["New message"]}

```text

### Method 3: Concurrent Safe

```python

# State com reducer garante thread-safety
class ConcurrentState(TypedDict):
    results: Annotated[list[dict], add]

# Múltiplos nodes podem adicionar concorrentemente
def node_a(state: ConcurrentState):
    return {"results": [{"node": "A", "data": "..."}]}

def node_b(state: ConcurrentState):
    return {"results": [{"node": "B", "data": "..."}]}

```text

## Multi-Agent Patterns

### Pattern 1: Shared Scratchpad

```python
class SharedState(TypedDict):
    # Todos agentes veem todo trabalho
    messages: Annotated[list[dict], add]
    current_agent: str

def agent_a(state: SharedState):
    # Lê trabalho de outros agentes
    previous_work = [m for m in state["messages"]]

    # Adiciona seu trabalho
    return {
        "messages": [{"agent": "A", "content": "..."}],
        "current_agent": "B"
    }

```text

### Pattern 2: Private Scratchpads

```python
class PrivateState(TypedDict):
    # Cada agente tem seu scratchpad
    agent_a_work: Annotated[list[str], add]
    agent_b_work: Annotated[list[str], add]

    # Apenas resultado final é compartilhado
    final_result: str

def agent_a(state: PrivateState):
    # Trabalha no seu scratchpad privado
    return {"agent_a_work": ["Step 1", "Step 2"]}

def agent_b(state: PrivateState):
    # Não vê agent_a_work, apenas final_result
    return {"agent_b_work": ["Analysis done"]}

def aggregator(state: PrivateState):
    # Combina resultados
    return {
        "final_result": f"A: {state['agent_a_work']}, B: {state['agent_b_work']}"
    }

```text

## Best Practices

✅ **Design State Lean**: Evite crescimento descontrolado
- Apenas dados essenciais
- Considere limitar tamanho de listas (use custom reducer)
- Limpe dados antigos quando possível

✅ **Use Reducers Apropriados**:
- Override para valores únicos (current_step, iteration)
- Add para acumulação (messages, scores)
- Custom para lógica especial (merge, dedupe, limit)

✅ **Thread Safety**:
- Sempre use reducers para execução concorrente
- Teste concurrent execution extensivamente

✅ **Memory Management**:
- Monitor tamanho de state em conversações longas
- Implemente estratégias de cleanup
- Use checkpointing para persistência

## Don't Use This Skill When

- ❌ Trabalhando com LCEL (não tem state management)
- ❌ State management fora de LangGraph
- ❌ Código não relacionado a frameworks LangChain

## Examples

**Example 1 - Basic Agent State**:

```python
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list[str], add]
    iteration: int

def agent_node(state: AgentState):
    state["messages"].append("Agent response")
    state["iteration"] += 1
    return state

```text

**Example 2 - Multi-Agent Shared State**:

```python
class MultiAgentState(TypedDict):
    messages: Annotated[list[dict], add]
    current_agent: str

def research_agent(state: MultiAgentState):
    return {
        "messages": [{"agent": "research", "content": "findings"}],
        "current_agent": "writer"
    }

```text

**Example 3 - Custom Reducer for Limiting History**:

```python
def keep_last_10(left: list, right: list) -> list:
    combined = left + right
    return combined[-10:]

class LimitedState(TypedDict):
    # Mantém apenas últimas 10 mensagens
    messages: Annotated[list[str], keep_last_10]

```text
````
