# LangSmith Dataset Manager - Implementação Completa

Classe completa para gerenciamento centralizado de datasets no LangSmith com versionamento, validação e automação.

## 🎯 Propósito

Encapsular toda lógica de criação, atualização, remoção e versionamento de datasets em uma classe reutilizável que segue best practices.

## 📋 Implementação Completa

```python
from langsmith import Client
from typing import List, Dict, Optional, Any
import json
from pathlib import Path
from datetime import datetime


class LangSmithDatasetManager:
    """
    Gerenciador centralizado de datasets para LangSmith.

    Funcionalidades:
    - Criar/recuperar datasets com versionamento
    - Upload de examples com validação
    - Versionamento semântico
    - Import de arquivos locais (JSON, CSV)
    - Export de datasets
    - Backtesting de produção
    """

    def __init__(self, client: Optional[Client] = None):
        """
        Inicializa o manager.

        Args:
            client: Cliente LangSmith (se None, cria novo)
        """
        self.client = client or Client()

    def create_or_get_dataset(
        self,
        name: str,
        description: str,
        version: Optional[str] = None
    ):
        """
        Cria dataset ou recupera se já existe.

        Args:
            name: Nome base do dataset
            version: Versão (ex: "1.0.0") - adicionado ao nome se fornecido
            description: Descrição do dataset

        Returns:
            Dataset object
        """
        dataset_name = f"{name}_v{version}" if version else name

        try:
            dataset = self.client.create_dataset(
                dataset_name=dataset_name,
                description=description
            )
            print(f"✅ Dataset criado: {dataset_name}")
        except Exception as e:
            dataset = self.client.read_dataset(dataset_name=dataset_name)
            print(f"📂 Dataset recuperado: {dataset_name} ({dataset.example_count} exemplos)")

        return dataset

    def validate_examples(self, examples: List[Dict[str, Any]]) -> bool:
        """
        Valida estrutura de examples antes de upload.

        Args:
            examples: Lista de examples

        Returns:
            True se válido, raise ValueError se inválido
        """
        if not examples:
            raise ValueError("Lista de examples vazia")

        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                raise ValueError(f"Example {idx} não é dict")

            if "inputs" not in example:
                raise ValueError(f"Example {idx} não tem 'inputs'")

            if not isinstance(example["inputs"], dict):
                raise ValueError(f"Example {idx} 'inputs' não é dict")

            # Outputs é opcional mas recomendado
            if "outputs" in example and not isinstance(example["outputs"], dict):
                raise ValueError(f"Example {idx} 'outputs' não é dict")

        return True

    def upload_examples(
        self,
        dataset_id: str,
        examples: List[Dict[str, Any]],
        validate: bool = True
    ):
        """
        Upload de examples com validação opcional.

        Args:
            dataset_id: ID do dataset
            examples: Lista de examples
            validate: Se deve validar estrutura antes de upload
        """
        if validate:
            self.validate_examples(examples)

        self.client.create_examples(
            dataset_id=dataset_id,
            examples=examples
        )

        print(f"✅ {len(examples)} examples enviados")

    def upload_from_json(
        self,
        dataset_id: str,
        json_path: str,
        input_keys: List[str],
        output_keys: Optional[List[str]] = None
    ):
        """
        Lê JSON local e faz upload como examples.

        Args:
            dataset_id: ID do dataset
            json_path: Caminho para arquivo JSON
            input_keys: Chaves do JSON a usar como inputs
            output_keys: Chaves do JSON a usar como outputs
        """
        with open(json_path, "r") as f:
            data = json.load(f)

        examples = []
        for item in data:
            example = {
                "inputs": {k: item[k] for k in input_keys if k in item}
            }

            if output_keys:
                example["outputs"] = {k: item[k] for k in output_keys if k in item}

            examples.append(example)

        self.upload_examples(dataset_id, examples)

    def upload_from_csv(
        self,
        dataset_name: str,
        csv_path: str,
        input_keys: List[str],
        output_keys: Optional[List[str]] = None,
        description: str = ""
    ):
        """
        Upload de CSV usando método nativo do LangSmith.

        Args:
            dataset_name: Nome do dataset a criar
            csv_path: Caminho para CSV
            input_keys: Colunas a usar como inputs
            output_keys: Colunas a usar como outputs
            description: Descrição do dataset
        """
        import pandas as pd

        df = pd.read_csv(csv_path)

        self.client.upload_dataframe(
            df=df,
            name=dataset_name,
            description=description,
            input_keys=input_keys,
            output_keys=output_keys or []
        )

        print(f"✅ CSV uploaded: {len(df)} rows → {dataset_name}")

    def create_from_production_runs(
        self,
        dataset_name: str,
        project_name: str,
        filter_query: str,
        description: str = "Dataset from production runs",
        max_examples: int = 100
    ):
        """
        Cria dataset a partir de runs de produção.

        Args:
            dataset_name: Nome do dataset a criar
            project_name: Projeto LangSmith de onde filtrar runs
            filter_query: Query de filtro (ex: "eq(error, true)")
            description: Descrição do dataset
            max_examples: Número máximo de examples
        """
        # Criar dataset
        dataset = self.create_or_get_dataset(dataset_name, description)

        # Filtrar runs
        runs = list(self.client.list_runs(
            project_name=project_name,
            filter=filter_query
        ))[:max_examples]

        # Converter para examples
        examples = []
        for run in runs:
            if run.inputs:
                example = {"inputs": run.inputs}

                # Incluir outputs se disponível
                if run.outputs:
                    example["outputs"] = run.outputs

                examples.append(example)

        # Upload
        if examples:
            self.upload_examples(dataset.id, examples)

        return dataset

    def tag_version(
        self,
        dataset_id: str,
        tag: str,
        version: Optional[str] = None
    ):
        """
        Tagear versão do dataset.

        Args:
            dataset_id: ID do dataset
            tag: Tag a aplicar (ex: "prod", "staging", "baseline")
            version: Versão específica (se None, usa latest)
        """
        # Note: API exata pode variar - verificar docs
        # Este é um exemplo conceitual
        try:
            self.client.tag_dataset_version(
                dataset_id=dataset_id,
                tag=tag,
                version=version
            )
            print(f"✅ Tag '{tag}' aplicada ao dataset")
        except AttributeError:
            print("⚠️ Método tag_dataset_version não disponível - usar UI")

    def export_dataset(
        self,
        dataset_name: str,
        output_path: str,
        format: str = "json"
    ):
        """
        Exporta dataset para arquivo local.

        Args:
            dataset_name: Nome do dataset
            output_path: Caminho de saída
            format: Formato (json ou csv)
        """
        dataset = self.client.read_dataset(dataset_name=dataset_name)
        examples = list(self.client.list_examples(dataset_id=dataset.id))

        data = [
            {
                "id": ex.id,
                "inputs": ex.inputs,
                "outputs": ex.outputs if ex.outputs else {}
            }
            for ex in examples
        ]

        if format == "json":
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
        elif format == "csv":
            import pandas as pd
            df = pd.json_normalize(data)
            df.to_csv(output_path, index=False)

        print(f"✅ Dataset exportado: {output_path} ({len(data)} exemplos)")

    def delete_dataset(self, dataset_name: str):
        """
        Deleta dataset (cuidado!).

        Args:
            dataset_name: Nome do dataset a deletar
        """
        dataset = self.client.read_dataset(dataset_name=dataset_name)
        self.client.delete_dataset(dataset_id=dataset.id)
        print(f"🗑️ Dataset deletado: {dataset_name}")

    def update_example(
        self,
        example_id: str,
        inputs: Optional[Dict] = None,
        outputs: Optional[Dict] = None
    ):
        """
        Atualiza example existente.

        Args:
            example_id: ID do example
            inputs: Novos inputs (se None, mantém)
            outputs: Novos outputs (se None, mantém)
        """
        self.client.update_example(
            example_id=example_id,
            inputs=inputs,
            outputs=outputs
        )
        print(f"✅ Example {example_id} atualizado")

    def list_datasets(self) -> List[Any]:
        """Lista todos os datasets disponíveis."""
        datasets = list(self.client.list_datasets())

        print("\n📊 Datasets Disponíveis:")
        for ds in datasets:
            print(f"  - {ds.name} ({ds.example_count} exemplos)")

        return datasets
```

