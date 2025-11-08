# LangSmith Upload Patterns - Padrões Avançados

Padrões de upload de datasets para diferentes fontes de dados e casos de uso.

## 🎯 Padrões por Fonte de Dados

### Pattern 1: Upload de JSON Local

**Use quando**: Dados curados manualmente em arquivo JSON

```python
import json
from langsmith import Client

client = Client()

# Ler JSON
with open("golden_examples.json", "r") as f:
    data = json.load(f)

# Converter para formato LangSmith
examples = [
    {
        "inputs": {
            "question": item["question"],
            "context": item.get("context", "")
        },
        "outputs": {
            "expected_answer": item["answer"],
            "category": item.get("category", "general")
        }
    }
    for item in data
]

# Criar dataset
dataset = client.create_dataset(
    dataset_name="golden-qa_v1.0.0",
    description="Curated Q&A examples"
)

# Upload
client.create_examples(dataset_id=dataset.id, examples=examples)
```

**Formato JSON esperado**:

```json
[
  {
    "question": "What is LangSmith?",
    "answer": "LangSmith is a platform for LLM development",
    "context": "...",
    "category": "product"
  }
]
```

### Pattern 2: Upload de CSV/DataFrame

**Use quando**: Dados tabulares (Excel, CSV, Google Sheets export)

```python
import pandas as pd
from langsmith import Client

client = Client()

# Opção A: Usar upload_dataframe (recomendado)
df = pd.read_csv("evaluation_data.csv")

client.upload_dataframe(
    df=df,
    name="csv-dataset_v1.0.0",
    description="Dataset from CSV file",
    input_keys=["question", "context"],  # Colunas para inputs
    output_keys=["answer", "reasoning"]   # Colunas para outputs
)

# Opção B: Conversão manual
examples = [
    {
        "inputs": {
            "question": row["question"],
            "context": row["context"]
        },
        "outputs": {
            "answer": row["answer"],
            "reasoning": row.get("reasoning", "")
        }
    }
    for _, row in df.iterrows()
]

dataset = client.create_dataset(
    dataset_name="manual-csv_v1.0.0",
    description="Manually converted CSV"
)
client.create_examples(dataset_id=dataset.id, examples=examples)
```

**CSV esperado**:

```csv
question,context,answer,reasoning
"What is X?","Context about X","X is...","Because..."
```

### Pattern 3: Upload de Runs de Produção (Backtesting)

**Use quando**: Criar dataset de casos que falharam em produção

```python
from langsmith import Client

client = Client()

# Filtrar runs que falharam
failed_runs = client.list_runs(
    project_name="production-app",
    filter="eq(error, true)",  # Apenas runs com erro
    limit=100
)

# Converter para examples
examples = []
for run in failed_runs:
    if run.inputs:
        example = {
            "inputs": run.inputs,
            "metadata": {
                "run_id": str(run.id),
                "error": run.error,
                "timestamp": run.start_time.isoformat()
            }
        }

        # Incluir outputs se disponível
        if run.outputs:
            example["outputs"] = run.outputs

        examples.append(example)

# Criar dataset de failures
dataset = client.create_dataset(
    dataset_name="production-failures_v1.0.0",
    description="Failed runs from production"
)

client.create_examples(dataset_id=dataset.id, examples=examples)
```

### Pattern 4: Upload de Feedback Positivo (Golden Dataset)

**Use quando**: Construir dataset de exemplos aprovados por usuários

```python
from langsmith import Client

client = Client()

# Filtrar runs com feedback positivo
positive_runs = client.list_runs(
    project_name="production-app",
    filter='and(eq(feedback_key, "user_rating"), gte(feedback_score, 4))'
)

# Converter para golden examples
examples = [
    {
        "inputs": run.inputs,
        "outputs": run.outputs,
        "metadata": {
            "feedback_score": run.feedback_stats.get("user_rating"),
            "run_id": str(run.id)
        }
    }
    for run in positive_runs
    if run.inputs and run.outputs
]

# Criar golden dataset
dataset = client.create_dataset(
    dataset_name="golden-approved_v1.0.0",
    description="User-approved examples (rating >= 4)"
)

client.create_examples(dataset_id=dataset.id, examples=examples)
```

### Pattern 5: Upload Incremental (Append)

**Use quando**: Adicionar novos examples a dataset existente

```python
from langsmith import Client

client = Client()

# Recuperar dataset existente
dataset = client.read_dataset(dataset_name="qa-system_v1.0.0")

# Novos examples
new_examples = [
    {
        "inputs": {"question": "New question?"},
        "outputs": {"answer": "New answer"}
    }
]

# Append (cria nova versão automaticamente)
client.create_examples(dataset_id=dataset.id, examples=new_examples)

print(f"Dataset agora tem {dataset.example_count + len(new_examples)} exemplos")
```

### Pattern 6: Upload de Annotation Queue

