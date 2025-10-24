---
name: langchain-test-specialist
description: Cria testes unitários e de integração para aplicações LangChain e LangGraph, incluindo mocking de LLMs, teste de grafos, validação de trajectories, e uso de agentevals. Use quando testar chains LCEL, grafos LangGraph, agents, ou validar trajectories de execução.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# LangChain Test Specialist

Especialista em criar testes unitários e de integração para aplicações **LangChain** e **LangGraph**, com padrões específicos para mocking de LLMs, validação de trajectories, e testes de grafos.

## Instructions

### 1. Detectar Contexto LangChain/LangGraph

Quando detectar código usando:
- `from langchain...` ou `from langgraph...`
- `StateGraph`, `MessageGraph`, `CompiledGraph`
- `ChatOpenAI`, `ChatAnthropic`, `ChatPromptTemplate`
- LCEL chains com pipe operator (`|`)
- Nodes, edges, checkpointers

**Ação**: Aplicar padrões de teste específicos para LangChain/LangGraph.

### 2. Escolher Padrão de Teste Apropriado

**Para LangGraph**:
- **State-based testing**: Testar grafos com `MemorySaver` checkpointer
- **Node-level testing**: Testar nodes individuais via `graph.nodes["node_name"]`
- **Partial execution**: Usar `update_state()` e `interrupt_after` para testar partes do grafo

**Para LangChain**:
- **Unit testing**: Mock LLMs com `GenericFakeChatModel`
- **Integration testing**: Usar `agentevals` para validar trajectories
- **Recording & Replaying**: Usar `vcrpy` para gravar/replay HTTP calls

### 3. Criar Testes Seguindo AAA Pattern

Todos os testes devem seguir:
```python
def test_feature(self):
    """Teste: Descrição clara do cenário"""
    # Arrange - Preparar estado e mocks
    ...

    # Act - Executar função/grafo
    ...

    # Assert - Validar resultado
    ...
```

### 4. Aplicar Padrões Específicos

Use os 7 padrões documentados abaixo dependendo do cenário.

---

## When to Use

Use esta skill quando encontrar:
- Código com `LangChain` ou `LangGraph`
- Chains usando LCEL (pipe operator `|`)
- Grafos com `StateGraph`, `MessageGraph`
- LLM calls (`ChatOpenAI`, `ChatAnthropic`, etc.)
- Agents, tools, ou trajectories
- Pedidos para testar conversational AI, chatbots, workflows LLM
- Termos: "testar chain", "testar grafo", "mock LLM", "trajectory validation"

---

## Test Patterns

### Pattern 1: Basic LangGraph Test (State-based)

**Quando usar**: Testar grafo completo com estado

```python
import pytest
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict


def create_graph() -> StateGraph:
    """Factory para criar grafo de teste"""
    class MyState(TypedDict):
        my_key: str

    graph = StateGraph(MyState)
    graph.add_node("node1", lambda state: {"my_key": "hello"})
    graph.add_edge(START, "node1")
    graph.add_edge("node1", END)
    return graph


def test_basic_graph_execution():
    """Teste: Grafo executa corretamente com estado inicial"""
    # Arrange
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled_graph = graph.compile(checkpointer=checkpointer)

    # Act
    result = compiled_graph.invoke(
        {"my_key": "initial"},
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert
    assert result["my_key"] == "hello"
```

**Aplicar quando**:
- Testar fluxo completo do grafo
- Validar transformações de estado
- Verificar comportamento end-to-end

---

### Pattern 2: Individual Node Testing

**Quando usar**: Testar nodes isoladamente sem executar grafo completo

```python
def test_individual_node():
    """Teste: Node individual funciona sem dependências do grafo"""
    # Arrange
    graph = create_graph()
    compiled_graph = graph.compile()

    # Act
    result = compiled_graph.nodes["node1"].invoke({"my_key": "test"})

    # Assert
    assert result["my_key"] == "hello"


def test_node_with_dependencies():
    """Teste: Node processa dependências corretamente"""
    # Arrange
    def node_with_deps(state):
        return {"result": state["input"] * 2}

    graph = StateGraph(TypedDict("State", {"input": int, "result": int}))
    graph.add_node("processor", node_with_deps)
    compiled = graph.compile()

    # Act
    result = compiled.nodes["processor"].invoke({"input": 5})

    # Assert
    assert result["result"] == 10
```

