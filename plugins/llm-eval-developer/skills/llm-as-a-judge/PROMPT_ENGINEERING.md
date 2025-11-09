# Prompt Engineering for LLM-as-Judge

Guia completo de engenharia de prompts para modelos juízes no LangSmith, cobrindo design de critérios, estrutura de prompts, calibração via few-shot, e correção de bias.

## 🎯 Anatomia de um Prompt Juiz Eficaz

Todo prompt LLM-as-Judge deve conter **3 componentes obrigatórios**:

```
┌────────────────────────────────────────┐
│      Prompt Anatomy (3 Parts)         │
├────────────────────────────────────────┤
│                                        │
│  1. ROLE: Quem é o juiz?               │
│     "Você é um avaliador especialista" │
│                                        │
│  2. DATA: Quais dados considerar?      │
│     - Input (pergunta, contexto)       │
│     - Reference (resposta esperada)    │
│     - Prediction (resposta gerada)     │
│                                        │
│  3. OUTPUT FORMAT: Como responder?     │
│     JSON: {score: X, comment: "..."}   │
│                                        │
└────────────────────────────────────────┘
```

### Template Base Recomendado

```python
base_prompt = """
# 1. ROLE
Você é um avaliador especialista em {domínio}.

# 2. DATA
Analise os seguintes dados:
- Input: {input_field}
- Reference Output: {reference_field}
- Prediction: {prediction_field}

# 3. OUTPUT FORMAT
Avalie se a Prediction está {critério}.

Retorne APENAS um JSON válido:
{{
  "score": 1 (se {critério}) ou 0 (se não),
  "comment": "Justificativa detalhada em 1-2 frases"
}}
"""
```

## 1. Definindo Critérios de Avaliação

### 1.1 Critérios Pré-Construídos do LangSmith

LangSmith oferece critérios prontos via constantes:

| Critério | Constante | O Que Avalia | Requer Reference? |
|----------|-----------|--------------|-------------------|
| Correção | `CORRECTNESS` | Precisão factual | ✅ Sim |
| Relevância | `RELEVANCE` | Alinhamento com pergunta | ❌ Não |
| Concisão | `CONCISENESS` | Brevidade | ❌ Não |
| Harmfulness | `HARMFULNESS` | Conteúdo prejudicial | ❌ Não |
| Helpfulness | `HELPFULNESS` | Utilidade da resposta | ❌ Não |

**Uso:**
```python
from langsmith.evaluation import create_llm_as_judge

judge = create_llm_as_judge(
    criteria="CORRECTNESS",  # Usa prompt pré-construído
    ...
)
```

### 1.2 Critérios Customizados

**Quando customizar:**
- ✅ Domínio específico (médico, legal, técnico)
- ✅ Rubrica complexa (escala 1-5 com descrições)
- ✅ Múltiplas dimensões (tom + precisão + estrutura)

**Como customizar:**
```python
custom_criteria = """
Avalie se a resposta é tecnicamente precisa E apropriada para público leigo.

Critérios:
1. Correção técnica (sem erros factuais)
2. Linguagem acessível (sem jargão excessivo)
3. Exemplos práticos (quando relevante)

Score:
- 1: Atende todos os critérios
- 0: Falha em qualquer critério
"""

judge = create_llm_as_judge(
    criteria=custom_criteria,  # String customizada
    ...
)
```

### 1.3 Rubrica de Scoring

**Escalas comuns:**

**Binary (0/1):**
```
score: 1 se correto, 0 se incorreto
```

**Likert (1-5):**
```
score:
  5 - Excelente (completo e preciso)
  4 - Bom (pequenas omissões)
  3 - Aceitável (parcialmente correto)
  2 - Insatisfatório (erros significativos)
  1 - Ruim (completamente incorreto)
```

**Percentage (0-100):**
```
score: 0-100 (% de informação correta)
```

**Recomendação**: Binary (0/1) para iteração rápida, Likert (1-5) para nuance.

