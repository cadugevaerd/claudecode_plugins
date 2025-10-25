---
description: Gera código de evaluator customizado para LLMs (OpenEvals, LangSmith, ou custom)
---

# Criar Evaluator Customizado

Gera código completo de um evaluator customizado para avaliar outputs de LLMs, incluindo imports, estrutura, e documentação.

## Como usar

Execute o comando e forneça:
- Tipo de evaluator (llm-as-judge, regex, similarity, custom)
- Framework (openevals, langsmith, custom)
- Nome do evaluator
- Critérios de avaliação

## Tipos de Evaluators Disponíveis

### 1. LLM-as-Judge
Usa um LLM para avaliar outputs de outro LLM com rubrica em linguagem natural.

**Frameworks suportados**: OpenEvals, LangSmith

**Quando usar**:
- Avaliação subjetiva (qualidade, relevância, tom)
- Critérios complexos difíceis de codificar
- Avaliação contextual

### 2. Regex-based
Valida outputs contra padrões de regex.

**Frameworks suportados**: OpenEvals, Custom

**Quando usar**:
- Validar formato (email, telefone, JSON)
- Detectar palavras-chave específicas
- Validar estrutura de resposta

### 3. Similarity-based
Compara outputs com referências usando métricas de similaridade.

**Frameworks suportados**: OpenEvals, LangSmith, Custom

**Métricas**: BLEU, ROUGE, embeddings similarity

**Quando usar**:
- Comparar com ground truth
- Avaliar consistência
- Medir precisão de tradução/summarização

### 4. Custom Rule-based
Lógica customizada de avaliação.

**Frameworks suportados**: LangSmith, Custom

**Quando usar**:
- Regras de negócio específicas
- Validações complexas
- Métricas proprietárias

## Exemplos de Uso

### Exemplo 1: LLM-as-Judge com OpenEvals
```
/create-evaluator

Tipo: llm-as-judge
Framework: openevals
Nome: hallucination_detector
Critério: Detectar alucinações comparando output com contexto
```

**Código gerado**:
```python
from openevals.llm import create_llm_as_judge

HALLUCINATION_PROMPT = """
Analise o output do LLM em busca de alucinações (informações não suportadas pelo contexto).

<context>
{context}
</context>

<input>
{inputs}
</input>

<output>
{outputs}
</output>

Avalie de 0-10 onde:
- 0: Totalmente alucinado
- 10: Totalmente factual

Retorne apenas o número.
"""

hallucination_detector = create_llm_as_judge(
    prompt=HALLUCINATION_PROMPT,
    model="openai:gpt-4o-mini",
)
```

### Exemplo 2: Regex-based com OpenEvals
```
/create-evaluator

Tipo: regex
Framework: openevals
Nome: email_format_validator
Critério: Validar se output contém email válido
```

**Código gerado**:
```python
import re
from typing import Any
from openevals.types import EvaluatorResult, SimpleEvaluator

def create_email_validator() -> SimpleEvaluator:
    """
    Valida se o output contém um email válido.

    Returns:
        SimpleEvaluator: Evaluator que retorna True se email válido
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def email_evaluator(outputs: dict) -> EvaluatorResult:
        output_text = outputs.get("output", "")
        match = re.search(email_pattern, output_text)

        return {
            "score": 1.0 if match else 0.0,
            "comment": f"Email encontrado: {match.group()}" if match else "Nenhum email válido encontrado"
        }

    return email_evaluator

email_validator = create_email_validator()
```

### Exemplo 3: LangSmith Custom Evaluator
```
/create-evaluator

Tipo: custom
Framework: langsmith
Nome: response_length_checker
Critério: Verificar se resposta tem tamanho adequado (50-200 palavras)
```

**Código gerado**:
```python
from langsmith.evaluation import evaluator

@evaluator
def response_length_checker(outputs: dict, reference_outputs: dict = None) -> dict:
    """
    Verifica se a resposta tem comprimento adequado (50-200 palavras).

    Args:
        outputs: Outputs do LLM (deve conter chave "answer")
        reference_outputs: Referências opcionais

    Returns:
        dict: Score (0-1) e comentário
    """
    answer = outputs.get("answer", "")
    word_count = len(answer.split())

    # Score baseado em distância do ideal (125 palavras)
    if 50 <= word_count <= 200:
        # Quanto mais próximo de 125, melhor
        distance_from_ideal = abs(125 - word_count)
        score = max(0, 1 - (distance_from_ideal / 75))
    else:
        score = 0.0

    return {
        "score": score,
        "comment": f"Resposta com {word_count} palavras (ideal: 50-200)"
    }
```

### Exemplo 4: BLEU Score Evaluator
```
/create-evaluator

Tipo: similarity
Framework: custom
Nome: bleu_evaluator
Métrica: BLEU
```

**Código gerado**:
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from typing import Dict, Any

def bleu_evaluator(outputs: Dict[str, Any], reference_outputs: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcula BLEU score entre output e referência.

    Args:
        outputs: Output do LLM (deve conter "answer")
        reference_outputs: Ground truth (deve conter "answer")

    Returns:
        dict: Score BLEU (0-1)
    """
    predicted = outputs.get("answer", "").split()
    reference = reference_outputs.get("answer", "").split()

    # Usar smoothing para evitar zero scores
    smoothing = SmoothingFunction().method1

    score = sentence_bleu(
        [reference],
        predicted,
        smoothing_function=smoothing
    )

    return {
        "score": score,
        "comment": f"BLEU score: {score:.3f}"
    }
```

## Outputs

O comando gera:
- ✅ Código completo do evaluator
- ✅ Imports necessários
- ✅ Docstrings explicativas
- ✅ Exemplos de uso
- ✅ Sugestões de testes

## Referências

- OpenEvals: https://github.com/langchain-ai/openevals
- LangSmith Evaluators: https://docs.smith.langchain.com/evaluation/how_to_guides/custom_evaluator
- BLEU/ROUGE: https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation