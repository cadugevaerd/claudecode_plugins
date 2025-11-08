# Dataset Structure - Anatomia e Schema Design

Documentação técnica completa sobre a estrutura fundamental de datasets no LangSmith.

## 📐 Anatomia Completa de um Example

### Estrutura Base

```python
{
    "inputs": {
        # Input dictionary - passed to target function
        "key1": "value1",
        "key2": "value2"
    },
    "outputs": {
        # Reference/ground truth outputs - used by evaluators
        "expected_key1": "expected_value1",
        "expected_key2": "expected_value2"
    },
    "metadata": {
        # Optional metadata for filtering/stratification
        "source": "manual|production|synthetic",
        "difficulty": "easy|medium|hard",
        "category": "category_name",
        "created_at": "2025-01-08T10:30:00Z",
        "created_by": "user@example.com",
        "version": "1.0.0"
    }
}
```

### Field-by-Field Breakdown

#### 1. Inputs (Required)

**Purpose**: Define what will be passed to the application/model under test.

**Guidelines**:

- ✅ Must match the application's expected input schema exactly
- ✅ Use descriptive keys that match your application's interface
- ✅ Include all required parameters
- ✅ Can include optional parameters for specific test scenarios

**Common patterns by use case**:

```python
# Q&A System
inputs = {"question": "What is LangChain?"}

# RAG System
inputs = {
    "query": "Explain vector databases",
    "context_type": "technical_docs"
}

# Chat Agent
inputs = {
    "message": "Book a flight to NYC",
    "conversation_history": [...]
}

# Multi-modal
inputs = {
    "text": "Describe this image",
    "image_url": "https://..."
}

# Function Calling
inputs = {
    "user_request": "What's the weather?",
    "available_tools": ["weather_api", "search"]
}
```

#### 2. Outputs (Reference/Ground Truth)

**Purpose**: Define the expected/correct output that evaluators will compare against.

**Types of reference outputs**:

1. **Exact Match** - For deterministic outputs

   ```python
   outputs = {"answer": "LangChain is a framework for building LLM applications"}
   ```

1. **Semantic Match** - For flexible outputs (evaluated by LLM-as-judge)

   ```python
   outputs = {
       "answer": "Should mention: framework, LLM, composition, agents",
       "key_concepts": ["framework", "LLM applications", "chains"]
   }
   ```

1. **Multiple Valid Outputs** - For non-deterministic scenarios

   ```python
   outputs = {
       "valid_answers": [
           "LangChain is a framework...",
           "LangChain helps build...",
           "A framework for developing..."
       ]
   }
   ```

1. **Structured Output** - For complex responses

   ```python
   outputs = {
       "entities": ["LangChain", "LLM"],
       "intent": "definition_request",
       "sentiment": "neutral",
       "answer": "..."
   }
   ```

1. **Partial Reference** - For HITL/progressive annotation

   ```python
   outputs = {
       "answer": None,  # To be filled by SME
       "answer_guidelines": "Should explain framework purpose and key features"
   }
   ```

**Guidelines**:

- ✅ Should be verifiable and measurable
- ✅ Can be partial (for HITL workflows)
- ✅ Must align with evaluation metrics being used
- ✅ Include enough detail for evaluator to assess quality

#### 3. Metadata (Optional but Recommended)

**Purpose**: Enable filtering, stratification, and analysis of evaluation results.

**Recommended metadata fields**:

```python
metadata = {
    # Source tracking
    "source": "manual|production|synthetic",
    "trace_id": "abc123",  # If from production
    "created_at": "2025-01-08T10:30:00Z",
    "created_by": "user@example.com",

    # Categorization
    "category": "authentication",
    "subcategory": "password_reset",
    "tags": ["edge_case", "multi_step"],

    # Difficulty/Priority
    "difficulty": "easy|medium|hard",
    "priority": "p0|p1|p2",
    "is_edge_case": true,

    # Domain-specific
    "language": "en",
    "region": "US",
    "user_segment": "enterprise",

    # Annotation tracking (for HITL)
    "annotator": "expert@company.com",
    "annotation_date": "2025-01-09",
    "confidence": 0.95,
    "needs_review": false
}
```