## 2. Estrutura de Prompts por Nível

### 2.1 Nível 1: Prompt Básico (Zero-Shot)

**Características:**
- Sem exemplos
- Instrução direta
- Formato de saída claro

```python
basic_prompt = """
Você é um avaliador de respostas de Q&A.

Dados:
- Pergunta: {pergunta}
- Resposta Esperada: {resposta_esperada}
- Resposta Gerada: {resposta}

Avalie se a Resposta Gerada está factualmente correta comparada à Resposta Esperada.

Retorne JSON:
{{
  "score": 1 se correta, 0 se incorreta,
  "comment": "Justificativa"
}}
"""
```

**Quando usar:**
- ✅ Critérios simples (correção binária)
- ✅ Domínio geral (não especializado)
- ✅ Iteração rápida (sem calibração)

### 2.2 Nível 2: Prompt com Rubrica Detalhada

**Características:**
- Rubrica explícita
- Múltiplos aspectos
- Escala clara

```python
rubric_prompt = """
Você é um avaliador especialista em respostas técnicas.

Dados:
- Pergunta: {pergunta}
- Resposta Esperada: {resposta_esperada}
- Resposta Gerada: {resposta}

Rubrica de Avaliação:
1. Correção Factual (50%)
   - Todos os fatos corretos? (+1)
   - Algum erro factual? (-1)

2. Completude (30%)
   - Cobre todos os pontos da referência? (+0.6)
   - Omite informações críticas? (-0.6)

3. Clareza (20%)
   - Explicação clara e organizada? (+0.4)
   - Confusa ou ambígua? (-0.4)

Score Final: Soma dos componentes (0-2 normalizado para 0-1)

Retorne JSON:
{{
  "score": 0.0-1.0,
  "comment": "Breakdown: Correção=X, Completude=Y, Clareza=Z"
}}
"""
```

**Quando usar:**
- ✅ Avaliação multidimensional
- ✅ Feedback detalhado necessário
- ✅ Domínio com múltiplos aspectos

### 2.3 Nível 3: Prompt com Chain-of-Thought (CoT)

**Características:**
- Raciocínio explícito
- Passo a passo
- Conclusão justificada

```python
cot_prompt = """
Você é um avaliador especialista. Siga um processo de raciocínio passo a passo.

Dados:
- Pergunta: {pergunta}
- Resposta Esperada: {resposta_esperada}
- Resposta Gerada: {resposta}

Processo de Avaliação:

1. ANÁLISE FACTUAL
   - Liste os fatos na Resposta Esperada
   - Liste os fatos na Resposta Gerada
   - Compare: quais estão corretos, incorretos ou omitidos?

2. AVALIAÇÃO DE COMPLETUDE
   - A resposta gerada cobre todos os pontos essenciais?
   - Há informações extras (bônus) ou irrelevantes (ruído)?

3. DECISÃO FINAL
   - Com base na análise acima, a resposta é correta?
   - Justificativa: por que sim ou não?

Retorne JSON:
{{
  "reasoning": "Passo 1: ... Passo 2: ... Passo 3: ...",
  "score": 1 ou 0,
  "comment": "Decisão final e justificativa"
}}
"""
```

**Quando usar:**
- ✅ Alta precisão necessária
- ✅ Debugging de decisões do juiz
- ✅ Domínio complexo (médico, legal)

**⚠️ Trade-off**: Mais tokens (mais caro + mais lento)

### 2.4 Nível 4: Prompt com Few-Shot Examples

**Características:**
- Exemplos de julgamentos corretos
- Calibração automática
- Alinhamento com preferências

