---
name: lcel-chain-builder
description: Constrói chains LCEL (LangChain Expression Language) com composição correta usando pipe operators, parallel execution e padrões v1. Use quando criar chains LangChain, compor runnables, implementar RAG, ou precisar de sequential/parallel execution.
allowed-tools: Read, Write, Edit, Grep, Glob
---

name: lcel-chain-builder
description: Constrói chains LCEL (LangChain Expression Language) com composição correta usando pipe operators, parallel execution e padrões v1. Use quando criar chains LangChain, compor runnables, implementar RAG, ou precisar de sequential/parallel execution.
allowed-tools: Read, Write, Edit, Grep, Glob

# LCEL Chain Builder

Skill para construir chains usando LangChain Expression Language (LCEL) v1 com padrões corretos de composição.

## Instructions

### STEP 0: Consultar Documentação via MCP (OBRIGATÓRIO)

**SEMPRE comece usando ferramentas MCP para validar abordagem**:

- Use `fetch_docs` para buscar exemplos similares de LCEL chains
- Busque por padrões relacionados (ex: "RAG chain", "parallel execution", "conditional routing")
- Valide sintaxe de componentes que você planeja usar
- Verifique se há exemplos oficiais de padrões similares

**Exemplo**:

````text

User: "Criar chain RAG com retrieval"
→ ANTES de gerar: Use fetch_docs para buscar "RAG tutorial" ou "retrieval chain"
→ Analise exemplos oficiais retornados
→ ENTÃO gere chain baseada em padrões oficiais

```text

### STEP 1: Analisar requisitos da chain solicitada

- Identificar passos sequenciais vs paralelos
- Determinar componentes necessários (LLM, prompts, parsers, retrievers)
- Verificar se LCEL é apropriado (se precisa state complexo/loops, sugerir LangGraph)

### STEP 2: Escolher padrão de composição
   - Sequential: Use pipe operator (`|`)
   - Parallel: Use `RunnableParallel`
   - Conditional: Use `RunnableBranch`
   - Custom logic: Use `RunnableLambda`

3. **Gerar código LCEL v1**:
   - Imports corretos dos pacotes v1
   - Type hints quando aplicável
   - Composição usando operators apropriados
   - Error handling se relevante

4. **Validar**:
   - Type compatibility entre componentes
   - Input/output schemas compatíveis
   - Sintaxe correta do pipe operator

## When to Use

Use esta skill quando:
- Criar chains LangChain do zero
- Compor múltiplos runnables (prompts, LLMs, parsers)
- Implementar RAG pipelines
- Adicionar parallel execution a chains
- Converter chains legadas para LCEL v1
- Otimizar chains existentes
- Usuário menciona: "criar chain", "LCEL", "pipe operator", "LangChain composição", "RAG pipeline"

## LCEL Patterns

### Pattern 1: Sequential Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = (
    ChatPromptTemplate.from_template("{input}")
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

```text

### Pattern 2: Parallel Execution

```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    branch1=chain1,
    branch2=chain2,
    branch3=chain3
)

```text

### Pattern 3: Conditional Router

```python
from langchain_core.runnables import RunnableBranch

router = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default_chain
)

```text

### Pattern 4: RAG Chain

```python
from langchain_core.runnables import RunnablePassthrough

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | parser
)

```text

## Key Validations

- ✅ Python 3.10+ imports (v1 requirement)
- ✅ Correct package names (`langchain-openai`, `langchain-core`)
- ✅ Type compatibility between chained components
- ✅ Proper use of pipe operator (not dict | runnable directly)
- ✅ RunnablePassthrough when input needs to be preserved
- ✅ Error handling with `.with_fallbacks()` if needed

## Don't Use This Skill When

- ❌ Complex state management needed → Use LangGraph
- ❌ Loops or cycles required → Use LangGraph
- ❌ Multi-agent orchestration → Use LangGraph
- ❌ More than ~100 sequential steps → Consider LangGraph
- ❌ Non-LangChain code (general Python, other frameworks)

## Examples

**Example 1 - Simple Chain**:

```python

# User: "Create a chain that answers questions"
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

qa_chain = (
    ChatPromptTemplate.from_template("Answer: {question}")
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

answer = qa_chain.invoke({"question": "What is Python?"})

```text

**Example 2 - Parallel Analysis**:

```python

# User: "Analyze text for summary and sentiment in parallel"
from langchain_core.runnables import RunnableParallel

analysis = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)

result = analysis.invoke({"text": "Input text here"})

# Returns: {"summary": "...", "sentiment": "..."}

```text

**Example 3 - RAG Pipeline**:

```python

# User: "Create RAG chain with retrieval"
from langchain_core.runnables import RunnablePassthrough

rag = (
    {
        "context": vectorstore.as_retriever(),
        "question": RunnablePassthrough()
    }
    | ChatPromptTemplate.from_template(
        "Context: {context}\nQuestion: {question}\nAnswer:"
    )
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

answer = rag.invoke("What is the main topic?")

```text
````
