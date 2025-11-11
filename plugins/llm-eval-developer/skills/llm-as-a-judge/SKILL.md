---
name: llm-as-a-judge
description: LLM-as-a-Judge evaluation with LangSmith - datasets, judge prompts, criteria, and LLMOps workflow. Use when implementing LLM evaluators, designing judge prompts, creating evaluation datasets, running offline evaluations, or measuring subjective quality metrics (correctness, relevance, coherence). Essential for LangSmith evaluate() workflows.
version: 1.0.0
allowed-tools:
  - Read
  - Grep
  - Bash
---

# LLM-as-a-Judge Evaluation with LangSmith

Conhecimento especializado para implementar avaliações usando LLM como juiz (LLM-as-Judge) no ecossistema LangSmith, cobrindo infraestrutura de datasets, engenharia de prompts para juízes e integração com ciclo de vida LLMOps.

## 📋 When to Use Me

Invoque esta skill automaticamente quando:

- **Implementar LLM-as-Judge evaluators** no LangSmith
- **Criar ou configurar datasets** de avaliação com reference outputs
- **Desenhar prompts para modelos juízes** (critérios, scoring, justificativas)
- **Mapear chaves de dados** (input_keys, reference_output_keys, prediction_key)
- **Executar avaliações offline** usando `langsmith.evaluate()`
- **Avaliar critérios subjetivos** (correção, relevância, concisão, coerência)
- **Debugar avaliações** usando LangSmith UI (heatmaps, traces)
- **Combinar métricas qualitativas + quantitativas** (score + latência + custo)
- **Configurar avaliação contínua** em produção (online evaluators)

**Gatilhos específicos:**

- "LLM as judge"
- "create_llm_as_judge"
- "evaluation criteria"
- "judge prompt"
- "offline evaluation LangSmith"
- "dataset reference outputs"

## 🎓 Core Knowledge

### 1. O Que é LLM-as-a-Judge

**Definição**: Técnica de avaliação híbrida onde um LLM atua como avaliador para critérios **subjetivos** que não podem ser capturados por regras determinísticas.

**Quando usar LLM-as-Judge:**

- ✅ Critérios subjetivos: relevância, coerência, tom, helpfulness
- ✅ Avaliação de qualidade factual (com ground truth)
- ✅ Comparações pairwise (qual resposta é melhor?)
- ✅ Safety e harmfulness detection

**Quando NÃO usar:**

- ❌ Métricas objetivas simples (latência, custo, token count)
- ❌ Validação de formato estruturado (JSON schema)
- ❌ Métricas determinísticas (exact match, regex)

### 2. Três Pilares Fundamentais

#### Pilar 1: Infraestrutura LangSmith

- **Datasets**: Coleção versionada de Examples (inputs + reference outputs)
- **Target Function**: Aplicação sob teste (Callable Python)
- **SDK Python**: `langsmith.evaluate()` orquestra dataset + target + evaluators

#### Pilar 2: Engenharia de Prompt Juiz

- **Critérios de avaliação**: CORRECTNESS, RELEVANCE, CONCISENESS, HARMFULNESS
- **Prompt estruturado**: Papel do juiz + dados de entrada + formato de saída (JSON)
- **Mapeamento de chaves**: input_keys, reference_output_keys, prediction_key
- **Modelo juiz**: Seleção do LLM (ex: `openai:gpt-4o-mini`)

#### Pilar 3: LLMOps Workflow

- **Avaliação offline**: Final de sprint/iteração
- **Experiments**: Comparações A/B de prompts/modelos
- **Debugging**: Heatmap + Traces para diagnosticar scores baixos
- **Métricas combinadas**: Score qualitativo + latência + custo
- **Avaliação online**: Monitoramento contínuo em produção

### 3. Estrutura de um Dataset LangSmith

```python
# Example structure
{
    "inputs": {"pergunta": "O que é LangChain?"},
    "outputs": {"resposta_esperada": "LangChain é um framework..."}  # Reference (ground truth)
}
```

**Características críticas:**

- ✅ Versionamento automático pelo LangSmith
- ✅ Reference outputs são cruciais para LLM-as-Judge
- ✅ Inputs mapeados para aplicação alvo
- ✅ Outputs comparados pelo modelo juiz

### 4. Fluxo de Avaliação Offline

