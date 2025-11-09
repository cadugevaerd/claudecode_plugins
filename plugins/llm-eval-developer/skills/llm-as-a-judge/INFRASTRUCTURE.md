# LangSmith Infrastructure for LLM-as-Judge

Documentação técnica completa da infraestrutura LangSmith necessária para executar avaliações offline usando LLM-as-Judge.

## 📦 Componentes Fundamentais

Qualquer avaliação offline no LangSmith, incluindo LLM-as-Judge, requer **três componentes fundamentais**:

1. **Dataset** - Coleção versionada de Examples
2. **Target Function** - Aplicação sob teste
3. **Evaluator(s)** - Funções de scoring (incluindo LLM-as-Judge)

```
┌─────────────────────────────────────────────────┐
│          LangSmith Evaluation Pipeline          │
├─────────────────────────────────────────────────┤
│                                                 │
│  Dataset (Examples)                             │
│  ├── Example 1: {inputs, outputs}               │
│  ├── Example 2: {inputs, outputs}               │
│  └── Example N: {inputs, outputs}               │
│           ↓                                     │
│  Target Function (Your App)                     │
│  ├── Receives: inputs                           │
│  └── Returns: predictions                       │
│           ↓                                     │
│  Evaluators (LLM-as-Judge + others)             │
│  ├── Receives: inputs + outputs + predictions   │
│  └── Returns: scores + comments                 │
│           ↓                                     │
│  Experiment Results (LangSmith UI)              │
│  └── Heatmap, Traces, Metrics                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 1. Datasets - Coleção Versionada de Examples

### 1.1 O Que é um Dataset LangSmith

**Definição**: Dataset é uma coleção estável e versionada de **Examples** usada para avaliar aplicações de forma reproduzível.

**Características:**
- ✅ Versionamento automático (imutabilidade)
- ✅ Armazenado no LangSmith (cloud)
- ✅ Compartilhável entre equipe
- ✅ Rastreável via UI

### 1.2 Estrutura de um Example

Cada Example contém **dois componentes principais**:

```python
{
    "inputs": {
        # Dicionário passado para Target Function
        "pergunta": "O que é LangChain?",
        "contexto": "Framework Python para LLMs"
    },
    "outputs": {
        # Reference outputs (ground truth) - OPCIONAL mas CRÍTICO para LLM-as-Judge
        "resposta_esperada": "LangChain é um framework Python...",
        "metadata": {"categoria": "definição"}
    }
}
```

**Campos:**

| Campo | Tipo | Obrigatório | Uso LLM-as-Judge |
|-------|------|-------------|------------------|
| `inputs` | dict | ✅ Sim | Passado para target function E prompt juiz |
| `outputs` | dict | ❌ Não | **✅ CRÍTICO** - Ground truth para comparação |

### 1.3 Reference Outputs (Ground Truth)

**⚠️ CRÍTICO para LLM-as-Judge**: Reference outputs são a **resposta correta esperada** que o modelo juiz usa para avaliar a prediction.

**Sem reference outputs:**
- ❌ Judge não tem baseline para comparação
- ❌ Avaliação de correção impossível
- ❌ Apenas critérios sem ground truth (ex: concisão) funcionam

**Com reference outputs:**
- ✅ Judge compara prediction vs reference
- ✅ Avaliação factual precisa
- ✅ Critérios como CORRECTNESS funcionam

**Exemplo comparativo:**

```python
# ❌ SEM reference - Judge não sabe se está correto
{
    "inputs": {"pergunta": "Capital da França?"},
    "outputs": {}  # Vazio!
}

# ✅ COM reference - Judge pode avaliar correção
{
    "inputs": {"pergunta": "Capital da França?"},
    "outputs": {"resposta_esperada": "Paris"}
}
```

### 1.4 Versionamento de Datasets

**Por que versionar?**
- ✅ Reprodutibilidade: mesma versão = mesmos resultados
- ✅ Rastreabilidade: qual dataset gerou qual experiment
- ✅ Evolução: adicionar examples sem quebrar histórico

**Como funciona:**
- Cada modificação cria nova versão
- Experiments referenciam versão específica
- UI mostra histórico de versões

**Exemplo:**
```python
# Versão 1: 50 examples
dataset_v1 = client.create_dataset("qa-eval", examples=[...])

# Versão 2: 50 + 20 novos examples (automático)
client.create_examples(dataset_id=dataset_v1.id, examples=[...])
```

### 1.5 Criando Datasets via SDK

#### Opção 1: Criar dataset + examples juntos

```python
from langsmith import Client

client = Client()

examples = [
    {
        "inputs": {"pergunta": "O que é Python?"},
        "outputs": {"resposta_esperada": "Python é uma linguagem..."}
    },
    {
        "inputs": {"pergunta": "O que é TypeScript?"},
        "outputs": {"resposta_esperada": "TypeScript é um superset..."}
    }
]

dataset = client.create_dataset(
    dataset_name="qa-golden-dataset",
    description="Dataset curado para Q&A",
    examples=examples
)
```

#### Opção 2: Criar dataset vazio + adicionar examples depois

```python
# 1. Criar dataset
dataset = client.create_dataset(
    dataset_name="qa-golden-dataset",
    description="Dataset curado para Q&A"
)

# 2. Adicionar examples incrementalmente
client.create_examples(
    dataset_id=dataset.id,
    examples=[
        {
            "inputs": {"pergunta": "..."},
            "outputs": {"resposta_esperada": "..."}
        }
    ]
)
```

#### Opção 3: Criar dataset de production runs

```python
# Converter runs existentes em dataset
client.create_dataset_from_runs(
    dataset_name="production-dataset",
    run_ids=["run-id-1", "run-id-2", ...]
)
```

### 1.6 Golden Datasets vs Production Datasets

**Golden Datasets** (Curado):
- ✅ Examples cuidadosamente selecionados
- ✅ Reference outputs validados por humanos
- ✅ Cobertura de edge cases
- ✅ Tamanho menor (~50-200 examples)
- ✅ Uso: Quick Evals, regression testing

**Production Datasets** (Real):
- ✅ Examples de runs reais
- ✅ Distribuição realista de inputs
- ✅ Sem reference outputs (geralmente)
- ✅ Tamanho maior (1000s+)
- ✅ Uso: A/B testing, backtesting

**Best Practice**: Usar ambos!
- Golden dataset para iteração rápida (< 5min)
- Production dataset para validação final

### 1.7 Estratégias de Curation

**Abordagem 1: Manual Curation**
```python
# Criar examples à mão
examples = [
    {"inputs": {...}, "outputs": {...}},
    # Curado por especialista de domínio
]
```

**Abordagem 2: Sample from Production**
```python
# Filtrar runs por critério
runs = client.list_runs(
    project_name="production",
    filter="feedback.score > 0.8"
)

# Converter em dataset
dataset = client.create_dataset_from_runs(
    dataset_name="high-quality-subset",
    run_ids=[r.id for r in runs]
)
```

**Abordagem 3: Hybrid (Production + Human Annotation)**
```python
# 1. Capturar production runs
# 2. Humanos anotam reference outputs
# 3. Criar dataset com inputs (prod) + outputs (humanos)
```

## 2. Target Function - Aplicação Sob Teste

### 2.1 O Que é Target Function

**Definição**: Função Python `Callable` que representa sua aplicação sob avaliação.

**Contrato:**
- **Input**: Dicionário de inputs (do dataset example)
- **Output**: Dicionário de predictions

```python
def my_qa_app(inputs: dict) -> dict:
    """
    Target function para Q&A.

    Args:
        inputs: {"pergunta": "...", "contexto": "..."}

    Returns:
        {"resposta": "..."}
    """
    pergunta = inputs["pergunta"]
    # Lógica da aplicação (LLM call, retrieval, etc)
    resposta = call_llm(pergunta)
    return {"resposta": resposta}
```

### 2.2 Requisitos da Target Function

**Obrigatórios:**
- ✅ Aceita `dict` como input
- ✅ Retorna `dict` como output
- ✅ É `Callable` (função ou objeto com `__call__`)
- ✅ Determinística (mesmo input = mesmo output) - idealmente

**Opcionais mas recomendados:**
- ✅ Type hints para clareza
- ✅ Docstring explicando I/O
- ✅ Error handling robusto
- ✅ Logging para debugging

### 2.3 Tipos de Target Functions

#### Função Simples
```python
def simple_app(inputs: dict) -> dict:
    return {"output": f"Processed: {inputs['input']}"}
```

#### LangChain Chain
```python
from langchain_core.runnables import RunnableLambda

chain = prompt | llm | output_parser

def chain_app(inputs: dict) -> dict:
    result = chain.invoke(inputs)
    return {"output": result}
```

#### LangGraph Graph
```python
from langgraph.graph import StateGraph

graph = StateGraph(...)

def graph_app(inputs: dict) -> dict:
    result = graph.invoke(inputs)
    return {"output": result["final_answer"]}
```

#### Classe com __call__
```python
class MyApp:
    def __init__(self, model):
        self.model = model

    def __call__(self, inputs: dict) -> dict:
        response = self.model.invoke(inputs["query"])
        return {"response": response}

app = MyApp(model=my_llm)
# app é Callable!
```

### 2.4 Mapeamento: Dataset → Target → Judge

**Fluxo de dados:**

```python
# Example do dataset
{
    "inputs": {"pergunta": "Capital da França?"},
    "outputs": {"resposta_esperada": "Paris"}
}

# ↓ inputs passados para Target Function

def target(inputs: dict) -> dict:
    return {"resposta": "Paris"}  # prediction

# ↓ Judge recebe inputs + outputs + prediction

# Judge prompt (simplificado):
"""
Pergunta: {pergunta}                 # De inputs
Resposta Esperada: {resposta_esperada}  # De outputs
Resposta Gerada: {resposta}           # De prediction
"""
```

**Chaves mapeadas via create_llm_as_judge:**
```python
judge = create_llm_as_judge(
    input_keys=["pergunta"],              # inputs do dataset
    reference_output_keys=["resposta_esperada"],  # outputs do dataset
    prediction_key="resposta"             # output da target function
)
```

## 3. SDK Python - Orquestração com langsmith.evaluate()

### 3.1 Função Central: evaluate()

**Assinatura:**
```python
from langsmith.evaluation import evaluate

results = evaluate(
    target_function,     # Callable - Aplicação sob teste
    data,                # str (dataset name) ou Dataset object
    evaluators,          # List[Evaluator] - Incluindo LLM-as-Judge
    experiment_prefix,   # str - Nome do experiment
    max_concurrency=10   # int - Paralelização
)
```

### 3.2 Workflow Interno do evaluate()

```
1. Fetch dataset
   └─> client.read_dataset(data)

2. For each example in dataset:
   a. Extract inputs
   b. Call target_function(inputs) → prediction
   c. For each evaluator:
      - Call evaluator(inputs, outputs, prediction) → score
   d. Log to LangSmith

3. Create Experiment
   └─> Aggregate scores, visualizar UI

4. Return EvaluationResults
```

### 3.3 Exemplo Completo End-to-End

```python
from langsmith import Client
from langsmith.evaluation import evaluate, create_llm_as_judge

# 1. Setup client
client = Client()

# 2. Criar dataset (ou usar existente)
dataset = client.create_dataset(
    dataset_name="qa-eval",
    examples=[
        {
            "inputs": {"pergunta": "Capital da França?"},
            "outputs": {"resposta_esperada": "Paris"}
        },
        {
            "inputs": {"pergunta": "Maior planeta do sistema solar?"},
            "outputs": {"resposta_esperada": "Júpiter"}
        }
    ]
)

# 3. Definir target function
def my_qa_app(inputs: dict) -> dict:
    # Simulação - na prática, chamar LLM
    return {"resposta": "Paris"}  # Hardcoded para exemplo

# 4. Criar LLM-as-Judge evaluator
judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",
    input_keys=["pergunta"],
    reference_output_keys=["resposta_esperada"],
    prediction_key="resposta"
)

# 5. Executar avaliação
results = evaluate(
    target_function=my_qa_app,
    data="qa-eval",  # Nome do dataset
    evaluators=[judge],
    experiment_prefix="qa-eval-v1",
    max_concurrency=5
)

# 6. Resultados
print(f"Aggregate Score: {results.aggregate_score}")
print(f"Experiment URL: {results.experiment_url}")
```

### 3.4 Paralelização e Performance

**max_concurrency** controla execuções paralelas:

```python
# Slow (sequencial)
evaluate(..., max_concurrency=1)  # 1 example por vez

# Fast (paralelo)
evaluate(..., max_concurrency=10)  # 10 examples simultâneos
```

**Trade-offs:**
- ✅ Maior concurrency = mais rápido
- ❌ Maior concurrency = mais custo (API calls simultâneas)
- ❌ Rate limits de modelos podem limitar

**Recomendação**: max_concurrency=5-10 para balancear

### 3.5 Resultado da Avaliação

**Objeto retornado**: `EvaluationResults`

**Campos principais:**
```python
results = evaluate(...)

# Aggregate metrics
results.aggregate_score  # float - Score médio

# Individual results
for result in results.results:
    print(result.score)      # Score deste example
    print(result.comment)    # Justificativa do judge
    print(result.example_id)  # ID do example avaliado

# UI link
results.experiment_url  # Link direto para LangSmith UI
```

## 4. Versionamento e Reprodutibilidade

### 4.1 Por Que Versionamento Importa

**Problema sem versionamento:**
- ❌ Dataset muda, resultados não comparáveis
- ❌ Impossível reproduzir experiment
- ❌ A/B testing inválido

**Solução com versionamento:**
- ✅ Dataset imutável por versão
- ✅ Experiment referencia versão específica
- ✅ Resultados reproduzíveis

### 4.2 Versionamento Automático

LangSmith versiona automaticamente quando você:

1. Cria dataset inicial (versão 1)
2. Adiciona/modifica examples (versão 2, 3, ...)
3. Cada versão tem ID único

```python
# Versão 1
dataset = client.create_dataset("my-dataset", examples=[...])

