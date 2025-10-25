---
description: Mostra padrões de código comuns para evaluation (dataset creation, testing, CI/CD)
---

# Padrões de Evaluation

Padrões de código comuns e best practices para desenvolver evaluations de LLMs.

## Como usar

Execute o comando e opcionalmente especifique:
- Tipo de padrão (dataset-creation, testing, ci-cd, mocking)
- Framework (openevals, langsmith, pytest)

## Padrões Disponíveis

### 1. Dataset Creation Patterns

#### Pattern 1.1: Golden Dataset Manual

**Quando usar**: Dataset pequeno (<100 exemplos), alta qualidade necessária

**Estrutura**:
```json
[
  {
    "inputs": {
      "question": "What is the capital of France?",
      "context": "France is a country in Western Europe. Paris is its capital."
    },
    "reference_outputs": {
      "answer": "Paris",
      "should_cite_context": true
    },
    "metadata": {
      "difficulty": "easy",
      "category": "factual",
      "created_by": "human_annotator",
      "created_at": "2025-01-15"
    }
  }
]
```

**Código de carregamento**:
```python
import json
from pathlib import Path
from typing import List, Dict, Any

def load_golden_dataset(path: str = "datasets/golden.json") -> List[Dict[str, Any]]:
    """Carrega dataset anotado manualmente."""
    with open(path) as f:
        return json.load(f)

def validate_dataset_schema(dataset: List[Dict[str, Any]]) -> bool:
    """Valida schema do dataset."""
    required_keys = {"inputs", "reference_outputs"}

    for example in dataset:
        if not required_keys.issubset(example.keys()):
            raise ValueError(f"Exemplo faltando chaves: {required_keys - set(example.keys())}")

    return True
```

---

#### Pattern 1.2: Synthetic Dataset Generation

**Quando usar**: Dataset grande (100+), diversidade necessária, bootstrap rápido

**Código (usando LLM)**:
```python
from openai import OpenAI
from typing import List, Dict
import json

def generate_synthetic_dataset(
    num_examples: int = 100,
    categories: List[str] = ["factual", "opinion", "math"],
    difficulty_levels: List[str] = ["easy", "medium", "hard"]
) -> List[Dict]:
    """
    Gera dataset sintético usando LLM.

    Args:
        num_examples: Número de exemplos a gerar
        categories: Categorias de perguntas
        difficulty_levels: Níveis de dificuldade

    Returns:
        List de exemplos sintéticos
    """
    client = OpenAI()
    dataset = []

    prompt_template = """
Gere um exemplo de Q&A com as seguintes características:
- Categoria: {category}
- Dificuldade: {difficulty}

Retorne JSON no formato:
{{
  "inputs": {{
    "question": "pergunta aqui",
    "context": "contexto relevante"
  }},
  "reference_outputs": {{
    "answer": "resposta esperada",
    "should_cite_context": true/false
  }}
}}
"""

    for _ in range(num_examples):
        category = categories[_ % len(categories)]
        difficulty = difficulty_levels[_ % len(difficulty_levels)]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": prompt_template.format(
                    category=category,
                    difficulty=difficulty
                )
            }],
            response_format={"type": "json_object"},
            temperature=0.9  # Alta temperatura para diversidade
        )

        example = json.loads(response.choices[0].message.content)
        example["metadata"] = {
            "category": category,
            "difficulty": difficulty,
            "synthetic": True
        }

        dataset.append(example)

    return dataset

# Uso
dataset = generate_synthetic_dataset(num_examples=50)
with open("datasets/synthetic.json", "w") as f:
    json.dump(dataset, f, indent=2)
```

---

#### Pattern 1.3: Real Data Sampling

**Quando usar**: Production data disponível, avaliação de casos reais