```
1. Dataset (inputs + references)
   ↓
2. Target Function (sua aplicação)
   ↓
3. Predictions (outputs gerados)
   ↓
4. LLM Judge (compara prediction vs reference)
   ↓
5. Score + Justificativa
   ↓
6. Experiment Results (LangSmith UI)
```

### 5. Critérios Pré-Construídos do LangSmith

| Critério | O Que Avalia | Exemplo de Uso |
|----------|--------------|----------------|
| `CORRECTNESS` | Precisão factual | Verificar se resposta está correta |
| `RELEVANCE` | Alinhamento com pergunta | Avaliar se resposta é relevante |
| `CONCISENESS` | Brevidade e objetividade | Medir se resposta é concisa |
| `HARMFULNESS` | Conteúdo prejudicial | Testes de safety/guardrails |

### 6. Função create_llm_as_judge

**Função principal**: `create_llm_as_judge()` do SDK LangSmith

**Parâmetros críticos:**

- `criteria`: Critério de avaliação (ex: "CORRECTNESS")
- `model`: Modelo juiz (ex: "openai:gpt-4o-mini")
- `input_keys`: Chaves do dataset inputs (ex: ["pergunta"])
- `reference_output_keys`: Chaves do ground truth (ex: ["resposta_esperada"])
- `prediction_key`: Chave da saída gerada (ex: "resposta")
- `prompt`: Template do prompt juiz (opcional, usa default se não fornecido)

**Exemplo básico:**

```python
from langsmith.evaluation import create_llm_as_judge

judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",
    input_keys=["pergunta"],
    reference_output_keys=["resposta_esperada"],
    prediction_key="resposta"
)
```

### 7. Anatomia de um Prompt Juiz Eficaz

**3 Componentes Obrigatórios:**

1. **Papel do Juiz**: "Você é um avaliador especialista"
1. **Dados de Entrada**: Quais elementos considerar
   - Input original (pergunta)
   - Reference output (ground truth)
   - Prediction (resposta gerada)
1. **Formato de Saída**: JSON estruturado
   ```json
   {
     "score": 1,  // 1 = correto, 0 = incorreto
     "comment": "Justificativa detalhada"
   }
   ```

**Padrões avançados:**

- ✅ Few-shot examples para calibrar juiz
- ✅ Chain-of-thought para raciocínio explícito
- ✅ Rubrica detalhada (escala 1-5 com descrições)
- ✅ Bias correction via human feedback

### 8. Mapeamento de Chaves (Critical!)

**Problema**: Dataset tem chaves diferentes da sua aplicação

**Solução**: Mapear explicitamente no `create_llm_as_judge`

**Exemplo:**

```python
# Dataset Example
{
    "inputs": {"question": "What is AI?"},
    "outputs": {"expected_answer": "AI is..."}
}

# Target Function Output
{
    "answer": "AI stands for..."
}

# Mapeamento correto
judge = create_llm_as_judge(
    input_keys=["question"],              # Do dataset inputs
    reference_output_keys=["expected_answer"],  # Do dataset outputs
    prediction_key="answer"               # Da sua aplicação
)
```

### 9. Execução com langsmith.evaluate()

**Função orquestradora**: `langsmith.evaluate()`

**Workflow:**

1. Busca dataset do LangSmith
1. Executa target function para cada example
1. Aplica evaluators (incluindo LLM-as-Judge)
1. Registra resultados em Experiment

**Exemplo:**

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

results = evaluate(
    target_function=my_app,
    data="my-dataset-name",
    evaluators=[judge],
    experiment_prefix="eval-v1"
)
```

### 10. Métricas Combinadas (ROI Decision)

**Best Practice**: Combinar qualidade + performance + custo

**Fórmula exemplo:**

```python
weighted_score = (
    0.6 * quality_score +    # LLM-as-Judge
    0.3 * (1 - latency_normalized) +
    0.1 * (1 - cost_normalized)
)
```

**Uso**: Decisões A/B informadas (não apenas qualidade!)

## 📚 Reference Files

Para conhecimento detalhado, consulte:

- **INFRASTRUCTURE.md** - LangSmith datasets, target functions, SDK Python, versionamento
- **PROMPT_ENGINEERING.md** - Design de prompts juiz, critérios, few-shot, bias correction
- **LLMOPS.md** - Ciclo de vida completo, Experiments, debugging, avaliação online

## 💡 Quick Examples

### Exemplo 1: Avaliador Simples de Correção

```python
from langsmith.evaluation import create_llm_as_judge, evaluate