```python
few_shot_prompt = """
Você é um avaliador de respostas técnicas.

# EXEMPLOS DE JULGAMENTO:

Exemplo 1:
Pergunta: "O que é Python?"
Esperada: "Python é uma linguagem de programação interpretada"
Gerada: "Python é uma linguagem interpretada criada por Guido van Rossum"
Score: 1 (Correta - inclui fato essencial + informação extra válida)

Exemplo 2:
Pergunta: "O que é Python?"
Esperada: "Python é uma linguagem de programação interpretada"
Gerada: "Python é uma cobra venenosa"
Score: 0 (Incorreta - contexto errado)

Exemplo 3:
Pergunta: "O que é Python?"
Esperada: "Python é uma linguagem de programação interpretada"
Gerada: "Python é uma linguagem compilada"
Score: 0 (Incorreta - erro factual)

# AGORA AVALIE:

Pergunta: {pergunta}
Esperada: {resposta_esperada}
Gerada: {resposta}

Retorne JSON:
{{
  "score": 1 ou 0,
  "comment": "Justificativa baseada nos exemplos"
}}
"""
```

**Quando usar:**
- ✅ Calibração necessária
- ✅ Critérios subjetivos
- ✅ Alinhamento com humanos

**Best Practice**: 3-5 exemplos (não mais!)

## 3. Mapeamento de Chaves de Dados

### 3.1 O Problema do Mapeamento

**Cenário comum:**
- Dataset usa chaves: `{"question", "answer"}`
- Target function retorna: `{"response"}`
- Prompt usa variáveis: `{pergunta}`, `{resposta}`

**Solução**: Mapear explicitamente via `create_llm_as_judge`

### 3.2 Parâmetros de Mapeamento

```python
judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",

    # Mapeamento crítico:
    input_keys=["question"],           # Do dataset.inputs
    reference_output_keys=["answer"],  # Do dataset.outputs
    prediction_key="response"          # Da target function output
)
```

**Variáveis no prompt:**
- `{question}` ← dataset.inputs["question"]
- `{answer}` ← dataset.outputs["answer"]
- `{response}` ← target_output["response"]

### 3.3 Exemplo Completo de Mapeamento

```python
# Dataset Example
{
    "inputs": {
        "user_query": "Capital da França?",
        "context": "Geografia europeia"
    },
    "outputs": {
        "expected_response": "Paris"
    }
}

# Target Function
def my_app(inputs: dict) -> dict:
    return {"generated_answer": "Paris"}

# Prompt Template
custom_prompt = """
Query: {user_query}
Context: {context}
Expected: {expected_response}
Generated: {generated_answer}

Avalie correção.
"""

# Mapeamento
judge = create_llm_as_judge(
    prompt=custom_prompt,
    input_keys=["user_query", "context"],      # 2 inputs!
    reference_output_keys=["expected_response"],
    prediction_key="generated_answer"
)
```

### 3.4 Debugging Mapeamento

**Problema**: KeyError ou variáveis vazias no prompt

**Solução**: Validar chaves antes de criar judge

```python
# 1. Inspecionar dataset example
example = client.read_example(example_id="...")
print("Inputs keys:", example.inputs.keys())
print("Outputs keys:", example.outputs.keys())

# 2. Testar target function
test_output = my_app(example.inputs)
print("Prediction keys:", test_output.keys())

# 3. Confirmar mapeamento
# input_keys deve estar em example.inputs.keys()
# reference_output_keys deve estar em example.outputs.keys()
# prediction_key deve estar em test_output.keys()
```

## 4. Seleção do Modelo Juiz

### 4.1 Modelos Disponíveis

**OpenAI:**
- `openai:gpt-4o` - Mais preciso, mais lento, mais caro
- `openai:gpt-4o-mini` - Balanceado (recomendado)
- `openai:gpt-3.5-turbo` - Mais rápido, menos preciso

**Anthropic:**
- `anthropic:claude-3-5-sonnet-20250219` - Alta qualidade
- `anthropic:claude-3-haiku-20240307` - Rápido e econômico

**Outros:**
- `fireworks_ai:accounts/...` - Modelos open-source

### 4.2 Trade-offs de Modelo