**Código**:
```python
from datetime import datetime, timedelta
import random
from typing import List, Dict

def sample_production_data(
    db_connection,
    num_samples: int = 100,
    date_range_days: int = 30,
    stratify_by: str = "category"
) -> List[Dict]:
    """
    Amostra dados de produção para criar dataset de evaluation.

    Args:
        db_connection: Conexão com banco de dados
        num_samples: Número de amostras
        date_range_days: Intervalo de dias para buscar
        stratify_by: Campo para estratificar amostras

    Returns:
        Dataset amostrado
    """
    # Buscar dados recentes
    end_date = datetime.now()
    start_date = end_date - timedelta(days=date_range_days)

    query = """
    SELECT
        user_query as question,
        llm_response as answer,
        context_used as context,
        category,
        feedback_score
    FROM llm_interactions
    WHERE created_at BETWEEN %s AND %s
    AND feedback_score IS NOT NULL
    ORDER BY RANDOM()
    LIMIT %s
    """

    cursor = db_connection.cursor()
    cursor.execute(query, (start_date, end_date, num_samples * 2))

    raw_data = cursor.fetchall()

    # Estratificar por categoria
    categorized = {}
    for row in raw_data:
        category = row["category"]
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(row)

    # Amostrar igualmente de cada categoria
    samples_per_category = num_samples // len(categorized)

    dataset = []
    for category, examples in categorized.items():
        sampled = random.sample(examples, min(samples_per_category, len(examples)))

        for example in sampled:
            dataset.append({
                "inputs": {
                    "question": example["question"],
                    "context": example["context"]
                },
                "reference_outputs": {
                    "answer": example["answer"]
                },
                "metadata": {
                    "category": category,
                    "feedback_score": example["feedback_score"],
                    "source": "production",
                    "sampled_at": datetime.now().isoformat()
                }
            })

    return dataset
```

---

### 2. Testing Patterns

#### Pattern 2.1: Unit Testing Evaluators

**Quando usar**: Sempre! Testar evaluators antes de usar em production

**Código (pytest)**:
```python
import pytest
from evaluators.hallucination_evaluator import hallucination_evaluator

class TestHallucinationEvaluator:
    """Testes unitários para hallucination evaluator."""

    def test_detects_factual_response(self):
        """Deve dar score alto para resposta factual."""
        outputs = {"answer": "Paris is the capital of France."}
        inputs = {"context": "France's capital city is Paris."}

        result = hallucination_evaluator(outputs, inputs)

        assert result["score"] >= 0.8, "Score deveria ser alto para resposta factual"

    def test_detects_hallucinated_response(self):
        """Deve dar score baixo para resposta com alucinação."""
        outputs = {"answer": "London is the capital of France."}
        inputs = {"context": "France's capital city is Paris."}

        result = hallucination_evaluator(outputs, inputs)

        assert result["score"] <= 0.3, "Score deveria ser baixo para alucinação"

    def test_handles_empty_context(self):
        """Deve lidar com contexto vazio."""
        outputs = {"answer": "Paris"}
        inputs = {"context": ""}

        result = hallucination_evaluator(outputs, inputs)

        assert "score" in result
        assert "comment" in result

    @pytest.mark.parametrize("answer,context,expected_min_score", [
        ("Paris", "Paris is the capital", 0.8),
        ("London", "Paris is the capital", 0.0),
        ("The capital is Paris", "Paris is the capital of France", 0.8),
    ])
    def test_various_cases(self, answer, context, expected_min_score):
        """Testa vários casos."""
        outputs = {"answer": answer}
        inputs = {"context": context}

        result = hallucination_evaluator(outputs, inputs)

        assert result["score"] >= expected_min_score
```

---

#### Pattern 2.2: Integration Testing with LangSmith

**Quando usar**: Testar evaluation completa end-to-end

