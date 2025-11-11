# LLMOps Workflow for LLM-as-Judge

Guia completo de integração do LLM-as-Judge no ciclo de vida de desenvolvimento (LLMOps), cobrindo avaliação offline/online, experiments, debugging, métricas combinadas e decisões de deployment.

## 🔄 Ciclo de Vida LLMOps com LLM-as-Judge

```
┌─────────────────────────────────────────────────────────┐
│          LLMOps Development Cycle                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. DEVELOP                                             │
│     ├── Iterar prompts/chains                           │
│     └── Quick Evals (subset dataset, < 5min)            │
│              ↓                                          │
│  2. EVALUATE (Offline - End of Sprint)                  │
│     ├── Full dataset evaluation                         │
│     ├── LLM-as-Judge + metrics (latency, cost)          │
│     └── Create Experiment in LangSmith                  │
│              ↓                                          │
│  3. COMPARE (A/B Testing)                               │
│     ├── Compare Experiments (v1 vs v2)                  │
│     ├── Heatmap analysis                                │
│     └── Decide: deploy, iterate, or rollback            │
│              ↓                                          │
│  4. DEBUG (If Needed)                                   │
│     ├── Traces: why low score?                          │
│     ├── Fix prompt/logic                                │
│     └── Re-evaluate (back to step 2)                    │
│              ↓                                          │
│  5. DEPLOY                                              │
│     ├── Promote to production                           │
│     └── Enable online evaluators                        │
│              ↓                                          │
│  6. MONITOR (Continuous)                                │
│     ├── Online LLM-as-Judge in real-time                │
│     ├── Alerts on quality degradation                   │
│     └── Feedback loop (back to step 1)                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 1. Avaliação Offline (End of Sprint)

### 1.1 O Que é Avaliação Offline

**Definição**: Avaliação executada em dataset estático **antes** de deploy em produção.

**Características:**

- ✅ Dataset versionado e imutável
- ✅ Execução batch (não real-time)
- ✅ Resultados armazenados em Experiment
- ✅ Comparável entre versões

**Quando executar:**

- 🔄 Final de cada sprint/iteração
- 🔄 Antes de merge de PR
- 🔄 Antes de deploy em staging
- 🔄 Quando mudança significativa no prompt/modelo

### 1.2 Setup de Avaliação Formal

**Workflow recomendado:**

```python
from langsmith import Client
from langsmith.evaluation import evaluate, create_llm_as_judge

# 1. Setup
client = Client()

# 2. Criar/usar dataset estável
dataset = client.read_dataset(dataset_name="golden-qa-eval")

# 3. Definir evaluators
judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",
    input_keys=["question"],
    reference_output_keys=["expected_answer"],
    prediction_key="answer"
)

# Evaluators adicionais (latência, custo)
from langsmith.evaluation import metrics

latency_evaluator = metrics.latency()
cost_evaluator = metrics.cost()

# 4. Executar avaliação formal
results = evaluate(
    target_function=my_qa_app,
    data="golden-qa-eval",
    evaluators=[judge, latency_evaluator, cost_evaluator],
    experiment_prefix="sprint-5-final",
    max_concurrency=10
)