| Modelo | Precisão | Velocidade | Custo | Caso de Uso |
|--------|----------|------------|-------|-------------|
| GPT-4o | ⭐⭐⭐⭐⭐ | ⭐⭐ | 💰💰💰 | Avaliação final, alta precisão |
| GPT-4o-mini | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | Iteração rápida, balanceado |
| GPT-3.5-turbo | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 | Quick evals, screening |

**Recomendação**: Iniciar com `gpt-4o-mini`, escalar para `gpt-4o` em produção.

### 4.3 Configuração do Modelo

```python
judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",  # Formato: provider:model
    # Parâmetros opcionais:
    # temperature=0.0,  # Determinístico
    # max_tokens=500    # Limite de resposta
)
```

## 5. Calibração via Few-Shot Examples

### 5.1 O Que é Calibração

**Problema**: Judge "out-of-the-box" pode não alinhar com suas preferências

**Solução**: Few-shot examples que mostram julgamentos desejados

### 5.2 LangSmith Human Corrections

**Workflow automatizado:**

1. **Executar avaliação inicial**
   ```python
   results = evaluate(data="dataset", evaluators=[judge])
   ```

2. **Humanos corrigem scores no LangSmith UI**
   - Navegar para Experiment
   - Clicar em example
   - Modificar score (ex: 0 → 1)
   - Adicionar feedback

3. **LangSmith auto-insere correções como few-shot**
   - Correções viram exemplos no prompt
   - Judge aprende com feedback humano

**Benefício**: Calibração automática sem reescrever prompts!

### 5.3 Few-Shot Manual (via Prompt)

**Alternativa**: Incluir examples diretamente no prompt

```python
few_shot_template = """
Você é avaliador de Q&A técnico.

# EXEMPLOS DE CALIBRAÇÃO:

[Exemplo 1]
Q: "O que é Docker?"
Esperada: "Docker é plataforma de containerização"
Gerada: "Docker é uma ferramenta de virtualização"
Score: 0.5 (Parcialmente correta - conceito relacionado mas não exato)
Feedback: "Virtualização ≠ Containerização"

[Exemplo 2]
Q: "O que é Kubernetes?"
Esperada: "Kubernetes orquestra containers"
Gerada: "Kubernetes gerencia Docker containers em cluster"
Score: 1 (Correta - adiciona detalhes válidos)
Feedback: "Inclui informação extra relevante"

# AGORA AVALIE:
Q: {pergunta}
Esperada: {resposta_esperada}
Gerada: {resposta}

Retorne JSON: {{"score": ..., "comment": ...}}
"""
```

**Quantos exemplos?**
- ✅ 3-5 exemplos = Sweet spot
- ❌ < 3 = Pouco contexto
- ❌ > 10 = Token waste + confusion

### 5.4 Estratégias de Seleção de Few-Shot

**Opção 1: Edge Cases**
- Casos difíceis onde judge errou
- Exemplos ambíguos

**Opção 2: Distribuição Balanceada**
- 50% positivos (score=1)
- 50% negativos (score=0)

**Opção 3: Coverage de Tipos de Erro**
- Erro factual
- Omissão de informação
- Informação extra irrelevante
- Formato incorreto

## 6. Correção de Bias

### 6.1 Tipos Comuns de Bias

**1. Positivity Bias**
- Judge tende a dar scores altos
- Problema: Não detecta erros sutis

**2. Length Bias**
- Respostas longas recebem scores melhores
- Problema: Verbosidade ≠ Qualidade

**3. Format Bias**
- Respostas bem formatadas (markdown, listas) pontuam alto
- Problema: Formato ≠ Correção

**4. Echo Chamber**
- LLM avalia outro LLM favoravelmente
- Problema: Bias sistêmico

### 6.2 Detectando Bias