**Código (pytest + LangSmith)**:
```python
import pytest
from langsmith import evaluate
from evaluators import hallucination_evaluator, relevance_evaluator

@pytest.mark.langsmith
def test_rag_chatbot_evaluation():
    """
    Testa evaluation completa do RAG chatbot.

    Este teste será sincronizado com LangSmith.
    """
    from app import rag_chatbot  # Sua app

    # Dataset de teste
    test_cases = [
        {
            "inputs": {
                "question": "What is the capital of France?",
                "context": "Paris is the capital of France."
            },
            "reference_outputs": {
                "answer": "Paris"
            }
        }
    ]

    # Executar evaluation
    results = evaluate(
        rag_chatbot,
        data=test_cases,
        evaluators=[hallucination_evaluator, relevance_evaluator],
        experiment_prefix="test-run"
    )

    # Asserts
    assert results["hallucination_evaluator"]["mean"] >= 0.8
    assert results["relevance_evaluator"]["mean"] >= 0.7
```

---

#### Pattern 2.3: Mocking LLM Calls in Tests

**Quando usar**: Testes rápidos, determinísticos, sem custos de API

**Código (pytest-mock)**:
```python
import pytest
from unittest.mock import Mock, patch

def test_llm_judge_evaluator_mocked(mocker):
    """Testa LLM-as-judge com mock de API."""

    # Mock da resposta do OpenAI
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"score": 0.9, "reason": "Highly relevant"}'))
    ]

    mocker.patch(
        "openai.OpenAI.chat.completions.create",
        return_value=mock_response
    )

    # Executar evaluator
    from evaluators.relevance_evaluator import relevance_evaluator

    result = relevance_evaluator(
        outputs={"answer": "Paris"},
        inputs={"question": "What is the capital of France?"}
    )

    assert result["score"] == 0.9
    assert "relevant" in result["reason"].lower()

@pytest.fixture
def mock_openai_client():
    """Fixture para mock de OpenAI client."""
    with patch("openai.OpenAI") as mock:
        yield mock

def test_with_fixture(mock_openai_client):
    """Usa fixture de mock."""
    mock_openai_client.return_value.embeddings.create.return_value.data = [
        Mock(embedding=[0.1] * 1536)
    ]

    # Seu teste aqui
    pass
```

---

### 3. CI/CD Patterns

#### Pattern 3.1: GitHub Actions Evaluation

**Quando usar**: Executar evaluations automaticamente em PRs

**Código (.github/workflows/evaluation.yml)**:
```yaml
name: LLM Evaluation

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  evaluate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install langsmith openevals pytest

      - name: Run Evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
        run: |
          pytest tests/evaluations/ -v --langsmith

      - name: Check Thresholds
        run: |
          python scripts/check_thresholds.py

      - name: Comment PR with Results
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('results/latest.json'));

            const comment = `
            ## Evaluation Results

            | Metric | Score | Threshold | Status |
            |--------|-------|-----------|--------|
            | Hallucination | ${results.hallucination} | 0.8 | ${results.hallucination >= 0.8 ? '✅' : '❌'} |
            | Relevance | ${results.relevance} | 0.7 | ${results.relevance >= 0.7 ? '✅' : '❌'} |
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

#### Pattern 3.2: Regression Detection

**Quando usar**: Detectar degradação de performance entre versões

**Código**:
```python
import json
from pathlib import Path
from typing import Dict

def detect_regression(
    current_results: Dict[str, float],
    baseline_path: str = "baselines/v1.0.json",
    threshold: float = 0.05  # 5% degradação
) -> Dict[str, bool]:
    """
    Detecta regressão comparando com baseline.

    Args:
        current_results: Resultados atuais {"metric": score}
        baseline_path: Path para baseline results
        threshold: % de degradação aceitável

    Returns:
        Dict com status de regressão por métrica
    """
    # Carregar baseline
    with open(baseline_path) as f:
        baseline = json.load(f)

    regressions = {}

    for metric, current_score in current_results.items():
        if metric not in baseline:
            continue

        baseline_score = baseline[metric]
        degradation = (baseline_score - current_score) / baseline_score

        is_regression = degradation > threshold

        regressions[metric] = {
            "is_regression": is_regression,
            "baseline_score": baseline_score,
            "current_score": current_score,
            "degradation_pct": degradation * 100
        }

        if is_regression:
            print(f"⚠️  REGRESSION in {metric}: {baseline_score:.3f} → {current_score:.3f} ({degradation*100:.1f}% worse)")

    return regressions

# Uso em CI
if __name__ == "__main__":
    current = json.load(open("results/current.json"))
    regressions = detect_regression(current)

    # Fail CI se houver regressão
    if any(r["is_regression"] for r in regressions.values()):
        exit(1)
```

