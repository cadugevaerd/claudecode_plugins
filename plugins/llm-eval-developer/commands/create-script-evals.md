---
description: Create automated evaluation script for LLM golden datasets with LangSmith integration
allowed-tools: Read, Write, Bash, Glob, Grep, Skill
model: claude-sonnet-4-5
argument-hint: '[EVALUATORS_DIR] [DATASETS_DIR]'
---

# Create Script Evals

Cria script automatizado que coleta informações de skills, envia datasets para LangSmith, executa quick-evals usando **LLM-as-Judge com critérios integrados do LangSmith**, e extrai métricas com ponderação customizada.

## 🎯 Objetivo

Este comando gera um script Python completo que:

- 🔍 Coleta informações de skills necessárias do projeto (incluindo `llm-as-a-judge`)
- 📊 **Analisa datasets** e seleciona critérios LLM-as-Judge apropriados (CORRECTNESS, RELEVANCE, CONCISENESS, COHERENCE, HELPFULNESS, HARMFULNESS, MALICIOUSNESS, CONTROVERSIALITY)
- 📤 Envia datasets da pasta `datasets/` para LangSmith (skip se já existir)
- ⚡ Configura e executa quick-evals usando `create_llm_as_judge` do LangSmith
- 📊 Extrai métricas de execução com ponderação configurável
- 🎯 Retorna score total baseado em pesos customizados

**Nota sobre o modelo:** Este comando usa **Sonnet 4.5** porque requer:

- Raciocínio complexo para integrar múltiplas skills (evaluation-developer, benchmark-runner)
- Análise de estrutura de datasets e mapeamento para LangSmith API
- Geração de código Python com error handling robusto e patterns avançados
- Compreensão de métricas de avaliação e cálculo de scores ponderados
- Validação de configurações e troubleshooting de integração com APIs externas

## 🔧 Instruções

### Passo 1: Coletar Informações de Skills

1.1 **Executar Skills Relevantes**

Usar `Skill` tool para coletar conhecimento especializado:

```bash
Skill(skill="llm-eval-developer:llm-as-a-judge")
Skill(skill="llm-eval-developer:evals-automator")
Skill(skill="llm-eval-developer:datasets-evals")
Skill(skill="llm-eval-developer:quick-evals")
```

1.2 **Extrair Patterns de Evaluation**

Das skills, extrair:

- **LLM-as-Judge com `create_llm_as_judge`**: Usar função helper do LangSmith
- **Critérios integrados do LangSmith**: CORRECTNESS, RELEVANCE, CONCISENESS, COHERENCE, HELPFULNESS, HARMFULNESS, MALICIOUSNESS, CONTROVERSIALITY
- **Mapeamento de chaves**: input_keys, reference_output_keys, prediction_key
- Quando usar cada critério de avaliação
- Integração com LangSmith API via `langsmith.evaluate()`
- Patterns de dataset upload
- Métricas disponíveis (accuracy, relevance, latency, cost, errors)
- Como analisar estrutura de datasets para selecionar critérios apropriados

### Passo 2: Analisar Estrutura Atual

2.1 **Verificar Diretórios**

- Usar `Glob` para verificar se `evaluators/scripts/` existe
- Criar diretório se não existir usando `Bash(mkdir -p evaluators/scripts/)`
- Verificar se `datasets/` existe e contém arquivos

2.2 **Escanear e Analisar Datasets Existentes**

- Usar `Glob` para listar arquivos em `datasets/` (JSON, JSONL, CSV)
- **Para cada dataset**, usar `Read` para analisar estrutura completa:
  - Ler primeiro exemplo do dataset
  - Detectar campos de input e output
  - Identificar tipo de tarefa (Q&A, summarization, classification, generation)
  - Verificar se há reference outputs (ground truth)
  - Analisar formato dos outputs esperados (texto livre, JSON estruturado, categorias)
  - Determinar natureza da avaliação necessária (objetiva vs subjetiva)
- Determinar schema necessário para LangSmith
- **Para cada dataset, decidir tipo de evaluator apropriado**:
  - **Similarity-based** (BLEU, ROUGE, embedding): Se há reference outputs exatos
  - **Rule-based** (regex, exact match): Se outputs têm formato fixo/validável
  - **LLM-as-Judge**: Se critérios são subjetivos, complexos ou sem ground truth
  - **Composite**: Se precisa avaliar múltiplos aspectos

2.3 **Documentar Decisões de Evaluators e Critérios LLM-as-Judge**

- Criar dict mapeando cada dataset para seus evaluators e critérios LLM-as-Judge recomendados
- **Para LLM-as-Judge**: Selecionar critério apropriado baseado na natureza do dataset
- Exemplo:
  ```python
  dataset_evaluators = {
      "qa-dataset": {
          "type": "llm_as_judge",
          "criteria": "CORRECTNESS",  # Precisão factual para Q&A
          "input_keys": ["question"],
          "reference_output_keys": ["expected_answer"],
          "prediction_key": "answer"
      },
      "summary-dataset": {
          "type": "llm_as_judge",
          "criteria": "CONCISENESS",  # Brevidade para summarization
          "input_keys": ["text"],
          "reference_output_keys": ["summary"],
          "prediction_key": "output"
      },
      "chatbot-dataset": {
          "type": "llm_as_judge",
          "criteria": "HELPFULNESS",  # Utilidade para assistentes
          "input_keys": ["user_message"],
          "reference_output_keys": None,  # Sem ground truth
          "prediction_key": "response"
      },
      "safety-test": {
          "type": "llm_as_judge",
          "criteria": "HARMFULNESS",  # Teste de segurança
          "input_keys": ["prompt"],
          "reference_output_keys": None,
          "prediction_key": "completion"
      }
  }
  ```
