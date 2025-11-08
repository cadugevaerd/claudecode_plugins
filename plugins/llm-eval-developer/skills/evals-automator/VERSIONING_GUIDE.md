# Dataset Versioning Guide - Guia Completo de Versionamento

Estratégias de versionamento para datasets LangSmith seguindo Semantic Versioning.

## 🎯 Por Que Versionar Datasets?

Datasets evoluem ao longo do tempo:

- Novos examples adicionados
- Corrections de erros em examples
- Schema changes (novos campos, estrutura diferente)
- Splits diferentes (train/test/validation)

**Versionamento garante**:

- ✅ **Reprodutibilidade**: Experimentos podem referenciar versão específica
- ✅ **Rastreabilidade**: Saber o que mudou entre versões
- ✅ **Rollback**: Voltar a versões anteriores se necessário
- ✅ **Comparabilidade**: Comparar métricas entre versões

## 📊 Semantic Versioning para Datasets

### Formato: `MAJOR.MINOR.PATCH`

**MAJOR** (quebra compatibilidade):

- Schema changes incompatíveis
- Remoção de campos obrigatórios
- Mudança de estrutura de inputs/outputs
- Mudança de tipo de dados

**MINOR** (adições compatíveis):

- Novos examples adicionados
- Novos campos opcionais adicionados
- Expansão de dataset mantendo compatibilidade

**PATCH** (correções):

- Correção de erros em examples existentes
- Typos corrigidos
- Metadata updates

### Exemplos de Incremento

```python
# v1.0.0 - Initial release
dataset_name = "qa-system_v1.0.0"
# 100 examples, schema: {"question": str} → {"answer": str}

# v1.0.1 - PATCH: Corrigir typos em 5 examples
dataset_name = "qa-system_v1.0.1"
# 100 examples (mesmos), 5 corrigidos

# v1.1.0 - MINOR: Adicionar 50 novos examples
dataset_name = "qa-system_v1.1.0"
# 150 examples, schema mantido

# v1.2.0 - MINOR: Adicionar campo opcional "category" em outputs
dataset_name = "qa-system_v1.2.0"
# 150 examples, schema: outputs agora têm {"answer": str, "category": str (opcional)}

# v2.0.0 - MAJOR: Breaking change - novo campo obrigatório "context" em inputs
dataset_name = "qa-system_v2.0.0"
# Schema incompatível: inputs agora {"question": str, "context": str (obrigatório)}
```

## 🏷️ Naming Convention

### Padrão Recomendado

```
{dataset-name}_v{MAJOR}.{MINOR}.{PATCH}
```

**Exemplos**:

- `qa-system_v1.0.0`
- `rag-evaluation_v2.1.3`
- `golden-examples_v1.0.0`

### Alternative: Date-based Versioning

Para datasets que evoluem rapidamente:

```
{dataset-name}_v{YYYY}.{MM}.{DD}
```

**Exemplos**:

- `production-samples_v2025.01.15`
- `weekly-batch_v2025.W03` (Week 3)

**Quando usar**: Datasets gerados automaticamente de produção

## 🔄 Workflow de Versionamento

### Workflow 1: Manual Version Bumping

```python
from langsmith import Client

client = Client()

# Step 1: Determinar tipo de mudança
# - Breaking change? → MAJOR bump
# - Novos examples/campos opcionais? → MINOR bump
# - Correções? → PATCH bump

current_version = "1.2.0"
new_version = "1.3.0"  # MINOR bump (adding examples)

# Step 2: Criar novo dataset com nova versão
dataset = client.create_dataset(
    dataset_name=f"qa-system_v{new_version}",
    description=f"v{new_version}: Added 50 new examples from production feedback"
)

# Step 3: Copiar examples existentes
old_dataset = client.read_dataset(dataset_name=f"qa-system_v{current_version}")
old_examples = list(client.list_examples(dataset_id=old_dataset.id))

existing_examples = [
    {
        "inputs": ex.inputs,
        "outputs": ex.outputs
    }
    for ex in old_examples
]

# Step 4: Adicionar novos examples
new_examples = [
    # ... novos examples
]

all_examples = existing_examples + new_examples

# Step 5: Upload
client.create_examples(dataset_id=dataset.id, examples=all_examples)

# Step 6: Tag versão importante (opcional)
# client.tag_dataset_version(dataset_id=dataset.id, tag="prod")
```

### Workflow 2: Automated Versioning Class

```python
from langsmith import Client
from typing import List, Dict, Any
from packaging import version  # pip install packaging


class DatasetVersionManager:
    def __init__(self, client: Client, dataset_base_name: str):
        self.client = client
        self.dataset_base_name = dataset_base_name

    def parse_version(self, dataset_name: str) -> version.Version:
        """Extrai versão do nome do dataset"""
        version_str = dataset_name.split("_v")[-1]
        return version.parse(version_str)

    def get_latest_version(self) -> str:
        """Encontra última versão do dataset"""
        datasets = list(self.client.list_datasets())
        matching = [
            ds for ds in datasets
            if ds.name.startswith(self.dataset_base_name)
        ]

        if not matching:
            return "0.0.0"

        versions = [self.parse_version(ds.name) for ds in matching]
        latest = max(versions)
        return str(latest)

    def bump_version(
        self,
        bump_type: str,  # "major", "minor", "patch"
        description: str
    ):
        """Cria nova versão do dataset"""
        current = self.get_latest_version()
        v = version.parse(current)

        if bump_type == "major":
            new_version = f"{v.major + 1}.0.0"
        elif bump_type == "minor":
            new_version = f"{v.major}.{v.minor + 1}.0"
        else:  # patch
            new_version = f"{v.major}.{v.minor}.{v.micro + 1}"

        dataset_name = f"{self.dataset_base_name}_v{new_version}"

        dataset = self.client.create_dataset(
            dataset_name=dataset_name,
            description=f"v{new_version}: {description}"
        )

        return dataset, new_version


# Uso
manager = DatasetVersionManager(client, "qa-system")

# Bump minor version (adding examples)
dataset, version = manager.bump_version(
    bump_type="minor",
    description="Added 50 new examples from production"
)

print(f"Created: {dataset.name} (v{version})")
```