---

### 4. Advanced Patterns

#### Pattern 4.1: A/B Testing Evaluators

**Quando usar**: Comparar duas versões de modelo/prompt

**Código**:
```python
from langsmith import evaluate
from typing import Callable, Dict

def ab_test_evaluators(
    app_a: Callable,
    app_b: Callable,
    dataset: list,
    evaluators: list,
    experiment_name: str = "ab-test"
) -> Dict:
    """
    Executa A/B test entre duas versões.

    Args:
        app_a: Versão A da aplicação
        app_b: Versão B da aplicação
        dataset: Dataset de teste
        evaluators: Lista de evaluators

    Returns:
        Comparação de resultados
    """
    # Avaliar versão A
    results_a = evaluate(
        app_a,
        data=dataset,
        evaluators=evaluators,
        experiment_prefix=f"{experiment_name}-version-a"
    )

    # Avaliar versão B
    results_b = evaluate(
        app_b,
        data=dataset,
        evaluators=evaluators,
        experiment_prefix=f"{experiment_name}-version-b"
    )

    # Comparar
    comparison = {}
    for metric in results_a.keys():
        if metric in results_b:
            score_a = results_a[metric]["mean"]
            score_b = results_b[metric]["mean"]

            improvement = ((score_b - score_a) / score_a) * 100

            comparison[metric] = {
                "version_a": score_a,
                "version_b": score_b,
                "improvement_pct": improvement,
                "winner": "B" if score_b > score_a else "A"
            }

    return comparison
```

---

#### Pattern 4.2: Pairwise Evaluation

**Quando usar**: Comparar outputs lado a lado

**Código**:
```python
from openai import OpenAI

def pairwise_evaluator(
    output_a: str,
    output_b: str,
    inputs: dict
) -> dict:
    """
    Compara dois outputs lado a lado usando LLM.

    Args:
        output_a: Output da versão A
        output_b: Output da versão B
        inputs: Inputs originais

    Returns:
        Resultado da comparação
    """
    client = OpenAI()

    prompt = f"""
Compare as duas respostas para a pergunta:

PERGUNTA: {inputs['question']}

RESPOSTA A:
{output_a}

RESPOSTA B:
{output_b}

Qual resposta é melhor? Considere:
- Precisão
- Relevância
- Clareza
- Completude

Retorne JSON:
{{
  "winner": "A" ou "B" ou "tie",
  "confidence": 0.0-1.0,
  "reasoning": "explicação"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0
    )

    return json.loads(response.choices[0].message.content)
```

---

## Best Practices Summary

1. **Always Test Evaluators**: Unit test evaluators antes de usar
2. **Version Your Datasets**: Track mudanças em datasets
3. **Monitor Drift**: Detecte degradação com regression tests
4. **Stratify Sampling**: Balance categorias em datasets
5. **Mock LLM Calls**: Use mocks em testes para velocidade/custo
6. **Automate in CI/CD**: Execute evaluations automaticamente
7. **Track Baselines**: Mantenha baselines para comparação
8. **Document Thresholds**: Documente por que escolheu cada threshold

## Referências

- Pytest Best Practices: https://docs.pytest.org/
- LangSmith CI/CD: https://docs.smith.langchain.com/evaluation/how_to_guides/pytest
- Synthetic Data: https://www.confident-ai.com/blog/the-definitive-guide-to-synthetic-data-generation-using-llms