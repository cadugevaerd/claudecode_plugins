# LangGraph, LangChain e LangSmith - Guia Completo de Desenvolvimento de Agentes (2025)

> Última atualização: Dezembro 2025
> Versões: LangGraph 0.3+, LangChain 1.0+, LangSmith

## Índice
1. [Visão Geral do Ecossistema](#visão-geral-do-ecossistema)
2. [LangGraph - Framework Principal para Agentes](#langgraph)
3. [Arquiteturas de Agentes](#arquiteturas-de-agentes)
4. [State Management e Persistência](#state-management-e-persistência)
5. [Memória (Short-Term e Long-Term)](#memória)
6. [Human-in-the-Loop](#human-in-the-loop)
7. [Tools e ToolNode](#tools-e-toolnode)
8. [Streaming](#streaming)
9. [Multi-Agent Systems](#multi-agent-systems)
10. [Subgraphs e Composição](#subgraphs-e-composição)
11. [LangSmith - Observabilidade e Avaliação](#langsmith)
12. [LangGraph Platform e Deploy](#langgraph-platform)
13. [Best Practices para Produção](#best-practices)
14. [Código de Referência](#código-de-referência)

---

## 1. Visão Geral do Ecossistema

### Recomendação Oficial 2025
- **LangGraph** é o framework recomendado para TODOS os novos projetos de agentes
- **LangChain** continua suportado mas indicado para "orquestração simples"
- **LangSmith** para observabilidade, tracing, debugging e avaliação

### Empresas em Produção
LinkedIn, Uber, Replit, Klarna e Elastic utilizam LangGraph em produção.

---

## 2. LangGraph - Framework Principal para Agentes

### Versão Atual: LangGraph 0.3+

LangGraph modela workflows de agentes como grafos usando três componentes:
- **State**: Estrutura de dados compartilhada representando snapshot atual
- **Nodes**: Funções Python que codificam a lógica do agente
- **Edges**: Funções que determinam qual Node executar próximo

### Duas APIs Disponíveis

#### Graph API (StateGraph)
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]
    
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
app = graph.compile()
```

#### Functional API (Introduzida Janeiro 2025)
```python
from langgraph.func import entrypoint, task

@task
async def my_task(input: str) -> str:
    return f"Processed: {input}"

@entrypoint(checkpointer=checkpointer)
async def my_workflow(input: str) -> str:
    result = await my_task(input)
    return result
```

### Diferenças entre APIs

| Aspecto | Functional API | Graph API |
|---------|---------------|-----------|
| Controle de Fluxo | Python nativo (if, for, funções) | Definição explícita do grafo |
| State Management | Escopo local à função | Declarar State + reducers |
| Time Travel | Limitado (beta) | Suporte completo |
| Checkpointing | Por entrypoint | Por superstep |

---

## 3. Arquiteturas de Agentes

### Padrão ReAct (Reasoning + Acting)
Combinação de raciocínio chain-of-thought com capacidade de tomar ações via tools.

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather, search_web],
    prompt="You are a helpful assistant"
)

# Executar
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

### Deep Agents (Arquitetura Avançada)
Para tarefas complexas, implementar combinação de:
1. **Planning Tool**: Para planejamento de longo prazo
2. **Sub-Agents**: Agentes especializados para subtarefas
3. **File System Access**: Persistência de artefatos
4. **Detailed Prompt**: Instruções detalhadas

### Multi-Agent Patterns

#### Supervisor Pattern
```python
# Supervisor roteia para agentes especializados
supervisor -> research_agent
           -> code_agent  
           -> writing_agent
```

#### Swarm Pattern
Agentes comunicam peer-to-peer, compartilhando informações autonomamente.

#### Sequential/Pipeline
Agentes executam em sequência definida, cada um processando output do anterior.

---

## 4. State Management e Persistência

### Checkpointers
Salvam snapshot do estado do grafo a cada super-step.

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.redis import RedisSaver

# Desenvolvimento
checkpointer = MemorySaver()

# Produção
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
# ou
checkpointer = RedisSaver(redis_client)

# Compilar com checkpointer
app = graph.compile(checkpointer=checkpointer)
```

### Threads
Cada thread tem `thread_id` único e mantém seu próprio conjunto de checkpoints.

```python
# Invocar com thread_id para persistência
config = {"configurable": {"thread_id": "user-123-session-1"}}
result = app.invoke({"messages": [...]}, config=config)
```

### State Schema com Reducers
```python
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]  # Reducer: concatena listas
    current_step: str
    results: Annotated[list, add]
```

---

## 5. Memória

### Short-Term Memory (Thread-Scoped)
Implementada via checkpointers - persiste durante uma conversa/thread.

```python
# Automático com checkpointer configurado
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Mensagens anteriores são lembradas na mesma thread
app.invoke({"messages": [HumanMessage("Olá")]}, config)
app.invoke({"messages": [HumanMessage("Lembra o que eu disse?")]}, config)
```

### Long-Term Memory (Cross-Thread via Store)
Para informações que persistem entre diferentes conversas/threads.

```python
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore

# Store para memória cross-thread
store = InMemoryStore()
# ou produção:
store = PostgresStore(conn_string=DATABASE_URL)

app = graph.compile(
    checkpointer=checkpointer,
    store=store
)

# Acessar store dentro de nodes
def my_node(state, config, store):
    # Namespace por usuário
    namespace = ("user", config["user_id"])
    
    # Recuperar memórias
    memories = store.search(namespace, query="preferências")
    
    # Salvar nova memória  
    store.put(namespace, "pref_theme", {"value": "dark"})
```

### Tipos de Memória (Inspirado em Cognição Humana)
- **Semantic Memory**: Fatos sobre o usuário
- **Episodic Memory**: Experiências passadas
- **Procedural Memory**: Regras e procedimentos

---

## 6. Human-in-the-Loop

### Função `interrupt` (Recomendada desde LangGraph 0.2.31)

```python
from langgraph.types import interrupt, Command

def review_node(state):
    # Pausar para revisão humana
    decision = interrupt({
        "action": "review_required",
        "data": state["pending_action"],
        "options": ["approve", "reject", "modify"]
    })
    
    if decision == "approve":
        return Command(goto="execute")
    elif decision == "reject":
        return Command(goto="abort")
    else:
        return Command(goto="modify", update={"action": decision})
```

### Três Padrões Principais

1. **Approve/Reject**: Pausar antes de ação crítica
```python
def critical_action_node(state):
    approval = interrupt({
        "type": "approval_required",
        "action": state["pending_api_call"]
    })
    if approval["approved"]:
        return execute_action(state)
    return abort_action(state)
```

2. **Edit State**: Pausar para edição manual do estado
3. **Get Input**: Solicitar input adicional do usuário

### Resumindo Execução
```python
# Após aprovação humana
result = app.invoke(
    Command(resume="approved"),
    config={"configurable": {"thread_id": "..."}}
)
```

---

## 7. Tools e ToolNode

### Criando Tools com @tool
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: Sunny, 25°C"

@tool  
def search_database(query: str, limit: int = 10) -> list:
    """Search the database for relevant records."""
    return db.search(query, limit=limit)
```

### ToolNode
```python
from langgraph.prebuilt import ToolNode

tools = [get_weather, search_database]
tool_node = ToolNode(tools)

# Adicionar ao grafo
graph.add_node("tools", tool_node)
```

### Structured Output com Tools
```python
from pydantic import BaseModel

class ResponseFormat(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

# Forçar output estruturado
agent = create_react_agent(
    model=model,
    tools=tools,
    response_format=ResponseFormat
)
```

### ToolRuntime (Novo em 2025)
Parâmetro unificado para acesso a state, store, streaming, config:

```python
from langgraph.prebuilt import InjectedToolRuntime

@tool
def my_tool(query: str, runtime: InjectedToolRuntime) -> str:
    # Acessar state
    current_state = runtime.state
    # Acessar store
    memory = runtime.store.get(...)
    # Streaming
    runtime.stream("Processing...")
    return result
```

---

## 8. Streaming

### Cinco Modos de Streaming

```python
# 1. values - Estado completo
async for chunk in app.astream(input, mode="values"):
    print(chunk)

# 2. updates - Apenas deltas do estado
async for chunk in app.astream(input, mode="updates"):
    print(chunk)

# 3. messages - Tokens do LLM + metadata (efeito "digitando")
async for chunk in app.astream(input, mode="messages"):
    print(chunk)

# 4. custom - Dados arbitrários do usuário
async for chunk in app.astream(input, mode="custom"):
    print(chunk)

# 5. debug - Traces detalhados
async for chunk in app.astream(input, mode="debug"):
    print(chunk)
```

### Streaming de Tokens em Tempo Real
```python
from langchain_openai import ChatOpenAI

# Habilitar streaming no modelo
model = ChatOpenAI(model="gpt-4", streaming=True)

# Usar astream_events para tokens
async for event in app.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="", flush=True)
```

### Streaming em Subgraphs
```python
# Capturar eventos de subgraphs aninhados
async for chunk in app.astream(
    input, 
    mode="updates",
    subgraphs=True  # Incluir updates de subgraphs
):
    print(chunk)
```

---

## 9. Multi-Agent Systems

### Quando Usar Multi-Agent
- **Context Management**: Conhecimento especializado sem sobrecarregar contexto
- **Desenvolvimento Distribuído**: Times diferentes mantêm agentes diferentes
- **Paralelização**: Workers especializados para subtarefas concorrentes

### Supervisor Architecture
```python
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph

# Agentes especializados
research_agent = create_react_agent(model, [search_tool, wiki_tool])
code_agent = create_react_agent(model, [execute_code, lint_tool])

def supervisor_node(state):
    # Decidir qual agente usar
    task_type = classify_task(state["messages"][-1])
    if task_type == "research":
        return Command(goto="research")
    elif task_type == "code":
        return Command(goto="code")
    return Command(goto="respond")

# Construir grafo
graph = StateGraph(State)
graph.add_node("supervisor", supervisor_node)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)
graph.add_node("respond", response_node)
```

### Handoff Pattern
```python
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

def transfer_to_sales(state: AgentState):
    """Transfer to sales agent."""
    return Command(goto="sales_agent")

def transfer_to_support(state: AgentState):
    """Transfer to support agent."""
    return Command(goto="support_agent")

# Agente com handoff tools
agent = create_react_agent(
    model,
    tools=[transfer_to_sales, transfer_to_support, ...other_tools]
)
```

---

## 10. Subgraphs e Composição

### Criando Subgraphs
```python
# Subgraph para processamento de documentos
class DocState(TypedDict):
    document: str
    extracted_text: str
    summary: str

doc_graph = StateGraph(DocState)
doc_graph.add_node("extract", extract_node)
doc_graph.add_node("summarize", summarize_node)
doc_graph.add_edge("extract", "summarize")
doc_subgraph = doc_graph.compile()

# Grafo principal
class MainState(TypedDict):
    messages: list
    documents: list

main_graph = StateGraph(MainState)
main_graph.add_node("process_docs", doc_subgraph)  # Subgraph como node
main_graph.add_node("respond", respond_node)
```

### State Transformation entre Grafos
```python
def transform_state_for_subgraph(state: MainState) -> DocState:
    return {
        "document": state["documents"][0],
        "extracted_text": "",
        "summary": ""
    }

def transform_result_to_main(result: DocState, state: MainState) -> MainState:
    return {
        **state,
        "processed_summary": result["summary"]
    }
```

### Subgraphs Aninhados
LangGraph suporta múltiplos níveis: parent → child → grandchild

---

## 11. LangSmith - Observabilidade e Avaliação

### Configuração Básica
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=my-project
```

### Tracing Automático
Com LangChain/LangGraph, basta configurar a variável de ambiente.

### OpenTelemetry (Março 2025)
Suporte end-to-end para padronizar tracing em toda a stack.

### Avaliação com Datasets

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Criar dataset
dataset = client.create_dataset("my-eval-dataset")
client.create_examples(
    inputs=[{"query": "What is 2+2?"}],
    outputs=[{"answer": "4"}],
    dataset_id=dataset.id
)

# Definir evaluator customizado
def accuracy_evaluator(run, example):
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]
    return {"score": 1.0 if predicted == expected else 0.0}

# Executar avaliação
results = evaluate(
    my_agent,
    data=dataset.name,
    evaluators=[accuracy_evaluator]
)
```

### Evaluators Pré-construídos (UI - Março 2025)
- **Hallucination**: Detecta alucinações
- **Correctness**: Verifica correção
- **Conciseness**: Avalia concisão
- **Code Checker**: Valida código

### Online vs Offline Evaluation
- **Offline**: Em datasets pré-compilados
- **Online**: Em tráfego de produção em tempo real

---

## 12. LangGraph Platform e Deploy

### Opções de Deploy (Outubro 2025 - GA)

| Opção | Descrição |
|-------|-----------|
| **Cloud (SaaS)** | Fully managed, deploy via LangSmith |
| **Hybrid** | SaaS control plane + self-hosted data plane |
| **Self-Hosted** | Infraestrutura própria, nada sai do VPC |
| **BYOC** | Bring Your Own Cloud (AWS) |

### LangGraph Server
```python
# langgraph.json
{
    "dependencies": ["langchain", "langgraph"],
    "graphs": {
        "my_agent": "./src/agent.py:graph"
    }
}
```

```bash
# Deploy
langgraph build
langgraph push
```

### Studio v2 (Maio 2025)
- Integração LangSmith
- Edição de configuração in-place
- Download de production traces para debug local

---

## 13. Best Practices para Produção

### Seis Features Essenciais
1. **Paralelização**: Executar tools/nodes em paralelo
2. **Streaming**: Feedback em tempo real
3. **Checkpointing**: Persistência e recuperação
4. **Human-in-the-Loop**: Supervisão humana
5. **Tracing**: Observabilidade completa
6. **Task Queue**: Gerenciamento de trabalhos

### Fault Tolerance
```python
# Retries automáticos
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model,
    tools,
    retry_policy={
        "max_attempts": 3,
        "backoff_factor": 2
    }
)
```

### Context Engineering
> "Context engineering is the next level of prompt engineering" — 2025

Automatizar dinamicamente a construção de contexto para modelos.

### Padrões de Implementação

1. **Workflow-first**: State machines explícitas com gates humanos
2. **Agent-first**: Raciocínio autônomo com delegação de tools
3. **Iteration-first**: Loops simples com reflexão

### Arquitetura Híbrida (Recomendada)
```python
# LangChain para chains de prompts
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chain = prompt | model | parser

# LangGraph para orquestração
graph = StateGraph(State)
graph.add_node("process", chain)  # Chain como node
graph.add_node("decide", decision_node)
```

---

## 14. Código de Referência

### Agente ReAct Completo com Memória
```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

# Tools
@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return web_search_api(query)

@tool
def get_user_preferences(user_id: str) -> dict:
    """Get user preferences from long-term memory."""
    return {"theme": "dark", "language": "pt-BR"}

# Model
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Persistência
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
store = PostgresStore.from_conn_string(DATABASE_URL)

# Criar agente
agent = create_react_agent(
    model=model,
    tools=[search_web, get_user_preferences],
    checkpointer=checkpointer,
    store=store,
    prompt="You are a helpful assistant. Remember user preferences."
)

# Executar
config = {
    "configurable": {
        "thread_id": "user-123-session-456",
        "user_id": "user-123"
    }
}

result = agent.invoke(
    {"messages": [HumanMessage("Busque notícias sobre IA")]},
    config=config
)
```

### Multi-Agent com Supervisor
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from typing import TypedDict, Annotated, Literal
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]
    next_agent: str

# Agentes especializados
research_agent = create_react_agent(model, [search_tool])
code_agent = create_react_agent(model, [execute_code])

def supervisor(state: State) -> Command:
    """Route to appropriate agent."""
    last_message = state["messages"][-1].content.lower()
    
    if "pesquise" in last_message or "busque" in last_message:
        return Command(goto="research")
    elif "código" in last_message or "implemente" in last_message:
        return Command(goto="code")
    else:
        return Command(goto=END)

# Construir grafo
graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)

graph.add_edge(START, "supervisor")
graph.add_edge("research", "supervisor")
graph.add_edge("code", "supervisor")

app = graph.compile(checkpointer=checkpointer)
```

---

## Referências

### Documentação Oficial
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/docs/)
- [LangSmith Docs](https://docs.smith.langchain.com/)

### Blog Posts Importantes
- [LangGraph 0.3 Release](https://blog.langchain.com/langgraph-0-3-release-prebuilt-agents/)
- [Functional API Introduction](https://blog.langchain.com/introducing-the-langgraph-functional-api/)
- [Deep Agents Architecture](https://blog.langchain.com/deep-agents/)
- [Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/)
- [LangGraph Platform GA](https://blog.langchain.com/langgraph-platform-ga/)
- [Long-Term Memory Support](https://blog.langchain.com/launching-long-term-memory-support-in-langgraph/)
- [Human-in-the-Loop with Interrupt](https://blog.langchain.com/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt/)

### Tutoriais
- [DataCamp LangGraph Tutorial](https://www.datacamp.com/tutorial/langgraph-agents)
- [Real Python LangGraph Guide](https://realpython.com/langgraph-python/)
- [LangChain Academy](https://academy.langchain.com/)

---

*Documento gerado automaticamente a partir de pesquisas web em Dezembro 2025*