- **Guia de Seleção de Critérios**:
  - `CORRECTNESS`: Q&A, RAG, extração de fatos (requer ground truth)
  - `RELEVANCE`: Verificar alinhamento com pergunta/contexto
  - `CONCISENESS`: Summarization, chatbots (respostas breves)
  - `COHERENCE`: Geração de texto longo, artigos
  - `HELPFULNESS`: Assistentes, chatbots (avaliação geral)
  - `HARMFULNESS`: Safety, guardrails (detectar conteúdo prejudicial)
  - `MALICIOUSNESS`: Detectar intenção maliciosa ou enganosa
  - `CONTROVERSIALITY`: Moderação de conteúdo
- Essa informação será usada para gerar o script `quick_evals.py` customizado com `create_llm_as_judge`

### Passo 3: Criar Script de Upload de Datasets

3.1 **Gerar `upload_datasets.py`**

Criar script que:

```python
"""
Upload Datasets para LangSmith
Skip se dataset já existir no LangSmith.
"""

import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def upload_dataset_to_langsmith(dataset_path: Path, client: Client):
    """
    Faz upload de dataset local para LangSmith.

    Args:
        dataset_path: Path para arquivo do dataset (JSON/JSONL)
        client: LangSmith Client

    Returns:
        str: Dataset name no LangSmith
    """
    dataset_name = dataset_path.stem

    # Check if exists
    try:
        existing = client.read_dataset(dataset_name=dataset_name)
        print(f"✅ Dataset '{dataset_name}' já existe. Skipping upload.")
        return dataset_name
    except:
        pass

    # Load local dataset
    with open(dataset_path, 'r') as f:
        if dataset_path.suffix == '.jsonl':
            examples = [json.loads(line) for line in f]
        else:
            examples = json.load(f)

    # Create dataset
    dataset = client.create_dataset(dataset_name=dataset_name)

    # Upload examples
    for example in examples:
        client.create_example(
            dataset_id=dataset.id,
            inputs=example.get("input", {}),
            outputs=example.get("output", {})
        )

    print(f"📤 Uploaded {len(examples)} examples to '{dataset_name}'")
    return dataset_name


def main():
    """Upload all datasets from datasets/ directory"""
    client = Client()
    datasets_dir = Path("datasets")

    if not datasets_dir.exists():
        print("❌ Directory 'datasets/' not found")
        return

    dataset_files = list(datasets_dir.glob("*.json")) + list(datasets_dir.glob("*.jsonl"))

    if not dataset_files:
        print("⚠️  No datasets found in datasets/")
        return

    uploaded = []
    for dataset_file in dataset_files:
        name = upload_dataset_to_langsmith(dataset_file, client)
        uploaded.append(name)

    print(f"\n✅ Upload complete. {len(uploaded)} datasets available in LangSmith:")
    for name in uploaded:
        print(f"  - {name}")

if __name__ == "__main__":
    main()
```

3.2 **Salvar Script**

Usar `Write` para criar `evaluators/scripts/upload_datasets.py`

### Passo 4: Criar Script de Quick Evals

4.1 **Preencher Configuração de Evaluators**

Usar o mapeamento criado no Passo 2.3 (`dataset_evaluators`) para popular a constante `DATASET_EVALUATORS` no script.

Exemplo de preenchimento:
```python
DATASET_EVALUATORS = {
    "qa-golden-set": ["qa", "context_qa"],
    "summary-eval": ["llm_as_judge"],
    "code-generation": ["llm_as_judge", "embedding_distance"],
}
```

4.2 **Gerar `quick_evals.py`**

Criar script que executa evaluations sobre golden datasets usando a configuração de evaluators:

```python
"""
Quick Evaluations sobre Golden Datasets no LangSmith
Executa evaluations e extrai métricas com ponderação customizada.
"""

import sys
import os
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langchain_core.callbacks import BaseCallbackHandler
import numpy as np
import time
import json

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# ==================== CONFIGURAÇÃO DE PESOS ====================

METRIC_WEIGHTS = {
    "accuracy": 0.45,      # 45% - Precisão das respostas
    "relevance": 0.20,     # 20% - Relevância do conteúdo
    "latency": 0.15,       # 15% - Tempo de resposta (P95)
    "cost": 0.15,          # 15% - Custo por execução
    "errors": 0.05         # 5%  - Taxa de erro
}

# Validar que soma = 100%
assert abs(sum(METRIC_WEIGHTS.values()) - 1.0) < 0.001, "Weights must sum to 1.0"


# ==================== DATASET EVALUATOR CONFIGURATION ====================

# Configuração de evaluators por dataset
# Esta configuração é gerada automaticamente pelo comando /create-script-evals
# baseado na análise dos datasets em datasets/
DATASET_EVALUATORS = {
    # Exemplo:
    # "qa-dataset": ["qa", "context_qa"],
    # "summary-dataset": ["llm_as_judge"],
    # "generation-dataset": ["llm_as_judge", "embedding_distance"]
}

# ==================== EVALUATORS ====================

# LLM-as-Judge usando create_llm_as_judge do LangSmith
from langsmith.evaluation import create_llm_as_judge


class LatencyCallback(BaseCallbackHandler):
    """Track latency metrics for P95 calculation"""
    def __init__(self):
        self.latencies = []
        self.start = None

    def on_llm_start(self, *args, **kwargs):
        self.start = time.perf_counter()

    def on_llm_end(self, *args, **kwargs):
        if self.start:
            latency_ms = (time.perf_counter() - self.start) * 1000
            self.latencies.append(latency_ms)
            self.start = None

    def get_p95(self):
        """Get P95 latency in milliseconds"""
        return np.percentile(self.latencies, 95) if self.latencies else 0


def normalize_score(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """
    Normaliza score para 0-1.

    Args:
        value: Valor atual
        min_val: Valor mínimo esperado
        max_val: Valor máximo esperado
        invert: Se True, valores menores = score maior (para latency/cost)

    Returns:
        float: Score normalizado 0-1
    """
    if max_val == min_val:
        return 1.0

    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0.0, min(1.0, normalized))  # Clamp 0-1

    if invert:
        normalized = 1.0 - normalized

    return normalized


# ==================== MAIN EVALUATION ====================

def select_evaluators_for_dataset(dataset_name: str) -> List:
    """
    Seleciona evaluators apropriados baseado na configuração DATASET_EVALUATORS.

    Esta configuração é gerada automaticamente pelo comando /create-script-evals
    após analisar a estrutura de cada dataset e escolher critérios LLM-as-Judge apropriados.

    Args:
        dataset_name: Nome do dataset

    Returns:
        list: Lista de evaluators a serem usados
    """
    # Verificar se há configuração específica para este dataset
    if dataset_name not in DATASET_EVALUATORS:
        print(f"⚠️  Dataset '{dataset_name}' não encontrado na configuração")
        print("   Usando evaluator padrão (LLM-as-Judge CORRECTNESS)...")

        # Fallback: LLM-as-Judge com critério CORRECTNESS
        default_judge = create_llm_as_judge(
            criteria="CORRECTNESS",
            model="openai:gpt-4o-mini",
            input_keys=["question"],
            reference_output_keys=["expected_answer"],
            prediction_key="answer"
        )
        return [default_judge]

    # Obter configuração do dataset
    config = DATASET_EVALUATORS[dataset_name]

    print(f"\n📊 Evaluators para Dataset '{dataset_name}':")

    evaluators = []

    if config["type"] == "llm_as_judge":
        # Criar LLM-as-Judge usando create_llm_as_judge do LangSmith
        criteria = config["criteria"]
        input_keys = config["input_keys"]
        reference_output_keys = config.get("reference_output_keys")
        prediction_key = config["prediction_key"]

        print(f"   ✅ LLM-as-Judge ({criteria})")
        print(f"      - Model: openai:gpt-4o-mini")
        print(f"      - Input Keys: {input_keys}")
        print(f"      - Reference Keys: {reference_output_keys}")
        print(f"      - Prediction Key: {prediction_key}")

        judge = create_llm_as_judge(
            criteria=criteria,
            model="openai:gpt-4o-mini",
            input_keys=input_keys,
            reference_output_keys=reference_output_keys,
            prediction_key=prediction_key
        )
        evaluators.append(judge)

    # Se nenhum evaluator válido foi adicionado, usar padrão
    if not evaluators:
        print("   ⚠️  Fallback para evaluator padrão (CORRECTNESS)")
        default_judge = create_llm_as_judge(
            criteria="CORRECTNESS",
            model="openai:gpt-4o-mini",
            input_keys=["question"],
            reference_output_keys=["expected_answer"],
            prediction_key="answer"
        )
        evaluators = [default_judge]

    return evaluators


def run_quick_eval(
    target_function,
    dataset_name: str,
    experiment_prefix: str = "quick-eval"
) -> Dict[str, float]:
    """
    Executa quick evaluation sobre golden dataset com seleção automática de evaluators.

    Args:
        target_function: Função que implementa seu LLM app
        dataset_name: Nome do dataset no LangSmith
        experiment_prefix: Prefixo para experimento

    Returns:
        dict: Métricas extraídas e score total ponderado
    """
    client = Client()

    # Callback para latency tracking
    latency_cb = LatencyCallback()

    # Wrapper para adicionar callback
    def predict_with_tracking(inputs):
        from langchain_core.runnables import RunnableConfig
        config = RunnableConfig(callbacks=[latency_cb])
        result = target_function(inputs, config=config)
        return result

    # Selecionar evaluators apropriados baseado no dataset
    evaluators = select_evaluators_for_dataset(dataset_name)

    # Executar evaluation
    results = evaluate(
        predict_with_tracking,
        data=dataset_name,
        evaluators=evaluators,
        experiment_prefix=experiment_prefix,
        max_concurrency=5
    )

    # ==================== EXTRAIR MÉTRICAS ====================

    # 1. Accuracy (from LangSmith evaluator)
    accuracy = results.get("qa", {}).get("mean", 0.0)

    # 2. Relevance (from LangSmith evaluator)
    relevance = results.get("context_qa", {}).get("mean", 0.0)

    # 3. Latency P95 (from custom callback)
    p95_latency = latency_cb.get_p95()
    latency_score = normalize_score(
        p95_latency,
        min_val=0,
        max_val=2000,  # 2s = score 0, 0ms = score 1
        invert=True
    )

    # 4. Cost (from LangSmith tracking)
    # Assumindo que LangSmith trackeia custo automaticamente
    total_cost = results.get("total_cost", 0.0)
    avg_cost_per_example = total_cost / max(results.get("example_count", 1), 1)
    cost_score = normalize_score(
        avg_cost_per_example,
        min_val=0.0,
        max_val=0.01,  # $0.01/example = score 0
        invert=True
    )

    # 5. Error Rate
    error_count = results.get("error_count", 0)
    total_examples = results.get("example_count", 1)
    error_rate = error_count / max(total_examples, 1)
    error_score = 1.0 - error_rate  # Menos erros = melhor score

    # ==================== CALCULAR SCORE TOTAL ====================

    weighted_score = (
        accuracy * METRIC_WEIGHTS["accuracy"] +
        relevance * METRIC_WEIGHTS["relevance"] +
        latency_score * METRIC_WEIGHTS["latency"] +
        cost_score * METRIC_WEIGHTS["cost"] +
        error_score * METRIC_WEIGHTS["errors"]
    )

    # ==================== RETORNO ====================

    metrics = {
        "accuracy": round(accuracy, 3),
        "relevance": round(relevance, 3),
        "p95_latency_ms": round(p95_latency, 0),
        "latency_score": round(latency_score, 3),
        "avg_cost_per_example": round(avg_cost_per_example, 5),
        "cost_score": round(cost_score, 3),
        "error_rate": round(error_rate, 3),
        "error_score": round(error_score, 3),
        "weighted_total_score": round(weighted_score, 3),
        "experiment_url": results.get("experiment_url", "")
    }

    return metrics


# ==================== EXEMPLO DE USO ====================

def example_llm_app(inputs, config=None):
    """
    Exemplo de aplicação LLM.
    SUBSTITUA pela sua implementação real.
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}")
    ])

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke(inputs, config=config or {})
    return {"output": result}


def main():
    """Run quick evaluation and print weighted results"""

    # CONFIGURAÇÃO: Ajuste conforme seu setup
    DATASET_NAME = "golden-dataset"  # Nome do dataset no LangSmith
    TARGET_FUNCTION = example_llm_app  # Sua função LLM

    print("=" * 60)
    print("🚀 QUICK EVALUATION - LANGSMITH")
    print("=" * 60)

    # Executar evaluation
    metrics = run_quick_eval(
        target_function=TARGET_FUNCTION,
        dataset_name=DATASET_NAME,
        experiment_prefix="quick-eval"
    )

    # ==================== EXIBIR RESULTADOS ====================

    print("\n📊 MÉTRICAS EXTRAÍDAS:")
    print("-" * 60)

    # Tabela de métricas
    print(f"{'Métrica':<25} {'Score':<12} {'Peso':<10} {'Contribuição'}")
    print("-" * 60)

    metrics_display = [
        ("Accuracy", metrics["accuracy"], METRIC_WEIGHTS["accuracy"]),
        ("Relevance", metrics["relevance"], METRIC_WEIGHTS["relevance"]),
        ("Latency Score", metrics["latency_score"], METRIC_WEIGHTS["latency"]),
        ("Cost Score", metrics["cost_score"], METRIC_WEIGHTS["cost"]),
        ("Error Score", metrics["error_score"], METRIC_WEIGHTS["errors"])
    ]

    for name, score, weight in metrics_display:
        contribution = score * weight
        print(f"{name:<25} {score:<12.3f} {weight*100:<9.0f}% {contribution:.3f}")

    print("-" * 60)
    print(f"{'SCORE TOTAL':<25} {metrics['weighted_total_score']:<12.3f} {'100%':<10} {metrics['weighted_total_score']:.3f}")
    print("=" * 60)

    # Detalhes adicionais
    print(f"\n📈 Detalhes:")
    print(f"  - P95 Latency: {metrics['p95_latency_ms']:.0f}ms")
    print(f"  - Avg Cost/Example: ${metrics['avg_cost_per_example']:.5f}")
    print(f"  - Error Rate: {metrics['error_rate']*100:.1f}%")
    print(f"  - LangSmith URL: {metrics['experiment_url']}")

    # Salvar resultados
    output_file = "evaluators/scripts/eval_results.json"
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n💾 Resultados salvos em: {output_file}")

    return metrics


if __name__ == "__main__":
    main()
```

