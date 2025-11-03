---
description: Configura CLAUDE.md do projeto com padrões de LLM evaluation, frameworks, métricas e estrutura de evaluators
---

# Setup Project for LLM Evaluation

Este comando configura o arquivo `CLAUDE.md` do projeto atual com instruções sobre desenvolvimento de evaluations de LLMs, frameworks, métricas e padrões de testing.

## 🎯 Objetivo

Adicionar ao `CLAUDE.md` do projeto instruções claras para que Claude:

- Desenvolva evaluators customizados (OpenEvals, LangSmith, custom)
- Estruture evaluation suites adequadamente
- Implemente métricas corretas (LLM-as-judge, similarity, rule-based)
- Gerencie datasets de evaluation (golden datasets, synthetic)
- Teste evaluators corretamente
- Configure CI/CD para regression testing

## 📋 Como usar

````bash
/setup-project-eval

```text

Ou com descrição do tipo de evaluation:

```bash
/setup-project-eval "RAG system evaluation com LangSmith + OpenAI"

```text

## 🔍 Processo de Execução

### 1. Detectar ou Criar CLAUDE.md

**Se CLAUDE.md existe**:
- Ler arquivo atual
- Adicionar seção "LLM Evaluation Standards" ao final
- Preservar conteúdo existente

**Se CLAUDE.md NÃO existe**:
- Criar arquivo na raiz do projeto
- Adicionar template completo de padrões de evaluation

### 2. Adicionar Instruções de LLM Evaluation

O comando deve adicionar a seguinte seção ao `CLAUDE.md`:

```markdown

# LLM Evaluation Standards

**IMPORTANTE**: Este projeto utiliza o plugin `llm-eval-developer` para desenvolvimento de evaluations de LLMs com padrões consistentes e frameworks profissionais.

## 📋 Padrões de Evaluation

### ✅ Frameworks de Evaluation

**Framework Principal**: [OpenEvals/LangSmith/Custom - detectado automaticamente]

**Bibliotecas de Evaluation**:
- Evaluation framework: OpenEvals, LangSmith
- Métricas: BLEU, ROUGE, BERTScore
- LLM-as-judge: OpenAI, Anthropic, local models
- Dataset management: datasets, pandas
- Testing: pytest, pytest-mock

### 📁 Estrutura de Diretórios

```text

projeto/
├── src/                        # Código do sistema (LLM app, RAG, etc.)
│   ├── __init__.py
│   ├── chains/
│   ├── agents/
│   └── tools/
├── evaluations/                # Evaluations
│   ├── __init__.py
│   ├── evaluators/            # Evaluators customizados
│   │   ├── __init__.py
│   │   ├── hallucination_detector.py
│   │   ├── relevance_evaluator.py
│   │   └── custom_metric.py
│   ├── datasets/              # Golden datasets
│   │   ├── qa_golden.json
│   │   ├── rag_examples.json
│   │   └── edge_cases.json
│   ├── suites/                # Evaluation suites
│   │   ├── rag_eval_suite.py
│   │   └── agent_eval_suite.py
│   └── tests/                 # Testes dos evaluators
│       ├── test_evaluators.py
│       └── conftest.py
├── scripts/                   # Scripts de execução
│   ├── run_eval.py
│   └── generate_report.py
└── .github/workflows/         # CI/CD
    └── eval_regression.yml

```text

### 🎯 Tipos de Evaluators

#### 1. LLM-as-Judge

**Quando usar**: Critérios subjetivos (relevance, hallucination, coherence, helpfulness)

```python
from langsmith.evaluation import evaluator
from openai import OpenAI

@evaluator
def hallucination_detector(run, example):
    """
    Detecta alucinações comparando output com contexto fornecido.

    Args:
        run: Execução do sistema (contém output)
        example: Exemplo de teste (contém contexto esperado)

    Returns:
        dict: Score (0-1) e raciocínio
    """
    client = OpenAI()

    prompt = f"""
    Compare o output gerado com o contexto fornecido.
    Identifique se há informações alucinadas (não presentes no contexto).

    Contexto: {example.inputs['context']}
    Output: {run.outputs['answer']}

    Retorne JSON:
    {{
        "score": 0.0-1.0,  // 1.0 = sem alucinação, 0.0 = muita alucinação
        "reasoning": "explicação"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    return {
        "key": "hallucination",
        "score": result["score"],
        "comment": result["reasoning"]
    }

```text