# 1. Criar judge para correção factual
correctness_judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",
    input_keys=["pergunta"],
    reference_output_keys=["resposta_esperada"],
    prediction_key="resposta"
)

# 2. Executar avaliação
results = evaluate(
    target_function=my_qa_app,
    data="qa-golden-dataset",
    evaluators=[correctness_judge],
    experiment_prefix="qa-eval"
)

# 3. Ver resultados no LangSmith UI
# Navigate to Experiments → qa-eval → Heatmap
```

### Exemplo 2: Judge Customizado com Prompt

```python
custom_prompt = """
Você é um avaliador especialista em respostas de chatbots.

Entrada:
- Pergunta: {pergunta}
- Resposta Esperada: {resposta_esperada}
- Resposta Gerada: {resposta}

Avalie se a Resposta Gerada está factualmente correta comparada à Resposta Esperada.

Retorne JSON:
{{
  "score": 1 se correta, 0 se incorreta,
  "comment": "Justificativa detalhada"
}}
"""

judge = create_llm_as_judge(
    criteria="custom",
    model="openai:gpt-4o-mini",
    input_keys=["pergunta"],
    reference_output_keys=["resposta_esperada"],
    prediction_key="resposta",
    prompt=custom_prompt
)
```

### Exemplo 3: Múltiplos Avaliadores

```python
# Avaliar correção + relevância + concisão
judges = [
    create_llm_as_judge(criteria="CORRECTNESS", ...),
    create_llm_as_judge(criteria="RELEVANCE", ...),
    create_llm_as_judge(criteria="CONCISENESS", ...)
]

results = evaluate(
    target_function=my_app,
    data="dataset",
    evaluators=judges  # Lista de evaluators
)
```

## ✅ Checklist Rápido

**Antes de criar LLM-as-Judge:**

- [ ] Dataset tem reference outputs (ground truth)?
- [ ] Critério é subjetivo (não pode ser regex/exato)?
- [ ] Modelo juiz selecionado (ex: gpt-4o-mini)?
- [ ] Chaves mapeadas corretamente (input_keys, reference_output_keys, prediction_key)?
- [ ] Prompt juiz define formato de saída (JSON com score + comment)?

**Ao executar avaliação:**

- [ ] Target function retorna dicionário com prediction_key?
- [ ] Dataset versionado e estável?
- [ ] `evaluate()` configurado com experiment_prefix?
- [ ] LangSmith API key configurada?

**Ao analisar resultados:**

- [ ] Heatmap mostra distribuição de scores?
- [ ] Traces revelam por que score baixo?
- [ ] Métricas combinadas (score + latência + custo)?
- [ ] Comparação A/B entre experiments?

## 🎯 Regras de Ouro

1. **Reference outputs são cruciais** - LLM-as-Judge precisa de ground truth
1. **Prompt juiz é crítico** - Invista tempo em engenharia de prompt
1. **Combine métricas** - Não avalie apenas qualidade (latência + custo importam)
1. **Itere com human feedback** - Alinhe juiz com preferências humanas
1. **Use few-shot examples** - Calibre comportamento do juiz
1. **Versione datasets** - Reprodutibilidade é essencial
1. **Debug com Traces** - LangSmith UI mostra reasoning do juiz

## 🔍 Troubleshooting Comum

**Problema**: Judge sempre dá score máximo (bias positivo)

- ✅ Adicionar few-shot examples com casos negativos
- ✅ Revisar prompt para ser mais crítico
- ✅ Usar human corrections no LangSmith

**Problema**: Chaves não mapeiam corretamente

- ✅ Verificar nomes exatos em dataset examples
- ✅ Validar output da target function
- ✅ Usar `print()` para debug durante desenvolvimento

**Problema**: Avaliação muito lenta

- ✅ Usar modelo juiz mais rápido (gpt-4o-mini vs gpt-4)
- ✅ Reduzir tamanho do dataset para iteração rápida
- ✅ Executar em paralelo (LangSmith faz automaticamente)

**Problema**: Scores inconsistentes

- ✅ Definir rubrica clara no prompt
- ✅ Usar chain-of-thought para reasoning explícito
- ✅ Calibrar com human feedback

## 🚀 Next Steps

Após dominar conceitos básicos:

1. Consulte **PROMPT_ENGINEERING.md** para padrões avançados de prompts
1. Veja **INFRASTRUCTURE.md** para setup completo de datasets
1. Leia **LLMOPS.md** para integração em ciclo de desenvolvimento
