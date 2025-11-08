# LangSmith Automation Examples - Exemplos Práticos

Exemplos completos de automações no LangSmith para construção de datasets, annotation queues e online evaluation.

## 🎯 O Que São Automations?

Automations no LangSmith permitem **ações automáticas** em datapoints (traces/runs) baseadas em:

1. **Filter**: Subset de datapoints para atuar
1. **Sampling Rate**: Percentual de datapoints filtrados
1. **Action**: O que fazer (ex: adicionar a dataset, annotation queue, evaluator)

## 📊 Anatomia de uma Automation

```python
# Conceitual - configurado via UI
automation = {
    "name": "Positive Feedback to Dataset",
    "filter": 'and(eq(feedback_key, "user_rating"), gte(feedback_score, 4))',
    "sampling_rate": 1.0,  # 100% dos filtered
    "action": {
        "type": "add_to_dataset",
        "dataset_name": "golden-examples_v1.0.0"
    }
}
```

## 🔧 Exemplo 1: Auto-Construção de Golden Dataset

**Use case**: Adicionar automaticamente runs aprovados por usuários a um dataset.

### Via UI (Recomendado)

1. **Navegar**: Project → Automations → New Rule
1. **Filter**: `feedback_key == "user_rating" AND feedback_score >= 4`
1. **Sampling**: 100%
1. **Action**: Add to Dataset → `golden-examples_v1.0.0`

### Via Code (Simulação)

```python
from langsmith import Client

client = Client()

# Setup: Criar golden dataset
golden_dataset = client.create_dataset(
    dataset_name="golden-examples_v1.0.0",
    description="Auto-populated with user-approved examples (rating >= 4)"
)

# Automation logic (rodaria periodicamente)
def automation_positive_feedback_to_dataset():
    # Filtrar runs com feedback positivo
    positive_runs = client.list_runs(
        project_name="production-app",
        filter='and(eq(feedback_key, "user_rating"), gte(feedback_score, 4))'
    )

    # Converter para examples
    examples = []
    for run in positive_runs:
        if run.inputs and run.outputs:
            example = {
                "inputs": run.inputs,
                "outputs": run.outputs,
                "metadata": {
                    "feedback_score": run.feedback_stats.get("user_rating"),
                    "run_id": str(run.id),
                    "timestamp": run.start_time.isoformat()
                }
            }
            examples.append(example)

    # Adicionar ao dataset
    if examples:
        client.create_examples(
            dataset_id=golden_dataset.id,
            examples=examples
        )
        print(f"✅ Added {len(examples)} new golden examples")


# Executar automation (agendado ou manual)
automation_positive_feedback_to_dataset()
```

## 📝 Exemplo 2: Annotation Queue para Feedback Negativo

**Use case**: Enviar runs com feedback negativo para revisão manual.

### Via UI

1. **Navegar**: Project → Automations → New Rule
1. **Filter**: `feedback_key == "user_rating" AND feedback_score < 3`
1. **Sampling**: 100%
1. **Action**: Send to Annotation Queue → `negative-feedback-review`

### Via Code (Simulação)

```python
from langsmith import Client

client = Client()

# Automation logic
def automation_negative_feedback_to_queue():
    # Filtrar runs com feedback negativo
    negative_runs = client.list_runs(
        project_name="production-app",
        filter='and(eq(feedback_key, "user_rating"), lt(feedback_score, 3))'
    )

    # Marcar para annotation (conceitual - API pode variar)
    items_for_annotation = []
    for run in negative_runs:
        item = {
            "run_id": str(run.id),
            "inputs": run.inputs,
            "outputs": run.outputs,
            "feedback_score": run.feedback_stats.get("user_rating"),
            "status": "pending_review"
        }
        items_for_annotation.append(item)

    # Save to annotation queue (arquivo local ou DB)
    import json
    with open("annotation_queue.json", "w") as f:
        json.dump(items_for_annotation, f, indent=2)

    print(f"📝 {len(items_for_annotation)} items added to annotation queue")


automation_negative_feedback_to_queue()
```

### Workflow de Annotation

```python
# 1. Reviewer anota items da queue
def annotate_item(run_id: str, correct_output: dict, notes: str):
    """Anotar item manualmente"""
    with open("annotation_queue.json", "r") as f:
        queue = json.load(f)

    # Encontrar item
    for item in queue:
        if item["run_id"] == run_id:
            item["annotation"] = {
                "correct_output": correct_output,
                "notes": notes,
                "annotator": "reviewer@example.com",
                "timestamp": datetime.now().isoformat()
            }
            item["status"] = "annotated"

    # Save
    with open("annotation_queue.json", "w") as f:
        json.dump(queue, f, indent=2)


# 2. Processar items anotados → adicionar a dataset
def process_annotated_items():
    """Mover items anotados para dataset"""
    with open("annotation_queue.json", "r") as f:
        queue = json.load(f)

    # Filtrar anotados
    annotated = [item for item in queue if item["status"] == "annotated"]

    # Converter para examples
    examples = [
        {
            "inputs": item["inputs"],
            "outputs": item["annotation"]["correct_output"],
            "metadata": {
                "original_output": item["outputs"],
                "annotator": item["annotation"]["annotator"],
                "notes": item["annotation"]["notes"]
            }
        }
        for item in annotated
    ]

    # Adicionar a dataset de corrections
    corrections_dataset = client.create_or_get_dataset(
        name="annotated-corrections_v1.0.0",
        description="Manually annotated corrections"
    )

    client.create_examples(
        dataset_id=corrections_dataset.id,
        examples=examples
    )

    print(f"✅ {len(examples)} annotated items added to dataset")


# Uso
annotate_item(
    run_id="run-123",
    correct_output={"answer": "Corrected answer"},
    notes="Original answer was incomplete"
)

process_annotated_items()
```

