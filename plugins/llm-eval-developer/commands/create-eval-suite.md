---
description: Gera estrutura completa de evaluation suite com dataset, evaluators e testes
---

# Criar Evaluation Suite

Gera scaffolding completo de uma evaluation suite, incluindo estrutura de projeto, datasets, evaluators, e configuração de testes.

## Como usar

Execute o comando e forneça:

- Nome da suite
- Tipo de aplicação sendo avaliada (chatbot, summarizer, translator, etc.)
- Métricas desejadas (accuracy, relevance, hallucination, etc.)
- Framework preferido (openevals, langsmith, pytest)

## Estrutura Gerada

````text

evaluations/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── eval_config.py          # Configuração de evaluators
├── datasets/
│   ├── __init__.py
│   ├── golden_dataset.json     # Dataset anotado
│   └── dataset_generator.py    # Gerador de datasets sintéticos
├── evaluators/
│   ├── __init__.py
│   ├── accuracy_evaluator.py
│   ├── relevance_evaluator.py
│   └── hallucination_evaluator.py
├── tests/
│   ├── __init__.py
│   ├── test_evaluators.py      # Testes unitários de evaluators
│   └── test_app_evaluation.py  # Evaluation completa da app
├── results/
│   └── .gitkeep
├── run_evaluation.py            # Script principal de execução
└── README.md                    # Documentação da suite

```text

## Exemplos de Uso

### Exemplo 1: Suite para Chatbot RAG

```text

/create-eval-suite

Nome: rag-chatbot-eval
Tipo: chatbot com RAG
Métricas: accuracy, relevance, hallucination, response_time
Framework: langsmith

```text

**Arquivos gerados**:

**evaluations/config/eval_config.py**:

```python
"""Configuração de evaluators para RAG Chatbot."""

from typing import Dict, Any, List
from langsmith.evaluation import evaluator

# Evaluators configuration
EVALUATORS = [
    "accuracy_evaluator",
    "relevance_evaluator",
    "hallucination_evaluator",
    "response_time_evaluator"
]

# LLM configuration for LLM-as-judge
LLM_JUDGE_CONFIG = {
    "model": "openai:gpt-4o-mini",
    "temperature": 0.0,
}

# Thresholds
THRESHOLDS = {
    "accuracy": 0.8,        # Mínimo 80%
    "relevance": 0.7,       # Mínimo 70%
    "hallucination": 0.9,   # Mínimo 90% (sem alucinação)
    "response_time": 2.0,   # Máximo 2 segundos
}

```text

**evaluations/datasets/golden_dataset.json**:

```json
[
  {
    "inputs": {
      "question": "What is the capital of France?",
      "context": "France is a country in Western Europe. Its capital and largest city is Paris."
    },
    "reference_outputs": {
      "answer": "Paris",
      "should_cite_context": true
    },
    "metadata": {
      "difficulty": "easy",
      "category": "factual",
      "expected_response_time_ms": 500
    }
  },
  {
    "inputs": {
      "question": "How does photosynthesis work?",
      "context": "Photosynthesis is a process used by plants to convert light energy into chemical energy."
    },
    "reference_outputs": {
      "answer": "Photosynthesis is the process by which plants use light energy to convert carbon dioxide and water into glucose and oxygen.",
      "should_cite_context": true
    },
    "metadata": {
      "difficulty": "medium",
      "category": "explanatory",
      "expected_response_time_ms": 1000
    }
  }
]

```text

**evaluations/evaluators/hallucination_evaluator.py**:

```python
"""Evaluator para detectar alucinações."""

from langsmith.evaluation import evaluator

@evaluator
def hallucination_evaluator(outputs: dict, inputs: dict) -> dict:
    """
    Detecta se o LLM gerou informações não suportadas pelo contexto.

    Args:
        outputs: Output do LLM (deve conter "answer")
        inputs: Inputs incluindo "context"

    Returns:
        dict: Score (0=alucinado, 1=factual) e comentário
    """
    from openai import OpenAI

    answer = outputs.get("answer", "")
    context = inputs.get("context", "")

    prompt = f"""
Analise se a resposta contém APENAS informações suportadas pelo contexto.

CONTEXTO:
{context}

RESPOSTA:
{answer}

Retorne um JSON com:
{{
  "is_factual": true/false,
  "hallucination_examples": ["exemplo1", "exemplo2"],
  "confidence": 0.0-1.0
}}
"""

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0
    )

    result = eval(response.choices[0].message.content)

    score = 1.0 if result["is_factual"] else 0.0
    comment = f"Factual: {result['is_factual']}. Confiança: {result['confidence']:.2f}"

    if result["hallucination_examples"]:
        comment += f" | Alucinações: {', '.join(result['hallucination_examples'])}"

    return {
        "score": score,
        "comment": comment
    }

