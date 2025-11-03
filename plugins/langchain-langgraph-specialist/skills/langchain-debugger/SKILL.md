---
name: langchain-debugger
description: Debug de chains LangChain e grafos LangGraph identificando erros de composição, type mismatch, state corruption e problemas de integração. Use quando encontrar erros em chains LCEL, grafos LangGraph, ou problemas com LLM integrations.
allowed-tools: Read, Grep, Glob
---

name: langchain-debugger
description: Debug de chains LangChain e grafos LangGraph identificando erros de composição, type mismatch, state corruption e problemas de integração. Use quando encontrar erros em chains LCEL, grafos LangGraph, ou problemas com LLM integrations.
allowed-tools: Read, Grep, Glob

# LangChain Debugger

Skill para debugar chains LangChain e grafos LangGraph identificando e resolvendo erros comuns.

## Instructions

### STEP 0: Consultar Documentação via MCP (PRIORITÁRIO)

**SEMPRE use MCP para verificar se erro já foi resolvido em docs oficiais**:

- Use `fetch_docs` para buscar sobre o tipo de erro específico
- Busque por troubleshooting guides relacionados
- Verifique se há breaking changes ou deprecations relacionadas
- Consulte migration guides se erro envolve versões diferentes

**Exemplo**:

````text

User: "Erro: TypeError with pipe operator"
→ PRIMEIRO: Use fetch_docs para buscar "pipe operator errors" ou "TypeError LCEL"
→ Verifique se há solução oficial documentada
→ ENTÃO: diagnostique baseado em docs + conhecimento base

```text

**Prioridade MCP para**:
- ✅ Migration errors (v0 → v1) - busque "migration guide"
- ✅ API deprecations - busque nome da API/método deprecated
- ✅ Erros de sintaxe específicos - busque mensagem de erro
- ✅ Integration issues - busque nome do provider + "integration"

### STEP 1: Identificar tipo de erro

- LCEL composition errors (pipe operator, type mismatch)
- LangGraph state errors (corruption, reducer issues)
- Integration errors (LLM providers, API keys)
- Runtime errors (timeouts, rate limits)

### STEP 2: Analisar contexto
   - Ler código relevante
   - Identificar componentes envolvidos
   - Verificar versões (v0 vs v1)
   - Checar imports

3. **Diagnosticar causa raiz**:
   - Type incompatibility
   - Incorrect composition
   - Missing configuration
   - Version mismatch
   - API issues

4. **Fornecer solução**:
   - Explicar o problema
   - Mostrar código correto
   - Sugerir prevenção futura

## When to Use

Use esta skill quando:
- Erro em chain LCEL (TypeError, AttributeError)
- Erro em grafo LangGraph (state corruption, node failure)
- Integration error (OpenAI, Anthropic, etc.)
- Performance issue (lentidão, timeouts)
- Migration error (v0 → v1)
- Usuário menciona: "erro chain", "debug LangChain", "não funciona", "TypeError", "bug no grafo"

## Common Errors & Solutions

### Error 1: Pipe Operator Type Mismatch
**Error**:

```text

TypeError: unsupported operand type(s) for |: 'dict' and 'ChatPromptTemplate'

```text

**Cause**: Dict não pode ser piped diretamente para runnable

**Solution**:

```python

# ❌ Errado
chain = {"input": "value"} | prompt | llm

# ✅ Correto - Use RunnableParallel
from langchain_core.runnables import RunnableParallel

chain = (
    RunnableParallel({"input": lambda x: x["value"]})
    | prompt
    | llm
)

```text

### Error 2: Message API v0 vs v1
**Error**:

```text

AttributeError: 'AIMessage' object has no attribute 'text'

```text

**Cause**: Usando v0 syntax em v1 (ou vice-versa)

**Solution**:

```python

# v0: método .text()
text = response.text()

# v1: property .text (sem parênteses)
text = response.text  # ✅ Correto em v1

```text

### Error 3: State Reducer Not Defined
**Error**:

```text

TypeError: Cannot concatenate lists without reducer

```text

**Cause**: Tentando adicionar a lista sem reducer Annotated

**Solution**:

```python
from typing import Annotated
from operator import add

# ❌ Errado
class State(TypedDict):
    messages: list[str]

# ✅ Correto - Com reducer
class State(TypedDict):
    messages: Annotated[list[str], add]

```text

### Error 4: Import Error v1
**Error**:

```text

ImportError: cannot import name 'AgentExecutor' from 'langchain'

```text

**Cause**: AgentExecutor removido em v1

**Solution**:

```python

