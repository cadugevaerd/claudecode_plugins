# Dataset Lifecycle - Versioning and Management

Complete lifecycle management: versioning patterns, creation vs update decisions, local storage organization, and CI/CD integration.

## 🔄 Dataset Lifecycle Overview

A dataset is a living artifact that evolves over time. Proper lifecycle management ensures:

- ✅ **Reproducibility** - Pin evaluations to specific dataset versions
- ✅ **Traceability** - Track what changed and when
- ✅ **Collaboration** - Multiple teams can work on datasets
- ✅ **CI/CD Integration** - Automated testing on every change

**Lifecycle stages**:

```
1. Creation → 2. Active Use → 3. Maintenance → 4. Versioning → 5. Archival
```

## 📦 Versioning Strategies

### Strategy 1: Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH` (e.g., `v2.1.3`)

**Rules**:

- **MAJOR**: Breaking schema changes, incompatible with previous evaluations
- **MINOR**: New examples added, backward-compatible
- **PATCH**: Fixes to existing examples (typos, corrections)

**Examples**:

```python
# v1.0.0 → v2.0.0 (MAJOR)
# Breaking change: Renamed input field
v1 = {"inputs": {"question": "..."}}
v2 = {"inputs": {"query": "..."}}  # Breaking!

# v1.0.0 → v1.1.0 (MINOR)
# Added 20 new examples
dataset_v1_1 = dataset_v1 + new_examples  # Backward-compatible

# v1.1.0 → v1.1.1 (PATCH)
# Fixed typo in reference output
example_before = {"outputs": {"answer": "Pari"}}  # Typo
example_after = {"outputs": {"answer": "Paris"}}  # Fixed
```

**When to use**:

- ✅ Long-lived datasets with multiple consumers
- ✅ Need clear communication of breaking changes
- ✅ Formal release processes

### Strategy 2: Branch-Based Versioning

**Format**: `dataset-name_branch-name_version` (e.g., `qa-system_feature-improved-rag_v1.0.0`)

**Rules**:

- Tie dataset version to git branch
- Create new dataset per feature branch
- Merge datasets when merging code

**Examples**:

```python
# Main branch
dataset_main = "qa-system_main_v1.5.0"

# Feature branch
dataset_feature = "qa-system_feature-improved-rag_v1.0.0"

# After feature merge → bump main version
dataset_main_updated = "qa-system_main_v1.6.0"
```

**When to use**:

- ✅ Parallel feature development
- ✅ Need to test features independently
- ✅ Git-based workflows

### Strategy 3: Timestamp-Based Versioning

**Format**: `dataset-name_YYYY-MM-DD` (e.g., `qa-system_2025-01-08`)

**Rules**:

- Create new version on schedule (weekly, monthly)
- Snapshot of production data at point in time

**Examples**:

```python
# Weekly snapshots
dataset_jan_01 = "prod-traces_2025-01-01"
dataset_jan_08 = "prod-traces_2025-01-08"
dataset_jan_15 = "prod-traces_2025-01-15"
```

**When to use**:

- ✅ Production data snapshots
- ✅ Trend analysis over time
- ✅ Compliance/audit requirements

### Choosing a Strategy

| Situation | Best Strategy |
|-----------|---------------|
| Golden dataset, stable schema | Semantic versioning |
| Active development, multiple features | Branch-based |
| Production data snapshots | Timestamp-based |
| Rapid iteration (daily changes) | Timestamp or branch-based |

## 🆕 Creation vs Update Decision

### When to CREATE a New Dataset Version

✅ **Create new version when**:

1. **Schema changes** (breaking or significant)

   ```python
   # Old schema
   v1 = {"inputs": {"question": "..."}}

   # New schema → NEW VERSION
   v2 = {"inputs": {"query": "...", "context": "..."}}
   ```

1. **End of sprint/milestone**

   - Freeze dataset for reproducibility
   - Tag with sprint version: `qa-system_sprint-5_v1.0.0`

