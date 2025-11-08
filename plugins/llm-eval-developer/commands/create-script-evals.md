---
description: Create automated evaluation script for LLM golden datasets with LangSmith integration
allowed-tools: Read, Write, Bash, Glob, Grep, Skill
model: claude-sonnet-4-5
argument-hint: '[EVALUATORS_DIR] [DATASETS_DIR]'
---

# Create Script Evals

Cria script automatizado que coleta informações de skills, envia datasets para LangSmith, executa quick-evals em golden datasets, e extrai métricas com ponderação customizada.

## 🎯 Objetivo

Este comando gera um script Python completo que:

- 🔍 Coleta informações de skills necessárias do projeto
- 📤 Envia datasets da pasta `datasets/` para LangSmith (skip se já existir)
- ⚡ Configura e executa quick-evals sobre golden datasets no LangSmith
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
Skill(skill="llm-eval-developer:evals-automator")
Skill(skill="llm-eval-developer:datasets-evals")
Skill(skill="llm-eval-developer:quick-evals")
```

1.2 **Extrair Patterns de Evaluation**

Das skills, extrair:

- Como criar evaluators customizados
- Integração com LangSmith API
- Patterns de dataset upload
- Métricas disponíveis (accuracy, relevance, latency, cost, errors)

### Passo 2: Analisar Estrutura Atual

2.1 **Verificar Diretórios**

- Usar `Glob` para verificar se `evaluators/scripts/` existe
- Criar diretório se não existir usando `Bash(mkdir -p evaluators/scripts/)`
- Verificar se `datasets/` existe e contém arquivos

2.2 **Escanear Datasets Existentes**

- Usar `Glob` para listar arquivos em `datasets/` (JSON, JSONL, CSV)
- Usar `Read` para verificar formato e estrutura de 1-2 exemplos
- Determinar schema necessário para LangSmith

### Passo 3: Criar Script de Upload de Datasets

3.1 **Gerar `upload_datasets.py`**

Criar script que:

```python
"""
Upload Datasets para LangSmith
Skip se dataset já existir no LangSmith.
"""

import os
import json
from pathlib import Path
from langsmith import Client

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

4.1 **Gerar `quick_evals.py`**

Criar script que executa evaluations sobre golden datasets:

```python
"""
Quick Evaluations sobre Golden Datasets no LangSmith
Executa evaluations e extrai métricas com ponderação customizada.
"""

import os
from typing import Dict, List
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langchain_core.callbacks import BaseCallbackHandler
import numpy as np
import time
import json

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


# ==================== EVALUATORS ====================

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

def run_quick_eval(
    target_function,
    dataset_name: str,
    experiment_prefix: str = "quick-eval"
) -> Dict[str, float]:
    """
    Executa quick evaluation sobre golden dataset.

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

    # Evaluators nativos do LangSmith
    evaluators = [
        LangChainStringEvaluator("qa"),           # Accuracy
        LangChainStringEvaluator("context_qa"),   # Relevance
    ]

    # Executar evaluation
    print(f"🔍 Running evaluation on dataset '{dataset_name}'...")

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

4.2 **Salvar Script**

Usar `Write` para criar `evaluators/scripts/quick_evals.py`

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
- `quick_evals.py`: Executa evaluations com métricas ponderadas
- `run_all_evals.py`: Orquestrador principal (executa tudo em ordem)
- `eval_results.json`: Resultados da última execução

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

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Configure as seguintes variáveis no `.env`:

```bash
LANGCHAIN_API_KEY=your-api-key
LANGCHAIN_PROJECT=your-project-name
LANGCHAIN_TRACING_V2=true
OPENAI_API_KEY=your-openai-key  # ou outro provider
```

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

### Erro: LangSmith API Key

Configure `LANGCHAIN_API_KEY` no `.env`.

### Erro: Nenhum dataset encontrado

Verifique se há arquivos `.json` ou `.jsonl` em `datasets/`.

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

- [ ] Skills de evaluation consultadas (evaluation-developer, benchmark-runner)
- [ ] Diretório `evaluators/scripts/` criado (se não existia)
- [ ] Script `upload_datasets.py` criado com skip logic
- [ ] Script `quick_evals.py` criado com 5 métricas ponderadas
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
