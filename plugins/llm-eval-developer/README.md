# LLM Eval Developer

Plugin especializado para **desenvolver evaluations de LLMs e agentes**. Gera código de evaluators, scaffolding de evaluation suites, e ensina padrões de testing.

**FOCO**: Este plugin ajuda você a **CRIAR código de evaluation**, não a executar evaluations.

## 🎯 O Que Este Plugin Faz

✅ **Gera código de evaluators customizados** (OpenEvals, LangSmith, custom)
✅ **Cria scaffolding completo de evaluation suites**
✅ **Implementa métricas** (BLEU, ROUGE, LLM-as-judge, similarity)
✅ **Ensina padrões de testing** (pytest, mocks, CI/CD)
✅ **Documenta best practices** de evaluation

❌ **NÃO** executa evaluations (apenas gera código para executar)
❌ **NÃO** analisa resultados (apenas ensina como analisar)

## 📦 Instalação

```bash
/plugin marketplace add cadugevaerd/claudecode_plugins
/plugin install llm-eval-developer
```

## 🚀 Funcionalidades

### 1. Criar Evaluators Customizados

Gera código completo de evaluators para diferentes tipos de métricas.

**Tipos suportados**:
- **LLM-as-Judge**: Para critérios subjetivos (relevance, hallucination, coherence)
- **Similarity-based**: BLEU, ROUGE, cosine similarity
- **Rule-based**: Regex, exact match, custom logic
- **Composite**: Múltiplas métricas combinadas

**Frameworks suportados**:
- OpenEvals (langchain-ai/openevals)
- LangSmith Evaluation
- Custom implementations

### 2. Scaffolding de Evaluation Suites

Cria estrutura completa de projeto de evaluation, incluindo:
- Datasets anotados (golden datasets)
- Evaluators implementados
- Testes unitários e integration
- Scripts de execução
- Configuração de CI/CD

### 3. Documentação de Métricas

Lista e documenta métricas de evaluation disponíveis, com:
- Explicação de como funcionam
- Quando usar cada métrica
- Exemplos de código completos
- Trade-offs e limitações

### 4. Padrões de Desenvolvimento

Mostra padrões comuns de código para:
- Dataset creation (manual, synthetic, sampling)
- Testing evaluators (pytest, mocks)
- CI/CD integration (GitHub Actions)
- Regression detection
- A/B testing

## 📋 Comandos Disponíveis

### `/setup-project-eval`

**Configura CLAUDE.md do projeto** com padrões de LLM evaluation.

**O que faz**:
- ✅ Cria ou atualiza `CLAUDE.md` na raiz do projeto
- ✅ Adiciona padrões de evaluators (LLM-as-judge, similarity, rule-based)
- ✅ Configura frameworks detectados (OpenEvals, LangSmith, custom)
- ✅ Documenta estrutura de evaluation suites
- ✅ Orienta sobre dataset management (golden datasets, synthetic)
- ✅ Preserva conteúdo existente (não sobrescreve)
- ✅ Detecta stack de evaluation automaticamente

**Uso**:
```bash
# Setup básico (detecta stack automaticamente)
/setup-project-eval

# Ou com descrição do tipo de evaluation
/setup-project-eval "RAG system evaluation com LangSmith + OpenAI"
```

**Resultado**:
Claude ficará automaticamente orientado a:
- Desenvolver evaluators customizados
- Estruturar evaluation suites adequadamente
- Implementar métricas corretas (LLM-as-judge, similarity, rule-based)
- Gerenciar datasets de evaluation (golden datasets, synthetic)
- Testar evaluators com pytest
- Configurar CI/CD para regression testing

**Quando usar**:
- ✅ No início de projetos de evaluation de LLMs
- ✅ Ao adicionar este plugin em projetos existentes
- ✅ Quando quiser padronizar evaluations no time

---

### `/create-evaluator`

Gera código de evaluator customizado.

**Uso**:
```
/create-evaluator

Tipo: llm-as-judge
Framework: langsmith
Nome: hallucination_detector
Critério: Detectar alucinações comparando output com contexto
```

**Output**: Código Python completo do evaluator com:
- Imports necessários
- Implementação funcional
- Docstrings explicativas
- Testes unitários
- Exemplos de uso

**Exemplos**:

<details>
<summary>Exemplo 1: Hallucination Detector (LangSmith)</summary>