1. **Significant content changes** (> 20% of examples)

   - Adding 50+ new examples to 200-example dataset
   - Major rebalancing of categories

1. **Production snapshots** (scheduled)

   - Weekly/monthly production data snapshots
   - Always create new version, never update

### When to UPDATE Existing Dataset

✅ **Update existing version when**:

1. **Minor corrections** (typos, small fixes)

   ```python
   # Fix typo - can update in place
   before = {"outputs": {"answer": "Pari"}}
   after = {"outputs": {"answer": "Paris"}}
   ```

1. **Metadata enrichment** (no schema change)

   ```python
   # Add metadata - backward-compatible
   before = {"metadata": {"category": "qa"}}
   after = {"metadata": {"category": "qa", "difficulty": "easy"}}
   ```

1. **During active development** (same sprint)

   - Iterating on golden dataset
   - Not yet "released"

1. **Small additions** (< 10% growth)

   - Adding 5 examples to 100-example dataset

### Decision Tree

```
Dataset change needed?
│
├─ Schema change?
│  └─ Yes → CREATE new version (MAJOR bump)
│
├─ > 20% content change?
│  └─ Yes → CREATE new version (MINOR bump)
│
├─ End of sprint/milestone?
│  └─ Yes → CREATE new version (freeze)
│
├─ Production snapshot?
│  └─ Yes → CREATE new version (timestamp)
│
└─ Small fix/addition/enrichment?
   └─ Yes → UPDATE existing version
```

## 📁 Local Storage Organization

### Recommended Structure

```
project-root/
├── datasets/
│   ├── golden/
│   │   ├── qa-system_v1.0.0.json
│   │   ├── qa-system_v1.1.0.json
│   │   └── qa-system_v1.2.0.json
│   │
│   ├── production/
│   │   ├── prod-traces_2025-01-01.json
│   │   ├── prod-traces_2025-01-08.json
│   │   └── prod-traces_2025-01-15.json
│   │
│   └── README.md  # Dataset catalog
│
├── src/
│   └── evaluations/
│       ├── sync_datasets.py  # Upload to LangSmith
│       └── run_eval.py       # Run evaluations
│
└── .gitignore  # Optionally track datasets in git
```

### Dataset File Format

**JSON format** (recommended):

```json
{
  "metadata": {
    "name": "qa-system_v1.0.0",
    "description": "Golden dataset for Q&A evaluation",
    "version": "1.0.0",
    "created_at": "2025-01-08T10:00:00Z",
    "created_by": "engineer@company.com",
    "schema_version": "1.0"
  },
  "examples": [
    {
      "inputs": {"question": "What is LangChain?"},
      "outputs": {"answer": "LangChain is a framework..."},
      "metadata": {"category": "basic_qa", "difficulty": "easy"}
    }
  ]
}
```

**CSV format** (for simple datasets):

```csv
question,answer,category,difficulty
"What is LangChain?","LangChain is a framework...","basic_qa","easy"
"What is the capital of France?","Paris","factual","easy"
```

### Syncing Local ↔ LangSmith

**Upload script** (`sync_datasets.py`):

```python
import json
from langsmith import Client

def upload_dataset(file_path: str):
    """Upload local JSON dataset to LangSmith."""

    # Load local file
    with open(file_path, "r") as f:
        data = json.load(f)

    # Initialize client
    client = Client()

    # Create or update dataset
    try:
        dataset = client.create_dataset(
            dataset_name=data["metadata"]["name"],
            description=data["metadata"]["description"]
        )
        print(f"Created dataset: {dataset.name}")
    except Exception as e:
        print(f"Dataset already exists: {e}")
        dataset = client.read_dataset(dataset_name=data["metadata"]["name"])

    # Upload examples
    client.create_examples(
        dataset_id=dataset.id,
        examples=data["examples"]
    )

    print(f"Uploaded {len(data['examples'])} examples")

# Usage
upload_dataset("datasets/golden/qa-system_v1.0.0.json")
```