**Aplicar quando**:
- Testar lógica de node isolada
- Validar transformações de dados
- Debugar issues específicos de node

---

### Pattern 3: Partial Execution (Interrupts)

**Quando usar**: Testar partes do grafo ou simular pausas

```python
def test_partial_execution_with_interrupt():
    """Teste: Grafo executa até ponto de interrupção"""
    # Arrange
    checkpointer = MemorySaver()

    class State(TypedDict):
        value: int

    def increment(state):
        return {"value": state["value"] + 1}

    graph = StateGraph(State)
    graph.add_node("node1", increment)
    graph.add_node("node2", increment)
    graph.add_node("node3", increment)
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", "node3")
    graph.add_edge("node3", END)

    compiled = graph.compile(checkpointer=checkpointer)

    # Act - Executar até node3
    result = compiled.invoke(
        {"value": 0},
        config={"configurable": {"thread_id": "1"}},
        interrupt_after=["node2"]
    )

    # Assert - Parou no node2, não executou node3
    assert result["value"] == 2

    # Act - Continuar execução
    final_result = compiled.invoke(
        None,
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert - Agora executou node3
    assert final_result["value"] == 3


def test_update_state_mid_execution():
    """Teste: Estado pode ser modificado durante execução"""
    # Arrange
    checkpointer = MemorySaver()
    graph = create_graph()
    compiled = graph.compile(checkpointer=checkpointer)

    # Act - Forçar estado como se fosse executado por node específico
    compiled.update_state(
        config={"configurable": {"thread_id": "1"}},
        values={"my_key": "injected_value"},
        as_node="node1"
    )

    # Continuar execução
    result = compiled.invoke(
        None,
        config={"configurable": {"thread_id": "1"}}
    )

    # Assert
    assert result["my_key"] == "injected_value"
```

**Aplicar quando**:
- Testar human-in-the-loop workflows
- Simular pausas/resumos
- Injetar estado para testar cenários específicos

---

### Pattern 4: Mocking LLM (GenericFakeChatModel)

**Quando usar**: Testar chains ou nodes que usam LLMs sem fazer API calls

```python
from unittest.mock import Mock
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolCall


def test_node_with_mocked_llm():
    """Teste: Node com LLM mockado retorna respostas esperadas"""
    # Arrange - Mock LLM com respostas predefinidas
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Primeira resposta"),
        AIMessage(content="Segunda resposta")
    ]))

    def node_with_llm(state):
        response = mock_llm.invoke(state["messages"])
        return {"response": response.content}

    # Act
    result = node_with_llm({"messages": [{"role": "user", "content": "test"}]})

    # Assert
    assert result["response"] == "Primeira resposta"

    # Act - Segunda chamada
    result2 = node_with_llm({"messages": [{"role": "user", "content": "test2"}]})

    # Assert
    assert result2["response"] == "Segunda resposta"


def test_node_with_tool_calls():
    """Teste: Node com LLM que invoca tools"""
    # Arrange - Mock LLM retornando tool call
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(
            content="",
            tool_calls=[
                ToolCall(
                    name="search_tool",
                    args={"query": "test query"},
                    id="call_123"
                )
            ]
        ),
        AIMessage(content="Final response based on tool")
    ]))

    def agent_node(state):
        response = mock_llm.invoke(state["messages"])
        return {"tool_calls": response.tool_calls, "response": response.content}

    # Act - Primeira chamada retorna tool call
    result = agent_node({"messages": []})

    # Assert
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0].name == "search_tool"
    assert result["tool_calls"][0].args == {"query": "test query"}

    # Act - Segunda chamada retorna resposta final
    result2 = agent_node({"messages": []})

    # Assert
    assert result2["response"] == "Final response based on tool"
```

**Aplicar quando**:
- Testar chains ou grafos com LLMs
- Evitar custos de API em testes
- Garantir respostas determinísticas
- Testar tool calling

---

### Pattern 5: Trajectory Match Evaluator (AgentEvals)

**Quando usar**: Validar sequência de ações/tools de um agent

```python
import pytest
from agentevals.trajectory.match import create_trajectory_match_evaluator
from langchain_core.messages import HumanMessage, AIMessage, ToolCall, ToolMessage


def test_trajectory_strict_match():
    """Teste: Trajectory corresponde exatamente à esperada (strict mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="strict"
    )

    # Trajectory esperada
    reference_trajectory = [
        HumanMessage(content="What's the weather?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="weather_tool", args={"location": "NYC"}, id="1")
        ]),
        ToolMessage(content="Sunny, 75F", tool_call_id="1"),
        AIMessage(content="It's sunny and 75F in NYC")
    ]

    # Trajectory real (idêntica)
    actual_trajectory = [
        HumanMessage(content="What's the weather?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="weather_tool", args={"location": "NYC"}, id="1")
        ]),
        ToolMessage(content="Sunny, 75F", tool_call_id="1"),
        AIMessage(content="It's sunny and 75F in NYC")
    ]

    # Act
    evaluation = evaluator(
        outputs=actual_trajectory,
        reference_outputs=reference_trajectory
    )

    # Assert
    assert evaluation["score"] is True


def test_trajectory_unordered_match():
    """Teste: Trajectory tem mesmas ações mas ordem diferente (unordered mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="unordered"
    )

    reference = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1"),
            ToolCall(name="tool_b", args={}, id="2")
        ])
    ]

    # Ordem diferente
    actual = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_b", args={}, id="2"),
            ToolCall(name="tool_a", args={}, id="1")
        ])
    ]

    # Act
    evaluation = evaluator(outputs=actual, reference_outputs=reference)

    # Assert
    assert evaluation["score"] is True


def test_trajectory_subset_match():
    """Teste: Trajectory contém pelo menos as ações esperadas (subset mode)"""
    # Arrange
    evaluator = create_trajectory_match_evaluator(
        trajectory_match_mode="subset"
    )

    # Esperado: pelo menos tool_a
    reference = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1")
        ])
    ]

    # Real: tool_a + tool_b (superset)
    actual = [
        AIMessage(content="", tool_calls=[
            ToolCall(name="tool_a", args={}, id="1"),
            ToolCall(name="tool_b", args={}, id="2")
        ])
    ]

    # Act
    evaluation = evaluator(outputs=actual, reference_outputs=reference)

    # Assert
    assert evaluation["score"] is True
```

**Aplicar quando**:
- Validar que agent executou ações corretas
- Testar sequência de tool calls
- Verificar comportamento de agents
- Validar multi-step reasoning

**Modos disponíveis**:
- `strict`: Ordem e conteúdo idênticos
- `unordered`: Mesmo conteúdo, ordem irrelevante
- `subset`: Trajectory real contém pelo menos as ações esperadas
- `superset`: Trajectory real é subconjunto das ações esperadas

---

### Pattern 6: LLM-as-Judge Evaluator

**Quando usar**: Usar LLM para avaliar qualidade de respostas do agent

```python
from agentevals.trajectory.llm import (
    create_trajectory_llm_as_judge,
    TRAJECTORY_ACCURACY_PROMPT
)


def test_trajectory_accuracy_with_llm_judge():
    """Teste: LLM avalia se trajectory atingiu objetivo corretamente"""
    # Arrange
    evaluator = create_trajectory_llm_as_judge(
        model="openai:gpt-4o-mini",  # ou "anthropic:claude-3-5-sonnet"
        prompt=TRAJECTORY_ACCURACY_PROMPT
    )

    # Trajectory de um agent que buscou informação corretamente
    trajectory = [
        HumanMessage(content="Who won the 2023 World Series?"),
        AIMessage(content="", tool_calls=[
            ToolCall(name="search", args={"query": "2023 World Series winner"}, id="1")
        ]),
        ToolMessage(content="Texas Rangers won 2023 World Series", tool_call_id="1"),
        AIMessage(content="The Texas Rangers won the 2023 World Series")
    ]

    # Act
    evaluation = evaluator(outputs=trajectory)

    # Assert - LLM julga se resposta foi precisa
    assert evaluation["score"] is True
    assert "reasoning" in evaluation  # LLM explica decisão


@pytest.mark.asyncio
async def test_async_llm_judge():
    """Teste: LLM judge com execução assíncrona"""
    # Arrange
    evaluator = create_trajectory_llm_as_judge(
        model="openai:gpt-4o-mini",
        prompt=TRAJECTORY_ACCURACY_PROMPT
    )

    trajectory = [
        HumanMessage(content="What's 2+2?"),
        AIMessage(content="2+2 equals 4")
    ]

    # Act
    evaluation = await evaluator.ainvoke(outputs=trajectory)

    # Assert
    assert evaluation["score"] is True
```

