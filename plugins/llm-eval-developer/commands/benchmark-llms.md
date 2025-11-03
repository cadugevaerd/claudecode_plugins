---
description: Cria suite de benchmark comparativo para avaliar múltiplos LLMs usando LangChain/LangGraph e LangSmith para tracking automático de métricas
---

# Benchmark LLMs - Comparative Evaluation com LangChain/LangGraph

Cria **suite completa de benchmarking comparativo** para avaliar múltiplos LLMs usando **LangChain/LangGraph** para execução e **LangSmith** para tracking automático de:

- **Métricas de qualidade** (accuracy, relevance, hallucination via LangSmith evaluators)
- **Métricas de performance** (latency P50/P95/P99, TTFT via callbacks)
- **Métricas de custo** (tracking automático via LangSmith)
- **Métricas de segurança** (bias detection, toxicity via LLM-as-judge)

## 🎯 Objetivo

Gerar código funcional completo usando **LangChain Expression Language (LCEL)** e **LangSmith** para executar benchmarks comparativos que permitam **decisões data-driven** sobre qual LLM usar.

## 📋 Como Usar

````bash
/benchmark-llms

```text

O agente perguntará interativamente:

### 1. **Quais LLMs comparar?**

**Exemplos**:
- `gpt-4o, claude-3.5-sonnet, gemini-1.5-pro`
- `gpt-4o-mini, claude-3-haiku, gemini-1.5-flash` (modelos menores)
- `gpt-4, gpt-3.5-turbo, claude-3-opus, claude-3-sonnet` (mix)

**Formato**: Lista separada por vírgulas

### 2. **Qual dataset/benchmark usar?**

**Opções padrão**:
- **LangSmith Dataset**: Nome do dataset já criado no LangSmith
- **MMLU**: Multi-task Q&A (57 subjects) - knowledge & reasoning
- **HumanEval**: Code generation (164 programming problems)
- **TruthfulQA**: Factual accuracy (817 questions)
- **Custom**: Seu próprio dataset local em JSON

**Ou fornecer caminho**:
- `datasets/my_benchmark.json` (custom dataset)

### 3. **Quais métricas avaliar?**

**Categorias de métricas**:

✅ **Qualidade/Acurácia** (via LangSmith evaluators):
- `accuracy` - Respostas corretas (%)
- `relevance` - Relevância das respostas (LLM-as-judge)
- `hallucination` - Taxa de alucinações (LLM-as-judge)
- `coherence` - Coerência do texto
- `f1_score` - F1 score para classificação

✅ **Performance/Velocidade** (via LangChain callbacks):
- `latency_p50` - Latência mediana
- `latency_p95` - Latência p95 (SLA)
- `latency_p99` - Latência p99 (worst-case)
- `ttft` - Time to First Token (streaming)
- `throughput` - Tokens por segundo
- `tpot` - Time Per Output Token

✅ **Custo** (via LangSmith automatic tracking):
- `cost_per_1k_tokens` - Custo por 1K tokens
- `total_cost` - Custo total do benchmark
- `cost_efficiency` - Accuracy per dollar

✅ **Robustez**:
- `task_consistency` - Consistência entre diferentes tipos de tarefa
- `failure_rate` - Taxa de falha/timeout
- `robustness_score` - Score de robustez geral

✅ **Segurança & Bias** (via LangSmith evaluators):
- `bias_detection` - Detecção de viés (BBQ benchmark)
- `toxicity` - Toxicidade (ToxiGen)
- `jailbreak_resistance` - Resistência a jailbreaks
- `pii_leakage` - Vazamento de PII

**Formato**: Lista separada por vírgulas ou `all` para todas

### 4. **Formato de output?**

**Opções**:
- `json` - Resultados estruturados em JSON
- `markdown` - Relatório em Markdown (human-readable)
- `html` - Dashboard HTML interativo
- `csv` - CSV para análise em Excel/Pandas
- `langsmith` - View direto no LangSmith UI (padrão)
- `all` - Todos os formatos

### 5. **Execução paralela?**

**Opções**:
- `yes` - Executa LLMs em paralelo usando LCEL batch (mais rápido, mais $$$)
- `no` - Executa sequencialmente (mais lento, mais barato)

**Recomendação**: `yes` para 2-3 modelos, `no` para 5+ modelos

## 🔍 Processo de Execução

### Passo 1: Coletar Informações

Pergunta interativa sobre:
- Modelos a comparar
- Dataset/benchmark
- Métricas desejadas
- Formato de output
- Parallelização

### Passo 2: Gerar Estrutura de Benchmark

Cria estrutura completa:

```text

