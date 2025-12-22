---
description: "This skill should be used when the user asks about LangChain architecture, chains, prompts, output parsers, chat models, embeddings, vector stores, retrievers, or LCEL (LangChain Expression Language). Trigger on questions like 'how to create a chain', 'LangChain prompts', 'RAG with LangChain', 'LCEL pipe syntax'."
---

# LangChain Architecture Guide (2025)

## Overview

LangChain is a framework for developing applications powered by LLMs. As of 2025, LangChain is recommended for **simple orchestration** while **LangGraph** is preferred for complex agent workflows.

**Version**: LangChain 1.0+
**Core Package**: `langchain-core`

## Core Architecture

### Package Structure
```
langchain-core        # Base abstractions and LCEL
langchain             # High-level chains and agents
langchain-community   # Third-party integrations
langchain-openai      # OpenAI integration
langchain-anthropic   # Anthropic integration
langgraph             # Agent orchestration
langsmith             # Observability & evaluation
```

## LangChain Expression Language (LCEL)

### Pipe Syntax
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic

# Chain with pipe syntax
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = StrOutputParser()

chain = prompt | model | parser

# Invoke
result = chain.invoke({"input": "Hello!"})
```

### LCEL Benefits
- **Streaming**: First-class streaming support
- **Async**: Native async support
- **Batching**: Automatic batching
- **Retries**: Built-in retry logic
- **Tracing**: Automatic LangSmith integration

### Advanced LCEL Patterns

#### RunnablePassthrough
```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)
```

#### RunnableParallel
```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    summary=summary_chain,
    translation=translation_chain,
)
result = parallel.invoke({"text": "..."})
```

#### RunnableLambda
```python
from langchain_core.runnables import RunnableLambda

def custom_transform(data):
    return data.upper()

chain = prompt | model | RunnableLambda(custom_transform)
```

#### Conditional Logic
```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x["type"] == "question", question_chain),
    (lambda x: x["type"] == "summary", summary_chain),
    default_chain,
)
```

## Prompts

### ChatPromptTemplate
```python
from langchain_core.prompts import ChatPromptTemplate

# From messages
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("human", "{question}"),
])

# From template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)
```

### MessagesPlaceholder
```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])
```

### Few-Shot Prompts
```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "3+3", "output": "6"},
]

few_shot = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}"),
    ]),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator."),
    few_shot,
    ("human", "{input}"),
])
```

## Chat Models

### Anthropic
```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0,
    max_tokens=4096,
)
```

### OpenAI
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    streaming=True,
)
```

### Tool Binding
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}"

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("Weather in Tokyo?")
```

### Structured Output
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

structured_model = model.with_structured_output(Person)
result = structured_model.invoke("John is 30 years old")
# Person(name='John', age=30)
```

## Output Parsers

### String Parser
```python
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
```

### JSON Parser
```python
from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()
```

### Pydantic Parser
```python
from langchain_core.output_parsers import PydanticOutputParser

class Answer(BaseModel):
    response: str
    confidence: float

parser = PydanticOutputParser(pydantic_object=Answer)
```

## RAG (Retrieval-Augmented Generation)

### Basic RAG Chain
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Setup
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Prompt
prompt = ChatPromptTemplate.from_template("""
Answer based on context:

Context: {context}

Question: {question}
""")

# RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

result = rag_chain.invoke("What is LangChain?")
```

### Retriever Types
```python
# Similarity search
retriever = vectorstore.as_retriever(search_type="similarity", k=4)

# MMR (Maximum Marginal Relevance)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    k=4,
    fetch_k=10,
)

# Similarity score threshold
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    score_threshold=0.8,
)
```

## Document Loaders

### Common Loaders
```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader,
    CSVLoader,
)

# Text file
loader = TextLoader("file.txt")
docs = loader.load()

# PDF
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# Web page
loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

## Text Splitters

### Character Splitter
```python
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = splitter.split_documents(docs)
```

### Recursive Character Splitter (Recommended)
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""],
)
chunks = splitter.split_documents(docs)
```

## Embeddings

### OpenAI
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectors = embeddings.embed_documents(["Hello", "World"])
```

### HuggingFace
```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## Vector Stores

### Chroma (Local)
```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
```

### FAISS (Local)
```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")
```

### Pinecone (Cloud)
```python
from langchain_pinecone import PineconeVectorStore

vectorstore = PineconeVectorStore.from_documents(
    docs, embeddings, index_name="my-index"
)
```

## Memory (Deprecated - Use LangGraph)

> **Note**: LangChain memory is deprecated. Use LangGraph for conversation memory.

```python
# Legacy - Not recommended
from langchain.memory import ConversationBufferMemory

# Modern approach - Use LangGraph
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)
```

## Callbacks & Tracing

### LangSmith Integration
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=my-project
```

### Custom Callbacks
```python
from langchain_core.callbacks import BaseCallbackHandler

class MyHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM starting with {len(prompts)} prompts")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM finished")

chain.invoke({"input": "Hello"}, config={"callbacks": [MyHandler()]})
```

## When to Use LangChain vs LangGraph

### Use LangChain for:
- Simple chains (prompt → model → parser)
- RAG pipelines
- Document processing
- Basic chat applications

### Use LangGraph for:
- Complex agent workflows
- Multi-agent systems
- State management across turns
- Human-in-the-loop
- Conditional branching

### Hybrid Approach (Recommended)
```python
# LangChain for chains
chain = prompt | model | parser

# LangGraph for orchestration
graph = StateGraph(State)
graph.add_node("process", chain)  # Chain as node
```

## Best Practices

1. **Use LCEL**: Modern, composable, streaming-ready
2. **Structured Output**: Use Pydantic models for type safety
3. **Streaming**: Enable for better UX
4. **Tracing**: Always use LangSmith in production
5. **Error Handling**: Use `.with_fallbacks()` for resilience
6. **Batching**: Use `.batch()` for multiple inputs

## References

- [LangChain Docs](https://python.langchain.com/docs/)
- [LCEL Documentation](https://python.langchain.com/docs/concepts/lcel/)
- [LangChain API Reference](https://api.python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)

---

**Use the MCP tool `SearchDocsByLangChain` to find specific documentation and examples.**