```text

**evaluations/tests/test_evaluators.py**:

```python
"""Testes unitários para evaluators."""

import pytest
from evaluators.hallucination_evaluator import hallucination_evaluator
from evaluators.relevance_evaluator import relevance_evaluator

def test_hallucination_evaluator_factual():
    """Testa detecção de resposta factual."""
    outputs = {"answer": "Paris is the capital of France."}
    inputs = {"context": "France's capital is Paris."}

    result = hallucination_evaluator(outputs, inputs)

    assert result["score"] >= 0.8, "Deveria detectar resposta factual"

def test_hallucination_evaluator_hallucinated():
    """Testa detecção de alucinação."""
    outputs = {"answer": "The capital of France is London."}
    inputs = {"context": "France's capital is Paris."}

    result = hallucination_evaluator(outputs, inputs)

    assert result["score"] <= 0.3, "Deveria detectar alucinação"

def test_relevance_evaluator_relevant():
    """Testa detecção de resposta relevante."""
    outputs = {"answer": "Paris"}
    inputs = {"question": "What is the capital of France?"}

    result = relevance_evaluator(outputs, inputs)

    assert result["score"] >= 0.8, "Deveria detectar relevância"

```text

**evaluations/run_evaluation.py**:

```python
"""Script principal para executar evaluation suite."""

import json
from pathlib import Path
from langsmith import evaluate
from evaluators.hallucination_evaluator import hallucination_evaluator
from evaluators.relevance_evaluator import relevance_evaluator
from config.eval_config import EVALUATORS, THRESHOLDS

def load_dataset(path: str = "datasets/golden_dataset.json"):
    """Carrega dataset de avaliação."""
    with open(path) as f:
        return json.load(f)

def your_app(inputs: dict) -> dict:
    """
    Substitua esta função pela sua aplicação real.

    Args:
        inputs: Dict com "question" e "context"

    Returns:
        dict: Output com "answer"
    """
    # TODO: Implementar sua app aqui
    return {"answer": "Placeholder answer"}

def main():
    """Executa evaluation completa."""

    # Carregar dataset
    dataset = load_dataset()

    # Definir evaluators
    evaluators = [
        hallucination_evaluator,
        relevance_evaluator,
    ]

    # Executar evaluation
    results = evaluate(
        your_app,
        data=dataset,
        evaluators=evaluators,
        experiment_prefix="rag-chatbot",
    )

    # Analisar resultados
    print("\n=== RESULTADOS DA EVALUATION ===\n")

    for metric, threshold in THRESHOLDS.items():
        if metric in results:
            score = results[metric]
            status = "✅ PASS" if score >= threshold else "❌ FAIL"
            print(f"{metric}: {score:.2f} (threshold: {threshold}) {status}")

    # Salvar resultados
    output_path = Path("results") / "latest_results.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResultados salvos em: {output_path}")

if __name__ == "__main__":
    main()

```text

### Exemplo 2: Suite para Summarization

```text

/create-eval-suite

Nome: summarization-eval
Tipo: text summarization
Métricas: rouge, bleu, coherence, conciseness
Framework: openevals

```text

**Arquivos gerados** (estrutura similar, mas com evaluators específicos):

**evaluations/evaluators/rouge_evaluator.py**:

```python
"""ROUGE score evaluator para summarization."""

from rouge import Rouge
from typing import Dict, Any

def rouge_evaluator(outputs: Dict[str, Any], reference_outputs: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcula ROUGE scores entre summary gerado e referência.

    Args:
        outputs: Summary gerado (deve conter "summary")
        reference_outputs: Summary de referência (deve conter "summary")

    Returns:
        dict: ROUGE-1, ROUGE-2, ROUGE-L scores
    """
    generated = outputs.get("summary", "")
    reference = reference_outputs.get("summary", "")

    rouge = Rouge()
    scores = rouge.get_scores(generated, reference)[0]

    # Retornar F1 scores
    return {
        "rouge_1_f1": scores["rouge-1"]["f"],
        "rouge_2_f1": scores["rouge-2"]["f"],
        "rouge_l_f1": scores["rouge-l"]["f"],
    }

```text

## Features da Suite

Cada evaluation suite gerada inclui:

- ✅ **Dataset anotado** com exemplos diversificados
- ✅ **Evaluators customizados** para métricas específicas
- ✅ **Testes unitários** para validar evaluators
- ✅ **Script de execução** pronto para uso
- ✅ **Configuração centralizada** de thresholds
- ✅ **Gerador de datasets sintéticos** (opcional)
- ✅ **README com documentação** completa
- ✅ **Integração com pytest** para CI/CD

## Referências

- LangSmith Evaluation: https://docs.smith.langchain.com/evaluation
- OpenEvals: https://github.com/langchain-ai/openevals
- ROUGE Metrics: https://pypi.org/project/rouge/
````