4.3 **Salvar Script**

Usar `Write` para criar `evaluators/scripts/quick_evals.py` com a configuração `DATASET_EVALUATORS` preenchida

### Passo 5: Criar Script Orquestrador Principal

5.1 **Gerar `run_all_evals.py`**

Script que executa todo o pipeline em ordem:

```python
"""
Orquestrador Principal - Evaluation Pipeline
Executa upload de datasets + quick evals em sequência.
"""

import subprocess
import sys
from pathlib import Path

def run_command(script_name: str, description: str):
    """Executa script Python e reporta resultado"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}\n")

    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print(f"\n❌ Erro ao executar {script_name}")
        sys.exit(1)

    print(f"\n✅ {description} - Concluído")


def main():
    """Executa pipeline completo de evaluation"""

    scripts_dir = Path("evaluators/scripts")

    # Verificar se diretório existe
    if not scripts_dir.exists():
        print(f"❌ Diretório '{scripts_dir}' não encontrado")
        sys.exit(1)

    # Passo 1: Upload de datasets
    upload_script = scripts_dir / "upload_datasets.py"
    if upload_script.exists():
        run_command(str(upload_script), "Passo 1: Upload de Datasets para LangSmith")
    else:
        print(f"⚠️  Script {upload_script} não encontrado. Skipping upload.")

    # Passo 2: Quick evaluations
    evals_script = scripts_dir / "quick_evals.py"
    if evals_script.exists():
        run_command(str(evals_script), "Passo 2: Quick Evaluations")
    else:
        print(f"❌ Script {evals_script} não encontrado")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("🎉 PIPELINE DE EVALUATION CONCLUÍDO")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
```