## 📋 Exemplo de Uso Completo

```python
from dotenv import load_dotenv

# Setup
load_dotenv()
manager = LangSmithDatasetManager()

# 1. Criar dataset versionado
dataset = manager.create_or_get_dataset(
    name="qa-system",
    version="1.0.0",
    description="Q&A evaluation dataset"
)

# 2. Upload de JSON local
manager.upload_from_json(
    dataset_id=dataset.id,
    json_path="./data/golden_examples.json",
    input_keys=["question", "context"],
    output_keys=["answer"]
)

# 3. Upload de CSV
manager.upload_from_csv(
    dataset_name="faq-dataset_v1.0.0",
    csv_path="./data/faq.csv",
    input_keys=["question"],
    output_keys=["answer"],
    description="FAQ dataset from CSV"
)

# 4. Criar dataset de produção (backtesting)
prod_dataset = manager.create_from_production_runs(
    dataset_name="production-failures_v1.0.0",
    project_name="production-app",
    filter_query="eq(error, true)",
    description="Failed runs from production",
    max_examples=50
)

# 5. Tag version importante
manager.tag_version(dataset.id, "prod")

# 6. Export para backup
manager.export_dataset(
    dataset_name="qa-system_v1.0.0",
    output_path="./backups/qa-system-backup.json",
    format="json"
)

# 7. Listar todos datasets
manager.list_datasets()
```

## 🎯 Best Practices

1. **Sempre use versionamento**: Inclua versão no nome do dataset
1. **Validate antes de upload**: Use `validate=True` (padrão)
1. **Backup datasets importantes**: Use `export_dataset()` regularmente
1. **Tag milestones**: Marque versões importantes (`prod`, `baseline`)
1. **Documente schema**: Adicione comments sobre estrutura esperada
1. **Handle exceptions**: Wrap calls em try/except apropriados
1. **Use batch operations**: `upload_examples()` é mais eficiente que loops

## ⚠️ Cuidados

- `delete_dataset()` é **irreversível** - cuidado!
- Upload de grandes volumes: considere pagination e chunks
- API keys: NUNCA commitar `.env` com credentials
- Versionamento: Sempre incremente versão ao modificar dataset existente
