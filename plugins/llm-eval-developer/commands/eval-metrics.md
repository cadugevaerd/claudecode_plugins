---
description: Lista e documenta métricas de evaluation disponíveis com exemplos de implementação
---

# Métricas de Evaluation

Lista completa de métricas de evaluation para LLMs, com explicações, quando usar, e exemplos de código.

## Como usar

Execute o comando e opcionalmente especifique:
- Categoria de métrica (traditional, llm-judge, similarity, task-specific)
- Framework preferido (openevals, langsmith, custom)
- Tipo de aplicação (chatbot, summarization, translation, etc.)

## Categorias de Métricas

### 1. Traditional Metrics (Rule-based)

Métricas baseadas em regras e comparações exatas.

#### BLEU (Bilingual Evaluation Understudy)

**Quando usar**: Machine translation, text generation

**Como funciona**: Calcula precisão de n-gramas entre output e referência, com penalidade de brevidade.

**Range**: 0.0 - 1.0 (maior = melhor)

**Código**:
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def bleu_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    predicted = outputs.get("translation", "").split()
    reference = reference_outputs.get("translation", "").split()

    smoothing = SmoothingFunction().method1
    score = sentence_bleu([reference], predicted, smoothing_function=smoothing)

    return {"bleu_score": score}
```

**Limitações**:
- Não captura nuances semânticas
- Favorece matches exatos de palavras
- Pode ser enganado por repetições

---

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

**Quando usar**: Text summarization, content generation

**Como funciona**: Calcula recall de n-gramas entre summary gerado e referência.

**Variantes**:
- ROUGE-1: Unigram overlap
- ROUGE-2: Bigram overlap
- ROUGE-L: Longest common subsequence

**Range**: 0.0 - 1.0 (maior = melhor)

**Código**:
```python
from rouge import Rouge

def rouge_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    generated = outputs.get("summary", "")
    reference = reference_outputs.get("summary", "")

    rouge = Rouge()
    scores = rouge.get_scores(generated, reference)[0]

    return {
        "rouge_1_f1": scores["rouge-1"]["f"],
        "rouge_2_f1": scores["rouge-2"]["f"],
        "rouge_l_f1": scores["rouge-l"]["f"],
    }
```

**Limitações**:
- Foca em overlap superficial
- Ignora paráfrase e sinônimos
- Não considera coerência

---

#### Exact Match

**Quando usar**: Q&A, classification, structured outputs

**Como funciona**: Compara se output é exatamente igual à referência.

**Range**: 0 ou 1 (binário)

**Código**:
```python
def exact_match_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    output = outputs.get("answer", "").strip().lower()
    reference = reference_outputs.get("answer", "").strip().lower()

    score = 1.0 if output == reference else 0.0

    return {
        "exact_match": score,
        "comment": "Match" if score == 1.0 else f"Expected: {reference}, Got: {output}"
    }
```

---

#### Regex Match

**Quando usar**: Format validation, pattern detection, structured outputs

**Como funciona**: Valida se output corresponde a padrão regex.

**Range**: 0 ou 1 (binário)

**Código (OpenEvals)**:
```python
import re
from openevals.types import EvaluatorResult, SimpleEvaluator

def create_regex_evaluator(pattern: str) -> SimpleEvaluator:
    """
    Cria evaluator que valida output contra regex pattern.

    Args:
        pattern: Regex pattern (ex: r"^\d{3}-\d{3}-\d{4}$" para telefone)
    """
    def evaluator(outputs: dict) -> EvaluatorResult:
        output = outputs.get("output", "")
        match = re.search(pattern, output)

        return {
            "score": 1.0 if match else 0.0,
            "comment": f"Pattern match: {bool(match)}"
        }

    return evaluator