**Prompts disponíveis**:
- `TRAJECTORY_ACCURACY_PROMPT`: Avalia se agent respondeu corretamente
- Prompts customizados: Crie seus próprios critérios de avaliação

**Modelos suportados**:
- `openai:gpt-4o-mini`, `openai:o3-mini`
- `anthropic:claude-3-5-sonnet`, `anthropic:claude-3-5-haiku`

**Aplicar quando**:
- Avaliar qualidade de respostas do agent
- Validar que agent atingiu objetivo
- Testes onde match exato não é possível
- Avaliar conversational quality

---

### Pattern 7: VCR Recording (HTTP Replay)

**Quando usar**: Gravar HTTP calls reais de LLMs e replay em testes subsequentes

```python
import pytest


@pytest.mark.vcr()
def test_agent_with_real_llm_vcr():
    """Teste: Grava chamadas LLM reais na primeira execução, replay depois"""
    # PRIMEIRA EXECUÇÃO:
    # - Faz chamadas reais para LLM API
    # - Grava requests/responses em cassette YAML
    #
    # EXECUÇÕES POSTERIORES:
    # - Lê cassette gravado
    # - Replay respostas sem chamar API
    # - Testes 100% determinísticos e rápidos

    # Arrange
    from my_agent import create_agent
    agent = create_agent()

    # Act
    result = agent.invoke({"input": "What's the capital of France?"})

    # Assert
    assert "Paris" in result["output"]


@pytest.mark.vcr(record_mode="once")
def test_agent_record_once():
    """Teste: Grava cassette apenas uma vez, falha se não existir"""
    # record_mode="once": Grava na primeira vez, erro se cassette não existir depois
    # Útil para CI/CD - garante que cassettes foram commitados

    from my_agent import create_agent
    agent = create_agent()

    result = agent.invoke({"input": "Who wrote Hamlet?"})

    assert "Shakespeare" in result["output"]


@pytest.mark.vcr(record_mode="new_episodes")
def test_agent_record_new_episodes():
    """Teste: Adiciona novas interações ao cassette existente"""
    # record_mode="new_episodes":
    # - Usa cassette existente para interações conhecidas
    # - Grava novas interações que ainda não existem
    # Útil quando expandindo testes

    from my_agent import create_agent
    agent = create_agent()

    # Esta chamada pode já estar no cassette
    result1 = agent.invoke({"input": "What's 2+2?"})
    assert result1["output"] == "4"

    # Esta é nova, será gravada
    result2 = agent.invoke({"input": "What's 3+3?"})
    assert "6" in result2["output"]
```

**Configuração pytest-recording**:

```python
# conftest.py
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """Configuração padrão para VCR"""
    return {
        "filter_headers": ["authorization", "api-key"],  # Remove headers sensíveis
        "record_mode": "once",  # Padrão: gravar apenas uma vez
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "cassette_library_dir": "tests/cassettes",  # Onde salvar cassettes
    }
```

**Record modes**:
- `once`: Grava apenas uma vez, erro se cassette não existir
- `new_episodes`: Adiciona novas interações ao cassette existente
- `none`: Nunca grava, só replay (falha se cassette não existir)
- `all`: Sempre regrava cassette (útil para atualizar)

**Aplicar quando**:
- Testar integração real com LLMs sem custos em CI/CD
- Garantir determinismo em testes de agent
- Debugar issues com API calls específicos
- Testar diferentes modelos LLM sem API key em CI

**Gerenciando cassettes**:
```bash
# Regravar todos os cassettes
pytest --record-mode=all

# Regravar cassettes específicos
pytest tests/test_agent.py --record-mode=all

# Validar que cassettes existem (CI/CD)
pytest --record-mode=none
```

