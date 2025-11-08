# LLM Eval Developer

> Plugin especializado em criar benchmarks comparativos de LLMs e evaluations com LangChain/LangGraph e LangSmith para tracking automático.

## 📋 Visão Geral

O **LLM Eval Developer** oferece ferramentas completas para:

- **Benchmarking**: Criar suites comparativas para testar múltiplos LLMs
- **Evaluations**: Desenvolver evaluators customizados (OpenEvals, LangSmith, custom)
- **Testing**: Padrões e melhores práticas para testar LLMs
- **Metrics**: Métricas de evaluation (BLEU, ROUGE, F1, LLM-as-judge, etc)
- **Patterns**: Padrões de código comuns reutilizáveis

## 🚀 Comandos Disponíveis

### `/benchmark-llms`

Cria suite de benchmark comparativo para avaliar múltiplos LLMs usando LangChain/LangGraph e LangSmith.

```bash
/benchmark-llms
```

**O que faz**:

- Configura dataset de test cases
- Define métricas de comparação
- Cria harness de benchmark com LangSmith
- Executa benchmark contra múltiplos modelos
- Gera relatório comparativo

### `/create-eval-suite`

Gera estrutura completa de evaluation suite com dataset, evaluators e testes.

```bash
/create-eval-suite
```

**O que faz**:

- Estrutura de diretórios para evaluations
- Dataset de exemplos (train/test)
- Evaluators customizados
- Test suite integrado
- Configuração CI/CD

### `/create-evaluator`

Gera código de evaluator customizado para LLMs (OpenEvals, LangSmith, custom).

```bash
/create-evaluator
```

**O que faz**:

- Seleciona tipo de evaluator (OpenEvals, LangSmith, custom)
- Gera código boilerplate
- Implementa métrica específica
- Adiciona docstring e exemplos
- Integra com LangSmith

### `/eval-metrics`

Lista e documenta métricas de evaluation disponíveis com exemplos.

```bash
/eval-metrics
```

**Métricas Cobertas**:

- BLEU (machine translation)
- ROUGE (text summarization)
- F1 Score (classification)
- Exact Match (QA)
- LLM-as-Judge (semantic)
- Custom metrics

### `/eval-patterns`

Mostra padrões de código comuns para evaluation (dataset, testing, CI/CD).

```bash
/eval-patterns
```

**Padrões**:

- Dataset creation and loading
- Test case organization
- Evaluation harness
- CI/CD integration
- Reporting and visualization

### `/setup-project-eval`

Configura CLAUDE.md do projeto com padrões de LLM evaluation, frameworks, métricas e estrutura.

```bash
/setup-project-eval
```

## 🤖 Agentes Disponíveis

### `benchmark-specialist`

Agente especializado em criar benchmarks comparativos de LLMs usando LangChain/LangGraph e LangSmith para tracking automático de métricas.

**Uso**:

```
Task tool com subagent_type=benchmark-specialist
```

### `eval-developer`

Agente especializado em desenvolver evaluations de LLMs - gera código, padrões e estruturas.

**Uso**:

```
Task tool com subagent_type=eval-developer
```

## 💡 Skills Disponíveis

### `benchmark-runner`

Executa benchmarks comparativos de LLMs usando LangChain/LangGraph e LangSmith.

**Uso**: Auto-invocado como skill via Skill tool

### `evaluation-developer`

Desenvolve código de evaluators para LLMs (OpenEvals, LangSmith, BLEU, ROUGE, LLM-as-judge).

**Uso**: Auto-invocado como skill via Skill tool

### `langchain-test-specialist`

Cria unit e integration tests para LangChain e LangGraph com advanced mocking patterns.

**Uso**: Auto-invocado como skill via Skill tool

### `smoke-test`

Smoke testing expertise - validação de funcionalidade crítica com pytest markers e CI integration.

**Uso**: Auto-invocado como skill via Skill tool

## 📚 Casos de Uso

### 1. Comparar Múltiplos LLMs

```bash
/benchmark-llms
# Compara Claude, GPT-4, Gemini em tarefas específicas
```

### 2. Criar Evaluation Suite Completa

```bash
/create-eval-suite
# Estrutura completa com dataset, evaluators e testes
```

### 3. Implementar Métrica Customizada

```bash
/create-evaluator
# Cria evaluator para métrica específica do seu domínio
```

### 4. Entender Métricas Disponíveis

```bash
/eval-metrics
# Lista todas as métricas com exemplos de uso
```

### 5. Consultar Padrões de Código

```bash
/eval-patterns
# Mostra patterns comuns reutilizáveis
```

### 6. Configurar Projeto para Evaluation

```bash
/setup-project-eval
# Configura CLAUDE.md com toda estrutura necessária
```

## 🔧 Integração com LangSmith

Todos os componentes integram automaticamente com LangSmith para:

- ✅ Tracing de execuções
- ✅ Logging automático de métricas
- ✅ Comparação de runs
- ✅ Visualização de resultados
- ✅ Análise de regressão

## 📊 Métricas Suportadas

| Métrica | Tipo | Caso de Uso |
|---------|------|-----------|
| BLEU | Léxical | Machine Translation |
| ROUGE | Léxical | Summarization |
| F1 Score | Classification | Multi-task |
| Exact Match | QA | Question Answering |
| LLM-as-Judge | Semântico | Avaliação geral |
| Custom | Domain-specific | Domínios específicos |

## 🛠️ Tecnologias

- **LangChain**: Framework para LLM apps
- **LangGraph**: State management e workflows
- **LangSmith**: Observability e evaluation
- **Python**: Linguagem principal
- **Pytest**: Testing framework

## 📖 Próximos Passos

1. **Comece com**: `/setup-project-eval` para configurar seu projeto
1. **Entenda métricas**: `/eval-metrics` para ver opções disponíveis
1. **Crie evaluation suite**: `/create-eval-suite` para estrutura completa
1. **Execute benchmark**: `/benchmark-llms` para comparar modelos
1. **Implemente evaluators**: `/create-evaluator` para métricas customizadas

## 📝 Changelog

Veja [CHANGELOG.md](./CHANGELOG.md) para histórico de versões.

## 📄 Licença

MIT

______________________________________________________________________

**Desenvolvido para Claude Code** 🚀
