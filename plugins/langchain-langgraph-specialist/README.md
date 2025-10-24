# LangChain & LangGraph Specialist

Plugin especialista completo em **LangChain v1** e **LangGraph v1**, as versões mais recentes dos frameworks para desenvolvimento de aplicações com LLMs e agentes.

## Descrição

Este plugin fornece assistência abrangente para desenvolvimento com LangChain e LangGraph, incluindo:

- ✅ **LangChain v1**: LCEL (Expression Language), chains, componentes, integrations
- ✅ **LangGraph v1**: Grafos, state management, multi-agent systems
- ✅ **Debugging**: Identificação e resolução de erros comuns
- ✅ **Migração**: Guias de atualização v0 → v1
- ✅ **Melhores Práticas**: Padrões recomendados para produção
- ✅ **Skills Auto-invocadas**: Claude detecta automaticamente quando aplicar expertise

## Instalação

### 1. Instalar Plugin

```bash
/plugin marketplace add cadugevaerd/claudecode_plugins
/plugin install langchain-langgraph-specialist
```

### 2. Instalar MCP Server (Recomendado)

Para acesso à documentação oficial em tempo real:

```bash
claude mcp add --transport http docs-langchain https://docs.langchain.com/mcp
```

O MCP Server permite que Claude acesse a documentação mais atualizada do LangChain/LangGraph automaticamente. **Altamente recomendado** para garantir informações precisas.

📖 **Mais detalhes**: Veja `mcp/README.md` no plugin para troubleshooting e configuração avançada.

## Funcionalidades

### 🎯 Comandos Disponíveis

#### `/langchain-help` - Ajuda Rápida LangChain v1
Referência rápida sobre LangChain v1:
- LCEL (LangChain Expression Language)
- Guia de migração v0 → v1
- Componentes principais (LLMs, prompts, retrievers)
- Message API e content blocks
- Melhores práticas

**Uso**:
```bash
/langchain-help
/langchain-help lcel
/langchain-help migration
```

#### `/langgraph-help` - Ajuda Rápida LangGraph v1
Referência rápida sobre LangGraph v1:
- Construção de grafos (nodes, edges, state)
- State management com reducers
- Padrões de agentes (ReAct, multi-agent)
- Control flow avançado (branching, loops)
- Checkpointing e persistência

**Uso**:
```bash
/langgraph-help
/langgraph-help graphs
/langgraph-help state
/langgraph-help agents
```

#### `/lcel-builder` - Construtor de Chains LCEL
Assistente interativo para construir chains LCEL:
- Composição com pipe operators
- Parallel execution (RunnableParallel)
- Conditional routing (RunnableBranch)
- RAG pipelines completas
- Código gerado pronto para uso

**Uso**:
```bash
/lcel-builder criar uma chain que gera piada e traduz para português
/lcel-builder chain RAG com retrieval de documentos técnicos
/lcel-builder parallel execution de análise de sentimento e resumo
```

### 🤖 Agente Especializado

#### `langchain-langgraph-expert`
Especialista completo para consultas complexas:
- Desenvolvimento de chains e grafos avançados
- Code review e otimizações
- Debugging profundo
- Consultoria arquitetural
- Migração v0 → v1

**Uso via Task**:
```python
# Delegar tarefa complexa ao especialista
Task(
    agent="langchain-langgraph-expert",
    description="Criar sistema RAG completo com LangChain v1"
)
```

### ⚡ Skills Auto-invocadas (Capacidades Automáticas)

Claude invoca estas skills automaticamente baseado no contexto:

#### `lcel-chain-builder` ⚡
- **O que faz**: Constrói chains LCEL com padrões corretos
- **Quando ativa**: Ao criar chains, compor runnables, implementar RAG
- **Padrões**: Sequential, parallel, conditional, RAG

#### `langgraph-state-manager` ⚡
- **O que faz**: Gerencia estado em grafos com TypedDict e reducers
- **Quando ativa**: Ao criar grafos, definir state schema, multi-agent state
- **Padrões**: Override, additive, custom reducers

#### `langchain-debugger` ⚡
- **O que faz**: Debug de chains e grafos identificando erros comuns
- **Quando ativa**: Ao encontrar erros em chains LCEL ou grafos LangGraph
- **Resolve**: Type mismatch, state corruption, integration errors

## Exemplos de Uso

### Exemplo 1: Criar Chain LCEL Simples

```bash
/lcel-builder criar chain que responde perguntas sobre Python
```