---

## Dependencies

Para usar estes padrões, certifique-se de que o projeto tem:

```toml
# pyproject.toml
[tool.poetry.dependencies]
langchain = "^0.3.0"
langchain-core = "^0.3.0"
langgraph = "^0.2.0"

[tool.poetry.group.test.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
agentevals = "^0.1.0"  # Trajectory validation
vcrpy = "^6.0.0"  # HTTP recording
pytest-recording = "^0.13.0"  # pytest-vcr integration
```

```bash
# pip/uv
pip install langchain langchain-core langgraph pytest pytest-asyncio agentevals vcrpy pytest-recording
```

---

## Examples

### Example 1: Complete LangGraph Test Suite

```python
import pytest
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage


class AgentState(TypedDict):
    messages: Annotated[list, "Messages in conversation"]
    next_action: str


def create_agent_graph():
    """Factory: Cria grafo de agent"""
    graph = StateGraph(AgentState)

    def router(state):
        if len(state["messages"]) > 3:
            return {"next_action": "end"}
        return {"next_action": "continue"}

    def responder(state):
        return {
            "messages": state["messages"] + [
                AIMessage(content="Response")
            ]
        }

    graph.add_node("router", router)
    graph.add_node("responder", responder)
    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", lambda s: s["next_action"])
    graph.add_edge("responder", END)

    return graph


class TestAgentGraph:
    """Test suite para agent graph"""

    def test_graph_basic_execution(self):
        """Teste: Grafo executa fluxo básico"""
        # Arrange
        checkpointer = MemorySaver()
        graph = create_agent_graph()
        compiled = graph.compile(checkpointer=checkpointer)

        # Act
        result = compiled.invoke(
            {"messages": [HumanMessage(content="Hi")], "next_action": ""},
            config={"configurable": {"thread_id": "1"}}
        )

        # Assert
        assert result["next_action"] == "continue"

    def test_router_node_individually(self):
        """Teste: Node router decide corretamente"""
        # Arrange
        graph = create_agent_graph()
        compiled = graph.compile()

        # Act - Poucas mensagens
        result1 = compiled.nodes["router"].invoke({
            "messages": [HumanMessage(content="Test")],
            "next_action": ""
        })

        # Assert
        assert result1["next_action"] == "continue"

        # Act - Muitas mensagens
        result2 = compiled.nodes["router"].invoke({
            "messages": [HumanMessage(content=f"Msg {i}") for i in range(5)],
            "next_action": ""
        })

        # Assert
        assert result2["next_action"] == "end"

    def test_partial_execution_with_interrupt(self):
        """Teste: Execução parcial até router"""
        # Arrange
        checkpointer = MemorySaver()
        graph = create_agent_graph()
        compiled = graph.compile(checkpointer=checkpointer)

        # Act
        result = compiled.invoke(
            {"messages": [HumanMessage(content="Test")], "next_action": ""},
            config={"configurable": {"thread_id": "1"}},
            interrupt_after=["router"]
        )

        # Assert - Parou no router
        assert result["next_action"] == "continue"
```

### Example 2: LangChain Chain with Mocked LLM

```python
from unittest.mock import Mock, patch
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate


def test_chain_with_pipe_operator_mocked():
    """Teste: Chain LCEL com pipe operator e LLM mockado"""
    # Arrange
    mock_llm = GenericFakeChatModel(messages=iter([
        AIMessage(content="Mocked response")
    ]))

    prompt = ChatPromptTemplate.from_template("Answer: {question}")
    chain = prompt | mock_llm

    # Act
    result = chain.invoke({"question": "What's 2+2?"})

    # Assert
    assert result.content == "Mocked response"


@patch("my_module.ChatOpenAI")
@patch("my_module.ChatPromptTemplate.from_template")
def test_chain_with_patch_mocking(mock_prompt, mock_chat):
    """Teste: Chain com mocking via @patch"""
    # Arrange - Mock chain com pipe operator
    mock_llm = Mock()
    mock_chain = Mock()
    mock_chain.invoke.return_value = AIMessage(content="Patched response")

    # Mock do pipe operator (|)
    mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)
    mock_chat.return_value = mock_llm

    # Importar DEPOIS do patch
    from my_module import process_question

    # Act
    result = process_question("What's the weather?")

    # Assert
    assert "Patched response" in result
    mock_chain.invoke.assert_called_once()
```