# 5. Revisar resultados
print(f"Quality Score: {results.aggregate_score}")
print(f"Experiment URL: {results.experiment_url}")
```

### 1.3 Métricas a Capturar

**Qualidade (LLM-as-Judge):**

- Score médio (0-1)
- Distribuição de scores
- Taxa de falha (score = 0)

**Performance:**

- Latência média (segundos)
- P95 latency
- Timeout rate

**Custo:**

- Custo por query (USD)
- Custo total do experiment
- Token usage (input + output)

**Exemplo de log:**

```python
# Resultados do experiment
{
    "quality": {
        "mean_score": 0.85,
        "score_distribution": {"0": 5, "1": 35},  # 5 falhas, 35 sucessos
        "failure_rate": 0.125  # 12.5%
    },
    "performance": {
        "mean_latency_ms": 450,
        "p95_latency_ms": 780,
        "timeout_rate": 0.02
    },
    "cost": {
        "total_usd": 0.42,
        "per_query_usd": 0.0105,
        "total_tokens": 15000
    }
}
```

### 1.4 Quick Evals vs Full Evals

**Quick Evals** (Iteração Rápida):

- ✅ Subset pequeno (20-50 examples)
- ✅ Executado frequentemente (a cada mudança)
- ✅ Tempo: < 5 minutos
- ✅ Custo: < $0.10

```python
# Quick eval setup
quick_eval = evaluate(
    data="golden-qa-eval",
    evaluators=[judge],
    max_concurrency=10,
    limit=20  # Apenas 20 examples!
)
```

**Full Evals** (Validação Formal):

- ✅ Dataset completo (100-1000s examples)
- ✅ Executado no final do sprint
- ✅ Tempo: 10-60 minutos
- ✅ Custo: $1-10

```python
# Full eval setup
full_eval = evaluate(
    data="golden-qa-eval",  # Todos examples
    evaluators=[judge, latency_evaluator, cost_evaluator],
    max_concurrency=10
)
```

**Estratégia recomendada:**

```
Durante desenvolvimento:
├── Quick evals (frequentes)
└── Feedback rápido (< 5min)

Final do sprint:
├── Full eval (validação)
└── Decisão de deploy
```

## 2. Experiments - Comparação A/B

### 2.1 O Que é um Experiment

**Definição**: Registro de uma execução de avaliação, incluindo dataset, evaluators, target function e resultados.

**Metadados armazenados:**

- Dataset name + version
- Evaluator configs
- Timestamp
- Git commit (se configurado)
- Results (scores, latencies, custos)

### 2.2 Criando Experiments Comparáveis

**Regra de ouro**: Mudar APENAS 1 variável por experiment

**Exemplo: Comparar 2 prompts**

```python
# Experiment 1: Prompt V1
results_v1 = evaluate(
    target_function=app_with_prompt_v1,
    data="qa-eval",
    evaluators=[judge],
    experiment_prefix="prompt-v1"
)

# Experiment 2: Prompt V2 (MESMOS dataset + evaluators!)
results_v2 = evaluate(
    target_function=app_with_prompt_v2,
    data="qa-eval",  # MESMO dataset
    evaluators=[judge],  # MESMO evaluator
    experiment_prefix="prompt-v2"
)

# Comparar no LangSmith UI:
# Navigate to Experiments → Compare (prompt-v1 vs prompt-v2)
```

**Variáveis que podem ser testadas:**

- Prompt template
- Modelo LLM (gpt-4 vs gpt-3.5)
- Temperatura
- Chain logic
- Retrieval strategy (RAG)

### 2.3 Análise Comparativa

**Heatmap Comparison:**

- Visualizar scores lado a lado
- Identificar examples onde v2 > v1
- Identificar regressions (v2 < v1)

**Score delta:**

```python
# Calcular diferença
delta = results_v2.aggregate_score - results_v1.aggregate_score

if delta > 0.05:  # Melhoria significativa
    print("✅ Deploy v2")
elif delta < -0.05:  # Regressão
    print("❌ Rollback, keep v1")
else:  # Neutro
    print("⚠️ Avaliar outros fatores (latência, custo)")
```

**ROI Analysis:**

```python
# Combinar qualidade + custo
roi_v1 = results_v1.aggregate_score / results_v1.total_cost
roi_v2 = results_v2.aggregate_score / results_v2.total_cost

if roi_v2 > roi_v1:
    print("✅ v2 tem melhor ROI")