#### 2. Similarity-Based

**Quando usar**: Comparação com output esperado (exact match, semantic similarity)

```python
from langsmith.evaluation import evaluator
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

@evaluator
def semantic_similarity(run, example):
    """
    Calcula similaridade semântica entre output e resposta esperada.

    Returns:
        dict: Cosine similarity score (0-1)
    """
    expected = example.outputs['answer']
    actual = run.outputs['answer']

    # Calcular embeddings
    emb_expected = model.encode(expected)
    emb_actual = model.encode(actual)

    # Cosine similarity
    similarity = np.dot(emb_expected, emb_actual) / (
        np.linalg.norm(emb_expected) * np.linalg.norm(emb_actual)
    )

    return {
        "key": "semantic_similarity",
        "score": float(similarity)
    }

```text

#### 3. Rule-Based

**Quando usar**: Validações objetivas (formato, length, keywords, regex)

```python
from langsmith.evaluation import evaluator

@evaluator
def answer_format_validator(run, example):
    """
    Valida se a resposta segue formato esperado.

    Validações:
    - Tem pelo menos 50 caracteres
    - Não contém placeholders
    - Termina com pontuação
    """
    answer = run.outputs['answer']

    validations = {
        "min_length": len(answer) >= 50,
        "no_placeholders": "[TODO]" not in answer and "..." not in answer,
        "proper_punctuation": answer.strip()[-1] in ".!?"
    }

    score = sum(validations.values()) / len(validations)

    return {
        "key": "format_validation",
        "score": score,
        "comment": f"Validations: {validations}"
    }

```text

### 📊 Dataset Management

#### Golden Datasets

**Estrutura recomendada** (JSON):

```json
{
  "examples": [
    {
      "id": "example_001",
      "inputs": {
        "question": "What is the capital of France?",
        "context": "France is a country in Europe. Its capital city is Paris."
      },
      "outputs": {
        "answer": "Paris",
        "confidence": 1.0
      },
      "metadata": {
        "category": "geography",
        "difficulty": "easy",
        "created_at": "2025-01-20"
      }
    }
  ]
}

```text

#### Synthetic Dataset Generation

```python
from openai import OpenAI

def generate_synthetic_examples(topic: str, count: int):
    """
    Gera exemplos sintéticos para evaluation.

    Args:
        topic: Tópico dos exemplos
        count: Quantidade de exemplos

    Returns:
        list: Exemplos gerados
    """
    client = OpenAI()
    examples = []

    for i in range(count):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Generate a question-answer pair about {topic}. Return JSON."
            }]
        )

        example = json.loads(response.choices[0].message.content)
        examples.append({
            "id": f"synthetic_{i:03d}",
            "inputs": {"question": example["question"]},
            "outputs": {"answer": example["answer"]},
            "metadata": {"source": "synthetic", "topic": topic}
        })

    return examples

```text

### 🧪 Testing Evaluators

**Sempre testar evaluators com pytest**:

```python
import pytest
from evaluations.evaluators.hallucination_detector import hallucination_detector

def test_hallucination_detector_no_hallucination(mocker):
    """Deve retornar score alto para resposta sem alucinação"""
    # Arrange
    mock_openai = mocker.patch('openai.OpenAI')
    mock_openai.return_value.chat.completions.create.return_value.choices = [
        mocker.MagicMock(
            message=mocker.MagicMock(
                content='{"score": 1.0, "reasoning": "No hallucination detected"}'
            )
        )
    ]

    run = mocker.MagicMock(outputs={"answer": "Paris is the capital of France"})
    example = mocker.MagicMock(
        inputs={"context": "France's capital is Paris"},
        outputs={"answer": "Paris"}
    )

    # Act
    result = hallucination_detector(run, example)

    # Assert
    assert result["score"] == 1.0
    assert "hallucination" in result["key"]

def test_hallucination_detector_with_hallucination(mocker):
    """Deve retornar score baixo para resposta alucinada"""
    # Similar ao anterior, mas com score baixo
    pass

```text

### 🔄 CI/CD para Regression Testing

**GitHub Actions** (.github/workflows/eval_regression.yml):

```yaml
name: Evaluation Regression Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  eval-regression:
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

      - name: Run evaluation suite
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/run_eval.py --suite rag_eval_suite

      - name: Check regression
        run: |
          python scripts/check_regression.py --baseline baseline_scores.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: eval-results
          path: eval_results.json

```text