**Stratification examples**:

After evaluation, you can analyze results by:

- Difficulty: "How well does the model perform on hard questions?"
- Category: "Which categories have the lowest accuracy?"
- Source: "Are production examples harder than manual ones?"
- Tags: "Do edge cases fail more often?"

## 🔧 Schema Design Patterns

### Pattern 1: Simple Q&A

**Use case**: Question answering, chatbots, simple retrieval

```python
{
    "inputs": {
        "question": "What is the capital of France?"
    },
    "outputs": {
        "answer": "Paris"
    },
    "metadata": {
        "category": "geography",
        "difficulty": "easy"
    }
}
```

### Pattern 2: RAG with Context

**Use case**: Retrieval-augmented generation

```python
{
    "inputs": {
        "query": "What are the benefits of vector databases?",
        "top_k": 5,
        "retrieval_method": "semantic"
    },
    "outputs": {
        "answer": "Vector databases enable...",
        "expected_sources": ["doc1.pdf", "doc2.pdf"],
        "key_concepts": ["similarity search", "embeddings"]
    },
    "metadata": {
        "category": "technical_qa",
        "requires_retrieval": true,
        "difficulty": "medium"
    }
}
```

### Pattern 3: Multi-turn Conversation

**Use case**: Conversational agents, multi-turn dialogs

```python
{
    "inputs": {
        "messages": [
            {"role": "user", "content": "I need to book a flight"},
            {"role": "assistant", "content": "Where would you like to go?"},
            {"role": "user", "content": "New York City"}
        ],
        "current_message": "When do you want to depart?"
    },
    "outputs": {
        "next_message": "Should ask for departure date",
        "extracted_info": {
            "destination": "New York City",
            "departure_date": null
        },
        "next_action": "ask_departure_date"
    },
    "metadata": {
        "category": "travel_booking",
        "conversation_turn": 3,
        "difficulty": "medium"
    }
}
```

### Pattern 4: Function/Tool Calling

**Use case**: Agent systems, tool-using LLMs

```python
{
    "inputs": {
        "user_request": "What's the weather in San Francisco?",
        "available_tools": [
            {"name": "get_weather", "description": "..."},
            {"name": "search_web", "description": "..."}
        ]
    },
    "outputs": {
        "tool_calls": [
            {
                "tool": "get_weather",
                "arguments": {"location": "San Francisco, CA"}
            }
        ],
        "should_call_tool": true
    },
    "metadata": {
        "category": "tool_calling",
        "expected_tool": "get_weather",
        "difficulty": "easy"
    }
}
```

### Pattern 5: Classification/Extraction

**Use case**: Entity extraction, intent classification

```python
{
    "inputs": {
        "text": "I want to cancel my subscription and get a refund"
    },
    "outputs": {
        "intent": "cancel_subscription",
        "entities": {
            "action": "cancel",
            "subject": "subscription",
            "secondary_request": "refund"
        },
        "sentiment": "negative"
    },
    "metadata": {
        "category": "customer_service",
        "has_multiple_intents": true,
        "difficulty": "medium"
    }
}
```

### Pattern 6: Code Generation

**Use case**: Code assistants, code completion

```python
{
    "inputs": {
        "prompt": "Write a Python function to calculate fibonacci numbers",
        "language": "python",
        "context": "# Existing code context here"
    },
    "outputs": {
        "code": "def fibonacci(n):\n    ...",
        "should_include": ["recursion or iteration", "base cases", "return value"],
        "should_not_include": ["external libraries"]
    },
    "metadata": {
        "category": "code_generation",
        "language": "python",
        "difficulty": "easy"
    }
}
```

## 📊 Schema Validation Best Practices

### Validation Checklist

Before uploading examples to LangSmith:

- [ ] **Inputs match application schema** - All required fields present
- [ ] **Outputs align with evaluators** - Reference data matches what evaluators expect
- [ ] **Metadata is consistent** - Same keys across all examples
- [ ] **No sensitive data** - PII, credentials, or proprietary info removed
- [ ] **Unicode/encoding correct** - Special characters handled properly
- [ ] **Size within limits** - Individual examples < 100KB recommended