```

### 2.4 Decisão de Deploy

**Framework de decisão:**

| Score Δ | Latency Δ | Cost Δ | Decisão |
|---------|-----------|--------|---------|
| +10% | 0% | 0% | ✅ Deploy (win claro) |
| +5% | +20% | +50% | ⚠️ Avaliar trade-off |
| -5% | -50% | -70% | ⚠️ Avaliar se performance vale regressão |
| -10% | 0% | 0% | ❌ Não deploy (regressão) |

**Checklist de decisão:**

- [ ] Quality score melhorou OU manteve?
- [ ] Não há regressions críticas (ex: 0% → 100% failure em categoria específica)?
- [ ] Latência está dentro de SLA (ex: < 1s)?
- [ ] Custo está dentro de budget?
- [ ] Stakeholders aprovaram?

## 3. Debugging com LangSmith UI

### 3.1 Ferramentas de Debug

**Heatmap:**

- Visualização de scores por example
- Cores: verde (1.0), amarelo (0.5), vermelho (0.0)
- Identificar patterns de falha

**Traces:**

- Detalhamento de cada run
- Input → LLM calls → Output
- Tempo de cada step
- Prompt enviado ao modelo

**Comments:**

- Justificativas do LLM-as-Judge
- Por que score foi X?

### 3.2 Workflow de Debug

**Cenário**: Aggregate score = 0.7 (esperava > 0.85)

**Passo 1: Identificar failures no Heatmap**

```
Navigate to: Experiment → Heatmap
Filter: score < 0.5
Result: 10 examples com score baixo
```

**Passo 2: Analisar Traces de failures**

```
Click em example com score = 0
Ver Trace:
- Input: {"question": "..."}
- Target output: {"answer": "..."}
- Judge output: {"score": 0, "comment": "Erro factual: ..."}
```

**Passo 3: Categorizar erros**

```
Erro 1: Prompt ambíguo (5 cases)
Erro 2: Retrieval falhou (3 cases)
Erro 3: Modelo LLM alucinando (2 cases)
```

**Passo 4: Priorizar fixes**

```
Fix 1: Clarificar prompt (impacto: +12% score)
Fix 2: Melhorar retrieval (impacto: +7% score)
Fix 3: Adicionar guardrails anti-alucinação (impacto: +5% score)
```

**Passo 5: Implementar + Re-avaliar**

```python
# Aplicar fix 1
fixed_app = update_prompt(...)

# Re-avaliar
results_fixed = evaluate(
    target_function=fixed_app,
    data="qa-eval",
    evaluators=[judge],
    experiment_prefix="post-fix-1"
)

# Comparar: original (0.70) vs fixed (0.82) ✅
```

### 3.3 Debugging do Judge Itself

**Problema**: Judge parece errado (ex: dando score alto para resposta claramente incorreta)

**Debug do judge:**

**Passo 1: Ver prompt enviado ao judge**

```
Trace → Judge LLM call → Input (prompt)
```

**Passo 2: Verificar mapeamento de chaves**

```
# Esperado:
{question}: "Capital da França?"
{expected_answer}: "Paris"
{generated_answer}: "Londres"  # ❌ Incorreto

# Se judge deu score = 1, investigar:
# - Prompt não menciona "compare com expected_answer"?
# - Judge tem positivity bias?
```

**Passo 3: Testar judge isoladamente**

```python
# Teste unitário do judge
test_input = {"question": "Capital da França?"}
test_reference = {"expected_answer": "Paris"}
test_prediction = {"generated_answer": "Londres"}  # Incorreta

judge_result = judge(
    inputs=test_input,
    outputs=test_reference,
    prediction=test_prediction
)

# Esperado: score = 0
# Se score = 1: judge está quebrado!
```

**Passo 4: Calibrar judge**

- Adicionar few-shot examples
- Revisar prompt para ser mais crítico
- Usar human corrections no LangSmith

## 4. Métricas Combinadas (Weighted Score)

### 4.1 Por Que Combinar Métricas

**Problema**: Score alto de qualidade pode vir com:

- ❌ Latência inaceitável (5s+ por query)
- ❌ Custo proibitivo ($1+ por query)

**Solução**: Weighted score que balanceia qualidade + performance + custo

### 4.2 Fórmula de Weighted Score

```python
# Normalizar métricas (0-1)
quality_norm = quality_score  # Já está 0-1
latency_norm = 1 - (latency_ms / max_acceptable_latency_ms)
cost_norm = 1 - (cost_usd / max_acceptable_cost_usd)

