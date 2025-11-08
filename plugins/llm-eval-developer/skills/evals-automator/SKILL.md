---
name: evals-automator
description: LangSmith dataset upload automation and Python scripting for LLM evaluations. Use when creating datasets, uploading examples to LangSmith, automating dataset creation from production runs, implementing golden datasets, or writing scripts for evaluation pipelines. Covers SDK setup, dataset versioning, and automation patterns.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Grep
  - Bash
---

# LangSmith Dataset Upload & Evaluation Automation

Conhecimento especializado em automação de uploads de datasets para LangSmith e criação de scripts Python para pipelines de avaliação de LLMs.

## 📋 When to Use Me

Invoque esta skill quando precisar de:

- **Upload de datasets**: Enviar exemplos (inputs/outputs) para LangSmith programaticamente
- **Automação de evaluations**: Criar scripts Python para pipelines de avaliação
- **Dataset management**: Criar, versionar e gerenciar datasets no LangSmith
- **Golden datasets**: Implementar curadoria manual de exemplos de alta qualidade
- **Backtesting**: Extrair exemplos de produção que falharam para datasets
- **SDK LangSmith**: Configurar e usar `langsmith-sdk` Python corretamente
- **Dataset versioning**: Implementar versionamento semântico de datasets
- **Automation patterns**: Configurar automações (filters, sampling, actions)

**Keywords de ativação**: "LangSmith dataset", "upload examples", "create evaluation dataset", "langsmith SDK", "golden dataset", "dataset versioning", "evaluation automation"

## 🎓 Core Knowledge

### 1. SDK Setup e Autenticação

**Bibliotecas necessárias**:

```python
pip install -U langsmith python-dotenv
```

**Configuração de ambiente**:

```python
# .env file
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=your_project_name
```

**Inicialização do cliente**:

```python
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()
client = Client()  # Usa env vars automaticamente
```

### 2. Estrutura de Dados (Dataset e Examples)

**Anatomia de um Example**:

```python
example = {
    "inputs": {
        "pergunta": "Onde Harrison trabalhou?",
        "contexto": "Harrison trabalhou na Kensho."
    },
    "outputs": {
        "resposta_esperada": "Harrison trabalhou na Kensho.",
        "categoria": "factual"
    }
}
```

**Componentes obrigatórios**:

- `inputs`: Dicionário de entradas passado para a aplicação durante avaliação
- `outputs`: Dicionário de saídas de referência (ground truth) - opcional mas crítico para evaluation

### 3. Workflow de Upload de Dataset

**Passo 1 - Criar Dataset (Container)**:

```python
dataset_name = "qa-system_v1.0.0"  # Versão explícita!

try:
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Dataset de Q&A para avaliação do sistema"
    )
except Exception as e:
    # Dataset já existe - recuperar
    dataset = client.read_dataset(dataset_name=dataset_name)
```

**Passo 2 - Upload de Examples (Batch)**:

```python
exemplos = [
    {
        "inputs": {"pergunta": "..."},
        "outputs": {"resposta_esperada": "..."}
    },
    # ... mais exemplos
]

client.create_examples(
    dataset_id=dataset.id,
    examples=exemplos
)
```

### 4. Dataset Versioning Best Practices

**Semantic Versioning para Datasets**:

- `MAJOR.MINOR.PATCH` (ex: `qa-system_v2.1.0`)
- **MAJOR**: Mudanças incompatíveis (schema diferente, inputs mudaram)
- **MINOR**: Novos exemplos adicionados (backward-compatible)
- **PATCH**: Correções de bugs em exemplos existentes

**Tagging de versões**:

```python
# LangSmith cria versões automaticamente ao adicionar/atualizar examples
# Use tags para marcar milestones
client.tag_dataset_version(
    dataset_id=dataset.id,
    version="v1.0.0",
    tag="prod"
)
```

### 5. Fontes de Dados para Datasets

**Tipo 1 - Golden Datasets (Curadoria Manual)**:

```python
import json

# Ler de arquivo local
with open("golden_examples.json", "r") as f:
    exemplos = json.load(f)

# Upload para LangSmith
client.create_examples(dataset_id=dataset.id, examples=exemplos)
```

**Tipo 2 - Backtesting (Produção)**:

```python
# Filtrar runs de produção que falharam
runs = client.list_runs(
    project_name="production-project",
    filter="eq(error, true)"  # Apenas runs com erro
)

# Converter runs em examples
exemplos = [
    {
        "inputs": run.inputs,
        "outputs": {"expected": run.reference_example.outputs}
    }
    for run in runs if run.reference_example
]

# Upload
client.create_examples(dataset_id=dataset.id, examples=exemplos)
```

### 6. Automation Patterns no LangSmith

**Estrutura de Automations**:

- **Filter**: Subset de datapoints para atuar (ex: feedback positivo)
- **Sampling Rate**: Percentual de datapoints filtrados
- **Action**: O que fazer (ex: adicionar a dataset, enviar para annotation queue)

**Use cases comuns**:

```python
# 1. Auto-construção de dataset com feedback positivo
# Filter: feedback == "positive"
# Action: Add to dataset "golden-examples"

# 2. Annotation queue para feedback negativo
# Filter: feedback == "negative"
# Action: Send to annotation queue

# 3. Online evaluation
# Filter: all traces
# Action: Run evaluator "relevance-check"
```

