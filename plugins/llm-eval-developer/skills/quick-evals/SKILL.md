---
name: quick-evals
description: Quick evaluation strategies for LLM development with fast feedback loops (<5min). Use when implementing rapid iteration cycles, validating code changes during development, setting up continuous testing, or designing evaluation rhythms. Covers Golden Datasets, upload_results=False patterns, subset strategies, and local execution.
version: 1.0.0
allowed-tools:
  - Read
  - Grep
  - Bash
  - Write
---

# Quick Evals - Fast Feedback Evaluation Strategies

**Estratégias de avaliação rápida para desenvolvimento de LLMs com feedback imediato**

## 📋 When to Use Me

Invoke this skill when you need to:

- **Implement rapid evaluation cycles** during LLM development (< 5 minutes)
- **Set up continuous testing** for each commit or significant code change
- **Design evaluation rhythms** distinguishing Quick vs Formal evaluations
- **Create Golden Datasets** with 50-200 curated examples for fast iteration
- **Configure local execution** using `upload_results=False` in LangSmith
- **Validate technical metrics** like latency, memory usage, and regressions
- **Balance speed and quality** in evaluation strategies
- **Debug LLM applications** with immediate feedback loops
- **Avoid polluting dashboards** during active development

**Trigger terms**: quick eval, fast feedback, golden dataset, upload_results false, continuous testing, evaluation rhythms, local evaluation, subset strategy, rapid iteration

## 🎓 Core Knowledge

### 1. The Three Evaluation Rhythms

Quick Evals are part of a multi-layered evaluation strategy with different rhythms:

| Rhythm | Timing | Duration | Dataset | Purpose |
|--------|--------|----------|---------|---------|
| **Quick** | Each commit | < 5 min | 1-5% subset | Fast feedback, catch regressions early |
| **Continuous** | Hourly/Daily | 15-30 min | 10-20% subset | Ongoing validation, trend monitoring |
| **Formal** | End of sprint | 30-60 min | 100% full dataset | Quality gate before deployment |

**Key principle**: Quick Evals prioritize **speed over completeness** to enable rapid debugging.

### 2. Golden Dataset Strategy

A Golden Dataset is a **manually curated** collection of 50-200 high-quality examples that:

- ✅ Covers standard cases and critical edge cases
- ✅ Acts as a "key answer sheet" for model behavior
- ✅ Enables fast, reliable benchmarking during iteration
- ✅ Balances curation time with comprehensive insights

**Size recommendations**:

- **Initial**: 10-20 examples for quick smoke tests
- **Development**: 50-100 examples for iterative improvements
- **Production-ready**: 100-200 examples for comprehensive assessment

### 3. Local Execution Pattern (LangSmith)

**Critical parameter**: `upload_results=False`

```python
from langsmith import Client

ls_client = Client()
experiment = ls_client.evaluate(
    target_function,
    data=golden_dataset,
    evaluators=[evaluator_list],
    upload_results=False  # ← Prevents cloud upload
)
```

**Benefits**:

- ⚡ Faster iteration (no network latency)
- 🧹 Clean dashboard (no dev pollution)
- 🔒 Local-only results during active development
- 📊 Analyze results in-memory before committing

### 4. Subset Strategies for Speed

To achieve < 5 minute execution:

- **1% subset**: 10 examples from 1000 → ultra-fast smoke test
- **5% subset**: 50 examples from 1000 → balanced quick eval
- **Golden Dataset**: Fixed 50-200 examples → consistent benchmark
- **Full dataset**: 1000+ examples → reserved for Formal Eval only

**Rule of thumb**: Use smallest subset that catches regressions reliably.

### 5. Technical Metrics Focus

Quick Evals prioritize **deterministic, technical validation**:

✅ **Must-have metrics**:

- Unit test pass/fail
- Latency thresholds (e.g., < 500ms)
- Memory usage limits
- Logic validation (expected output format)
- Regression detection (comparison with baseline)

⚠️ **Optional for Quick Evals** (save for Formal):

- Comprehensive accuracy scores
- Human evaluation
- A/B testing results
- Business metrics

### 6. Alerts and Checkpoints