**Use quando**: Converter items anotados manualmente em dataset

```python
from langsmith import Client

client = Client()

# Supondo que você tem annotation queue results
annotated_items = [
    {
        "original_input": {"query": "..."},
        "annotation": {
            "correct_output": "...",
            "annotator": "user@example.com",
            "notes": "..."
        }
    }
    # ... items da annotation queue
]

# Converter para examples
examples = [
    {
        "inputs": item["original_input"],
        "outputs": {
            "expected": item["annotation"]["correct_output"]
        },
        "metadata": {
            "annotator": item["annotation"]["annotator"],
            "notes": item["annotation"].get("notes", "")
        }
    }
    for item in annotated_items
]

# Upload
dataset = client.create_dataset(
    dataset_name="annotated-corrections_v1.0.0",
    description="Manually annotated corrections"
)
client.create_examples(dataset_id=dataset.id, examples=examples)
```

## 🔄 Padrões de Versionamento

### Pattern: Semantic Versioning para Datasets

```python
from langsmith import Client

client = Client()

# v1.0.0 - Initial release
dataset_v1 = client.create_dataset(
    dataset_name="qa-system_v1.0.0",
    description="Initial Q&A dataset"
)
client.create_examples(dataset_id=dataset_v1.id, examples=initial_examples)

# v1.1.0 - Added examples (MINOR bump)
dataset_v1_1 = client.create_dataset(
    dataset_name="qa-system_v1.1.0",
    description="Added 50 new examples (backward compatible)"
)
# Copy previous + add new
all_examples = initial_examples + new_examples
client.create_examples(dataset_id=dataset_v1_1.id, examples=all_examples)

# v2.0.0 - Schema change (MAJOR bump)
dataset_v2 = client.create_dataset(
    dataset_name="qa-system_v2.0.0",
    description="Breaking change: added 'context' field to inputs"
)
# Examples agora têm estrutura diferente
new_schema_examples = [
    {
        "inputs": {
            "question": ex["inputs"]["question"],
            "context": "..."  # Novo campo obrigatório
        },
        "outputs": ex["outputs"]
    }
    for ex in initial_examples
]
client.create_examples(dataset_id=dataset_v2.id, examples=new_schema_examples)
```

### Pattern: Tagging de Versões Importantes

```python
# Tag versions importantes
# Nota: API exata pode variar - verificar docs
client.tag_dataset_version(
    dataset_id=dataset.id,
    tag="prod"  # ou "baseline", "staging", "release-2024-01"
)
```

## 📊 Padrões de Validação

### Pattern: Validação de Schema antes de Upload

```python
from langsmith import Client
from typing import Dict, Any

def validate_example_schema(example: Dict[str, Any]) -> bool:
    """Valida estrutura de example antes de upload"""

    # Validar estrutura básica
    if not isinstance(example, dict):
        raise ValueError("Example must be dict")

    if "inputs" not in example:
        raise ValueError("Example must have 'inputs'")

    if not isinstance(example["inputs"], dict):
        raise ValueError("'inputs' must be dict")

    # Validar campos obrigatórios do schema
    required_input_keys = ["question"]  # Definir schema
    for key in required_input_keys:
        if key not in example["inputs"]:
            raise ValueError(f"Missing required input key: {key}")

    # Validar outputs (se presente)
    if "outputs" in example:
        if not isinstance(example["outputs"], dict):
            raise ValueError("'outputs' must be dict")

    return True

# Uso
examples = [...]
for idx, ex in enumerate(examples):
    try:
        validate_example_schema(ex)
    except ValueError as e:
        print(f"❌ Example {idx} inválido: {e}")
```

## ⚡ Performance Patterns

### Pattern: Batch Upload em Chunks

**Use quando**: Upload de muitos examples (> 1000)

```python
from langsmith import Client

client = Client()

# Função helper para chunking
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Upload em chunks de 100
large_examples = [...]  # Milhares de examples
dataset = client.create_dataset(
    dataset_name="large-dataset_v1.0.0",
    description="Large dataset uploaded in chunks"
)

chunk_size = 100
for idx, chunk in enumerate(chunk_list(large_examples, chunk_size)):
    client.create_examples(dataset_id=dataset.id, examples=chunk)
    print(f"✅ Chunk {idx+1} uploaded ({len(chunk)} examples)")
```

## 🎯 Best Practices Resumo

1. **Sempre valide estrutura**: Use schema validation antes de upload
1. **Use batch operations**: `create_examples()` (plural) é mais eficiente
1. **Versione datasets**: Inclua versão no nome (`v1.0.0`)
1. **Handle duplicates**: Try/except ao criar dataset
1. **Metadata útil**: Adicione metadata field para rastreabilidade
1. **Chunk large uploads**: Upload em batches de 100-500 examples
1. **Tag milestones**: Marque versões importantes (`prod`, `baseline`)
1. **Backup datasets**: Export regularmente para arquivos locais