## 📚 Reference Files

- **DATASET_MANAGER.md** - Classe completa para gerenciamento de datasets
- **UPLOAD_PATTERNS.md** - Padrões de upload (CSV, DataFrame, JSON, runs)
- **VERSIONING_GUIDE.md** - Guia completo de versionamento de datasets
- **AUTOMATION_EXAMPLES.md** - Exemplos de automações LangSmith

## 💡 Quick Examples

### Exemplo 1: Script Básico de Upload

```python
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()
client = Client()

# 1. Preparar dados
exemplos = [
    {
        "inputs": {"pergunta": "O que é LangSmith?"},
        "outputs": {"resposta_esperada": "LangSmith é uma plataforma para development de aplicações LLM."}
    },
    {
        "inputs": {"pergunta": "Como fazer upload de datasets?"},
        "outputs": {"resposta_esperada": "Use client.create_examples() com lista de exemplos."}
    }
]

# 2. Criar dataset (ou recuperar existente)
dataset_name = "faq-dataset_v1.0.0"
try:
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="FAQ examples for evaluation"
    )
except:
    dataset = client.read_dataset(dataset_name=dataset_name)

# 3. Upload examples
client.create_examples(dataset_id=dataset.id, examples=exemplos)

print(f"✅ Upload completo! Dataset: {dataset.name} ({dataset.example_count} exemplos)")
```

### Exemplo 2: Upload de CSV para LangSmith

```python
import pandas as pd
from langsmith import Client

client = Client()

# Ler CSV
df = pd.read_csv("evaluation_data.csv")

# Converter para formato LangSmith
exemplos = [
    {
        "inputs": {"pergunta": row["question"]},
        "outputs": {"resposta_esperada": row["answer"]}
    }
    for _, row in df.iterrows()
]

# Upload usando upload_dataframe (mais eficiente)
client.upload_dataframe(
    df=df,
    name="csv-dataset_v1.0.0",
    description="Dataset importado de CSV",
    input_keys=["question"],
    output_keys=["answer"]
)
```

### Exemplo 3: Dataset Manager Class

```python
class LangSmithDatasetManager:
    def __init__(self, client: Client):
        self.client = client

    def create_or_get_dataset(self, name: str, description: str):
        """Cria dataset ou recupera se já existe"""
        try:
            return self.client.create_dataset(
                dataset_name=name,
                description=description
            )
        except:
            return self.client.read_dataset(dataset_name=name)

    def upload_examples(self, dataset_id: str, examples: list):
        """Upload em lote com validação"""
        for example in examples:
            if "inputs" not in example:
                raise ValueError("Example must have 'inputs' key")

        self.client.create_examples(
            dataset_id=dataset_id,
            examples=examples
        )

    def version_dataset(self, dataset_id: str, version_tag: str):
        """Tagear versão do dataset"""
        self.client.tag_dataset_version(
            dataset_id=dataset_id,
            tag=version_tag
        )

# Uso
manager = LangSmithDatasetManager(client)
dataset = manager.create_or_get_dataset(
    name="production-examples_v2.0.0",
    description="Examples from production runs"
)
manager.upload_examples(dataset.id, exemplos)
manager.version_dataset(dataset.id, "prod-release")
```

## ✅ Checklist Rápido

**Antes de Upload**:

- [ ] SDK instalado: `pip install -U langsmith`
- [ ] Variáveis de ambiente configuradas (`LANGCHAIN_API_KEY`, etc)
- [ ] Cliente inicializado corretamente
- [ ] Dados no formato correto (inputs/outputs dict)

**Durante Upload**:

- [ ] Nome do dataset inclui versão (ex: `dataset_v1.0.0`)
- [ ] Description clara e descritiva
- [ ] Validação de estrutura de examples (inputs presente)
- [ ] Handle de exceções (dataset já existe)

**Após Upload**:

- [ ] Verificar contagem de exemplos
- [ ] Tagear versão importante (`prod`, `staging`, etc)
- [ ] Documentar mudanças (changelog)
- [ ] Testar evaluation com dataset criado

## 🎯 Regras de Ouro

1. **Sempre versione datasets**: Nome deve incluir versão explícita (`v1.0.0`)
1. **Validate structure**: Todo example DEVE ter `inputs` (outputs opcional mas recomendado)
1. **Use batch operations**: `create_examples()` (plural) é mais eficiente que loop de `create_example()`
1. **Handle duplicates**: Use try/except ao criar dataset (pode já existir)
1. **Document schema**: Defina schema de dataset no LangSmith para validação automática
1. **Tag milestones**: Marque versões importantes (`prod`, `baseline`, `v2.0`)
1. **Automate evaluation**: Configure evaluators bound to datasets no UI

## 📖 Quando Consultar Reference Files

- **DATASET_MANAGER.md**: Implementar classe completa de gerenciamento
- **UPLOAD_PATTERNS.md**: Padrões avançados (CSV, DataFrame, runs)
- **VERSIONING_GUIDE.md**: Estratégias de versionamento e changelog
- **AUTOMATION_EXAMPLES.md**: Configurar automations (filters, actions)