**Análise estatística:**
```python
# Calcular distribuição de scores
scores = [r.score for r in results.results]
mean_score = sum(scores) / len(scores)

# Red flags:
# - mean_score > 0.9 (positivity bias?)
# - mean_score < 0.1 (negativity bias?)
# - std_dev < 0.1 (todos scores iguais - não discrimina)
```

**Comparação com human judgments:**
```python
# Correlação judge vs human
# Se correlation < 0.7 → bias ou critérios mal definidos
```

### 6.3 Técnicas de Correção

**Técnica 1: Prompt Engineering**
```python
# Adicionar instrução explícita
bias_aware_prompt = """
IMPORTANTE: Seja crítico. Penalize erros sutis.
Não favoreça respostas longas ou bem formatadas automaticamente.
Foque apenas em correção factual.

{resto do prompt}
"""
```

**Técnica 2: Few-Shot com Casos Negativos**
```python
# Incluir exemplos de respostas longas mas incorretas
negative_example = """
Gerada: "Python é uma linguagem compilada criada em 1991 por Guido van Rossum..."
(200 palavras de texto bem formatado)
Score: 0 (Erro factual: Python é INTERPRETADA, não compilada)
"""
```

**Técnica 3: Human Corrections (LangSmith)**
- Corrigir false positives no UI
- LangSmith usa correções como few-shot
- Bias reduz gradualmente

**Técnica 4: Dual Judging**
```python
# Usar 2 judges independentes
judge_1 = create_llm_as_judge(model="openai:gpt-4o-mini", ...)
judge_2 = create_llm_as_judge(model="anthropic:claude-3-5-sonnet", ...)

# Average ou majority vote
final_score = (score_1 + score_2) / 2
```

### 6.4 Validação de Calibração

**Checklist:**
- [ ] Distribuição de scores razoável (não só 0 ou 1)?
- [ ] Correlação com human judgments > 0.7?
- [ ] Respostas incorretas óbvias recebem score 0?
- [ ] Respostas longas mas erradas não pontuam alto?
- [ ] Few-shot examples incluem edge cases?

## 7. Padrões Avançados

### 7.1 Multi-Aspect Evaluation

**Cenário**: Avaliar múltiplas dimensões separadamente

```python
# Judge 1: Correção
correctness_judge = create_llm_as_judge(criteria="CORRECTNESS", ...)

# Judge 2: Concisão
conciseness_judge = create_llm_as_judge(criteria="CONCISENESS", ...)

# Judge 3: Tom
tone_judge = create_llm_as_judge(
    criteria="Avalie se o tom é profissional e amigável",
    ...
)

# Combinar
results = evaluate(
    data="dataset",
    evaluators=[correctness_judge, conciseness_judge, tone_judge]
)

# Resultado: 3 scores por example
```

### 7.2 Pairwise Comparison

**Cenário**: Comparar 2 respostas (A vs B)

```python
pairwise_prompt = """
Você é um avaliador comparativo.

Pergunta: {pergunta}

Resposta A: {resposta_a}
Resposta B: {resposta_b}

Qual resposta é melhor? Considere:
- Correção factual
- Completude
- Clareza

Retorne JSON:
{{
  "winner": "A" ou "B",
  "score_a": 0-1,
  "score_b": 0-1,
  "comment": "Justificativa da escolha"
}}
"""

pairwise_judge = create_llm_as_judge(
    prompt=pairwise_prompt,
    input_keys=["pergunta", "resposta_a", "resposta_b"],
    prediction_key="comparison"  # Dummy (não usado)
)
```

### 7.3 Adaptive Rubric

**Cenário**: Rubrica muda baseado no tipo de pergunta

```python
adaptive_prompt = """
Você é avaliador adaptativo.

Tipo de Pergunta: {question_type}

Se {question_type} == "factual":
    Rubrica: Correção binária (0 ou 1)
Senão se {question_type} == "opinião":
    Rubrica: Fundamentação (argumentos válidos = 1)
Senão:
    Rubrica: Relevância (alinhamento com pergunta)

{dados para avaliar}

Retorne JSON: {{"score": ..., "comment": ...}}
"""
```