# Uso
phone_validator = create_regex_evaluator(r"^\d{3}-\d{3}-\d{4}$")
email_validator = create_regex_evaluator(r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

---

### 2. Embedding-based Similarity

Métricas baseadas em similaridade semântica usando embeddings.

#### Cosine Similarity

**Quando usar**: Semantic similarity, paraphrase detection, retrieval evaluation

**Como funciona**: Calcula similaridade de cosseno entre embeddings de output e referência.

**Range**: -1.0 a 1.0 (maior = mais similar)

**Código**:
```python
from openai import OpenAI
import numpy as np

def cosine_similarity_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """Calcula similaridade semântica usando embeddings."""

    client = OpenAI()

    output_text = outputs.get("answer", "")
    reference_text = reference_outputs.get("answer", "")

    # Gerar embeddings
    output_emb = client.embeddings.create(
        input=output_text,
        model="text-embedding-3-small"
    ).data[0].embedding

    reference_emb = client.embeddings.create(
        input=reference_text,
        model="text-embedding-3-small"
    ).data[0].embedding

    # Calcular similaridade
    similarity = np.dot(output_emb, reference_emb) / (
        np.linalg.norm(output_emb) * np.linalg.norm(reference_emb)
    )

    return {
        "cosine_similarity": float(similarity),
        "comment": f"Similarity: {similarity:.3f}"
    }
```

---

### 3. LLM-as-Judge Metrics

Métricas que usam LLMs para avaliar outputs.

#### Relevance (LLM-as-Judge)

**Quando usar**: Q&A, chatbots, information retrieval

**Como funciona**: LLM avalia se resposta é relevante para pergunta.

**Range**: 0.0 - 1.0 (maior = mais relevante)

**Código (OpenEvals)**:
```python
from openevals.llm import create_llm_as_judge

RELEVANCE_PROMPT = """
Avalie a relevância da resposta para a pergunta.

PERGUNTA:
{inputs}

RESPOSTA:
{outputs}

Dê uma nota de 0-10 onde:
- 0: Completamente irrelevante
- 5: Parcialmente relevante
- 10: Perfeitamente relevante

Retorne APENAS o número.
"""

relevance_evaluator = create_llm_as_judge(
    prompt=RELEVANCE_PROMPT,
    model="openai:gpt-4o-mini",
)
```

---

#### Hallucination Detection (LLM-as-Judge)

**Quando usar**: RAG systems, fact-based Q&A, summarization

**Como funciona**: LLM verifica se output contém informações não suportadas pelo contexto.

**Range**: 0.0 - 1.0 (0 = alucinado, 1 = factual)

**Código (LangSmith)**:
```python
from langsmith.evaluation import evaluator
from openai import OpenAI

@evaluator
def hallucination_evaluator(outputs: dict, inputs: dict) -> dict:
    """Detecta alucinações comparando output com contexto."""

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
  "hallucination_score": 0.0-1.0,
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
        "score": result["hallucination_score"],
        "comment": result["reason"]
    }
```

---

#### Coherence (LLM-as-Judge)

**Quando usar**: Long-form generation, summarization, storytelling

**Como funciona**: LLM avalia coerência lógica e flow do texto.

**Range**: 0.0 - 1.0 (maior = mais coerente)

**Código**:
```python
from openevals.llm import create_llm_as_judge

COHERENCE_PROMPT = """
Avalie a coerência e flow lógico do texto.

TEXTO:
{outputs}

Critérios:
- Ideias se conectam logicamente?
- Transições fazem sentido?
- Não há contradições?

Dê nota 0-10. Retorne APENAS o número.
"""

coherence_evaluator = create_llm_as_judge(
    prompt=COHERENCE_PROMPT,
    model="openai:gpt-4o-mini",
)
```

---

### 4. Task-Specific Metrics

Métricas específicas para tarefas particulares.

#### Response Time

**Quando usar**: Production systems, performance testing

**Como funciona**: Mede tempo de resposta da aplicação.

**Range**: 0+ segundos (menor = melhor)

**Código**:
```python
import time

def response_time_evaluator(outputs: dict, metadata: dict) -> dict:
    """
    Avalia tempo de resposta.

    Metadata deve conter "start_time" e "end_time" em timestamp.
    """
    start = metadata.get("start_time", 0)
    end = metadata.get("end_time", 0)

    response_time = end - start

    # Threshold: 2 segundos
    threshold = 2.0
    score = 1.0 if response_time <= threshold else threshold / response_time

    return {
        "response_time_seconds": response_time,
        "score": score,
        "comment": f"Tempo: {response_time:.2f}s (threshold: {threshold}s)"
    }
```

---

#### Citation Accuracy

**Quando usar**: RAG systems, research assistants

**Como funciona**: Verifica se resposta cita corretamente as fontes.

**Range**: 0.0 - 1.0 (maior = melhor)

**Código**:
```python
def citation_accuracy_evaluator(outputs: dict, inputs: dict) -> dict:
    """
    Verifica se citações são precisas e completas.

    Inputs deve conter "sources" (list de IDs de documentos).
    Outputs deve conter "answer" com citações [1], [2], etc.
    """
    import re

    answer = outputs.get("answer", "")
    expected_sources = set(inputs.get("sources", []))

    # Extrair citações do answer
    citations = re.findall(r'\[(\d+)\]', answer)
    cited_sources = set(map(int, citations))

    # Calcular precisão e recall
    if not expected_sources:
        return {"citation_accuracy": 1.0, "comment": "Nenhuma fonte esperada"}

    precision = len(cited_sources & expected_sources) / len(cited_sources) if cited_sources else 0
    recall = len(cited_sources & expected_sources) / len(expected_sources)

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "citation_precision": precision,
        "citation_recall": recall,
        "citation_f1": f1,
        "comment": f"Citou {len(cited_sources)} de {len(expected_sources)} fontes"
    }
```

---

## Tabela de Decisão de Métricas

| Use Case | Métricas Recomendadas |
|----------|----------------------|
| **Q&A Factual** | Exact Match, Cosine Similarity, Hallucination Detection |
| **Summarization** | ROUGE, BLEU, Coherence, Conciseness |
| **Translation** | BLEU, Cosine Similarity, Fluency |
| **RAG Systems** | Relevance, Hallucination Detection, Citation Accuracy |
| **Chatbot** | Relevance, Coherence, Response Time, Tone |
| **Classification** | Exact Match, F1 Score, Confusion Matrix |
| **Code Generation** | Exact Match (output), Pass@K (tests), Syntax Validity |

## Combining Multiple Metrics

**Exemplo de Composite Evaluator**:
```python
def composite_evaluator(outputs: dict, inputs: dict, reference_outputs: dict) -> dict:
    """
    Combina múltiplas métricas em score final.
    """
    # Executar evaluators individuais
    relevance = relevance_evaluator(outputs, inputs)
    hallucination = hallucination_evaluator(outputs, inputs)
    similarity = cosine_similarity_evaluator(outputs, reference_outputs)

    # Pesos para cada métrica
    weights = {
        "relevance": 0.4,
        "hallucination": 0.4,
        "similarity": 0.2
    }

    # Calcular score ponderado
    final_score = (
        relevance["score"] * weights["relevance"] +
        hallucination["score"] * weights["hallucination"] +
        similarity["cosine_similarity"] * weights["similarity"]
    )

    return {
        "composite_score": final_score,
        "relevance": relevance["score"],
        "hallucination": hallucination["score"],
        "similarity": similarity["cosine_similarity"]
    }
```

## Referências

- BLEU/ROUGE: https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation
- LLM-as-Judge: https://www.evidentlyai.com/llm-guide/llm-as-a-judge
- OpenEvals Metrics: https://github.com/langchain-ai/openevals