5.2 **Salvar Script Orquestrador**

Usar `Write` para criar `evaluators/scripts/run_all_evals.py`

### Passo 6: Criar Documentação

6.1 **Gerar README.md**

````markdown
# Evaluation Scripts

Scripts automatizados para upload de datasets e execução de quick evaluations no LangSmith.

## 📁 Estrutura

- `upload_datasets.py`: Upload de datasets locais para LangSmith (skip se existir)
- `quick_evals.py`: Executa evaluations com evaluators customizados por dataset e métricas ponderadas
- `run_all_evals.py`: Orquestrador principal (executa tudo em ordem)
- `eval_results.json`: Resultados da última execução

## 🎯 Configuração Automática de Evaluators

O comando `/create-script-evals` analisa todos os datasets **durante sua execução** e gera o script `quick_evals.py` com a configuração `DATASET_EVALUATORS` pré-populada:

### Análise de Dataset (Feita pelo Comando)

Durante a execução do `/create-script-evals`, o comando:

1. **Lê cada dataset** em `datasets/`
2. **Analisa a estrutura** detectando:
   - Tipo de tarefa (Q&A, summarization, classification, generation)
   - Tipo de output (texto livre ou estruturado)
   - Presença de referência (ground truth)
   - Campos disponíveis (inputs/outputs)

3. **Decide evaluators apropriados** para cada dataset
4. **Gera `quick_evals.py`** com configuração fixa:

```python
DATASET_EVALUATORS = {
    "qa-dataset": ["qa", "context_qa"],
    "summary-dataset": ["llm_as_judge"],
    "generation-dataset": ["llm_as_judge", "embedding_distance"]
}
```

### Seleção de Critérios LLM-as-Judge (Feita pelo Comando)

Baseado na análise, o **comando** seleciona automaticamente o **critério LLM-as-Judge** apropriado:

| Tipo de Dataset | Critério Selecionado | Razão |
|-----------------|---------------------|-------|
| **Q&A com referência** | CORRECTNESS | Verifica precisão factual comparando com ground truth |
| **Q&A sem referência** | RELEVANCE | Avalia alinhamento da resposta com a pergunta |
| **Summarization** | CONCISENESS | Mede brevidade e objetividade |
| **Geração de texto longo** | COHERENCE | Avalia fluxo lógico e consistência |
| **Assistentes/Chatbots** | HELPFULNESS | Avalia utilidade geral da resposta |
| **Safety/Guardrails** | HARMFULNESS | Detecta potencial de dano (físico ou emocional) |
| **Moderação** | MALICIOUSNESS | Detecta intenção de causar dano ou enganar |
| **Conteúdo sensível** | CONTROVERSIALITY | Avalia potencial para gerar desacordo |

### LLM-as-Judge com `create_llm_as_judge`

O script usa **`create_llm_as_judge`** do LangSmith SDK com os **critérios integrados**:

**Critérios disponíveis**:
1. **CORRECTNESS**: Precisão factual (requer ground truth)
2. **RELEVANCE**: Alinhamento com pergunta/contexto
3. **CONCISENESS**: Brevidade e objetividade
4. **COHERENCE**: Fluxo lógico e consistência
5. **HELPFULNESS**: Utilidade geral para o usuário
6. **HARMFULNESS**: Detecção de conteúdo prejudicial
7. **MALICIOUSNESS**: Detecção de intenção maliciosa
8. **CONTROVERSIALITY**: Potencial para gerar controvérsia

**Estrutura gerada**:
```python
from langsmith.evaluation import create_llm_as_judge

judge = create_llm_as_judge(
    criteria="CORRECTNESS",  # Ou outro critério apropriado
    model="openai:gpt-4o-mini",
    input_keys=["question"],
    reference_output_keys=["expected_answer"],  # Opcional
    prediction_key="answer"
)
```

**Vantagens**:
- ✅ Usa helpers oficiais do LangSmith (mantido pela equipe LangChain)
- ✅ Critérios pré-calibrados e validados
- ✅ Funciona com ou sem ground truth
- ✅ Avalia aspectos subjetivos com consistência
- ✅ Fornece justificativa detalhada
- ✅ Integração nativa com `langsmith.evaluate()`

**Trade-offs**:
- ⚠️ Custo adicional de API (GPT-4o-mini)
- ⚠️ Latência maior que evaluators rule-based
- ⚠️ Não determinístico (pode variar ligeiramente)

## 🚀 Como Usar

### Opção 1: Pipeline Completo

```bash
uv run evaluators/scripts/run_all_evals.py
````

### Opção 2: Executar Individualmente

```bash
# 1. Upload datasets
uv run evaluators/scripts/upload_datasets.py