# Versão 2 (automático ao adicionar examples)
client.create_examples(dataset_id=dataset.id, examples=[...])
```

### 4.3 Experiment Linking

Cada experiment armazena:
- Dataset name
- Dataset version
- Timestamp
- Evaluator configs
- Results

**Benefício**: Rastreabilidade completa

```python
# Experiment mostra no UI:
# - Dataset: qa-eval (versão 3)
# - Evaluators: CORRECTNESS judge
# - Date: 2025-01-15
# - Results: 0.85 avg score
```

## 5. Setup e Configuração

### 5.1 Instalação SDK

```bash
pip install langsmith
```

### 5.2 Autenticação

**Opção 1: Environment variable**
```bash
export LANGSMITH_API_KEY="lsv2_pt_..."
```

**Opção 2: .env file**
```bash
# .env
LANGSMITH_API_KEY=lsv2_pt_...
```

**Opção 3: Código**
```python
import os
os.environ["LANGSMITH_API_KEY"] = "lsv2_pt_..."
```

### 5.3 Client Configuration

```python
from langsmith import Client

# Default (usa LANGSMITH_API_KEY)
client = Client()

# Custom endpoint (para self-hosted)
client = Client(
    api_url="https://custom.langsmith.com",
    api_key="..."
)
```

### 5.4 Verificar Conexão

```python
# Listar datasets para validar conexão
datasets = list(client.list_datasets())
print(f"Conectado! {len(datasets)} datasets encontrados")
```

## 6. Casos de Uso Avançados

### 6.1 Subset Evaluation (Quick Evals)

**Problema**: Dataset grande (1000s examples) = lento + caro

**Solução**: Avaliar subset pequeno para iteração rápida

```python
# Criar subset de 20 examples do dataset original
subset_examples = client.list_examples(
    dataset_name="large-dataset",
    limit=20
)

# Criar dataset temporário
subset = client.create_dataset(
    dataset_name="quick-eval-subset",
    examples=[ex.inputs for ex in subset_examples]
)

# Avaliar subset rapidamente
evaluate(
    target_function=my_app,
    data="quick-eval-subset",
    evaluators=[judge]
)
```

### 6.2 Upload Results Only (No Re-execution)

**Cenário**: Você já tem predictions armazenadas, quer apenas avaliar

```python
# Opção: upload_results=False
results = evaluate(
    target_function=my_app,
    data="dataset",
    evaluators=[judge],
    upload_results=False  # Não envia para LangSmith (local apenas)
)
```

**Uso**: Desenvolvimento local rápido sem custo de armazenamento

### 6.3 Incremental Dataset Building

**Pattern**: Adicionar examples gradualmente

```python
# Dia 1: 50 examples
dataset = client.create_dataset("growing-dataset", examples=[...])

# Dia 2: +20 examples
client.create_examples(dataset_id=dataset.id, examples=[...])

# Dia 3: +30 examples
client.create_examples(dataset_id=dataset.id, examples=[...])

# Total: 100 examples em versão 3
```

## 7. Troubleshooting

### Problema: Dataset não encontrado
```python
# ❌ Erro
evaluate(data="non-existent-dataset", ...)

# ✅ Solução: Verificar nome
datasets = client.list_datasets()
print([d.name for d in datasets])
```

### Problema: Target function não retorna dict
```python
# ❌ Errado
def bad_target(inputs):
    return "string response"  # Não é dict!

# ✅ Correto
def good_target(inputs):
    return {"response": "string response"}
```

### Problema: Chaves não existem no example
```python
# ❌ Dataset
{"inputs": {"question": "..."}}  # "question"

# ❌ Judge config
judge = create_llm_as_judge(
    input_keys=["pergunta"]  # "pergunta" ≠ "question"!
)

# ✅ Solução: Usar nomes exatos
judge = create_llm_as_judge(
    input_keys=["question"]
)
```

## 8. Checklist de Infraestrutura

**Antes de executar evaluate():**
- [ ] LangSmith API key configurada?
- [ ] Dataset criado e versionado?
- [ ] Examples têm reference outputs (para CORRECTNESS)?
- [ ] Target function retorna dict?
- [ ] Chaves mapeadas corretamente (input_keys, reference_output_keys, prediction_key)?
- [ ] Evaluator (LLM-as-Judge) criado?
- [ ] Conexão com LangSmith validada?

**Para Quick Evals:**
- [ ] Subset dataset criado (< 50 examples)?
- [ ] upload_results=False configurado (opcional)?

**Para Reprodutibilidade:**
- [ ] Dataset versionado?
- [ ] Experiment prefix descritivo?
- [ ] Timestamp registrado?