### Dataset Schema Definition (New LangSmith Feature)

LangSmith now supports **dataset schemas** for validation:

```python
from langsmith import Client

client = Client()

# Define schema
schema = {
    "inputs": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "minLength": 1}
        },
        "required": ["question"]
    },
    "outputs": {
        "type": "object",
        "properties": {
            "answer": {"type": "string", "minLength": 1}
        },
        "required": ["answer"]
    }
}

# Create dataset with schema
dataset = client.create_dataset(
    dataset_name="qa-system_v1.0.0",
    description="Q&A dataset with schema validation",
    data_schema=schema  # All examples will be validated
)
```

**Benefits**:

- ✅ Automatic validation on example upload
- ✅ Prevent schema drift over time
- ✅ Clear contract for data producers
- ✅ Easier to consume in evaluation code

## 🎯 Common Schema Anti-Patterns

### ❌ Anti-Pattern 1: Inconsistent Input Keys

```python
# Bad - different keys across examples
example1 = {"inputs": {"question": "..."}}
example2 = {"inputs": {"query": "..."}}  # Different key!

# Good - consistent keys
example1 = {"inputs": {"question": "..."}}
example2 = {"inputs": {"question": "..."}}
```

### ❌ Anti-Pattern 2: Vague Reference Outputs

```python
# Bad - too vague for evaluation
outputs = {"answer": "Something about LangChain"}

# Good - specific and measurable
outputs = {
    "answer": "LangChain is a framework for building LLM applications",
    "must_mention": ["framework", "LLM", "applications"]
}
```

### ❌ Anti-Pattern 3: Missing Context in Metadata

```python
# Bad - no context for stratification
metadata = {}

# Good - rich metadata for analysis
metadata = {
    "source": "production",
    "category": "authentication",
    "difficulty": "hard",
    "created_at": "2025-01-08"
}
```

### ❌ Anti-Pattern 4: Mixing Schema Versions

```python
# Bad - schema changes mid-dataset
example1 = {"inputs": {"question": "..."}}
example2 = {"inputs": {"question": "...", "context": "..."}}  # New field!

# Good - create new dataset version
dataset_v1 = {"inputs": {"question": "..."}}
dataset_v2 = {"inputs": {"question": "...", "context": "..."}}  # New version
```

## 🔄 Schema Evolution Strategy

When your application's schema changes:

1. **Backward-compatible changes** (adding optional fields):

   - ✅ Can update existing dataset (MINOR version bump)
   - ✅ Add new optional fields to new examples
   - ✅ Old examples still valid

1. **Breaking changes** (removing/renaming required fields):

   - ❌ Cannot update existing dataset
   - ✅ Create new dataset version (MAJOR version bump)
   - ✅ Migrate old examples if needed

Example:

```python
# v1.0.0 schema
inputs_v1 = {"question": "..."}

# v1.1.0 schema (backward-compatible)
inputs_v1_1 = {"question": "...", "context": "..."}  # Added optional field

# v2.0.0 schema (breaking change)
inputs_v2 = {"query": "...", "mode": "..."}  # Renamed required field
```

## 📚 Additional Resources

- **LangSmith Dataset Schemas Blog**: https://blog.langchain.com/dataset-schemas/
- **LangSmith UI Dataset Management**: https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application
- **JSON Schema Specification**: https://json-schema.org/

## ✅ Quick Reference Table

| Component | Required | Purpose | Best Practice |
|-----------|----------|---------|---------------|
| `inputs` | ✅ Yes | Define test inputs | Match app schema exactly |
| `outputs` | ✅ Yes | Ground truth reference | Align with evaluators |
| `metadata` | ❌ No | Enable stratification | Include source, difficulty, category |
| Schema validation | ❌ No | Prevent drift | Use for production datasets |
| Versioning | ✅ Yes | Reproducibility | Semantic or branch-based |