# 2. Run evaluations
uv run evaluators/scripts/quick_evals.py
```

## 📦 Dependências

Os scripts requerem as seguintes bibliotecas Python:

```bash
pip install langsmith langchain langchain-openai openai python-dotenv numpy
```

Ou usando `uv`:

```bash
uv pip install langsmith langchain langchain-openai openai python-dotenv numpy
```

**Nota**: A biblioteca `openai` é necessária para o LLM-as-Judge evaluator que usa GPT-4o-mini para avaliar respostas quando não há ground truth ou critérios são subjetivos.

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Configure as seguintes variáveis no `.env`:

```bash
LANGSMITH_API_KEY=your-api-key
LANGCHAIN_PROJECT=your-project-name
LANGCHAIN_TRACING_V2=true
OPENAI_API_KEY=your-openai-key  # ou outro provider
```

**Importante**: Os scripts utilizam `python-dotenv` para carregar automaticamente as variáveis do arquivo `.env`. Certifique-se de que:
- O arquivo `.env` está na raiz do projeto
- A variável `LANGSMITH_API_KEY` está configurada corretamente
- A biblioteca `python-dotenv` está instalada (`pip install python-dotenv`)

**Configuração de Python Path**: Os scripts automaticamente adicionam o diretório raiz do projeto ao `sys.path`:
- Estrutura esperada: `project_root/evaluators/scripts/[script].py`
- O script resolve o caminho com `.parents[2]` para alcançar o diretório raiz
- Isso permite importar módulos do projeto sem conflitos de path
- Se sua estrutura for diferente, ajuste o número em `.parents[N]` conforme necessário

### 2. Ajustar Pesos das Métricas

Edite `quick_evals.py` para customizar os pesos:

```python
METRIC_WEIGHTS = {
    "accuracy": 0.45,      # 45% - Ajuste conforme necessário
    "relevance": 0.20,     # 20%
    "latency": 0.15,       # 15%
    "cost": 0.15,          # 15%
    "errors": 0.05         # 5%
}
```

**Importante**: A soma dos pesos deve ser 1.0 (100%)

### 3. Configurar Sua Aplicação LLM

Em `quick_evals.py`, substitua `example_llm_app` pela sua implementação:

```python
def my_llm_app(inputs, config=None):
    # Sua lógica aqui
    return {"output": result}

# Depois, em main():
TARGET_FUNCTION = my_llm_app
```

## 📊 Métricas Calculadas

| Métrica | Descrição | Peso Padrão | Fonte |
|---------|-----------|-------------|-------|
| **Accuracy** | Precisão das respostas | 45% | LangSmith `qa` evaluator |
| **Relevance** | Relevância do conteúdo | 20% | LangSmith `context_qa` evaluator |
| **Latency** | P95 tempo de resposta | 15% | Custom callback |
| **Cost** | Custo médio por exemplo | 15% | LangSmith tracking |
| **Errors** | Taxa de erro (1 - error_rate) | 5% | LangSmith error tracking |

### Score Total

Score final = Σ (métrica × peso)

Exemplo:

- Accuracy: 0.85 × 0.45 = 0.3825
- Relevance: 0.78 × 0.20 = 0.156
- Latency: 0.92 × 0.15 = 0.138
- Cost: 0.88 × 0.15 = 0.132
- Errors: 0.95 × 0.05 = 0.0475
- **Total: 0.856 (85.6%)**

## 📁 Formato dos Datasets

Os datasets em `datasets/` devem seguir o formato:

**JSON:**

```json
[
  {
    "input": {"question": "What is AI?"},
    "output": {"answer": "AI is artificial intelligence."}
  }
]
```

**JSONL:**

```jsonl
{"input": {"question": "What is AI?"}, "output": {"answer": "AI is artificial intelligence."}}
{"input": {"question": "What is ML?"}, "output": {"answer": "ML is machine learning."}}
```

## 🔍 Troubleshooting

### Erro: Dataset já existe

Comportamento esperado! O script faz skip automático.

### Erro: LangSmith API Key (401 "Invalid token")

**Causa**: Variável `LANGSMITH_API_KEY` não está sendo carregada do arquivo `.env`.

**Soluções**:
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Certifique-se de que a variável está definida corretamente: `LANGSMITH_API_KEY=your-api-key`
3. Instale `python-dotenv`: `pip install python-dotenv`
4. Verifique se `load_dotenv()` está sendo chamado no início dos scripts
5. Teste manualmente: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('LANGSMITH_API_KEY'))"`

### Erro: Nenhum dataset encontrado

Verifique se há arquivos `.json` ou `.jsonl` em `datasets/`.

### Erro: ModuleNotFoundError ao importar módulos do projeto

**Causa**: Script não consegue importar módulos do projeto.

**Soluções**:
1. Verifique se a estrutura de diretórios está correta: `project_root/evaluators/scripts/`
2. Ajuste `.parents[N]` se a estrutura for diferente:
   - `.parents[1]`: Para `project_root/scripts/[script].py`
   - `.parents[2]`: Para `project_root/evaluators/scripts/[script].py` (padrão)
   - `.parents[3]`: Para `project_root/foo/evaluators/scripts/[script].py`
3. Teste o path: Adicione `print(f"Project root: {project_root}")` após `project_root = ...`
4. Verifique se os módulos que você quer importar existem no `project_root`

## 📖 Referências

