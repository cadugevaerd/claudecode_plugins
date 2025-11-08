# LangGraph 1.0 - Real Code Examples

Exemplos completos e testados usando LangGraph versão 1.0 API.

## 📦 Setup Inicial

```bash
pip install langgraph langchain-anthropic langchain-core
```

## Exemplo 1: Basic Sequential Workflow

**Caso de uso**: Processar texto em múltiplas etapas sequenciais.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. Definir State Schema
class TextState(TypedDict):
    text: str
    word_count: int

# 2. Definir Nodes
def clean_text(state: TextState) -> dict:
    """Remove espaços extras e normaliza"""
    cleaned = " ".join(state["text"].split())
    return {"text": cleaned}

def count_words(state: TextState) -> dict:
    """Conta palavras no texto"""
    count = len(state["text"].split())
    return {"word_count": count}

def format_output(state: TextState) -> dict:
    """Formata saída final"""
    result = f"Text: {state['text']}\nWords: {state['word_count']}"
    return {"text": result}

# 3. Construir Graph
builder = StateGraph(TextState)
builder.add_node("clean", clean_text)
builder.add_node("count", count_words)
builder.add_node("format", format_output)

# 4. Definir Edges
builder.add_edge(START, "clean")
builder.add_edge("clean", "count")
builder.add_edge("count", "format")
builder.add_edge("format", END)

# 5. Compilar
graph = builder.compile()

# 6. Executar
result = graph.invoke({
    "text": "  Hello    world  from   LangGraph  ",
    "word_count": 0
})
print(result)
# Output:
# {
#   "text": "Text: Hello world from LangGraph\nWords: 4",
#   "word_count": 4
# }
```

**Conceitos demonstrados**:

- State como TypedDict
- Nodes como funções puras
- Sequential edges (START → clean → count → format → END)

______________________________________________________________________

## Exemplo 2: Conditional Routing (Decision Making)

**Caso de uso**: Rotear baseado em condições do state.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
import random

# 1. State com score
class DecisionState(TypedDict):
    message: str
    score: float
    decision: str

# 2. Nodes
def evaluate(state: DecisionState) -> dict:
    """Avalia mensagem e atribui score"""
    score = random.random()  # Simulação
    return {"score": score}

def handle_high_score(state: DecisionState) -> dict:
    """Processamento para high score"""
    return {"decision": f"APPROVED (score: {state['score']:.2f})"}

def handle_low_score(state: DecisionState) -> dict:
    """Processamento para low score"""
    return {"decision": f"REJECTED (score: {state['score']:.2f})"}

# 3. Conditional Router Function
def decide_path(state: DecisionState) -> Literal["high", "low"]:
    """
    Retorna nome da próxima edge baseado em condição.
    IMPORTANTE: Usar Literal type hint para type safety.
    """
    if state["score"] >= 0.5:
        return "high"
    return "low"

# 4. Construir Graph
builder = StateGraph(DecisionState)
builder.add_node("evaluate", evaluate)
builder.add_node("approve", handle_high_score)
builder.add_node("reject", handle_low_score)

builder.add_edge(START, "evaluate")

# Conditional edge: evaluate → {approve OR reject}
builder.add_conditional_edges(
    "evaluate",
    decide_path,
    {
        "high": "approve",
        "low": "reject"
    }
)

builder.add_edge("approve", END)
builder.add_edge("reject", END)

graph = builder.compile()

# Executar múltiplas vezes
for i in range(3):
    result = graph.invoke({"message": f"Request {i}", "score": 0.0, "decision": ""})
    print(result["decision"])

# Output (varia aleatoriamente):
# APPROVED (score: 0.73)
# REJECTED (score: 0.21)
# APPROVED (score: 0.89)
```

**Conceitos demonstrados**:

- Conditional edges com router function
- Literal type hints para type safety
- Routing dinâmico baseado em state

______________________________________________________________________

## Exemplo 3: Agentic Loop (ReAct Pattern)

**Caso de uso**: Agent que decide quando usar tools vs. responder diretamente.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 1. State com messages (padrão para agents)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Reducer built-in

# 2. Nodes
def llm_node(state: AgentState) -> dict:
    """
    LLM decide: usar tool ou responder diretamente.
    Simulação simplificada.
    """
    last_message = state["messages"][-1]

    # Simulação: se pergunta contém "calculate", usa tool
    if "calculate" in last_message.content.lower():
        response = AIMessage(content="TOOL_CALL:calculator:2+2")
    else:
        response = AIMessage(content="I can help you with that!")

    return {"messages": [response]}

def tool_executor(state: AgentState) -> dict:
    """
    Executa tool e retorna resultado.
    """
    last_message = state["messages"][-1]

    # Parse tool call (simplificado)
    if "calculator" in last_message.content:
        result = "4"  # Simulação
        tool_response = AIMessage(content=f"Calculator result: {result}")
        return {"messages": [tool_response]}

    return {"messages": []}