```python
from langsmith.evaluation import evaluator
from openai import OpenAI

@evaluator
def hallucination_detector(outputs: dict, inputs: dict) -> dict:
    """Detecta alucinações comparando output com contexto."""
    answer = outputs.get("answer", "")
    context = inputs.get("context", "")

    prompt = f"""
Verifique se a RESPOSTA contém APENAS informações do CONTEXTO.

CONTEXTO: {context}
RESPOSTA: {answer}

Retorne JSON: {{"is_factual": true/false, "score": 0.0-1.0, "reason": "..."}}
"""

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0
    )

    result = eval(response.choices[0].message.content)
    return {"score": result["score"], "comment": result["reason"]}


# Teste unitário
def test_hallucination_detector():
    result = hallucination_detector(
        outputs={"answer": "Paris is the capital."},
        inputs={"context": "Paris is France's capital."}
    )
    assert result["score"] >= 0.8
```

</details>

<details>
<summary>Exemplo 2: BLEU Score Evaluator (Custom)</summary>

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def bleu_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """Calcula BLEU score para translation/generation."""
    predicted = outputs.get("translation", "").split()
    reference = reference_outputs.get("translation", "").split()

    smoothing = SmoothingFunction().method1
    score = sentence_bleu([reference], predicted, smoothing_function=smoothing)

    return {"bleu_score": score}
```

</details>

<details>
<summary>Exemplo 3: Regex Validator (OpenEvals)</summary>

```python
import re
from openevals.types import EvaluatorResult, SimpleEvaluator