**Download script** (backup):

```python
from langsmith import Client

def download_dataset(dataset_name: str, output_path: str):
    """Download LangSmith dataset to local JSON."""

    client = Client()

    # Fetch dataset
    dataset = client.read_dataset(dataset_name=dataset_name)
    examples = list(client.list_examples(dataset_id=dataset.id))

    # Convert to JSON
    data = {
        "metadata": {
            "name": dataset.name,
            "description": dataset.description,
            "created_at": dataset.created_at.isoformat(),
        },
        "examples": [
            {
                "inputs": ex.inputs,
                "outputs": ex.outputs,
                "metadata": ex.metadata if hasattr(ex, "metadata") else {}
            }
            for ex in examples
        ]
    }

    # Save to file
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Downloaded {len(examples)} examples to {output_path}")

# Usage
download_dataset("qa-system_v1.0.0", "datasets/golden/qa-system_v1.0.0.json")
```

### Git Integration

**Option 1: Track datasets in Git** (small datasets)

```bash
# .gitignore - do NOT ignore datasets
# datasets/ should be tracked

git add datasets/golden/qa-system_v1.0.0.json
git commit -m "feat: add qa-system golden dataset v1.0.0"
```

**Benefits**:

- ✅ Full version control
- ✅ Easy rollback
- ✅ PR review of dataset changes

**Limitations**:

- ❌ Large files slow down git
- ❌ Not suitable for > 100MB datasets

**Option 2: Use Git LFS** (large datasets)

```bash
# Track large dataset files with Git LFS
git lfs track "datasets/**/*.json"
git add .gitattributes
git commit -m "chore: track datasets with Git LFS"

# Add large dataset
git add datasets/production/prod-traces_2025-01-08.json
git commit -m "feat: add production snapshot 2025-01-08"
```

**Benefits**:

- ✅ Handles large files (GB scale)
- ✅ Still versioned in git

**Option 3: External storage** (very large datasets)

Store in S3/GCS, track metadata in git:

```json
// datasets/catalog.json (tracked in git)
{
  "qa-system_v1.0.0": {
    "location": "s3://datasets/golden/qa-system_v1.0.0.json",
    "size_mb": 450,
    "created_at": "2025-01-08",
    "examples_count": 1500
  }
}
```

## 🚀 CI/CD Integration

### Automated Evaluation on Dataset Changes

**GitHub Actions example**:

```yaml
# .github/workflows/eval-on-dataset-change.yml
name: Run Evaluation on Dataset Change

on:
  push:
    paths:
      - 'datasets/golden/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install langsmith langchain

      - name: Sync datasets to LangSmith
        env:
          LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}
        run: |
          python src/evaluations/sync_datasets.py

      - name: Run evaluation
        env:
          LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}
        run: |
          python src/evaluations/run_eval.py --dataset qa-system_v1.0.0

      - name: Comment results on PR
        uses: actions/github-script@v6
        with:
          script: |
            const results = require('./eval_results.json')
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Evaluation Results: ${results.accuracy}% accuracy`
            })
```

### Regression Testing on Model Changes

**Workflow**:

```
1. Model/prompt change committed
   ↓
2. CI triggers evaluation on LATEST production dataset
   ↓
3. Compare results to baseline (previous model)
   ↓
4. Block merge if regression detected (accuracy drops > 5%)
```

**Example regression check**:

```python
# src/evaluations/regression_check.py
from langsmith import Client

def check_regression(dataset_name: str, threshold: float = 0.05):
    """Check if new model regresses on dataset."""

    client = Client()

    # Get latest evaluation results
    current_results = client.get_test_results(
        dataset_name=dataset_name,
        project_name="current-model"
    )

    # Get baseline results
    baseline_results = client.get_test_results(
        dataset_name=dataset_name,
        project_name="baseline-model"
    )

    # Compare accuracy
    current_acc = current_results.metrics["accuracy"]
    baseline_acc = baseline_results.metrics["accuracy"]

    regression = baseline_acc - current_acc

    if regression > threshold:
        raise ValueError(
            f"Regression detected! "
            f"Accuracy dropped {regression:.2%} "
            f"({baseline_acc:.2%} → {current_acc:.2%})"
        )

    print(f"No regression. Accuracy: {current_acc:.2%}")