### 📈 Métricas Recomendadas por Tipo de Sistema

#### RAG Systems
- ✅ **Hallucination Detection**: LLM-as-judge
- ✅ **Relevance**: LLM-as-judge ou semantic similarity
- ✅ **Faithfulness**: Verifica se output está no contexto
- ✅ **Context Precision**: Ranking de documentos recuperados
- ✅ **Answer Correctness**: Exact match ou similarity com golden answer

#### Conversational Agents
- ✅ **Coherence**: LLM-as-judge
- ✅ **Helpfulness**: LLM-as-judge
- ✅ **Safety**: Rule-based (detectar conteúdo impróprio)
- ✅ **Tool Usage**: Validar se tools corretos foram chamados
- ✅ **Multi-turn Consistency**: Verificar contexto entre turnos

#### Summarization
- ✅ **ROUGE**: N-gram overlap com summary esperado
- ✅ **Factuality**: LLM-as-judge comparando com fonte
- ✅ **Conciseness**: Length ratio
- ✅ **Coverage**: Verifica se pontos principais estão presentes

#### Code Generation
- ✅ **Syntax Validation**: AST parsing
- ✅ **Test Pass Rate**: Executar testes gerados
- ✅ **Code Similarity**: Diff com código esperado
- ✅ **Security**: Detectar vulnerabilidades

## 🎯 Plugin LLM Eval Developer

Este projeto usa o plugin `llm-eval-developer` com os seguintes recursos:

**Comandos**:
- `/create-evaluator` - Gerar código de evaluator customizado
- `/create-eval-suite` - Scaffold completo de evaluation suite
- `/eval-metrics` - Documentar métricas disponíveis
- `/eval-patterns` - Mostrar padrões de desenvolvimento

**Agente**:
- `eval-developer` - Especialista em criar código de evaluators

**Skill**:
- `evaluation-developer` - Auto-invocada para scaffolding de evaluations

**Frameworks Suportados**:
- OpenEvals (langchain-ai/openevals)
- LangSmith Evaluation
- Custom implementations

**Métricas**:
- LLM-as-judge (GPT-4, Claude, local models)
- Similarity-based (BLEU, ROUGE, BERTScore, cosine)
- Rule-based (regex, format, length, keywords)
- Composite (múltiplas métricas combinadas)


**Filosofia**: Measure > Guess | Automate > Manual | Regression Tests > Hope

```text

### 3. Adicionar Contexto do Projeto (Se Fornecido)

Se o usuário fornecer descrição do tipo de evaluation, adicionar seção customizada:

```markdown

## 📊 Contexto Deste Projeto

**Tipo de Sistema**: [RAG/Agent/Summarization/Code Gen]
**Framework de Evaluation**: [OpenEvals/LangSmith/Custom]

**Evaluators Recomendados**:
- [Hallucination detector para RAG]
- [Relevance evaluator para retrieval]
- [Safety checker para conversational]

**Métricas Principais**:
- [Métricas específicas do tipo de sistema]

**Datasets Necessários**:
- Golden examples: [quantidade recomendada]
- Edge cases: [exemplos específicos]
- Regression test cases: [baseline]

```text

### 4. Detectar Stack de Evaluation do Projeto

Analisar projeto para customizar instruções:

- Verificar `requirements.txt`, `pyproject.toml` para frameworks
- Detectar se usa OpenEvals, LangSmith, ou custom
- Identificar modelos LLM em uso (OpenAI, Anthropic, local)
- Localizar datasets existentes (JSON, CSV)
- Verificar se há evaluators implementados

**Adicionar ao CLAUDE.md**:

```markdown

## 🔧 Stack de Evaluation Detectada

**Framework**: [OpenEvals/LangSmith/Custom]
**LLM Provider**: [OpenAI/Anthropic/Local]
**Dataset Format**: [JSON/CSV/HuggingFace]
**Testing**: [pytest/unittest]

**Evaluators Existentes**:
- [listar evaluators encontrados]

**Datasets Existentes**:
- [listar datasets encontrados]

```text

### 5. Confirmar com Usuário

Mostrar preview do que será adicionado:

```text

═══════════════════════════════════════════
📝 SETUP LLM EVALUATION
═══════════════════════════════════════════

Arquivo: CLAUDE.md