benchmarks/
├── config/
│   ├── benchmark_config.py          # Configuração de modelos e métricas
│   └── langsmith_config.py          # Config LangSmith project/dataset
├── datasets/
│   ├── dataset_loader.py            # Carregador de datasets LangSmith
│   └── dataset_uploader.py          # Upload dataset para LangSmith
├── benchmarking/
│   ├── langchain_benchmark.py       # Benchmark usando LCEL chains
│   ├── langgraph_benchmark.py       # Benchmark usando LangGraph (parallel)
│   ├── llm_clients.py               # Clientes LangChain por provider
│   ├── callbacks/
│   │   ├── latency_callback.py      # Callback para latência/TTFT
│   │   └── token_callback.py        # Callback para token tracking
│   ├── evaluators/
│   │   ├── langsmith_evaluators.py  # LangSmith evaluators nativos
│   │   └── custom_evaluators.py     # Custom evaluators
│   └── reporters/
│       ├── json_reporter.py         # JSON output
│       ├── markdown_reporter.py     # Markdown report
│       ├── html_reporter.py         # HTML dashboard
│       └── csv_reporter.py          # CSV export
├── results/
│   └── .gitkeep
├── tests/
│   ├── test_benchmark.py            # Testes unitários
│   └── test_evaluators.py           # Testes de evaluators
├── run_benchmark.py                 # Script principal
├── analyze_results.py               # Análise via LangSmith API
├── requirements.txt                 # Dependências
└── README.md                        # Documentação