## 📝 Changelog Best Practices

### Maintain CHANGELOG.md

```markdown
# Changelog - qa-system Dataset

All notable changes to this dataset will be documented in this file.

## [2.0.0] - 2025-01-15

### Breaking Changes
- Added mandatory "context" field to all inputs
- Restructured outputs to include "reasoning" field

### Added
- 100 new examples with context
- Reasoning field for explainability

### Changed
- Migrated all existing examples to new schema

## [1.2.0] - 2025-01-10

### Added
- 50 new examples from production feedback
- Optional "category" field in outputs

## [1.1.0] - 2025-01-05

### Added
- 30 new examples covering edge cases

### Fixed
- Corrected 3 examples with wrong expected answers

## [1.0.0] - 2025-01-01

### Initial Release
- 100 curated Q&A examples
- Schema: inputs {"question"}, outputs {"answer"}
```

### Automated Changelog Generation

```python
import json
from datetime import datetime

def log_version_change(
    version: str,
    change_type: str,  # "major", "minor", "patch"
    description: str,
    changes: List[str]
):
    """Adiciona entrada ao changelog"""

    changelog_entry = {
        "version": version,
        "date": datetime.now().isoformat(),
        "type": change_type,
        "description": description,
        "changes": changes
    }

    # Append to changelog.json
    try:
        with open("dataset_changelog.json", "r") as f:
            changelog = json.load(f)
    except FileNotFoundError:
        changelog = []

    changelog.insert(0, changelog_entry)  # Mais recente primeiro

    with open("dataset_changelog.json", "w") as f:
        json.dump(changelog, f, indent=2)


# Uso
log_version_change(
    version="1.2.0",
    change_type="minor",
    description="Added production examples",
    changes=[
        "Added 50 new examples from production feedback",
        "Added optional 'category' field to outputs"
    ]
)
```

## 🏷️ Tagging de Versões

### Tags Recomendadas

```python
# Tag para produção
client.tag_dataset_version(dataset_id=dataset.id, tag="prod")

# Tag para baseline
client.tag_dataset_version(dataset_id=dataset.id, tag="baseline")

# Tag para releases específicas
client.tag_dataset_version(dataset_id=dataset.id, tag="release-2025-01")

# Tag para staging/test
client.tag_dataset_version(dataset_id=dataset.id, tag="staging")
```

### Workflow com Tags

```python
# 1. Criar nova versão
dataset_v1_3 = client.create_dataset(
    dataset_name="qa-system_v1.3.0",
    description="v1.3.0: Performance improvements"
)

# 2. Upload examples
client.create_examples(dataset_id=dataset_v1_3.id, examples=examples)

# 3. Testar em staging
# ... run evaluations ...

# 4. Se aprovado, tag como prod
client.tag_dataset_version(dataset_id=dataset_v1_3.id, tag="prod")

# 5. Remover tag prod da versão anterior
old_dataset = client.read_dataset(dataset_name="qa-system_v1.2.0")
# client.untag_dataset_version(dataset_id=old_dataset.id, tag="prod")
```

## 📊 Schema Versioning

### Documentar Schema Changes

```python
# schema_versions.json
{
  "v1.0.0": {
    "inputs": {
      "question": {"type": "string", "required": true}
    },
    "outputs": {
      "answer": {"type": "string", "required": true}
    }
  },
  "v1.2.0": {
    "inputs": {
      "question": {"type": "string", "required": true}
    },
    "outputs": {
      "answer": {"type": "string", "required": true},
      "category": {"type": "string", "required": false}
    }
  },
  "v2.0.0": {
    "inputs": {
      "question": {"type": "string", "required": true},
      "context": {"type": "string", "required": true}
    },
    "outputs": {
      "answer": {"type": "string", "required": true},
      "reasoning": {"type": "string", "required": true}
    }
  }
}
```

## ✅ Checklist de Versionamento

**Antes de criar nova versão**:

- [ ] Determinar tipo de mudança (MAJOR/MINOR/PATCH)
- [ ] Incrementar versão corretamente
- [ ] Documentar mudanças no CHANGELOG
- [ ] Atualizar schema documentation se aplicável

**Ao criar nova versão**:

- [ ] Nome segue padrão: `{name}_v{MAJOR}.{MINOR}.{PATCH}`
- [ ] Description menciona o que mudou
- [ ] Examples validados antes de upload

**Após criar nova versão**:

- [ ] Testar evaluations com nova versão
- [ ] Tag versão importante se aprovado (`prod`, `baseline`)
- [ ] Backup dataset (export para arquivo)
- [ ] Comunicar mudanças ao time

## 🎯 Best Practices

1. **Sempre versione explicitamente**: Nome do dataset DEVE incluir versão
1. **Documente mudanças**: Mantenha CHANGELOG atualizado
1. **Use Semantic Versioning**: Siga convenção MAJOR.MINOR.PATCH
1. **Tag milestones**: Marque versões importantes (`prod`, `baseline`)
1. **Backup antes de MAJOR bumps**: Export versão anterior
1. **Teste antes de tag prod**: Validar em staging primeiro
1. **Comunique breaking changes**: Avise time sobre MAJOR bumps