Ação: [CRIAR NOVO / ADICIONAR SEÇÃO]

Stack de Evaluation Detectada:
- Framework: [OpenEvals/LangSmith]
- LLM Provider: [OpenAI/Anthropic]
- Tipo de Sistema: [RAG/Agent/Summarization]

Evaluators Existentes:
- [X] evaluators detectados

Datasets Existentes:
- [Y] golden datasets encontrados

Conteúdo a ser adicionado:

[Preview das instruções]

Adicionar ao CLAUDE.md? (s/n)

```text

### 6. Criar/Atualizar Arquivo

Se usuário confirmar:
- Criar ou atualizar CLAUDE.md
- Adicionar instruções completas
- Preservar conteúdo existente (NUNCA sobrescrever)
- Validar que arquivo foi criado corretamente

```text

✅ CLAUDE.md configurado com sucesso!

Instruções de LLM evaluation adicionadas.

Stack de Evaluation detectada:
- Framework: LangSmith
- LLM Provider: OpenAI
- Tipo de Sistema: RAG

Evaluators existentes:
- 3 evaluators encontrados

Datasets existentes:
- 2 golden datasets

Próximos passos:
1. Revisar CLAUDE.md
2. Customizar evaluators (se necessário)
3. Executar: /create-evaluator
4. Criar eval suite: /create-eval-suite
5. Testar evaluators: pytest evaluations/tests/

Claude agora está orientado a:
✓ Desenvolver evaluators customizados
✓ Estruturar evaluation suites adequadamente
✓ Implementar métricas corretas
✓ Gerenciar datasets de evaluation
✓ Testar evaluators com pytest
✓ Configurar CI/CD para regression testing

```text

## 📚 Exemplos de Uso

### Exemplo 1: Novo Projeto RAG

```bash
/setup-project-eval "RAG system com LangSmith + OpenAI"

```text

**Resultado**:
- Cria `CLAUDE.md` na raiz do projeto
- Adiciona padrões LangSmith + OpenAI
- Configura evaluators para RAG (hallucination, relevance, faithfulness)
- Define estrutura de golden datasets
- Orienta sobre LLM-as-judge

### Exemplo 2: Projeto Conversational Agent

```bash
/setup-project-eval "Conversational agent com OpenEvals"

```text

**Resultado**:
- Detecta `CLAUDE.md` existente
- Adiciona seção de evaluation ao final
- Preserva conteúdo existente
- Inclui evaluators de coherence, helpfulness, safety
- Configura multi-turn consistency testing

### Exemplo 3: Projeto Code Generation

```bash
/setup-project-eval "Code generation LLM"

```text

**Resultado**:
- Adiciona evaluators de syntax validation
- Configura test execution evaluation
- Orienta sobre security scanning
- Define métricas de code similarity

## ⚠️ Importante

### Não Sobrescrever Conteúdo Existente

Se `CLAUDE.md` já existe:
- ❌ NUNCA sobrescrever conteúdo
- ✅ SEMPRE adicionar ao final
- ✅ Usar separador claro: `---`

### Detectar Framework de Evaluation

Analisar projeto para customizar instruções:
- Verificar se usa OpenEvals, LangSmith, ou custom
- Detectar modelos LLM (OpenAI, Anthropic, local)
- Identificar tipo de sistema (RAG, agent, summarization)
- Localizar datasets e evaluators existentes

### Validar Sintaxe Markdown

Após criar/atualizar:
- Verificar que markdown está válido
- Headers bem formatados
- Code blocks Python com syntax highlighting
- Links funcionando

## 🚀 Após Executar Este Comando

O usuário terá:

1. ✅ `CLAUDE.md` configurado com padrões de LLM evaluation
2. ✅ Claude orientado a desenvolver evaluators customizados
3. ✅ Estrutura de evaluation suite definida
4. ✅ Métricas recomendadas documentadas
5. ✅ Padrões de testing de evaluators

**Próximo passo**: Executar `/create-evaluator` para criar primeiro evaluator!

## 💡 Dica

Após configurar o projeto, sempre teste evaluators antes de usar em production:

```bash

# Criar evaluator customizado
/create-evaluator

# Testar evaluator
pytest evaluations/tests/

# Criar evaluation suite completa
/create-eval-suite

# Executar evaluation
python scripts/run_eval.py

```text

Isso garantirá que evaluations são confiáveis e detectam regressões corretamente.
````