## 🔍 Exemplo 3: Online Evaluation Automation

**Use case**: Executar evaluator automaticamente em todos os runs de produção.

### Via UI

1. **Navegar**: Project → Automations → New Rule
1. **Filter**: `all` (todos os runs)
1. **Sampling**: 10% (para reduzir custos)
1. **Action**: Run Evaluator → `relevance-check`

### Via Code (Simulation)

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Definir evaluator
def relevance_evaluator(run, example):
    """Avalia relevância da resposta"""
    # Usar LLM-as-judge ou regra
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    prompt = f"""
    Question: {run.inputs.get('question')}
    Answer: {run.outputs.get('answer')}

    Is the answer relevant to the question? Respond with score 0-1.
    """

    response = llm.invoke(prompt)
    score = float(response.content.strip())

    return {"score": score}


# Automation logic
def automation_online_evaluation():
    """Executar evaluator em runs recentes"""
    # Filtrar runs recentes
    recent_runs = client.list_runs(
        project_name="production-app",
        limit=100  # Últimos 100 runs
    )

    # Sampling 10%
    import random
    sampled_runs = random.sample(list(recent_runs), k=len(recent_runs) // 10)

    # Executar evaluator
    for run in sampled_runs:
        result = relevance_evaluator(run, None)

        # Log resultado
        print(f"Run {run.id}: relevance score = {result['score']}")

        # Adicionar feedback ao run (conceitual)
        # client.add_feedback(
        #     run_id=run.id,
        #     key="relevance_score",
        #     score=result["score"]
        # )


automation_online_evaluation()
```

## 📊 Exemplo 4: Dataset Construction por Error Type

**Use case**: Criar datasets separados por tipo de erro.

```python
from langsmith import Client

client = Client()

# Criar datasets por error type
error_types = {
    "timeout": "timeout-errors_v1.0.0",
    "validation": "validation-errors_v1.0.0",
    "llm-error": "llm-errors_v1.0.0"
}

datasets = {}
for error_type, dataset_name in error_types.items():
    datasets[error_type] = client.create_dataset(
        dataset_name=dataset_name,
        description=f"Examples with {error_type} errors"
    )


# Automation logic
def automation_categorize_errors():
    """Categoriza errors e adiciona a datasets apropriados"""
    # Filtrar runs com erro
    error_runs = client.list_runs(
        project_name="production-app",
        filter="eq(error, true)"
    )

    for run in error_runs:
        # Categorizar erro
        error_msg = run.error or ""

        if "timeout" in error_msg.lower():
            category = "timeout"
        elif "validation" in error_msg.lower():
            category = "validation"
        else:
            category = "llm-error"

        # Adicionar ao dataset apropriado
        example = {
            "inputs": run.inputs,
            "metadata": {
                "error": run.error,
                "run_id": str(run.id),
                "category": category
            }
        }

        client.create_examples(
            dataset_id=datasets[category].id,
            examples=[example]
        )

    print(f"✅ Errors categorized and added to datasets")


automation_categorize_errors()
```

## 🎯 Exemplo 5: A/B Test Dataset Creation

**Use case**: Criar datasets separados para cada variante de A/B test.

```python
from langsmith import Client

client = Client()

# Criar datasets por variante
variants = ["control", "variant_a", "variant_b"]
datasets = {}

for variant in variants:
    datasets[variant] = client.create_dataset(
        dataset_name=f"ab-test-{variant}_v1.0.0",
        description=f"Examples from {variant} variant"
    )


# Automation logic
def automation_ab_test_datasets():
    """Separar runs por variante de A/B test"""
    for variant in variants:
        # Filtrar runs da variante
        variant_runs = client.list_runs(
            project_name="production-app",
            filter=f'eq(metadata.variant, "{variant}")'
        )

        # Converter para examples
        examples = [
            {
                "inputs": run.inputs,
                "outputs": run.outputs,
                "metadata": {
                    "variant": variant,
                    "run_id": str(run.id),
                    "feedback_score": run.feedback_stats.get("user_rating")
                }
            }
            for run in variant_runs
            if run.inputs and run.outputs
        ]

        # Adicionar ao dataset
        if examples:
            client.create_examples(
                dataset_id=datasets[variant].id,
                examples=examples
            )
            print(f"✅ {len(examples)} examples added to {variant} dataset")


automation_ab_test_datasets()
```

## 📅 Scheduling Automations

### Usando Cron (Linux/Mac)

```bash
# crontab -e
# Executar automation a cada hora
0 * * * * cd /path/to/project && uv run python automation_script.py

# Executar diariamente às 2am
0 2 * * * cd /path/to/project && uv run python automation_script.py
```

### Usando GitHub Actions

```yaml
# .github/workflows/langsmith-automation.yml
name: LangSmith Automation

on:
  schedule:
    - cron: '0 */6 * * *'  # A cada 6 horas
  workflow_dispatch:  # Manual trigger

jobs:
  run-automation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install langsmith python-dotenv

      - name: Run automation
        env:
          LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}
        run: |
          python automation_script.py
```

## ✅ Best Practices para Automations

1. **Start with sampling**: Use 10-20% inicialmente para testar
1. **Monitor closely**: Verifique logs e datasets regularmente
1. **Validate before prod**: Teste em staging primeiro
1. **Use metadata**: Adicione metadata para rastreabilidade
1. **Handle duplicates**: Check se example já existe antes de add
1. **Version datasets**: Crie nova versão ao adicionar muitos examples
1. **Document filters**: Mantenha docs de filtros usados
1. **Alert on failures**: Configure notificações se automation falhar