- [LangSmith Evaluation Docs](https://docs.smith.langchain.com/evaluation)
- [LangChain Evaluators](https://python.langchain.com/docs/guides/productionization/evaluation/)

````

6.2 **Salvar README**

Usar `Write` para criar `evaluators/scripts/README.md`

### Passo 7: Validação e Teste

7.1 **Verificar Estrutura Criada**

Usar `Glob` para confirmar:
- `evaluators/scripts/upload_datasets.py` existe
- `evaluators/scripts/quick_evals.py` existe
- `evaluators/scripts/run_all_evals.py` existe
- `evaluators/scripts/README.md` existe

7.2 **Executar Validação Sintática (Opcional)**

```bash
uv run python -m py_compile evaluators/scripts/*.py
````

## 📊 Formato de Saída

### Durante Execução

```text
============================================================
🚀 QUICK EVALUATION - LANGSMITH
============================================================

🔍 Running evaluation on dataset 'golden-dataset'...
✅ Evaluation complete

📊 MÉTRICAS EXTRAÍDAS:
------------------------------------------------------------
Métrica                   Score        Peso       Contribuição
------------------------------------------------------------
Accuracy                  0.850        45%        0.383
Relevance                 0.780        20%        0.156
Latency Score             0.920        15%        0.138
Cost Score                0.880        15%        0.132
Error Score               0.950        5%         0.048
------------------------------------------------------------
SCORE TOTAL               0.856        100%       0.856
============================================================

📈 Detalhes:
  - P95 Latency: 450ms
  - Avg Cost/Example: $0.00125
  - Error Rate: 5.0%
  - LangSmith URL: https://smith.langchain.com/...

💾 Resultados salvos em: evaluators/scripts/eval_results.json
```

### Arquivo JSON Gerado

```json
{
  "accuracy": 0.850,
  "relevance": 0.780,
  "p95_latency_ms": 450,
  "latency_score": 0.920,
  "avg_cost_per_example": 0.00125,
  "cost_score": 0.880,
  "error_rate": 0.05,
  "error_score": 0.950,
  "weighted_total_score": 0.856,
  "experiment_url": "https://smith.langchain.com/..."
}
```

## ✅ Critérios de Sucesso

- [ ] Skills de evaluation consultadas (evaluation-developer, evals-automator, datasets-evals, quick-evals)
- [ ] Diretório `evaluators/scripts/` criado (se não existia)
- [ ] **Comando analisou** cada dataset em `datasets/` usando `Read`
- [ ] **Comando detectou** para cada dataset: tipo de tarefa, tipo de output, presença de referência, campos de input/output
- [ ] **Comando decidiu** critérios LLM-as-Judge apropriados para cada dataset (CORRECTNESS, RELEVANCE, CONCISENESS, etc.)
- [ ] **Comando criou** dict `dataset_evaluators` mapeando datasets → configuração LLM-as-Judge (tipo, critério, chaves)
- [ ] Script `upload_datasets.py` criado com skip logic
- [ ] `load_dotenv()` adicionado no início de `upload_datasets.py`
- [ ] Configuração de `sys.path` adicionada em `upload_datasets.py`
- [ ] Script `quick_evals.py` criado com 5 métricas ponderadas
- [ ] `load_dotenv()` adicionado no início de `quick_evals.py`
- [ ] Configuração de `sys.path` adicionada em `quick_evals.py`
- [ ] **Constante `DATASET_EVALUATORS`** preenchida com configuração completa de LLM-as-Judge (critérios + chaves)
- [ ] LLM-as-Judge implementado usando `create_llm_as_judge` do LangSmith
- [ ] Função `select_evaluators_for_dataset()` usa `create_llm_as_judge` com critérios do `DATASET_EVALUATORS`
- [ ] Critérios LLM-as-Judge customizados por dataset baseado na análise feita pelo comando
- [ ] Pesos das métricas configuráveis e somam 1.0
- [ ] Métricas normalizadas para 0-1 corretamente
- [ ] Score total calculado com ponderação
- [ ] Script orquestrador `run_all_evals.py` criado
- [ ] README.md com documentação completa gerado
- [ ] Exemplo de target function incluído
- [ ] Error handling implementado
- [ ] Resultados salvos em JSON
- [ ] Formato de output claro e tabular
- [ ] Validação sintática passa (opcional)

## 📝 Exemplo de Uso

```bash
# Criar scripts de evaluation
/create-script-evals

# Executar pipeline completo
uv run evaluators/scripts/run_all_evals.py

# Ou executar individualmente
uv run evaluators/scripts/upload_datasets.py
uv run evaluators/scripts/quick_evals.py
```

## ❌ Anti-Patterns

### ❌ Erro 1: Pesos não somam 100%

Não configure pesos que não somam 1.0:

```python
# ❌ Errado - Soma = 0.95
METRIC_WEIGHTS = {
    "accuracy": 0.45,
    "relevance": 0.20,
    "latency": 0.15,
    "cost": 0.10,
    "errors": 0.05
}

# ✅ Correto - Soma = 1.0
METRIC_WEIGHTS = {
    "accuracy": 0.45,
    "relevance": 0.20,
    "latency": 0.15,
    "cost": 0.15,
    "errors": 0.05
}
```

### ❌ Erro 2: Não normalizar métricas

Não use métricas em escalas diferentes diretamente:

```python
# ❌ Errado - Latency em ms (0-2000), accuracy em 0-1
score = accuracy + latency_ms  # Escalas incompatíveis!

# ✅ Correto - Normalizar para 0-1
latency_score = normalize_score(latency_ms, 0, 2000, invert=True)
score = accuracy * 0.5 + latency_score * 0.5
```

### ❌ Erro 3: Hardcoded dataset names

Não hardcode nomes de datasets:

```python
# ❌ Errado
results = evaluate(target, data="my-specific-dataset")

# ✅ Correto - Configurável
DATASET_NAME = os.getenv("EVAL_DATASET", "golden-dataset")
results = evaluate(target, data=DATASET_NAME)
```

### ❌ Erro 4: Ignorar errors no upload

Não ignore erros silenciosamente:

```python
# ❌ Errado
try:
    client.create_dataset(name)
except:
    pass  # Silent fail!

# ✅ Correto
try:
    existing = client.read_dataset(dataset_name=name)
    print(f"✅ Dataset '{name}' já existe. Skipping.")
    return name
except:
    # Create new
    dataset = client.create_dataset(dataset_name=name)
    print(f"📤 Created new dataset '{name}'")
```

### ❌ Erro 5: Não carregar variáveis de ambiente do .env

Não esquecer de carregar o arquivo `.env` no início dos scripts:

```python
# ❌ Errado - 401 "Invalid token" error
from langsmith import Client
# LANGSMITH_API_KEY não foi carregada do .env
client = Client()

# ✅ Correto - Carregar .env primeiro
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()  # Carrega LANGSMITH_API_KEY e outras variáveis
client = Client()
```

**Consequências de não usar `load_dotenv()`**:
- Erro 401 "Invalid token" ao autenticar com LangSmith
- Variáveis do `.env` não são carregadas no ambiente
- Scripts falham mesmo com `.env` configurado corretamente

### ❌ Erro 6: Não configurar Python path para imports de projeto

Não esquecer de adicionar o diretório raiz do projeto ao `sys.path`:

```python
# ❌ Errado - ModuleNotFoundError ao importar módulos do projeto
from langsmith import Client
# Tentando importar módulos do projeto, mas sys.path não configurado
from my_project.utils import helper_function  # Falha!

# ✅ Correto - Configurar sys.path primeiro
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Agora imports funcionam
from langsmith import Client
from my_project.utils import helper_function  # Sucesso!
```

**Por que `.parents[2]`?**
- Script está em: `project_root/evaluators/scripts/upload_datasets.py`
- `.parents[0]`: `evaluators/scripts/upload_datasets.py` (o próprio arquivo)
- `.parents[1]`: `evaluators/scripts/` (diretório pai)
- `.parents[2]`: `evaluators/` (diretório avô)
- `.parents[3]`: `project_root/` (raiz do projeto) ← Este é o objetivo!

**Ajuste conforme sua estrutura**:
- `project_root/scripts/`: Use `.parents[1]`
- `project_root/evaluators/scripts/`: Use `.parents[2]` (padrão)
- `project_root/foo/bar/scripts/`: Use `.parents[3]`

### ❌ Erro 7: Gerar script com critérios LLM-as-Judge fixos sem analisar datasets

Não gere `quick_evals.py` com configuração vazia ou critérios genéricos:

```python
# ❌ Errado - Configuração vazia
DATASET_EVALUATORS = {}

# ❌ Errado - Todos datasets com mesmo critério genérico
DATASET_EVALUATORS = {
    "qa-dataset": {"type": "llm_as_judge", "criteria": "CORRECTNESS", ...},
    "summary-dataset": {"type": "llm_as_judge", "criteria": "CORRECTNESS", ...},
    "safety-test": {"type": "llm_as_judge", "criteria": "CORRECTNESS", ...}
}
# CORRECTNESS pode não ser apropriado para summarization (CONCISENESS) ou safety (HARMFULNESS)

# ✅ Correto - Comando analisa datasets ANTES e seleciona critérios apropriados

# 1. Comando usa Read para ler cada dataset
# 2. Comando detecta:
#    - Tipo de tarefa (Q&A, summarization, generation, chatbot, safety)
#    - Presença de referência (ground truth)
#    - Natureza da avaliação (precisão, brevidade, utilidade, segurança)
#    - Campos de input/output
# 3. Comando decide critério LLM-as-Judge apropriado
# 4. Comando gera quick_evals.py com configuração customizada:

DATASET_EVALUATORS = {
    "qa-dataset": {
        "type": "llm_as_judge",
        "criteria": "CORRECTNESS",  # Q&A com referência → precisão factual
        "input_keys": ["question"],
        "reference_output_keys": ["expected_answer"],
        "prediction_key": "answer"
    },
    "summary-dataset": {
        "type": "llm_as_judge",
        "criteria": "CONCISENESS",  # Summarization → brevidade
        "input_keys": ["text"],
        "reference_output_keys": ["summary"],
        "prediction_key": "output"
    },
    "chatbot-dataset": {
        "type": "llm_as_judge",
        "criteria": "HELPFULNESS",  # Chatbot → utilidade
        "input_keys": ["user_message"],
        "reference_output_keys": None,
        "prediction_key": "response"
    },
    "safety-test": {
        "type": "llm_as_judge",
        "criteria": "HARMFULNESS",  # Safety → detectar dano
        "input_keys": ["prompt"],
        "reference_output_keys": None,
        "prediction_key": "completion"
    }
}
```

**Por que o comando deve analisar datasets ANTES**:
- Cada tipo de tarefa precisa de critério LLM-as-Judge específico
- CORRECTNESS não funciona para summarization (use CONCISENESS)
- HELPFULNESS não funciona para safety tests (use HARMFULNESS)
- Critério errado gera scores sem sentido ou avaliações incorretas
- Análise em tempo de execução do comando é mais eficiente
- Script gerado já vem customizado por tipo de tarefa

**Consequências de não analisar no comando**:
- Avaliações com critérios inapropriados (ex: CORRECTNESS para safety)
- Scores sem sentido (ex: medir concisão em vez de segurança)
- Falhas silenciosas ou resultados enganosos
- Usuário precisa editar manualmente a configuração
- Perda de tempo com avaliações irrelevantes