## 8. Best Practices Resumidas

### Checklist de Design de Prompt

**Estrutura:**
- [ ] Role claro (especialista em X)?
- [ ] Dados mapeados corretamente (input, reference, prediction)?
- [ ] Formato de saída explícito (JSON com score + comment)?

**Critérios:**
- [ ] Critério bem definido (não vago)?
- [ ] Escala clara (0/1 ou 1-5 com descrições)?
- [ ] Rubrica explícita (quando usar escala numérica)?

**Calibração:**
- [ ] Few-shot examples incluídos (3-5)?
- [ ] Edge cases cobertos?
- [ ] Distribuição balanceada (positivos + negativos)?

**Bias:**
- [ ] Instrução para ser crítico?
- [ ] Exemplos de respostas longas mas incorretas?
- [ ] Human corrections planejadas?

**Performance:**
- [ ] Modelo apropriado (gpt-4o-mini para iteração)?
- [ ] Prompt conciso (< 1000 tokens)?
- [ ] Chain-of-thought apenas quando necessário?

## 9. Troubleshooting de Prompts

**Problema**: Judge sempre dá score máximo
```python
# Diagnóstico: Positivity bias
# Solução: Adicionar few-shot com casos negativos + instrução crítica
```

**Problema**: Scores inconsistentes
```python
# Diagnóstico: Rubrica vaga ou modelo fraco
# Solução: Definir rubrica detalhada OU usar modelo melhor (gpt-4o)
```

**Problema**: Judge não usa reference output
```python
# Diagnóstico: Prompt não menciona reference explicitamente
# Solução: Adicionar "Compare Prediction vs Reference Output"
```

**Problema**: JSON inválido retornado
```python
# Diagnóstico: Modelo não segue formato
# Solução: Enfatizar "Retorne APENAS JSON válido, sem texto adicional"
```

**Problema**: Comentários vazios ou genéricos
```python
# Diagnóstico: Prompt não exige justificativa específica
# Solução: "comment deve mencionar QUAL fato está incorreto e POR QUÊ"
```

## 10. Exemplos Completos

### Exemplo 1: Judge Básico (Zero-Shot)
```python
from langsmith.evaluation import create_llm_as_judge

basic_judge = create_llm_as_judge(
    criteria="CORRECTNESS",
    model="openai:gpt-4o-mini",
    input_keys=["question"],
    reference_output_keys=["answer"],
    prediction_key="response"
)
```

### Exemplo 2: Judge Customizado (Rubrica Detalhada)
```python
rubric = """
Avalie resposta técnica em escala 1-5:
5 - Completa e precisa
4 - Pequenas omissões
3 - Parcialmente correta
2 - Erros significativos
1 - Completamente incorreta

Retorne JSON: {{"score": 1-5, "comment": "..."}}
"""

custom_judge = create_llm_as_judge(
    criteria=rubric,
    model="openai:gpt-4o",
    input_keys=["question"],
    reference_output_keys=["expected_answer"],
    prediction_key="generated_answer"
)
```

### Exemplo 3: Judge com Few-Shot e CoT
```python
few_shot_cot = """
Você é avaliador com raciocínio explícito.

EXEMPLOS:
[3 exemplos de julgamento com reasoning]

PROCESSO:
1. Analisar fatos
2. Comparar com referência
3. Decidir score

AGORA AVALIE:
Q: {question}
Ref: {reference}
Pred: {prediction}

Retorne JSON:
{{
  "reasoning": "Passo 1: ... Passo 2: ... Passo 3: ...",
  "score": 0 ou 1,
  "comment": "Decisão final"
}}
"""

advanced_judge = create_llm_as_judge(
    prompt=few_shot_cot,
    model="openai:gpt-4o",
    input_keys=["question"],
    reference_output_keys=["reference"],
    prediction_key="prediction"
)
```