# Weighted average
weighted_score = (
    0.6 * quality_norm +      # 60% peso em qualidade
    0.3 * latency_norm +      # 30% peso em performance
    0.1 * cost_norm           # 10% peso em custo
)
```

**Ajustar pesos por prioridade do negócio:**

| Cenário | Quality | Latency | Cost |
|---------|---------|---------|------|
| Médico/Legal | 0.8 | 0.1 | 0.1 | (Qualidade crítica) |
| Chatbot | 0.5 | 0.4 | 0.1 | (Latência importante) |
| Análise batch | 0.7 | 0.1 | 0.2 | (Custo importante) |

### 4.3 Implementação

```python
def calculate_weighted_score(
    quality: float,
    latency_ms: float,
    cost_usd: float,
    quality_weight: float = 0.6,
    latency_weight: float = 0.3,
    cost_weight: float = 0.1,
    max_latency_ms: float = 1000,
    max_cost_usd: float = 0.05
) -> float:
    """
    Calcular score ponderado combinando qualidade + performance + custo.
    """
    # Normalizar (0-1)
    quality_norm = quality
    latency_norm = max(0, 1 - (latency_ms / max_latency_ms))
    cost_norm = max(0, 1 - (cost_usd / max_cost_usd))

    # Weighted average
    weighted = (
        quality_weight * quality_norm +
        latency_weight * latency_norm +
        cost_weight * cost_norm
    )

    return weighted

# Uso
weighted = calculate_weighted_score(
    quality=0.85,
    latency_ms=450,
    cost_usd=0.01
)
# Resultado: 0.82 (bom!)
```

### 4.4 Decisão Informada

**Cenário: Comparar 2 versões**

```python
# V1: Alta qualidade, lenta, cara
v1_weighted = calculate_weighted_score(
    quality=0.90, latency_ms=1200, cost_usd=0.08
)  # 0.70

# V2: Qualidade razoável, rápida, barata
v2_weighted = calculate_weighted_score(
    quality=0.80, latency_ms=300, cost_usd=0.01
)  # 0.85

# Decisão: V2 wins (melhor balanceamento)
```

## 5. Avaliação Online (Produção)

### 5.1 O Que é Avaliação Online

**Definição**: Avaliação executada em **tempo real** em produção, aplicada a cada request de usuário.

**Características:**

- ✅ Aplica evaluators a production runs
- ✅ Sem reference outputs (geralmente)
- ✅ Detecta degradação de qualidade
- ✅ Permite HITL (Human-in-the-Loop)

**Diferença de Offline:**

| Aspecto | Offline | Online |
|---------|---------|--------|
| Quando | Pré-deploy | Produção (real-time) |
| Dataset | Estático | Production runs |
| Reference | Disponível | Geralmente não |
| Latência | Não importa | Crítica (< 100ms overhead) |

### 5.2 Configurando Online Evaluators

**Setup no LangSmith:**

```python
from langsmith import Client

client = Client()

