---
description: Assistente interativo para construir chains LCEL corretas com pipe operators, parallel execution e composições avançadas
---

# LCEL Builder - Construtor de Chains LCEL

Sou um assistente interativo para construir chains usando LangChain Expression Language (LCEL) v1. Ajudo a criar composições corretas com pipe operators, parallel execution e padrões avançados.

## Como usar:

```bash
/lcel-builder [descrição da chain]
```

**Exemplos**:
- `/lcel-builder criar uma chain que gera piada e traduz para português`
- `/lcel-builder chain com execução paralela de análise de sentimento e resumo`
- `/lcel-builder chain com router condicional baseado em input`

## O que faço:

### 1. Análise de Requisitos
Entendo o que você quer construir:
- Passos sequenciais vs paralelos
- Componentes necessários (LLM, prompts, parsers, retrievers)
- Estrutura de input/output
- Conditional routing se necessário

### 2. Geração de Chain LCEL
Gero código completo e funcional:
- Imports corretos dos componentes v1
- Composição usando pipe operator (`|`)
- RunnableParallel para execução paralela
- Type coercion apropriado
- Error handling quando relevante

### 3. Explicação e Otimizações
Explico:
- Como a chain funciona passo a passo
- Por que escolhi cada padrão
- Possíveis otimizações
- Trade-offs de design

## Padrões que Domino:

### 1. Sequential Chain (Pipe Operator)
```python
chain = component1 | component2 | component3
```

### 2. Parallel Execution
```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    branch1=chain1,
    branch2=chain2
)
```

### 3. Conditional Routing
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["type"] == "A", chain_a),
    (lambda x: x["type"] == "B", chain_b),
    default_chain
)
```

### 4. Custom Functions (RunnableLambda)
```python
from langchain_core.runnables import RunnableLambda

def custom_logic(input_data):
    # Processamento customizado
    return processed_data

chain = llm | RunnableLambda(custom_logic) | parser
```

### 5. Fallback Pattern
```python
chain_with_fallback = primary_chain.with_fallbacks(
    [fallback_chain1, fallback_chain2]
)
```

## Exemplos Completos:

### Exemplo 1: Simple Sequential Chain
**Requisito**: "Chain que gera uma piada e formata como JSON"

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Componentes
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template(
    "Generate a joke about {topic} and format as JSON with 'setup' and 'punchline' keys."
)
parser = JsonOutputParser()

# Chain usando pipe operator
joke_chain = prompt | llm | parser

# Uso
result = joke_chain.invoke({"topic": "python"})
print(result)  # {"setup": "...", "punchline": "..."}
```

### Exemplo 2: Parallel Execution
**Requisito**: "Analisar texto gerando resumo e sentimento em paralelo"

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

# Chains individuais
summary_chain = (
    ChatPromptTemplate.from_template("Summarize this text: {text}")
    | llm
    | parser
)

sentiment_chain = (
    ChatPromptTemplate.from_template("Analyze sentiment of: {text}")
    | llm
    | parser
)

# Execução paralela
analysis_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)

# Uso
result = analysis_chain.invoke({"text": "Long text here..."})
print(result)  # {"summary": "...", "sentiment": "..."}
```

### Exemplo 3: Conditional Router
**Requisito**: "Chain que roteia input para chain especializada baseado em categoria"

```python
from langchain_core.runnables import RunnableBranch

# Chains especializadas
tech_chain = ChatPromptTemplate.from_template("Technical answer: {question}") | llm
casual_chain = ChatPromptTemplate.from_template("Casual answer: {question}") | llm

# Router condicional
def categorize(input_data):
    return input_data.get("category", "casual")

router = RunnableBranch(
    (lambda x: categorize(x) == "tech", tech_chain),
    (lambda x: categorize(x) == "casual", casual_chain),
    casual_chain  # default
)

# Uso
result1 = router.invoke({"category": "tech", "question": "What is Docker?"})
result2 = router.invoke({"category": "casual", "question": "How are you?"})
```

### Exemplo 4: RAG Chain
**Requisito**: "Chain RAG completa com retrieval e generation"

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Setup
vectorstore = FAISS.from_texts(
    ["doc1", "doc2", "doc3"],
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Template com contexto
template = """Answer based on context:
Context: {context}
Question: {question}
Answer:"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4")

# RAG Chain
rag_chain = (
    {
        "context": retriever,  # Auto-retrieval do input
        "question": RunnablePassthrough()  # Passa question diretamente
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Uso
answer = rag_chain.invoke("What is the main topic?")
```

## Quando me usar:

- ✅ Construir chains LCEL do zero
- ✅ Compor múltiplos componentes LangChain
- ✅ Implementar parallel execution
- ✅ Adicionar conditional routing
- ✅ Verificar sintaxe correta de LCEL v1
- ✅ Otimizar chains existentes

## Checklist de Quality:

Ao construir chains, verifico:
- ✅ Imports corretos (v1 packages)
- ✅ Pipe operator usado corretamente
- ✅ Type compatibility entre componentes
- ✅ Error handling quando necessário
- ✅ Streaming support se aplicável
- ✅ Async support se requerido
- ✅ Proper input/output schemas

## Limitações do LCEL:

**Quando NÃO usar LCEL** (use LangGraph):
- ❌ State management complexo necessário
- ❌ Loops ou cycles na lógica
- ❌ Multi-agent orchestration avançada
- ❌ Branching muito complexo (> 5 branches)
- ❌ Necessidade de persistência de estado

**Limites recomendados**:
- Chains com < 100 steps
- Branching simples (< 5 condições)
- State simples (não precisa de reducers)