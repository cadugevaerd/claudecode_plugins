---
description: Ajuda rápida e referência sobre LangChain v1 - LCEL, chains, componentes e migrações
---

# LangChain Help - Assistência Rápida LangChain v1

Forneço ajuda rápida e referência sobre LangChain v1, incluindo LCEL (LangChain Expression Language), chains, componentes e guias de migração.

## Como usar:

```bash
/langchain-help [tópico opcional]
```

**Tópicos disponíveis**:
- `lcel` - LangChain Expression Language (composição de chains)
- `migration` - Guia de migração de v0 para v1
- `components` - Componentes principais (LLMs, prompts, retrievers)
- `chains` - Padrões de chains e composição
- `messages` - API de mensagens e content blocks

## O que faço:

### 1. Referência Rápida de LCEL
Explico os principais padrões de composição:
- Pipe operator (`|`) para sequências
- RunnableParallel para execução paralela
- RunnableSequence para composições complexas
- Type coercion automático

### 2. Guia de Migração v0 → v1
Ajudo com mudanças importantes:
- **Python 3.10+** obrigatório (3.9 deprecated)
- Namespace `langchain` reduzido - use `langchain-classic` para legado
- AgentExecutor deprecated → migrar para LangGraph
- Message API: `.text()` → `.text` (property)
- Content blocks provider-agnostic

### 3. Melhores Práticas v1
- LCEL para orquestrações simples
- LangGraph para state management complexo, branching, cycles
- Chains com múltiplos passos (< 100 steps recomendado)
- Uso correto de Runnables

## Exemplos:

### LCEL Basic Chain
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Composição usando pipe operator
chain = (
    ChatPromptTemplate.from_template("Tell me a joke about {topic}")
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

result = chain.invoke({"topic": "python"})
```

### Parallel Execution
```python
from langchain_core.runnables import RunnableParallel

# Execução paralela de múltiplas chains
parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain,
    story=story_chain
)

results = parallel_chain.invoke({"topic": "AI"})
```

### Message API v1
```python
from langchain_core.messages import AIMessage

response = llm.invoke("Hello")
# v1: use .text como property (não .text())
text_content = response.text

# Content blocks (provider-agnostic)
content_blocks = response.content_blocks
```

## Quando me usar:

- ✅ Precisa de referência rápida sobre LCEL
- ✅ Dúvidas sobre migração v0 → v1
- ✅ Verificar sintaxe correta de chains
- ✅ Escolher entre LCEL e LangGraph
- ✅ Entender mudanças na Message API

## Notas Importantes:

**Requisitos v1**:
- Python 3.10+ (3.9 EOL em outubro 2025)
- Instalação: `pip install --upgrade langchain`
- Legado: `pip install langchain-classic` (se necessário)

**Quando usar LangGraph em vez de LCEL**:
- State management complexo
- Branching condicional
- Cycles (loops)
- Multi-agent orchestration
- Persistência de estado

**Recursos Oficiais**:
- Docs: https://python.langchain.com/docs/
- Migration Guide: https://docs.langchain.com/oss/python/migrate/langchain-v1
- Blog Post v1: https://blog.langchain.com/langchain-langgraph-1dot0/