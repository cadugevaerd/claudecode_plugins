---
name: evaluation-developer
description: Desenvolve código de evaluators para LLMs (OpenEvals, LangSmith, BLEU, ROUGE, LLM-as-judge). Use quando criar evaluators, métricas customizadas, evaluation suites, ou testar LLMs.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Evaluation Developer Skill

## Instructions

Skill especializada em **desenvolver código de evaluation** para LLMs e agentes. Foco em **criar**, não executar.

### Step 1: Identify Evaluation Need

Quando usuário menciona termos como:
- "criar evaluator", "desenvolver evaluation"
- "métricas para LLM", "testar meu chatbot"
- "hallucination detection", "relevance evaluation"
- "BLEU score", "ROUGE", "LLM-as-judge"
- "evaluation suite", "evaluation dataset"
- "como avaliar meu LLM"

### Step 2: Determine Type of Evaluation

Identificar tipo de evaluator necessário:

**LLM-as-Judge**:
- Para critérios subjetivos (relevance, tone, coherence)
- Quando regras são complexas demais para codificar
- Exemplo: Detectar alucinações, avaliar qualidade

**Similarity-based**:
- Para comparar com ground truth
- BLEU (translation), ROUGE (summarization), embeddings
- Exemplo: Avaliar precisão de summary

**Rule-based**:
- Para validações exatas
- Regex, exact match, custom logic
- Exemplo: Validar formato de email

**Composite**:
- Combina múltiplas métricas
- Quando precisa avaliar vários aspectos
- Exemplo: Accuracy + Relevance + Response Time

### Step 3: Generate Evaluator Code

Gerar código completo incluindo:

1. **Imports necessários**
2. **Função do evaluator** com:
   - Docstring clara
   - Type hints
   - Error handling
   - Retorno padronizado
3. **Testes unitários** com pytest
4. **Exemplo de uso**
5. **Explicação de quando usar**

#### Template para OpenEvals LLM-as-Judge:

```python
from openevals.llm import create_llm_as_judge

CUSTOM_PROMPT = """
[Instruções claras do que avaliar]

<context_or_inputs>
{inputs}
</context_or_inputs>

<output_to_evaluate>
{outputs}
</output_to_evaluate>

[Critérios de avaliação]
[Escala de score]

Retorne apenas o score numérico.
"""

evaluator_name = create_llm_as_judge(
    prompt=CUSTOM_PROMPT,
    model="openai:gpt-4o-mini",
)
```

#### Template para LangSmith Custom Evaluator:

```python
from langsmith.evaluation import evaluator

@evaluator
def custom_evaluator(outputs: dict, inputs: dict = None, reference_outputs: dict = None) -> dict:
    """
    [Descrição do que avalia]

    Args:
        outputs: [Explicar estrutura esperada]
        inputs: [Explicar se usado]
        reference_outputs: [Explicar se usado]

    Returns:
        dict: Score (0-1) e comentário
    """
    # Implementação

    return {
        "score": score,
        "comment": "explicação"
    }
```

#### Template para Similarity Metric:

```python
from [library] import [metric]

def metric_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """
    Calcula [métrica] entre output e referência.

    [Explicação da métrica]
    """
    output = outputs.get("field", "")
    reference = reference_outputs.get("field", "")

    # Calcular métrica
    score = calculate_metric(output, reference)

    return {
        "metric_name": score,
        "comment": f"Score: {score:.3f}"
    }
```

### Step 4: Include Testing Patterns

SEMPRE incluir testes unitários:

```python
import pytest

def test_evaluator_positive_case():
    """Testa caso que deve ter score alto."""
    result = evaluator(
        outputs={"answer": "good answer"},
        inputs={"question": "question"}
    )
    assert result["score"] >= 0.8

def test_evaluator_negative_case():
    """Testa caso que deve ter score baixo."""
    result = evaluator(
        outputs={"answer": "bad answer"},
        inputs={"question": "question"}
    )
    assert result["score"] <= 0.3

@pytest.mark.parametrize("input,expected_min", [
    ("test1", 0.8),
    ("test2", 0.5),
])
def test_evaluator_various(input, expected_min):
    """Testa múltiplos casos."""
    result = evaluator(outputs={"answer": input})
    assert result["score"] >= expected_min
```