# 3. Router: Decide se continua loop ou termina
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Se última mensagem é tool call, vai para tools.
    Senão, termina.
    """
    last_message = state["messages"][-1]

    if "TOOL_CALL" in last_message.content:
        return "tools"
    return "end"

# 4. Construir Agentic Loop
builder = StateGraph(AgentState)
builder.add_node("llm", llm_node)
builder.add_node("tools", tool_executor)

builder.add_edge(START, "llm")
builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
builder.add_edge("tools", "llm")  # Loop back!

graph = builder.compile()

# Executar
result = graph.invoke({
    "messages": [HumanMessage(content="Can you calculate 2+2?")]
})

for msg in result["messages"]:
    print(f"{msg.__class__.__name__}: {msg.content}")

# Output:
# HumanMessage: Can you calculate 2+2?
# AIMessage: TOOL_CALL:calculator:2+2
# AIMessage: Calculator result: 4
# AIMessage: I can help you with that!
```

**Conceitos demonstrados**:

- Agentic loop (LLM ↔ Tools)
- Messages reducer (add_messages)
- Loop back edge (tools → llm)
- Conditional routing para terminar loop

______________________________________________________________________

## Exemplo 4: Persistence & Memory (Checkpointing)

**Caso de uso**: Manter contexto entre múltiplas invocações (chat com memória).

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

# 1. State
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Node
def chatbot(state: ChatState) -> dict:
    """Chatbot simples que responde baseado em histórico"""
    last_msg = state["messages"][-1]

    # Resposta baseada em contexto
    response = AIMessage(content=f"You said: {last_msg.content}")
    return {"messages": [response]}

# 3. Construir Graph com Checkpointer
builder = StateGraph(ChatState)
builder.add_node("chat", chatbot)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# CRÍTICO: Adicionar checkpointer para persistence
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 4. Executar com thread_id
config = {"configurable": {"thread_id": "user-123"}}

# Primeira mensagem
result1 = graph.invoke(
    {"messages": [HumanMessage(content="Hi, I'm Alice")]},
    config=config
)
print("Turn 1:", result1["messages"][-1].content)

# Segunda mensagem (MESMA thread_id)
result2 = graph.invoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config=config
)
print("Turn 2:", result2["messages"][-1].content)

# Histórico completo
print("\nFull history:")
for msg in result2["messages"]:
    print(f"  {msg.__class__.__name__}: {msg.content}")

# Output:
# Turn 1: You said: Hi, I'm Alice
# Turn 2: You said: What's my name?
#
# Full history:
#   HumanMessage: Hi, I'm Alice
#   AIMessage: You said: Hi, I'm Alice
#   HumanMessage: What's my name?
#   AIMessage: You said: What's my name?
```

**Conceitos demonstrados**:

- MemorySaver checkpointer
- thread_id para separar conversas
- State persistence entre invocações
- Messages acumulam automaticamente (add_messages reducer)

______________________________________________________________________

## Exemplo 5: Human-in-the-Loop (Approval Workflow)

**Caso de uso**: Pausar execução para aprovação humana.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from typing import TypedDict

# 1. State
class ApprovalState(TypedDict):
    request: str
    approved: bool
    result: str

# 2. Nodes
def prepare_request(state: ApprovalState) -> dict:
    """Prepara requisição"""
    return {"request": f"Processing: {state['request']}"}

def human_approval(state: ApprovalState) -> dict:
    """
    PAUSA execução e solicita aprovação humana.
    interrupt() retorna valor fornecido pelo humano.
    """
    approval = interrupt("Approve this request? (yes/no)")

    approved = approval.lower() == "yes" if approval else False
    return {"approved": approved}

def execute_action(state: ApprovalState) -> dict:
    """Executa ação se aprovado"""
    if state["approved"]:
        result = f"Action executed for: {state['request']}"
    else:
        result = "Action cancelled"

    return {"result": result}

# 3. Construir Graph
builder = StateGraph(ApprovalState)
builder.add_node("prepare", prepare_request)
builder.add_node("approval", human_approval)
builder.add_node("execute", execute_action)

builder.add_edge(START, "prepare")
builder.add_edge("prepare", "approval")
builder.add_edge("approval", "execute")
builder.add_edge("execute", END)

# OBRIGATÓRIO: Checkpointer para human-in-the-loop
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 4. Primeira invocação (pausa no interrupt)
config = {"configurable": {"thread_id": "approval-1"}}

try:
    result = graph.invoke(
        {"request": "Delete database", "approved": False, "result": ""},
        config=config
    )
except Exception as e:
    print(f"Paused at interrupt: {e}")

# 5. Fornecer input humano e resumir
from langgraph.types import Command

# Opção 1: Aprovar
resumed = graph.invoke(
    Command(resume="yes"),  # Input humano
    config=config
)
print(resumed["result"])  # "Action executed for: Processing: Delete database"

# Opção 2: Rejeitar (nova thread)
config2 = {"configurable": {"thread_id": "approval-2"}}
graph.invoke(
    {"request": "Delete database", "approved": False, "result": ""},
    config2
)
resumed2 = graph.invoke(Command(resume="no"), config2)
print(resumed2["result"])  # "Action cancelled"
```

**Conceitos demonstrados**:

- interrupt() para pausar execução
- Command(resume=...) para fornecer input humano
- Checkpointer obrigatório para HITL
- Workflow de aprovação

______________________________________________________________________

## Exemplo 6: Streaming Real-Time Updates

**Caso de uso**: Stream state updates em tempo real.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

# 1. State
class StreamState(TypedDict):
    step: int
    status: str

# 2. Nodes (com delay simulando processamento)
def step_1(state: StreamState) -> dict:
    time.sleep(0.5)
    return {"step": 1, "status": "Step 1 completed"}

def step_2(state: StreamState) -> dict:
    time.sleep(0.5)
    return {"step": 2, "status": "Step 2 completed"}

def step_3(state: StreamState) -> dict:
    time.sleep(0.5)
    return {"step": 3, "status": "Step 3 completed"}

# 3. Construir Graph
builder = StateGraph(StreamState)
builder.add_node("s1", step_1)
builder.add_node("s2", step_2)
builder.add_node("s3", step_3)

builder.add_edge(START, "s1")
builder.add_edge("s1", "s2")
builder.add_edge("s2", "s3")
builder.add_edge("s3", END)

graph = builder.compile()

# 4. Stream updates
print("Streaming updates:")
for chunk in graph.stream({"step": 0, "status": "Starting"}):
    print(f"  {chunk}")

# Output:
# Streaming updates:
#   {'s1': {'step': 1, 'status': 'Step 1 completed'}}
#   {'s2': {'step': 2, 'status': 'Step 2 completed'}}
#   {'s3': {'step': 3, 'status': 'Step 3 completed'}}
```

**Conceitos demonstrados**:

- graph.stream() para real-time updates
- Cada chunk = output de um node
- Útil para UIs com progress indicators

______________________________________________________________________

## Exemplo 7: Prebuilt ReAct Agent (Production-Ready)

**Caso de uso**: Agent completo com tools usando prebuilt components.

```python
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# 1. Definir Tools
@tool
def search(query: str) -> str:
    """Search the web for information"""
    # Simulação
    return f"Search results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        result = eval(expression)  # CUIDADO: eval em produção!
        return str(result)
    except:
        return "Invalid expression"

# 2. Criar ReAct Agent (prebuilt)
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",  # Ou outro modelo
    tools=[search, calculator],
    prompt="You are a helpful assistant with search and calculation capabilities."
)

# 3. Usar Agent
result = agent.invoke({
    "messages": [("user", "What's 15 * 23?")]
})

print(result["messages"][-1].content)
# Output: "The result of 15 * 23 is 345."
```

**Conceitos demonstrados**:

- create_react_agent() prebuilt
- @tool decorator para definir tools
- Agent decide automaticamente quando usar tools
- Production-ready com model failover, retry, etc

______________________________________________________________________

## 📊 Comparação de Padrões

| Padrão | Use Case | Complexity | Persistence | HITL |
|--------|----------|-----------|-------------|------|
| Sequential | Pipeline linear | Baixa | Opcional | Não |
| Conditional | Decision trees | Média | Opcional | Não |
| Agentic Loop | Autonomous agents | Alta | Recomendado | Opcional |
| Checkpointing | Multi-turn chat | Média | Obrigatório | Opcional |
| HITL | Approval workflows | Alta | Obrigatório | Sim |
| Prebuilt | Quick prototypes | Baixa | Built-in | Built-in |

## 🎯 Best Practices

1. **Start Simple**: Comece com sequential flow, adicione complexity gradualmente
1. **Type Safety**: Use TypedDict + Literal para evitar bugs
1. **Reducers**: Use add_messages para chat, operator.add para listas
1. **Checkpointing**: Adicione cedo se precisar memory ou HITL
1. **Streaming**: Sempre considere UX com streaming
1. **Prebuilt**: Use create_react_agent() para prototipagem rápida
1. **Testing**: Teste cada node isoladamente antes de integrar

## 📚 Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Academy](https://academy.langchain.com/) - Free course
- [Templates](https://github.com/langchain-ai/langgraph/tree/main/templates)
- [Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)