# 1. Criar online evaluator
client.create_online_evaluator(
    name="production-relevance-judge",
    evaluator=create_llm_as_judge(
        criteria="RELEVANCE",  # Não requer reference
        model="openai:gpt-4o-mini",
        input_keys=["query"],
        prediction_key="response"
    ),
    project_name="production-chatbot",  # Aplicar a este projeto
    sampling_rate=0.1  # Avaliar 10% dos runs (economizar custo)
)
```

**Sampling rate trade-off:**

- 1.0 (100%): Máxima cobertura, alto custo
- 0.1 (10%): Amostra representativa, custo controlado
- 0.01 (1%): Monitoramento básico, muito econômico

### 5.3 Casos de Uso de Online Eval

**1. Quality Monitoring**

- Detectar degradação gradual
- Alertar se score médio cai abaixo de threshold

**2. A/B Testing em Produção**

- 50% tráfego → v1
- 50% tráfego → v2
- Comparar scores online

**3. Human-in-the-Loop (HITL)**

- LLM-as-Judge avalia automaticamente
- Humanos revisam casos de baixo score
- Feedback humano melhora judge

**4. Safety Guardrails**

- Online judge de harmfulness
- Bloquear resposta se score alto de harmful
- Log para revisão

### 5.4 Alerting

**Setup de alerts:**

```python
# Pseudo-código (via LangSmith UI ou API)
client.create_alert(
    name="quality-degradation",
    condition="avg_score < 0.7",  # Threshold
    window="1 hour",  # Janela de tempo
    action="send_email",  # email, slack, webhook
    recipients=["team@example.com"]
)
```

**Tipos de alerts:**

- Quality degradation (score médio caindo)
- High failure rate (% de score = 0)
- Latency spike (P95 > threshold)
- Cost spike (custo/query > budget)

## 6. Integração com CI/CD

### 6.1 Eval como Gate de CI/CD

**Workflow:**

```yaml
# .github/workflows/eval.yml
name: LangSmith Evaluation

on:
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run LangSmith Eval
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
        run: |
          python scripts/run_eval.py

      - name: Check Score Threshold
        run: |
          SCORE=$(cat eval_results.json | jq '.aggregate_score')
          if (( $(echo "$SCORE < 0.80" | bc -l) )); then
            echo "❌ Score $SCORE below threshold 0.80"
            exit 1
          fi
          echo "✅ Score $SCORE passes threshold"
```

**Benefício**: Bloqueia merge se qualidade regressar

### 6.2 Script de Avaliação

```python
# scripts/run_eval.py
import json
from langsmith import Client
from langsmith.evaluation import evaluate, create_llm_as_judge

def main():
    # Setup
    judge = create_llm_as_judge(...)

    # Executar eval
    results = evaluate(
        target_function=my_app,
        data="ci-dataset",  # Dataset pequeno para CI (fast)
        evaluators=[judge],
        experiment_prefix=f"ci-pr-{os.getenv('PR_NUMBER')}"
    )

    # Salvar resultados
    with open("eval_results.json", "w") as f:
        json.dump({
            "aggregate_score": results.aggregate_score,
            "experiment_url": results.experiment_url
        }, f)

    # Exit code baseado em threshold
    if results.aggregate_score < 0.80:
        print(f"❌ Failed: {results.aggregate_score}")
        exit(1)
    else:
        print(f"✅ Passed: {results.aggregate_score}")
        exit(0)

if __name__ == "__main__":
    main()
```

### 6.3 Regression Testing

**Pattern**: Rodar eval antes de cada release

```python
# Pre-release checklist
def pre_release_eval():
    # 1. Full eval em dataset golden
    results = evaluate(data="golden-dataset", ...)

    # 2. Comparar com baseline (última release)
    baseline_score = get_last_release_score()
    current_score = results.aggregate_score

    # 3. Bloquear se regressão
    if current_score < baseline_score - 0.05:  # 5% tolerance
        raise Exception("Quality regression detected!")

    # 4. Atualizar baseline
    update_baseline(current_score)