# Usage in CI
check_regression("prod-regression_v2.0.0", threshold=0.05)
```

## 📊 Dataset Metrics Tracking

Track these metrics over time:

```python
# Dataset health metrics
metrics = {
    "version": "v1.2.0",
    "total_examples": 150,
    "examples_added_this_version": 20,
    "examples_removed_this_version": 5,
    "schema_version": "1.0",
    "last_updated": "2025-01-08",
    "avg_input_length": 45,  # characters
    "avg_output_length": 120,
    "category_distribution": {
        "basic_qa": 70,
        "factual": 40,
        "edge_case": 40
    },
    "difficulty_distribution": {
        "easy": 90,
        "medium": 50,
        "hard": 10
    }
}
```

**Dashboard example** (Streamlit):

```python
import streamlit as st
import json

st.title("Dataset Health Dashboard")

# Load metrics history
with open("datasets/metrics_history.json") as f:
    history = json.load(f)

# Plot growth over time
st.line_chart(history["total_examples"])

# Show category balance
st.bar_chart(history["latest"]["category_distribution"])
```

## ✅ Lifecycle Best Practices

1. **Always version datasets** - Never overwrite without versioning
1. **Local storage first** - Keep local copies, sync to LangSmith
1. **Automate syncing** - Use scripts to avoid manual uploads
1. **Track in git** - Small datasets in git, large in Git LFS
1. **CI/CD integration** - Auto-eval on dataset changes
1. **Regression testing** - Block merges on performance drops
1. **Metrics tracking** - Monitor dataset health over time
1. **Scheduled snapshots** - Production data weekly/monthly
1. **Archival policy** - Remove datasets older than 1 year
1. **Documentation** - Maintain README in `datasets/` folder

## 📚 Dataset Catalog Template

**datasets/README.md**:

````markdown
# Dataset Catalog

## Golden Datasets

| Name | Version | Examples | Purpose | Last Updated |
|------|---------|----------|---------|--------------|
| qa-system | v1.2.0 | 150 | Quick Evals | 2025-01-08 |
| rag-system | v2.0.0 | 200 | A/B Testing | 2025-01-05 |

## Production Datasets

| Name | Date | Examples | Source | Status |
|------|------|----------|--------|--------|
| prod-traces | 2025-01-08 | 500 | Sampled failures | Active |
| prod-traces | 2025-01-01 | 480 | Sampled failures | Archived |

## Versioning Convention

- Golden: Semantic versioning (`vMAJOR.MINOR.PATCH`)
- Production: Timestamp (`YYYY-MM-DD`)

## Sync Instructions

```bash
# Upload to LangSmith
python src/evaluations/sync_datasets.py

# Download from LangSmith
python src/evaluations/download_dataset.py qa-system_v1.2.0
````

## Contact

- Dataset Owner: data-team@company.com
- Questions: #data-quality Slack channel

```

## 🎯 Lifecycle Checklist

- [ ] Versioning strategy chosen (semantic/branch/timestamp)
- [ ] Local storage structure created (`datasets/`)
- [ ] Sync scripts implemented (upload/download)
- [ ] Git integration configured (direct/LFS/external)
- [ ] CI/CD workflows added (auto-eval, regression)
- [ ] Metrics tracking setup (health dashboard)
- [ ] Dataset catalog maintained (README.md)
- [ ] Archival policy defined (> 1 year old)
- [ ] Team documentation shared (how to create/update)

## 📚 Additional Resources

- **Data Versioning with DVC**: https://dvc.org/doc/use-cases/versioning-data-and-models
- **LangSmith Dataset Management UI**: https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application
- **Git LFS**: https://git-lfs.github.com/
```