# ❌ v0 (deprecated)
from langchain.agents import AgentExecutor

# ✅ v1 - Use LangGraph
from langgraph.graph import StateGraph

# Migre para grafo LangGraph

```text

### Error 5: OpenAI API Key Missing
**Error**:

```text

openai.error.AuthenticationError: No API key provided

```text

**Cause**: API key não configurada

**Solution**:

```python
import os

# Opção 1: Environment variable
os.environ["OPENAI_API_KEY"] = "sk-..."

# Opção 2: Passar diretamente
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key="sk-...", model="gpt-4")

```text

### Error 6: State Corruption in LangGraph
**Error**:

```text

KeyError: 'messages' or State has incorrect structure

```text

**Cause**: Node retornando state com estrutura incompatível

**Solution**:

```python

# ✅ Sempre retorne state completo ou partial válido
def node_function(state: State):
    # Opção 1: Modifica e retorna completo
    state["messages"].append("new")
    return state

    # Opção 2: Retorna partial (merged automaticamente)
    return {"messages": ["new"]}

    # ❌ NÃO retorne None ou estrutura incompatível

```text

### Error 7: RunnableLambda Not Serializable
**Error**:

```text

TypeError: RunnableLambda with lambda function is not serializable

```text

**Cause**: Lambda functions não podem ser serializadas

**Solution**:

```python

# ❌ Lambda não serializable
chain = llm | RunnableLambda(lambda x: x.upper())

# ✅ Use função nomeada
def uppercase(text: str) -> str:
    return text.upper()

chain = llm | RunnableLambda(uppercase)

```text

### Error 8: Retriever Not Found in RAG
**Error**:

```text

AttributeError: 'VectorStore' object has no attribute '__or__'

```text

**Cause**: VectorStore não é Runnable, precisa converter

**Solution**:

```python

# ❌ VectorStore diretamente
chain = vectorstore | prompt | llm

# ✅ Converter para retriever primeiro
retriever = vectorstore.as_retriever()
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

```text

## Debugging Checklist

Ao debugar, verificar:

✅ **Imports**:
- Pacotes corretos (`langchain-openai`, não `langchain.llms`)
- Versão v1 imports

✅ **Composition**:
- Pipe operator usado corretamente
- Type compatibility entre componentes
- RunnableParallel para dicts

✅ **State (LangGraph)**:
- TypedDict definido corretamente
- Reducers para campos aditivos
- Nodes retornando state válido

✅ **Configuration**:
- API keys configuradas
- Model names corretos
- Environment variables set

✅ **Version Compatibility**:
- Python 3.10+ (v1 requirement)
- Deprecated features não usadas
- Message API syntax correta

## Debug Patterns

### Pattern 1: Trace LCEL Chain

```python

# Adicionar debug tracing
chain = (
    prompt
    | llm.with_config({"verbose": True})  # Habilita logging
    | parser
)

# Ou use callbacks
from langchain.callbacks import StdOutCallbackHandler

chain.invoke(
    input_data,
    config={"callbacks": [StdOutCallbackHandler()]}
)

```text

### Pattern 2: Inspect LangGraph State

```python

# Após execução, inspecionar estado
result = app.invoke(initial_state)

# Ver estado final
print("Final state:", result)

# Com checkpointing, ver histórico
for checkpoint in app.get_state_history():
    print("Checkpoint:", checkpoint)

```text

### Pattern 3: Test Individual Components

```python

# Testar cada componente isoladamente
prompt_result = prompt.invoke({"input": "test"})
print("Prompt:", prompt_result)

llm_result = llm.invoke(prompt_result)
print("LLM:", llm_result)

parser_result = parser.invoke(llm_result)
print("Parser:", parser_result)

```text

## Don't Use This Skill When

- ❌ Erros não relacionados a LangChain/LangGraph
- ❌ Bugs em código Python geral
- ❌ Problemas de infraestrutura (não do framework)

## Examples

**Example 1 - Debug Pipe Error**:

```text

User: "Getting TypeError with pipe operator"
Code: chain = {"input": value} | prompt | llm

Response: O erro ocorre porque dict não pode ser piped diretamente.
Solução:

```python
from langchain_core.runnables import RunnableParallel
chain = RunnableParallel({"input": lambda x: x}) | prompt | llm

```text

**Example 2 - Debug State Error**:

```text

User: "LangGraph state corruption - messages not accumulating"
Code: class State(TypedDict): messages: list[str]

Response: Falta reducer para acumulação. Solução:

```python
from typing import Annotated
from operator import add

class State(TypedDict):
    messages: Annotated[list[str], add]  # Agora acumula

```text
````