def create_email_validator() -> SimpleEvaluator:
    """Valida se output contém email válido."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def email_evaluator(outputs: dict) -> EvaluatorResult:
        output_text = outputs.get("output", "")
        match = re.search(email_pattern, output_text)

        return {
            "score": 1.0 if match else 0.0,
            "comment": f"Email: {match.group()}" if match else "No email found"
        }

    return email_evaluator
```

</details>

---

### `/create-eval-suite`

Gera scaffolding completo de evaluation suite.

**Uso**:
```
/create-eval-suite

Nome: rag-chatbot-eval
Tipo: chatbot com RAG
Métricas: accuracy, relevance, hallucination, response_time
Framework: langsmith
```

**Output**: Estrutura completa de diretórios e arquivos:

```
evaluations/
├── config/
│   └── eval_config.py           # Configuração e thresholds
├── datasets/
│   ├── golden_dataset.json      # Dataset anotado
│   └── dataset_generator.py     # Gerador sintético
├── evaluators/
│   ├── accuracy_evaluator.py
│   ├── relevance_evaluator.py
│   ├── hallucination_evaluator.py
│   └── response_time_evaluator.py
├── tests/
│   ├── test_evaluators.py       # Testes unitários
│   └── test_app_evaluation.py   # Integration tests
├── results/
│   └── .gitkeep
├── run_evaluation.py             # Script principal
└── README.md                     # Documentação
```

**Cada arquivo é gerado com código funcional completo!**

---

### `/eval-metrics`

Lista e documenta métricas de evaluation disponíveis.

**Uso**:
```
/eval-metrics

# Lista todas as métricas

# Ou filtrar por categoria:
/eval-metrics
Categoria: llm-judge
```

**Output**: Documentação completa de métricas com:

**Traditional Metrics**:
- **BLEU**: Translation, text generation
- **ROUGE**: Summarization (ROUGE-1, ROUGE-2, ROUGE-L)
- **Exact Match**: Q&A, classification
- **Regex Match**: Format validation

**Embedding-based**:
- **Cosine Similarity**: Semantic similarity

**LLM-as-Judge**:
- **Relevance**: Q&A relevance
- **Hallucination Detection**: Factual accuracy
- **Coherence**: Text coherence and flow
- **Fluency**: Language fluency

**Task-specific**:
- **Response Time**: Performance testing
- **Citation Accuracy**: RAG systems

Cada métrica inclui:
- ✅ Como funciona
- ✅ Quando usar
- ✅ Código de implementação
- ✅ Limitações e trade-offs

---

### `/eval-patterns`

Mostra padrões de código comuns para evaluation.

**Uso**:
```
/eval-patterns

# Lista todos os padrões

# Ou filtrar:
/eval-patterns
Tipo: testing
```

**Output**: Padrões de código para:

**Dataset Creation**:
- Golden dataset manual
- Synthetic data generation
- Production data sampling

**Testing Patterns**:
- Unit testing evaluators (pytest)
- Mocking LLM calls (pytest-mock)
- Integration testing (LangSmith pytest plugin)
- Parametrized tests

**CI/CD Patterns**:
- GitHub Actions evaluation
- Regression detection
- Threshold checking
- PR comments with results

**Advanced Patterns**:
- A/B testing evaluators
- Pairwise evaluation
- Composite evaluators

---

## 🤖 Agente Especializado

### `eval-developer`

Agente focado em **desenvolvimento de evaluations**.

**Invoke via Task tool**:
```
Task: Crie um evaluator para detectar toxicidade em chatbot responses usando LLM-as-judge. Framework: LangSmith.
```

**O agente irá**:
1. Gerar código completo do evaluator
2. Incluir testes unitários
3. Explicar trade-offs e quando usar
4. Mostrar como integrar em pipeline

**Exemplos de tarefas**:

<details>
<summary>Tarefa 1: Criar Evaluator de Relevância</summary>

```
Task: Implemente um evaluator de relevância para Q&A usando LLM-as-judge com OpenEvals.
```

**Agente gera**:
- Código do evaluator com prompt otimizado
- Testes unitários (casos positivos e negativos)
- Exemplo de integração
- Explicação de quando usar vs não usar

</details>

<details>
<summary>Tarefa 2: Implementar ROUGE Score</summary>

```
Task: Como implemento ROUGE score para avaliar meu summarizer? Sem usar frameworks externos.
```

**Agente gera**:
- Implementação custom de ROUGE
- Explicação de ROUGE-1, ROUGE-2, ROUGE-L
- Testes com diferentes casos
- Trade-offs e limitações

</details>

<details>
<summary>Tarefa 3: Suite Completa de Evaluation</summary>

```
Task: Crie evaluation suite completa para RAG system com métricas de hallucination, relevance e citation accuracy.
```

**Agente gera**:
- Estrutura completa de diretórios
- 3 evaluators implementados
- Dataset de exemplo
- Testes unitários e integration
- Script de execução
- README com documentação

</details>

---

## 🧠 Skill de Auto-Discovery

### `evaluation-developer`

Skill automaticamente invocada por Claude quando detectar necessidade de evaluation.

**Trigger terms**:
- "criar evaluator", "desenvolver evaluation"
- "como avaliar meu LLM", "métricas para"
- "hallucination detection", "BLEU", "ROUGE"
- "evaluation suite", "testar chatbot"

**O que a skill faz**:
- Identifica tipo de evaluation necessário
- Gera código de evaluator apropriado
- Inclui testes e documentação
- Explica trade-offs

**Exemplo de ativação**:

```
Você: "Preciso detectar alucinações no meu RAG system"

Claude (usando skill automaticamente):
Vou criar um hallucination detector usando LLM-as-judge...

[Gera código completo do evaluator]
```

---

## 💡 Exemplos de Uso do Plugin

### Exemplo 1: Criar Evaluator de Hallucination

```
/create-evaluator

Tipo: llm-as-judge
Framework: langsmith
Nome: hallucination_detector
Critério: Detectar alucinações comparando output com contexto fornecido
```

**Plugin gera código completo pronto para usar!**

---

### Exemplo 2: Suite para Chatbot

```
/create-eval-suite

Nome: chatbot-evaluation
Tipo: customer support chatbot
Métricas: relevance, tone, response_time, accuracy
Framework: langsmith
```

**Plugin cria**:
- 4 evaluators implementados
- Dataset com exemplos de conversas
- Testes unitários
- Script de execução
- GitHub Actions workflow

---

### Exemplo 3: Consultar Métricas

```
/eval-metrics

Categoria: llm-judge
```

**Plugin mostra**:
- Lista de métricas LLM-as-judge
- Como implementar cada uma
- Quando usar
- Código de exemplo

---

### Exemplo 4: Padrões de Testing

```
/eval-patterns

Tipo: testing
```

**Plugin mostra**:
- Como testar evaluators com pytest
- Patterns de mock (evitar custos de API)
- Integration testing
- Parametrized tests

---

## 📚 Casos de Uso

### Use Case 1: RAG System Evaluation

**Necessidade**: Avaliar se RAG retorna respostas factuais sem alucinações.

**Solução com plugin**:
```
1. /create-evaluator → hallucination_detector (LLM-as-judge)
2. /create-evaluator → relevance_evaluator (LLM-as-judge)
3. /create-evaluator → citation_accuracy (rule-based)
4. /create-eval-suite → rag-eval-suite
```

**Resultado**: Suite completa de evaluation para RAG com 3 métricas.

---

### Use Case 2: Summarization System

**Necessidade**: Avaliar qualidade de summaries gerados.

**Solução com plugin**:
```
1. /create-evaluator → rouge_evaluator (similarity)
2. /create-evaluator → coherence_evaluator (LLM-as-judge)
3. /create-evaluator → conciseness_evaluator (rule-based)
```

**Resultado**: 3 evaluators complementares para avaliar summaries.

---

### Use Case 3: Chatbot Testing

**Necessidade**: Testar chatbot em production antes de deploy.

**Solução com plugin**:
```
1. /create-eval-suite → chatbot-eval
2. /eval-patterns → ci-cd
```

**Resultado**: Suite com CI/CD integration, executa testes automaticamente em PRs.

---

## 🎓 Melhores Práticas

### 1. Sempre Teste Evaluators

**Use testes unitários** antes de usar evaluators em production:

```python
def test_evaluator_positive_case():
    result = evaluator(outputs={"good": "answer"})
    assert result["score"] >= 0.8

def test_evaluator_negative_case():
    result = evaluator(outputs={"bad": "answer"})
    assert result["score"] <= 0.3
```

### 2. Combine Múltiplas Métricas

**Não confie em uma única métrica**. Combine:
- LLM-as-judge (qualidade subjetiva)
- Similarity metrics (comparação com ground truth)
- Rule-based (validações exatas)

### 3. Mock LLM Calls em Testes

**Evite custos** de API em testes usando mocks:

```python
def test_with_mock(mocker):
    mocker.patch("openai.OpenAI.chat.completions.create", return_value=mock_response)
    result = evaluator(outputs={"test": "data"})
    assert result["score"] == expected
```

### 4. Version Your Datasets

**Track mudanças** em datasets para detectar drift:
```
datasets/
├── v1.0/
│   └── golden_dataset.json
├── v1.1/
│   └── golden_dataset.json
└── current/
    └── golden_dataset.json
```

### 5. Automate in CI/CD

**Execute evaluations automaticamente** em PRs:
```yaml
# .github/workflows/evaluation.yml
- name: Run Evaluations
  run: pytest tests/evaluations/ --langsmith
```

---

## 🔧 Integração com Frameworks

### OpenEvals

```python
from openevals.llm import create_llm_as_judge

evaluator = create_llm_as_judge(
    prompt=YOUR_PROMPT,
    model="openai:gpt-4o-mini",
)
```

### LangSmith

```python
from langsmith import evaluate
from langsmith.evaluation import evaluator

@evaluator
def custom_evaluator(outputs: dict) -> dict:
    return {"score": score}

results = evaluate(
    your_app,
    data="dataset-name",
    evaluators=[custom_evaluator]
)
```

### Pytest Integration

```python
@pytest.mark.langsmith
def test_evaluation():
    results = evaluate(app, data=dataset)
    assert results["metric"]["mean"] >= threshold
```

---

## 📖 Referências

### Documentação
- [OpenEvals GitHub](https://github.com/langchain-ai/openevals)
- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation)
- [LLM Evaluation Metrics](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation)
- [LLM-as-a-Judge Guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)

### Papers
- BLEU: [Papineni et al., 2002](https://aclanthology.org/P02-1040/)
- ROUGE: [Lin, 2004](https://aclanthology.org/W04-1013/)
- G-Eval: [Liu et al., 2023](https://arxiv.org/abs/2303.16634)

---

## 🤝 Contribuindo

Este plugin faz parte do [claudecode_plugins marketplace](https://github.com/cadugevaerd/claudecode_plugins).

## 👤 Autor

**Carlos Araujo**
- Email: cadu.gevaerd@gmail.com
- GitHub: [@cadugevaerd](https://github.com/cadugevaerd)

## 📄 Licença

MIT

---

**Desenvolvido para ajudar você a CRIAR evaluations de qualidade para seus LLMs! 🚀**