```

## 7. Best Practices LLMOps

### 7.1 Checklist de Integração

**Durante Desenvolvimento:**

- [ ] Quick evals configurados (< 5min)?
- [ ] Feedback rápido a cada mudança?

**Final de Sprint:**

- [ ] Full eval executado em dataset golden?
- [ ] Experiment criado com nome descritivo?
- [ ] Métricas combinadas calculadas (quality + latency + cost)?
- [ ] Comparação A/B com versão anterior?

**Antes de Deploy:**

- [ ] Score acima de threshold (ex: > 0.80)?
- [ ] Sem regressions críticas?
- [ ] Stakeholders aprovaram?
- [ ] Latência e custo aceitáveis?

**Pós-Deploy:**

- [ ] Online evaluators habilitados?
- [ ] Alerts configurados (quality, latency, cost)?
- [ ] Sampling rate apropriado (10-20%)?
- [ ] HITL planejado para casos de baixo score?

### 7.2 Versionamento de Artifacts

**O que versionar:**

- ✅ Datasets (automático no LangSmith)
- ✅ Prompt templates (Git)
- ✅ Evaluator configs (Git)
- ✅ Experiment results (LangSmith)

**Exemplo de estrutura Git:**

```
repo/
├── prompts/
│   ├── v1.txt
│   └── v2.txt
├── evaluators/
│   └── correctness_judge.py
├── datasets/
│   └── golden_qa_v3.json  # Backup local
└── experiments/
    └── sprint_5_results.json
```

### 7.3 Evitando Overfitting ao Dataset

**Problema**: Otimizar demais para dataset golden → não generaliza em produção

**Soluções:**

**1. Múltiplos datasets:**

```python
# Dataset 1: Curado (golden)
eval_golden = evaluate(data="golden-dataset", ...)

# Dataset 2: Production sample
eval_prod = evaluate(data="production-sample", ...)

# Ambos devem passar threshold!
```

**2. Holdout set:**

```python
# 80% training/dev (iteração)
# 20% holdout (validação final)

# Iterar em dev set
dev_results = evaluate(data="dev-set", ...)

# Validar em holdout (apenas 1x antes de deploy!)
holdout_results = evaluate(data="holdout-set", ...)
```

**3. Refresh periódico:**

```
A cada 3-6 meses:
├── Adicionar novos examples (edge cases de produção)
├── Remover examples obsoletos
└── Re-validar todos prompts
```

## 8. Troubleshooting LLMOps

**Problema**: Eval passa em CI mas falha em produção

- ✅ CI dataset muito fácil (não representa produção)
- ✅ Solução: Usar production sample como dataset CI

**Problema**: Online evals aumentam latência

- ✅ Sampling rate muito alto (100%)
- ✅ Solução: Reduzir para 10-20% ou async evaluation

**Problema**: Alerts falsos (muito ruído)

- ✅ Threshold muito sensível
- ✅ Solução: Aumentar janela de tempo (1h → 4h)

**Problema**: Experiments não comparáveis

- ✅ Dataset mudou entre experiments
- ✅ Solução: Pin dataset version nos experiments

## 9. Métricas de Sucesso LLMOps

**Velocidade de Iteração:**

- Tempo de feedback: < 5min (quick eval)
- Frequency de evals: diária (durante dev)

**Qualidade:**

- Aggregate score: > 0.80 (threshold)
- Regression rate: < 5% (comparado a baseline)

**Eficiência:**

- Custo de eval: < 10% do custo de produção
- Tempo de debug: < 2h (de identificação a fix)

**Confiabilidade:**

- False positive rate (bad deploy): < 2%
- Alert noise: < 10% (alertas falsos)

## 10. Roadmap de Adoção

**Semana 1-2: Setup Básico**

- [ ] Criar dataset golden (50 examples)
- [ ] Implementar primeiro LLM-as-Judge
- [ ] Executar eval manual

**Semana 3-4: Automação**

- [ ] Integrar eval em CI/CD
- [ ] Configurar quick evals para dev
- [ ] Estabelecer threshold de qualidade

**Semana 5-6: Refinamento**

- [ ] Adicionar métricas combinadas (weighted score)
- [ ] Implementar A/B testing workflow
- [ ] Calibrar judge com few-shot/human feedback

**Semana 7-8: Produção**

- [ ] Habilitar online evaluators
- [ ] Configurar alerts de qualidade
- [ ] HITL para casos de baixo score

**Mês 3+: Otimização**

- [ ] Expandir coverage de dataset (100+ examples)
- [ ] Múltiplos judges (multi-aspect eval)
- [ ] Regression testing automatizado