Incorporate automatic alerts in Quick Eval scripts:

```python
# Example checkpoint
if avg_latency > 500:  # ms
    print("⚠️ ALERTA: Latency exceeds threshold!")
    print(f"Current: {avg_latency}ms | Limit: 500ms")
```

**Alert triggers**:

- Performance degradation (latency, memory)
- Logic failures (unexpected outputs)
- Regression detection (worse than baseline)
- Critical edge case failures

### 7. Node-Level Metrics (LangGraph Agents)

For complex agent architectures, collect metrics **per node**:

```python
# Per-node metrics collection
node_metrics = {
    "node_name": {
        "latency": measure_latency(node),
        "tokens": count_tokens(node),
        "cost": calculate_cost(node),
    }
}
```

Even with local execution, understanding bottlenecks at node level is critical.

## 📚 Reference Files

For detailed technical implementations and patterns:

- **REFERENCE.md** - Complete technical documentation on Quick Eval implementation
- **PATTERNS.md** - Implementation patterns for different frameworks (LangSmith, LangChain, custom)
- **EXAMPLES.md** - Practical code examples and real-world scenarios

## 💡 Quick Examples

### Example 1: Basic Quick Eval with Golden Dataset

```python
from langsmith import Client

# 1. Define Golden Dataset (50 curated examples)
golden_dataset = [
    {"input": "What is 2+2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
    # ... 48 more carefully selected examples
]

# 2. Run local Quick Eval (< 5 min)
client = Client()
results = client.evaluate(
    my_llm_function,
    data=golden_dataset,
    evaluators=[correctness_check, latency_check],
    upload_results=False  # Local only
)

# 3. Check alerts
if results.avg_latency > 500:
    print("⚠️ ALERTA: Latency too high!")
```

### Example 2: Continuous Testing Integration

```python
# In CI/CD pipeline or git hook
def run_quick_eval():
    """Runs on every commit"""
    subset = load_golden_dataset()[:50]  # 50 examples

    start = time.time()
    results = evaluate_locally(subset)
    duration = time.time() - start

    assert duration < 300, "Quick Eval exceeded 5 minutes"
    assert results.pass_rate > 0.90, "Regression detected"

    return results
```

### Example 3: Three-Rhythm Strategy

```python
# Quick Eval - Each commit
quick_eval(dataset=golden_50, upload=False, duration="<5min")

# Continuous Eval - Hourly
continuous_eval(dataset=subset_200, upload=True, duration="15min")

# Formal Eval - End of sprint
formal_eval(dataset=full_10k, upload=True, duration="60min")
```

## ✅ Quick Checklist

Before implementing Quick Evals, ensure:

- [ ] Golden Dataset created with 50-200 curated examples
- [ ] Execution time target set (< 5 minutes)
- [ ] `upload_results=False` configured for local runs
- [ ] Technical metrics defined (latency, memory, pass/fail)
- [ ] Alert thresholds configured (performance, regressions)
- [ ] Subset strategy chosen (1%, 5%, or Golden Dataset)
- [ ] Clear distinction from Formal Eval (timing, dataset size)
- [ ] Integration with development workflow (commit hooks, CI/CD)
- [ ] Node-level metrics planned (for complex agents)

## 🎯 Remember

> **Quick Evals are like a microwave test for a complex recipe.**
>
> You don't cook the entire dish for formal judges every time you add seasoning. Instead, you take a **small sample** (Golden Dataset), test it **rapidly** (< 5 min), and correct **immediately** before ruining the main dish. The microwave test is local and doesn't go into the official kitchen history.

**Golden Rule**: Prioritize **speed and immediate feedback** over comprehensive coverage during active development. Reserve full evaluation for quality gates.

## 📏 Sizing Guidelines

- **SKILL.md**: ~300 lines ✅
- **Total with references**: ~1300 lines (SKILL + REFERENCE + PATTERNS + EXAMPLES)
- **Specialization**: Fast feedback evaluation strategies (unique focus)

**For implementation details**, see REFERENCE.md
**For code patterns**, see PATTERNS.md
**For practical scenarios**, see EXAMPLES.md