**Resultado**:
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (
    ChatPromptTemplate.from_template("Answer this question about Python: {question}")
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

answer = chain.invoke({"question": "What are decorators?"})
```

### Exemplo 2: RAG Pipeline Completa

```bash
/lcel-builder chain RAG com retrieval de documentos e citações
```

**Resultado**:
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Setup vectorstore
vectorstore = FAISS.from_texts(
    ["doc1", "doc2", "doc3"],
    embedding=OpenAIEmbeddings()
)

# RAG Chain
rag_chain = (
    {
        "context": vectorstore.as_retriever(),
        "question": RunnablePassthrough()
    }
    | ChatPromptTemplate.from_template(
        "Answer based on context:\nContext: {context}\nQuestion: {question}\nAnswer:"
    )
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the main topic?")
```

### Exemplo 3: LangGraph Multi-Agent System

```bash
/langgraph-help agents
```

Depois de consultar a ajuda, use a skill automaticamente:

```python
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
from operator import add

class MultiAgentState(TypedDict):
    messages: Annotated[list[dict], add]
    current_agent: str
    final_answer: str

def research_agent(state):
    # Pesquisa e adiciona ao scratchpad compartilhado
    state["messages"].append({
        "agent": "research",
        "content": "Research findings..."
    })
    state["current_agent"] = "writer"
    return state

def writer_agent(state):
    # Lê pesquisa e gera resposta final
    research = [m for m in state["messages"] if m["agent"] == "research"]
    state["final_answer"] = f"Based on {research}, here's the answer..."
    return state

# Criar grafo
graph = StateGraph(MultiAgentState)
graph.add_node("research", research_agent)
graph.add_node("writer", writer_agent)
graph.add_edge("research", "writer")
graph.set_entry_point("research")
graph.set_finish_point("writer")

app = graph.compile()
```

### Exemplo 4: Debug de Erro LCEL

Claude detecta automaticamente o erro e usa `langchain-debugger` skill:

```python
# ❌ Código com erro
chain = {"input": "value"} | prompt | llm
# TypeError: unsupported operand type(s) for |: 'dict' and 'ChatPromptTemplate'

# ✅ Claude identifica e corrige automaticamente
from langchain_core.runnables import RunnableParallel

chain = (
    RunnableParallel({"input": lambda x: x})
    | prompt
    | llm
)
```

### Exemplo 5: Migração v0 → v1

```bash
/langchain-help migration
```

Claude fornece guia detalhado:
- ✅ Atualizar Python para 3.10+
- ✅ Instalar `langchain-classic` para código legado
- ✅ Migrar `AgentExecutor` → `LangGraph`
- ✅ Atualizar `.text()` → `.text`
- ✅ Atualizar imports para pacotes v1

## Quando Usar Este Plugin

### ✅ Use para:
- Desenvolver aplicações com LangChain v1 ou LangGraph v1
- Criar chains LCEL com composições complexas
- Implementar RAG pipelines
- Construir sistemas multi-agent
- Debugar erros em chains ou grafos
- Migrar código de v0 para v1
- Aprender melhores práticas dos frameworks
- Otimizar chains/grafos existentes

### ❌ Não use para:
- Perguntas genéricas sobre IA/ML (não específicas dos frameworks)
- Implementação de modelos de ML customizados
- Fine-tuning de LLMs
- Infraestrutura/DevOps não relacionado

## Melhores Práticas

### LangChain LCEL
1. ✅ Use type hints para input/output schemas
2. ✅ Implemente error handling com `.with_fallbacks()`
3. ✅ Prefira async (`.ainvoke()`) quando possível
4. ✅ Limite chains a ~100 steps
5. ✅ Use `RunnableParallel` para IO-bound operations
6. ✅ Para state complexo/loops, use LangGraph

### LangGraph
1. ✅ Design estado enxuto (evite crescimento descontrolado)
2. ✅ Use reducers apropriados para concurrent execution
3. ✅ Implemente error handling em nodes críticos
4. ✅ Use checkpointing para conversações longas
5. ✅ Considere memory management em multi-agent systems
6. ✅ Teste conditional edges extensivamente

## Decision Matrix: LCEL vs LangGraph

| Característica | Use LCEL | Use LangGraph |
|----------------|----------|---------------|
| Composição simples | ✅ | ❌ |
| < 100 steps | ✅ | ⚠️ |
| State management complexo | ❌ | ✅ |
| Loops/Cycles | ❌ | ✅ |
| Branching condicional | ⚠️ Simples | ✅ Complexo |
| Multi-agent | ❌ | ✅ |
| Persistência estado | ❌ | ✅ |
| Human-in-the-loop | ❌ | ✅ |
| Parallel execution | ✅ | ✅ |

## Requisitos

- **Python**: 3.10+ (obrigatório para v1)
- **LangChain**: v1.0+
- **LangGraph**: v1.0+ (se usar grafos)

**Instalação dos frameworks**:
```bash
# LangChain v1
pip install --upgrade langchain langchain-core

# Providers
pip install langchain-openai langchain-anthropic

# LangGraph v1
pip install langgraph

# Legado (se necessário)
pip install langchain-classic
```

## Recursos Adicionais

### Documentação Oficial
- **LangChain**: https://python.langchain.com/docs/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Migration Guide**: https://docs.langchain.com/oss/python/migrate/langchain-v1
- **Blog Post v1**: https://blog.langchain.com/langchain-langgraph-1dot0/

### Tutoriais
- LangChain Academy (curso gratuito)
- LangGraph Tutorials: https://langchain-ai.github.io/langgraph/tutorials/
- Real Python LangGraph Tutorial

### Comunidade
- GitHub LangChain: https://github.com/langchain-ai/langchain
- GitHub LangGraph: https://github.com/langchain-ai/langgraph
- Discord LangChain Community

## Troubleshooting

### Erro: "Python 3.9 not supported"
LangChain v1 requer Python 3.10+. Atualize:
```bash
pyenv install 3.10
pyenv global 3.10
```

### Erro: "cannot import AgentExecutor"
`AgentExecutor` foi deprecated. Migre para LangGraph:
```bash
/langchain-help migration
```

### Erro: "TypeError with pipe operator"
Verifique type compatibility. Use:
```bash
/lcel-builder [descrever sua chain]
```

### Performance Issues
Para chains lentas, considere:
- Async execution com `.ainvoke()`
- Parallel execution com `RunnableParallel`
- Migrar para LangGraph se > 100 steps

## Autor

**Carlos Araujo**
- Email: cadu.gevaerd@gmail.com
- GitHub: https://github.com/cadugevaerd/claudecode_plugins

## Licença

MIT License

---

**Desenvolvido para Claude Code Marketplace** 🚀

*Versão 1.1.0 - Outubro 2025*