```text

### Passo 3: Implementar Código com LangChain/LangGraph

Cada arquivo é gerado com código completo usando LangChain/LangGraph!

**Exemplo: `langchain_benchmark.py`** (Benchmark com LCEL)

```python
"""
LangChain Benchmark Suite
Usa LCEL chains e LangSmith para benchmark comparativo.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import asyncio
import numpy as np

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.callbacks import BaseCallbackHandler

from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator

@dataclass
class BenchmarkConfig:
    """Configuração de benchmark"""
    models: List[Dict[str, str]]  # [{"provider": "openai", "model": "gpt-4o"}]
    dataset_name: str  # Nome do dataset no LangSmith
    evaluators: List[str]  # Lista de evaluators
    project_name: str  # Projeto LangSmith
    parallel: bool = True
    max_concurrency: int = 10


class LatencyCallback(BaseCallbackHandler):
    """Callback para medir latência e TTFT usando LangChain"""

    def __init__(self):
        self.latencies = []
        self.ttfts = []
        self.start_time = None
        self.first_token_time = None

    def on_llm_start(self, *args, **kwargs):
        """Marca início da inferência"""
        import time
        self.start_time = time.perf_counter()
        self.first_token_time = None

    def on_llm_new_token(self, token: str, **kwargs):
        """Captura Time to First Token"""
        if self.first_token_time is None:
            import time
            self.first_token_time = time.perf_counter()
            ttft = (self.first_token_time - self.start_time) * 1000
            self.ttfts.append(ttft)

    def on_llm_end(self, *args, **kwargs):
        """Marca fim e calcula latência total"""
        import time
        if self.start_time:
            latency = (time.perf_counter() - self.start_time) * 1000
            self.latencies.append(latency)

    def get_stats(self) -> Dict[str, float]:
        """Retorna estatísticas de performance"""
        return {
            "avg_latency_ms": np.mean(self.latencies) if self.latencies else 0.0,
            "p50_latency_ms": np.percentile(self.latencies, 50) if self.latencies else 0.0,
            "p95_latency_ms": np.percentile(self.latencies, 95) if self.latencies else 0.0,
            "p99_latency_ms": np.percentile(self.latencies, 99) if self.latencies else 0.0,
            "avg_ttft_ms": np.mean(self.ttfts) if self.ttfts else 0.0,
        }


class LangChainBenchmark:
    """
    Benchmark de múltiplos LLMs usando LangChain LCEL e LangSmith.

    Usa:
    - LCEL chains para definir workflows
    - LangSmith evaluate() API para execução
    - LangSmith evaluators para métricas
    - Custom callbacks para latência/TTFT
    - Automatic cost tracking via LangSmith
    """

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.client = Client()  # LangSmith client
        self.results = {}

    def create_chain(self, model_config: Dict[str, str]):
        """
        Cria chain LCEL com modelo específico.

        Args:
            model_config: {"provider": "openai", "model": "gpt-4o", "temperature": 0}

        Returns:
            Runnable chain (prompt | llm | parser)
        """
        # Criar LLM baseado no provider
        if model_config["provider"] == "openai":
            llm = ChatOpenAI(
                model=model_config["model"],
                temperature=model_config.get("temperature", 0)
            )
        elif model_config["provider"] == "anthropic":
            llm = ChatAnthropic(
                model=model_config["model"],
                temperature=model_config.get("temperature", 0)
            )
        elif model_config["provider"] == "google":
            llm = ChatGoogleGenerativeAI(
                model=model_config["model"],
                temperature=model_config.get("temperature", 0)
            )
        else:
            raise ValueError(f"Provider {model_config['provider']} não suportado")

        # Chain LCEL: prompt | llm | parser
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])

        chain = prompt | llm | StrOutputParser()
        return chain

    def create_langsmith_evaluators(self) -> List:
        """
        Cria evaluators do LangSmith para quality metrics.

        Returns:
            Lista de evaluators prontos para usar no evaluate()
        """
        evaluators = []

        for evaluator_name in self.config.evaluators:
            if evaluator_name == "qa":
                # Q&A correctness evaluator
                evaluators.append(LangChainStringEvaluator("qa"))

            elif evaluator_name == "context_qa":
                # Context-aware Q&A evaluator
                evaluators.append(LangChainStringEvaluator("context_qa"))

            elif evaluator_name == "helpfulness":
                # Helpfulness criteria evaluator
                evaluators.append(
                    LangChainStringEvaluator("criteria",
                        config={"criteria": "helpfulness"})
                )

            elif evaluator_name == "harmfulness":
                # Harmfulness criteria evaluator
                evaluators.append(
                    LangChainStringEvaluator("criteria",
                        config={"criteria": "harmfulness"})
                )

            elif evaluator_name == "relevance":
                # Custom LLM-as-judge for relevance
                from langchain_openai import ChatOpenAI
                evaluators.append(
                    LangChainStringEvaluator("labeled_criteria",
                        config={
                            "criteria": {
                                "relevance": "Is the answer relevant to the question?"
                            },
                            "llm": ChatOpenAI(model="gpt-4o-mini")
                        }
                    )
                )

        return evaluators

    async def run_benchmark(self) -> Dict[str, Dict]:
        """
        Executa benchmark em todos os modelos usando LangSmith evaluate().

        Returns:
            Dict com resultados por modelo
        """
        print(f"🚀 Iniciando benchmark de {len(self.config.models)} modelos...")
        print(f"📊 Dataset: {self.config.dataset_name}")
        print(f"⚙️  Modo: {'Paralelo (LCEL batch)' if self.config.parallel else 'Sequencial'}")
        print(f"🔍 LangSmith Project: {self.config.project_name}")

        # Criar evaluators do LangSmith
        evaluators = self.create_langsmith_evaluators()

        for model_config in self.config.models:
            model_name = f"{model_config['provider']}:{model_config['model']}"

            print(f"\n📍 Benchmarking {model_name}...")

            # Criar chain LCEL
            chain = self.create_chain(model_config)

            # Callback para latência
            latency_callback = LatencyCallback()

            # Função target para evaluate
            def predict(inputs: Dict) -> Dict:
                """Wrapper para chain.invoke com callbacks"""
                config = RunnableConfig(
                    callbacks=[latency_callback],
                    max_concurrency=self.config.max_concurrency if self.config.parallel else 1
                )
                result = chain.invoke(inputs, config=config)
                return {"output": result}

            # Executar evaluation com LangSmith
            # LangSmith automaticamente trackeia:
            # - Token usage
            # - Costs (se pricing configurado)
            # - Traces completos
            # - Evaluator scores
            results = evaluate(
                predict,
                data=self.config.dataset_name,
                evaluators=evaluators,
                experiment_prefix=f"benchmark-{model_name}",
                project_name=self.config.project_name,
                max_concurrency=self.config.max_concurrency if self.config.parallel else 1
            )

            # Agregar resultados de performance (via callbacks)
            perf_stats = latency_callback.get_stats()

            # Extrair custo total do LangSmith
            # LangSmith trackeia automaticamente se pricing estiver configurado
            total_cost = self._get_cost_from_langsmith(results)

            # Armazenar resultados
            self.results[model_name] = {
                # Quality metrics (do LangSmith evaluators)
                "evaluator_scores": {
                    evaluator_name: results.get(evaluator_name, {}).get("mean", 0.0)
                    for evaluator_name in self.config.evaluators
                },

                # Performance metrics (dos callbacks)
                **perf_stats,

                # Cost metrics (do LangSmith tracking)
                "total_cost_usd": total_cost,
                "cost_efficiency": (
                    results.get("qa", {}).get("mean", 0.0) / total_cost
                    if total_cost > 0 else 0.0
                ),

                # Metadata
                "experiment_url": results.experiment_url if hasattr(results, 'experiment_url') else None
            }

            print(f"✅ {model_name} concluído!")
            print(f"   Avg Latency: {perf_stats['avg_latency_ms']:.0f}ms")
            print(f"   P95 Latency: {perf_stats['p95_latency_ms']:.0f}ms")
            print(f"   Total Cost: ${total_cost:.4f}")

        return self.results

    def _get_cost_from_langsmith(self, results) -> float:
        """
        Extrai custo total do LangSmith tracking.

        LangSmith automaticamente trackeia custos se pricing estiver configurado.

        Args:
            results: Resultado do evaluate()

        Returns:
            Custo total em USD
        """
        # LangSmith fornece custo automaticamente se configurado
        # Aqui você pode extrair do results ou consultar via API

        # Placeholder - substituir por extração real
        # do results ou query via LangSmith API
        return 0.0

    def generate_reports(self, output_formats: List[str]):
        """
        Gera relatórios nos formatos especificados.

        Args:
            output_formats: ['json', 'markdown', 'html', 'csv', 'langsmith']
        """
        from benchmarking.reporters import (
            JSONReporter,
            MarkdownReporter,
            HTMLReporter,
            CSVReporter
        )

        reporters = {
            "json": JSONReporter(),
            "markdown": MarkdownReporter(),
            "html": HTMLReporter(),
            "csv": CSVReporter()
        }

        for format in output_formats:
            if format == "langsmith":
                print(f"📊 Resultados disponíveis no LangSmith: {self.config.project_name}")
                continue

            reporter = reporters.get(format)
            if reporter:
                reporter.generate(self.results)
                print(f"📄 Relatório {format.upper()} gerado!")

```text

**Exemplo: `langgraph_benchmark.py`** (Benchmark com LangGraph - Parallel)

```python
"""
LangGraph Benchmark Suite
Usa LangGraph para execução paralela de múltiplos LLMs.
"""

from typing import TypedDict, Annotated, Dict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class BenchmarkState(TypedDict):
    """Estado do benchmark workflow"""
    input: str
    models: List[str]
    responses: Annotated[Dict[str, str], "Respostas de cada modelo"]
    latencies: Annotated[Dict[str, float], "Latências por modelo"]
    costs: Annotated[Dict[str, float], "Custos por modelo"]
    metrics: Annotated[Dict[str, Dict], "Métricas por modelo"]
    comparison: str  # Análise comparativa final


def create_model_node(model_name: str, llm):
    """
    Cria node para chamar um modelo específico.

    Args:
        model_name: Nome do modelo (ex: "gpt-4o")
        llm: Instância do LLM (ChatOpenAI, ChatAnthropic, etc.)

    Returns:
        Function node para o grafo
    """
    def node(state: BenchmarkState):
        import time

        # Timing
        start = time.perf_counter()

        # Invocar LLM
        response = llm.invoke(state["input"])

        # Latência
        latency = (time.perf_counter() - start) * 1000

        # Atualizar estado
        return {
            "responses": {
                **state.get("responses", {}),
                model_name: response.content
            },
            "latencies": {
                **state.get("latencies", {}),
                model_name: latency
            }
        }

    return node


def evaluate_responses_node(state: BenchmarkState):
    """
    Node para avaliar todas as respostas usando LLM-as-judge.

    Args:
        state: Estado atual do grafo

    Returns:
        Estado atualizado com métricas
    """
    from langchain_openai import ChatOpenAI

    evaluator_llm = ChatOpenAI(model="gpt-4o-mini")

    metrics = {}
    for model_name, response in state["responses"].items():
        # Avaliar qualidade usando LLM-as-judge
        eval_prompt = f"""
        Avalie a resposta abaixo em uma escala de 1-10:

        Input: {state['input']}
        Resposta: {response}

        Critérios: acurácia, relevância, completude, coerência

        Retorne apenas um JSON:
        {{"quality_score": N, "reasoning": "..."}}
        """

        eval_result = evaluator_llm.invoke(eval_prompt)

        # Parse score
        import json
        try:
            score_data = json.loads(eval_result.content)
            quality_score = score_data.get("quality_score", 5)
        except:
            quality_score = 5

        metrics[model_name] = {
            "quality_score": quality_score / 10.0,  # Normalizar 0-1
            "latency_ms": state["latencies"][model_name]
        }

    return {"metrics": metrics}


def create_benchmark_graph(models_config: List[Dict]):
    """
    Cria grafo LangGraph para benchmark paralelo.

    Args:
        models_config: Lista de configs [{"provider": "openai", "model": "gpt-4o"}]

    Returns:
        Compiled LangGraph
    """
    workflow = StateGraph(BenchmarkState)

    # Criar LLMs
    llms = {}
    for config in models_config:
        model_name = f"{config['provider']}:{config['model']}"

        if config["provider"] == "openai":
            llms[model_name] = ChatOpenAI(model=config["model"])
        elif config["provider"] == "anthropic":
            llms[model_name] = ChatAnthropic(model=config["model"])
        elif config["provider"] == "google":
            llms[model_name] = ChatGoogleGenerativeAI(model=config["model"])

    # Adicionar nodes para cada modelo (execução paralela)
    for model_name, llm in llms.items():
        workflow.add_node(
            model_name,
            create_model_node(model_name, llm)
        )

    # Node de avaliação
    workflow.add_node("evaluate", evaluate_responses_node)

    # Entry point (start parallelization)
    first_model = list(llms.keys())[0]
    workflow.set_entry_point(first_model)

    # Conectar modelos em paralelo (todos executam concorrentemente)
    # e convergem para evaluate
    for model_name in llms.keys():
        workflow.add_edge(model_name, "evaluate")

    workflow.add_edge("evaluate", END)

    return workflow.compile()


# Uso
if __name__ == "__main__":
    models = [
        {"provider": "openai", "model": "gpt-4o"},
        {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
        {"provider": "google", "model": "gemini-1.5-pro"}
    ]

    graph = create_benchmark_graph(models)

    result = graph.invoke({
        "input": "Explique machine learning em 2 parágrafos",
        "models": [f"{m['provider']}:{m['model']}" for m in models]
    })

    print("\n📊 Resultados:")
    for model, metrics in result["metrics"].items():
        print(f"\n{model}:")
        print(f"  Quality: {metrics['quality_score']:.2f}")
        print(f"  Latency: {metrics['latency_ms']:.0f}ms")

```text

**Exemplo: `langsmith_evaluators.py`** (LangSmith Evaluators)

```python
"""
LangSmith Evaluators para Benchmark
Usa evaluators nativos e custom do LangSmith.
"""

from langsmith.evaluation import LangChainStringEvaluator
from langchain_openai import ChatOpenAI

def get_quality_evaluators():
    """
    Retorna evaluators de qualidade do LangSmith.

    Returns:
        Lista de evaluators prontos para usar
    """
    return [
        # Q&A correctness
        LangChainStringEvaluator("qa"),

        # Context-aware Q&A
        LangChainStringEvaluator("context_qa"),

        # Helpfulness
        LangChainStringEvaluator("criteria",
            config={"criteria": "helpfulness"}),

        # Harmfulness (safety)
        LangChainStringEvaluator("criteria",
            config={"criteria": "harmfulness"}),
    ]


def get_custom_evaluators():
    """
    Retorna custom evaluators usando LLM-as-judge.

    Returns:
        Lista de custom evaluators
    """
    return [
        # Relevance evaluator
        LangChainStringEvaluator("labeled_criteria",
            config={
                "criteria": {
                    "relevance": "Is the answer relevant to the question?"
                },
                "llm": ChatOpenAI(model="gpt-4o-mini")
            }
        ),

        # Accuracy evaluator
        LangChainStringEvaluator("labeled_criteria",
            config={
                "criteria": {
                    "accuracy": "Is the answer factually correct based on the context?"
                },
                "llm": ChatOpenAI(model="gpt-4o-mini")
            }
        ),

        # Coherence evaluator
        LangChainStringEvaluator("labeled_criteria",
            config={
                "criteria": {
                    "coherence": "Is the answer coherent and well-structured?"
                },
                "llm": ChatOpenAI(model="gpt-4o-mini")
            }
        ),
    ]


def get_all_evaluators():
    """
    Retorna todos os evaluators (nativos + custom).

    Returns:
        Lista completa de evaluators
    """
    return get_quality_evaluators() + get_custom_evaluators()

```text

### Passo 4: Implementar Callbacks para Métricas

**Exemplo: `latency_callback.py`**

```python
"""
LangChain Callback para tracking de latência e TTFT.
"""

from langchain_core.callbacks import BaseCallbackHandler
import time
from typing import List, Dict
import numpy as np


class LatencyTracker(BaseCallbackHandler):
    """
    Callback para medir latência e Time to First Token.

    Usa hooks do LangChain:
    - on_llm_start: marca início
    - on_llm_new_token: captura TTFT (primeiro token)
    - on_llm_end: calcula latência total
    """

    def __init__(self):
        self.latencies: List[float] = []
        self.ttfts: List[float] = []
        self.current_start: float = None
        self.current_first_token: float = None

    def on_llm_start(self, serialized: Dict, prompts: List[str], **kwargs):
        """Marca início da inferência"""
        self.current_start = time.perf_counter()
        self.current_first_token = None

    def on_llm_new_token(self, token: str, **kwargs):
        """Captura Time to First Token (streaming)"""
        if self.current_first_token is None and self.current_start:
            self.current_first_token = time.perf_counter()
            ttft = (self.current_first_token - self.current_start) * 1000
            self.ttfts.append(ttft)

    def on_llm_end(self, response, **kwargs):
        """Calcula latência total"""
        if self.current_start:
            latency = (time.perf_counter() - self.current_start) * 1000
            self.latencies.append(latency)

    def on_llm_error(self, error: Exception, **kwargs):
        """Reset em caso de erro"""
        self.current_start = None
        self.current_first_token = None

    def get_statistics(self) -> Dict[str, float]:
        """
        Retorna estatísticas de performance.

        Returns:
            Dict com métricas de latência e TTFT
        """
        if not self.latencies:
            return {
                "avg_latency_ms": 0.0,
                "p50_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "avg_ttft_ms": 0.0,
                "p95_ttft_ms": 0.0,
            }

        stats = {
            "avg_latency_ms": np.mean(self.latencies),
            "p50_latency_ms": np.percentile(self.latencies, 50),
            "p95_latency_ms": np.percentile(self.latencies, 95),
            "p99_latency_ms": np.percentile(self.latencies, 99),
            "min_latency_ms": np.min(self.latencies),
            "max_latency_ms": np.max(self.latencies),
        }

        if self.ttfts:
            stats.update({
                "avg_ttft_ms": np.mean(self.ttfts),
                "p50_ttft_ms": np.percentile(self.ttfts, 50),
                "p95_ttft_ms": np.percentile(self.ttfts, 95),
                "p99_ttft_ms": np.percentile(self.ttfts, 99),
            })
        else:
            stats.update({
                "avg_ttft_ms": 0.0,
                "p50_ttft_ms": 0.0,
                "p95_ttft_ms": 0.0,
                "p99_ttft_ms": 0.0,
            })

        return stats

    def reset(self):
        """Reset das métricas"""
        self.latencies = []
        self.ttfts = []
        self.current_start = None
        self.current_first_token = None

```text

### Passo 5: Script Principal

**`run_benchmark.py`**:

```python
"""
Script principal para executar benchmark usando LangChain/LangSmith.
"""

import asyncio
from benchmarking.langchain_benchmark import LangChainBenchmark, BenchmarkConfig

async def main():
    """Executa benchmark comparativo com LangChain/LangSmith"""

    # Configuração
    config = BenchmarkConfig(
        models=[
            {"provider": "openai", "model": "gpt-4o", "temperature": 0},
            {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022", "temperature": 0},
            {"provider": "google", "model": "gemini-1.5-pro", "temperature": 0}
        ],
        dataset_name="my-benchmark-dataset",  # Dataset no LangSmith
        evaluators=["qa", "context_qa", "helpfulness", "relevance"],
        project_name="llm-benchmark-comparison",  # Projeto LangSmith
        parallel=True,
        max_concurrency=10
    )

    # Executar benchmark
    benchmark = LangChainBenchmark(config)
    results = await benchmark.run_benchmark()

    # Gerar relatórios
    benchmark.generate_reports(["json", "markdown", "html", "langsmith"])

    print("\n✅ Benchmark concluído!")
    print(f"📊 Veja resultados no LangSmith: https://smith.langchain.com/o/your-org/projects/p/{config.project_name}")
    print("📄 Relatórios gerados em results/")

if __name__ == "__main__":
    asyncio.run(main())

```text

## 📊 Exemplo de Output

### LangSmith UI

Todos os resultados são automaticamente trackados no LangSmith:
- ✅ Traces completos de cada inferência
- ✅ Token usage automático
- ✅ Costs automáticos (se pricing configurado)
- ✅ Evaluator scores
- ✅ Comparison view entre modelos
- ✅ Dataset annotations

### Markdown Report

```markdown

# 📊 LLM Benchmark Report

## Summary
- **Models Evaluated**: 3 (gpt-4o, claude-3.5-sonnet, gemini-1.5-pro)
- **Dataset**: my-benchmark-dataset (500 examples)
- **LangSmith Project**: llm-benchmark-comparison
- **Duration**: 127 seconds
- **Total Cost**: $2.45

## 📈 Comparison Tables

### Quality Metrics (LangSmith Evaluators)

| Model | QA Score | Helpfulness | Relevance | Harmfulness |
|-------|----------|-------------|-----------|-------------|
| gpt-4o | 0.872 | 0.91 | 0.89 | 0.02 |
| claude-3.5-sonnet | 0.858 | 0.89 | 0.91 | 0.01 |
| gemini-1.5-pro | 0.843 | 0.87 | 0.85 | 0.03 |

### Performance Metrics (LangChain Callbacks)

| Model | Avg Latency | P95 Latency | P99 Latency | TTFT (P95) |
|-------|-------------|-------------|-------------|------------|
| claude-3.5-sonnet | 432ms | 891ms | 1203ms | 187ms |
| gemini-1.5-pro | 521ms | 1034ms | 1421ms | 203ms |
| gpt-4o | 687ms | 1456ms | 2103ms | 312ms |

### Cost Metrics (LangSmith Tracking)

| Model | Total Cost | Cost/1K Tokens | Cost Efficiency |
|-------|------------|----------------|-----------------|
| gemini-1.5-pro | $0.43 | $0.001234 | 196.05 qa/$ |
| claude-3.5-sonnet | $0.87 | $0.002891 | 98.62 qa/$ |
| gpt-4o | $1.15 | $0.003421 | 75.83 qa/$ |

## 🏆 Winner Analysis

🎯 **Best Quality**: gpt-4o (QA Score: 0.872)
⚡ **Fastest (P95)**: claude-3.5-sonnet (891ms)
💰 **Best Value**: gemini-1.5-pro (196.05 qa per $)
🛡️ **Safest**: claude-3.5-sonnet (Harmfulness: 0.01)

## 💡 Recommendations

### For Production Use
- **Best overall**: **claude-3.5-sonnet** (balanced quality, speed, safety)
- **Budget-conscious**: **gemini-1.5-pro** (best cost-efficiency)
- **Highest quality**: **gpt-4o** (best QA score)

```text

## 🎓 Melhores Práticas

### 1. Use LangSmith para Tracking Automático

**LangSmith automaticamente trackeia**:
- Token usage por request
- Costs (se pricing configurado)
- Traces completos
- Evaluator scores
- Latências (via UI)

**Não precisa calcular manualmente!**

### 2. Use LCEL Batch para Paralelização

```python

# LCEL batch executa em paralelo automaticamente
results = chain.batch(
    inputs,
    config=RunnableConfig(max_concurrency=10)
)

```text

### 3. Use LangSmith Evaluators Nativos

**Vantagens**:
- Implementações testadas
- Sem código extra
- Tracking automático
- Consistency

### 4. Use Callbacks para Métricas Customizadas

**Para métricas que LangSmith não trackeia automaticamente**:
- TTFT (Time to First Token)
- Percentis de latência (P95, P99)
- Custom performance metrics

### 5. Configure Pricing no LangSmith

**Para cost tracking automático**:

```python

# Via LangSmith UI ou API
client.update_pricing({
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
    # etc
})

```text

## ⚙️ Variáveis de Ambiente Necessárias

```bash

# API Keys dos LLMs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LangSmith (OBRIGATÓRIO para tracking)
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=llm-benchmark-comparison

# Opcional: Endpoint customizado
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

```text

## 🔗 Integração com LangSmith

### Setup Inicial

```bash

# Instalar dependências
pip install langchain-openai langchain-anthropic langchain-google-genai
pip install langsmith langgraph
pip install numpy

# Configurar LangSmith
export LANGSMITH_API_KEY=lsv2_...
export LANGSMITH_TRACING=true

```text

### Upload Dataset para LangSmith

```python
from langsmith import Client

client = Client()

# Upload dataset
dataset = client.create_dataset("my-benchmark-dataset")

# Adicionar exemplos
client.create_examples(
    inputs=[
        {"input": "What is the capital of France?"},
        {"input": "Explain quantum computing"},
        # ...
    ],
    outputs=[
        {"output": "Paris"},
        {"output": "..."},
        # ...
    ],
    dataset_id=dataset.id
)

```text

## 🚨 Vantagens de Usar LangChain/LangSmith

✅ **Automatic Tracking**: Custos, tokens, latências trackados automaticamente
✅ **Built-in Evaluators**: Evaluators prontos (qa, context_qa, criteria)
✅ **LCEL Parallelization**: Batch processing otimizado
✅ **Visualization**: UI do LangSmith para análise visual
✅ **Versioning**: Experiments versionados automaticamente
✅ **Comparison View**: Compare modelos lado a lado no UI
✅ **No Reinventar Roda**: Infraestrutura pronta de evaluation

## 📖 Referências

### LangChain/LangSmith
- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [LCEL Batch Processing](https://python.langchain.com/docs/how_to/parallel/)
- [LangChain Callbacks](https://python.langchain.com/docs/integrations/callbacks/)
- [LangGraph Parallel Workflows](https://langchain-ai.github.io/langgraph/how-tos/)

### Benchmarks
- [MMLU](https://arxiv.org/abs/2009.03300)
- [HumanEval](https://github.com/openai/human-eval)
- [BBQ Bias Benchmark](https://arxiv.org/abs/2110.08193)


**Criado com llm-eval-developer plugin usando LangChain/LangGraph/LangSmith** 🚀
````