---

## Best Practices

### 1. Sempre Use Factories para Grafos

```python
# ✅ BOM - Factory reutilizável
def create_graph() -> StateGraph:
    graph = StateGraph(MyState)
    # ... configuração
    return graph

def test_feature():
    graph = create_graph()
    compiled = graph.compile()
```

```python
# ❌ RUIM - Grafo global
GRAPH = StateGraph(MyState)
# ... pode causar state compartilhado entre testes
```

### 2. Use MemorySaver para Testes com Checkpointer

```python
# ✅ BOM - Checkpointer em memória
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
compiled = graph.compile(checkpointer=checkpointer)
```

```python
# ❌ RUIM - Checkpointer persistente em testes
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver("test.db")  # Cria arquivo, slow
```

### 3. Mock LLMs para Testes Unitários

```python
# ✅ BOM - Mock determinístico
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

mock_llm = GenericFakeChatModel(messages=iter([
    AIMessage(content="Expected response")
]))
```

```python
# ❌ RUIM - LLM real em unit test
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()  # Custa $$$, não determinístico
```

### 4. Use VCR para Integration Tests

```python
# ✅ BOM - Integration test com VCR
@pytest.mark.vcr()
def test_integration_with_real_api():
    # Grava na primeira vez, replay depois
    agent = create_agent()
    result = agent.invoke(...)
```

### 5. Valide Trajectories com AgentEvals

```python
# ✅ BOM - Validação estruturada
from agentevals.trajectory.match import create_trajectory_match_evaluator

evaluator = create_trajectory_match_evaluator(trajectory_match_mode="subset")
evaluation = evaluator(outputs=result, reference_outputs=expected)
assert evaluation["score"] is True
```

```python
# ❌ RUIM - Validação manual frágil
assert len(result["messages"]) == 4
assert result["messages"][1].tool_calls[0].name == "search"
# Frágil, quebra com mudanças pequenas
```

### 6. Teste Nodes Individuais Primeiro

```python
# ✅ BOM - Testar nodes isoladamente primeiro
def test_individual_node():
    graph = create_graph()
    compiled = graph.compile()
    result = compiled.nodes["my_node"].invoke(state)
    assert result["key"] == "expected"

def test_full_graph():
    # Depois testar grafo completo
    ...
```

---

## Common Pitfalls

### ❌ Não usar thread_id em checkpointer

```python
# ERRO - Falta thread_id
result = compiled.invoke({"key": "value"})

# CORRETO
result = compiled.invoke(
    {"key": "value"},
    config={"configurable": {"thread_id": "1"}}
)
```

### ❌ Esquecer de compilar grafo

```python
# ERRO
graph = StateGraph(MyState)
result = graph.invoke(...)  # StateGraph não é invocável

# CORRETO
compiled = graph.compile()
result = compiled.invoke(...)
```

### ❌ Mock de pipe operator incorreto

```python
# ERRO - Mock de pipe incompleto
mock_prompt.return_value | mock_llm  # Não funciona

# CORRETO
mock_prompt.return_value.__or__ = Mock(return_value=mock_chain)
```

### ❌ Não instalar dependencies de teste

```bash
# ERRO - Falha ao importar agentevals
pytest test_agent.py
# ModuleNotFoundError: No module named 'agentevals'

# CORRETO
pip install agentevals pytest-recording
pytest test_agent.py
```

---

## Summary

Esta skill fornece **7 padrões de teste** completos para LangChain/LangGraph:

1. **Basic LangGraph Test**: Testes state-based com checkpointer
2. **Individual Node Testing**: Testar nodes isoladamente
3. **Partial Execution**: Interrupts e state injection
4. **Mocking LLM**: GenericFakeChatModel para unit tests
5. **Trajectory Match**: Validação de sequência de ações (agentevals)
6. **LLM-as-Judge**: Avaliação de qualidade com LLM
7. **VCR Recording**: Gravar/replay HTTP calls

**Use quando**: Detectar LangChain, LangGraph, chains LCEL, grafos, agents, ou pedidos para testar LLMs.