### Step 5: Explain Trade-offs

Para cada evaluator, explicar:

**Quando usar**:
- ✅ Cenário 1
- ✅ Cenário 2

**Quando NÃO usar**:
- ❌ Limitação 1
- ❌ Limitação 2

**Trade-offs**:
- Custo vs Precisão
- Velocidade vs Qualidade
- Determinismo vs Flexibilidade

### Step 6: Provide Integration Code

Mostrar como integrar em evaluation pipeline:

```python
from langsmith import evaluate

results = evaluate(
    your_app,
    data="dataset-name",
    evaluators=[evaluator1, evaluator2],
    experiment_prefix="experiment-name"
)
```

## When to Use

Esta skill é invocada automaticamente quando:

- Usuário quer **criar** evaluator customizado
- Precisa implementar métricas (BLEU, ROUGE, custom)
- Quer scaffolding de evaluation suite
- Pergunta sobre **como avaliar** LLM
- Menciona OpenEvals, LangSmith, evaluation
- Precisa de **código** de evaluation (não execução)

**Trigger terms**:
- "criar evaluator", "desenvolver evaluation"
- "como avaliar", "métricas para"
- "hallucination detection", "relevance scoring"
- "BLEU", "ROUGE", "LLM-as-judge"
- "evaluation suite", "dataset de evaluation"
- "testar meu LLM", "avaliar chatbot"

## Examples

### Example 1: Create Hallucination Detector

**User says**: "Preciso detectar alucinações no meu RAG system"

**Skill generates**:

```python
"""
Hallucination Detector para RAG Systems
Usa LLM-as-judge para verificar se output é suportado pelo contexto.
"""

from langsmith.evaluation import evaluator
from openai import OpenAI

@evaluator
def hallucination_detector(outputs: dict, inputs: dict) -> dict:
    """
    Detecta alucinações comparando resposta com contexto.

    Args:
        outputs: Dict com "answer" - resposta do RAG
        inputs: Dict com "context" - contexto usado pelo RAG

    Returns:
        dict: Score 0-1 (1=factual, 0=alucinado)
    """
    answer = outputs.get("answer", "")
    context = inputs.get("context", "")

    prompt = f"""
Verifique se a RESPOSTA contém APENAS informações do CONTEXTO.

CONTEXTO:
{context}

RESPOSTA:
{answer}

Retorne JSON:
{{
  "is_factual": true/false,
  "score": 0.0-1.0,
  "reason": "explicação"
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

    return {
        "score": result["score"],
        "comment": result["reason"]
    }


# === TESTES ===

def test_hallucination_detector_factual():
    """Deve dar score alto para resposta factual."""
    result = hallucination_detector(
        outputs={"answer": "Paris is the capital."},
        inputs={"context": "Paris is France's capital."}
    )
    assert result["score"] >= 0.8

def test_hallucination_detector_hallucinated():
    """Deve dar score baixo para alucinação."""
    result = hallucination_detector(
        outputs={"answer": "London is the capital."},
        inputs={"context": "Paris is France's capital."}
    )
    assert result["score"] <= 0.3


# === USO ===

from langsmith import evaluate

results = evaluate(
    your_rag_app,
    data="rag-dataset",
    evaluators=[hallucination_detector]
)
```

**E explica**:
✅ Use para: RAG systems, Q&A factual
✅ Vantagens: Detecta alucinações semânticas
❌ Limitações: Custo de API, latência
💡 Trade-off: Precisão alta vs custo

---

### Example 2: Implement ROUGE Score

**User says**: "Como implemento ROUGE para meu summarizer?"

**Skill generates**:

```python
"""
ROUGE Score Evaluator
Métrica padrão para avaliar summarization.
"""

from rouge import Rouge
from typing import Dict

def rouge_evaluator(outputs: Dict, reference_outputs: Dict) -> Dict:
    """
    Calcula ROUGE scores para summarization.

    ROUGE mede overlap de n-gramas entre summaries.

    Args:
        outputs: {"summary": "generated summary"}
        reference_outputs: {"summary": "reference summary"}

    Returns:
        dict: ROUGE-1, ROUGE-2, ROUGE-L F1 scores
    """
    generated = outputs.get("summary", "")
    reference = reference_outputs.get("summary", "")

    if not generated or not reference:
        return {
            "rouge_1_f1": 0.0,
            "rouge_2_f1": 0.0,
            "rouge_l_f1": 0.0
        }

    rouge = Rouge()
    scores = rouge.get_scores(generated, reference)[0]

    return {
        "rouge_1_f1": scores["rouge-1"]["f"],
        "rouge_2_f1": scores["rouge-2"]["f"],
        "rouge_l_f1": scores["rouge-l"]["f"],
    }


# === TESTES ===

def test_rouge_perfect_match():
    """Score perfeito para match exato."""
    result = rouge_evaluator(
        outputs={"summary": "Paris is capital."},
        reference_outputs={"summary": "Paris is capital."}
    )
    assert result["rouge_1_f1"] == 1.0

def test_rouge_partial():
    """Score parcial para overlap parcial."""
    result = rouge_evaluator(
        outputs={"summary": "Paris is beautiful."},
        reference_outputs={"summary": "Paris is capital."}
    )
    assert 0.3 < result["rouge_1_f1"] < 0.8


# === QUANDO USAR ===

"""
✅ Use ROUGE para:
  - Summarization tasks
  - Comparar com ground truth
  - Avaliar overlap de conteúdo

❌ NÃO use para:
  - Paráfrase (palavras diferentes, mesmo sentido)
  - Avaliar coerência/fluência
  - Quando não há referência exata

💡 Trade-offs:
  - Rápido e determinístico
  - Mas ignora semântica
  - Combine com LLM-as-judge para melhor avaliação
"""
```

---

### Example 3: Create Evaluation Suite

**User says**: "Preciso de uma evaluation suite completa para meu chatbot"

**Skill generates**:

```
evaluations/
├── config/
│   └── eval_config.py           # Thresholds e configuração
├── datasets/
│   ├── golden_dataset.json      # Dataset anotado
│   └── dataset_generator.py     # Gerador sintético
├── evaluators/
│   ├── accuracy_evaluator.py
│   ├── relevance_evaluator.py
│   └── response_time_evaluator.py
├── tests/
│   ├── test_evaluators.py       # Testes unitários
│   └── test_integration.py      # Testes end-to-end
├── run_evaluation.py             # Script principal
└── README.md
```

**E gera código funcional para cada arquivo**, incluindo:
- Evaluators implementados
- Dataset de exemplo
- Testes completos
- Script de execução
- Documentação

## Key Patterns

### Pattern 1: Always Include Tests

Todo evaluator DEVE ter testes unitários:
- Casos positivos (score alto esperado)
- Casos negativos (score baixo esperado)
- Edge cases (empty, null, etc.)
- Parametrized tests para múltiplos casos

### Pattern 2: Explain Trade-offs

Sempre explicar:
- ✅ Quando usar
- ❌ Limitações
- 💡 Trade-offs (custo, latência, precisão)

### Pattern 3: Provide Integration Code

Mostrar como usar em:
- LangSmith evaluate()
- OpenEvals evaluation pipeline
- Pytest integration
- CI/CD (GitHub Actions)

### Pattern 4: Mock for Testing

Ensinar patterns de mock para:
- Evitar custos de API em testes
- Testes determinísticos
- Testes offline

### Pattern 5: Documentation

Incluir:
- Docstrings completas
- Type hints
- Exemplos de uso
- Referências (papers, docs)

## References

- OpenEvals: https://github.com/langchain-ai/openevals
- LangSmith Evaluation: https://docs.smith.langchain.com/evaluation
- BLEU/ROUGE: https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation
- LLM-as-Judge: https://www.evidentlyai.com/llm-guide/llm-as-a-judge
- Pytest: https://docs.pytest.org/