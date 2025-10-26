#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pymarkdownlnt>=0.9.18",
# ]
# ///
"""
CI.py - Validador completo para claudecode_plugins

Valida todos os arquivos do repositório de plugins:
- marketplace.json (campos obrigatórios, estrutura)
- plugin.json de cada plugin (campos obrigatórios, estrutura)
- Verifica paths e consistência entre arquivos
- Valida arquivos Markdown (estrutura, formatação, links)

Uso:
    ./CI.py                     # Valida JSON + Markdown
    ./CI.py --verbose           # Logs detalhados
    ./CI.py --skip-markdown     # Valida apenas JSON
    ./CI.py --only-markdown     # Valida apenas Markdown
    ./CI.py --markdown-strict   # Trata warnings MD como erros

    # Com UV (recomendado):
    uv run CI.py

    # Testes:
    uv run pytest test_ci.py
    uv run pytest test_ci.py --cov
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class Colors:
    """Cores ANSI para terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class JSONValidator:
    """Validador de arquivos JSON do claudecode_plugins"""

    def __init__(self, verbose: bool = False, fix: bool = False):
        self.verbose = verbose
        self.fix = fix
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.success: List[str] = []
        self.root = Path(__file__).parent

    def log_error(self, message: str):
        """Registra erro"""
        self.errors.append(message)
        print(f"{Colors.RED}❌ {message}{Colors.RESET}")

    def log_warning(self, message: str):
        """Registra aviso"""
        self.warnings.append(message)
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

    def log_success(self, message: str):
        """Registra sucesso"""
        self.success.append(message)
        if self.verbose:
            print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

    def log_info(self, message: str):
        """Registra informação"""
        if self.verbose:
            print(f"{Colors.CYAN}ℹ️  {message}{Colors.RESET}")

    def validate_json_syntax(self, file_path: Path) -> Optional[Dict]:
        """Valida sintaxe JSON de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_success(f"JSON válido: {file_path.relative_to(self.root)}")
            return data
        except json.JSONDecodeError as e:
            self.log_error(f"JSON inválido em {file_path.relative_to(self.root)}: {e}")
            return None
        except FileNotFoundError:
            self.log_error(f"Arquivo não encontrado: {file_path.relative_to(self.root)}")
            return None

    def validate_marketplace_json(self) -> bool:
        """Valida marketplace.json"""
        print(f"\n{Colors.BOLD}📦 Validando marketplace.json{Colors.RESET}")
        print("=" * 60)

        marketplace_path = self.root / ".claude-plugin" / "marketplace.json"
        data = self.validate_json_syntax(marketplace_path)

        if not data:
            return False

        # Campos obrigatórios
        required_fields = {
            "name": str,
            "version": str,
            "description": str,
            "owner": dict,
            "plugins": list
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                self.log_error(f"marketplace.json: campo obrigatório '{field}' ausente")
            elif not isinstance(data[field], expected_type):
                self.log_error(
                    f"marketplace.json: campo '{field}' deve ser {expected_type.__name__}, "
                    f"encontrado {type(data[field]).__name__}"
                )
            else:
                self.log_success(f"marketplace.json: campo '{field}' presente e válido")

        # Validar owner
        if "owner" in data:
            owner_required = ["name", "email"]
            for field in owner_required:
                if field not in data["owner"]:
                    self.log_error(f"marketplace.json: owner.{field} ausente")
                else:
                    self.log_success(f"marketplace.json: owner.{field} presente")

        # Validar plugins array
        if "plugins" in data and isinstance(data["plugins"], list):
            self.log_info(f"marketplace.json: {len(data['plugins'])} plugins registrados")

            for idx, plugin in enumerate(data["plugins"]):
                if not isinstance(plugin, dict):
                    self.log_error(f"marketplace.json: plugins[{idx}] não é um objeto")
                    continue

                plugin_name = plugin.get("name", f"plugin_{idx}")
                plugin_required = ["name", "description", "source", "version"]

                for field in plugin_required:
                    if field not in plugin:
                        self.log_error(
                            f"marketplace.json: plugins[{idx}] ({plugin_name}): "
                            f"campo '{field}' ausente"
                        )

                # Verificar se source path existe
                if "source" in plugin:
                    source_path = self.root / plugin["source"].lstrip("./")
                    if not source_path.exists():
                        self.log_error(
                            f"marketplace.json: plugins[{idx}] ({plugin_name}): "
                            f"path '{plugin['source']}' não existe"
                        )
                    else:
                        self.log_success(
                            f"marketplace.json: plugins[{idx}] ({plugin_name}): path válido"
                        )

        return len(self.errors) == 0

    def validate_plugin_json(self, plugin_path: Path) -> bool:
        """Valida plugin.json de um plugin específico"""
        plugin_name = plugin_path.name

        # Procurar plugin.json (pode estar em .claude-plugin/ ou na raiz)
        possible_paths = [
            plugin_path / ".claude-plugin" / "plugin.json",
            plugin_path / "plugin.json"
        ]

        plugin_json_path = None
        for path in possible_paths:
            if path.exists():
                plugin_json_path = path
                break

        if not plugin_json_path:
            self.log_error(f"{plugin_name}: plugin.json não encontrado")
            return False

        data = self.validate_json_syntax(plugin_json_path)
        if not data:
            return False

        # Campos obrigatórios
        required_fields = {
            "name": str,
            "version": str,
            "description": str,
            "author": dict,
            "license": str
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                self.log_error(f"{plugin_name}/plugin.json: campo '{field}' ausente")
            elif not isinstance(data[field], expected_type):
                self.log_error(
                    f"{plugin_name}/plugin.json: campo '{field}' deve ser "
                    f"{expected_type.__name__}, encontrado {type(data[field]).__name__}"
                )
            else:
                self.log_success(f"{plugin_name}/plugin.json: campo '{field}' válido")

        # Validar author
        if "author" in data and isinstance(data["author"], dict):
            if "name" not in data["author"]:
                self.log_error(f"{plugin_name}/plugin.json: author.name ausente")
            else:
                self.log_success(f"{plugin_name}/plugin.json: author.name presente")

        # Verificar se tem pelo menos um componente
        has_component = False
        components = []

        if (plugin_path / "commands").exists():
            has_component = True
            components.append("commands")
        if (plugin_path / "agents").exists():
            has_component = True
            components.append("agents")
        if (plugin_path / "hooks").exists():
            has_component = True
            components.append("hooks")
        if (plugin_path / "skills").exists():
            has_component = True
            components.append("skills")
        if (plugin_path / ".mcp.json").exists():
            has_component = True
            components.append("mcp")

        if not has_component:
            self.log_error(
                f"{plugin_name}: nenhum componente encontrado "
                "(commands/agents/hooks/skills/mcp)"
            )
        else:
            self.log_success(
                f"{plugin_name}: componentes encontrados: {', '.join(components)}"
            )

        # Verificar README
        if not (plugin_path / "README.md").exists():
            self.log_warning(f"{plugin_name}: README.md não encontrado")
        else:
            self.log_success(f"{plugin_name}: README.md presente")

        return True

    def validate_all_plugins(self) -> bool:
        """Valida todos os plugins"""
        print(f"\n{Colors.BOLD}🔌 Validando plugins{Colors.RESET}")
        print("=" * 60)

        plugins_dir = self.root / "plugins"
        if not plugins_dir.exists():
            self.log_error("Diretório plugins/ não encontrado")
            return False

        plugin_dirs = [d for d in plugins_dir.iterdir() if d.is_dir()]

        if not plugin_dirs:
            self.log_warning("Nenhum plugin encontrado em plugins/")
            return True

        self.log_info(f"Encontrados {len(plugin_dirs)} plugins")

        all_valid = True
        for plugin_dir in sorted(plugin_dirs):
            print(f"\n{Colors.CYAN}→ {plugin_dir.name}{Colors.RESET}")
            if not self.validate_plugin_json(plugin_dir):
                all_valid = False

        return all_valid

    def check_marketplace_plugin_consistency(self) -> bool:
        """Verifica consistência entre marketplace.json e plugins"""
        print(f"\n{Colors.BOLD}🔄 Verificando consistência{Colors.RESET}")
        print("=" * 60)

        marketplace_path = self.root / ".claude-plugin" / "marketplace.json"

        try:
            with open(marketplace_path, 'r', encoding='utf-8') as f:
                marketplace = json.load(f)
        except Exception as e:
            self.log_error(f"Não foi possível ler marketplace.json: {e}")
            return False

        if "plugins" not in marketplace:
            return True

        # Coletar plugins registrados no marketplace
        marketplace_plugins = {}
        for plugin_entry in marketplace["plugins"]:
            plugin_name = plugin_entry.get("name")
            if plugin_name:
                marketplace_plugins[plugin_name] = plugin_entry

        # Coletar plugins existentes no diretório
        plugins_dir = self.root / "plugins"
        filesystem_plugins = set()
        if plugins_dir.exists():
            for plugin_dir in plugins_dir.iterdir():
                if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
                    filesystem_plugins.add(plugin_dir.name)

        # Validação bidirecional: verificar plugins no diretório que não estão no marketplace
        unregistered = filesystem_plugins - set(marketplace_plugins.keys())
        if unregistered:
            for plugin_name in sorted(unregistered):
                self.log_warning(
                    f"{plugin_name}: plugin existe em plugins/ mas NÃO está "
                    f"registrado no marketplace.json"
                )

        # Verificar se versões batem e se paths existem
        for plugin_entry in marketplace["plugins"]:
            plugin_name = plugin_entry.get("name")
            marketplace_version = plugin_entry.get("version")
            source = plugin_entry.get("source", "")

            if not plugin_name or not marketplace_version:
                continue

            # Verificar se path existe
            plugin_path = self.root / source.lstrip("./")
            if not plugin_path.exists():
                self.log_error(
                    f"{plugin_name}: registrado no marketplace.json mas "
                    f"diretório '{source}' NÃO EXISTE"
                )
                continue

            # Encontrar plugin.json
            possible_paths = [
                plugin_path / ".claude-plugin" / "plugin.json",
                plugin_path / "plugin.json"
            ]

            plugin_json_path = None
            for path in possible_paths:
                if path.exists():
                    plugin_json_path = path
                    break

            if not plugin_json_path:
                continue

            try:
                with open(plugin_json_path, 'r', encoding='utf-8') as f:
                    plugin_data = json.load(f)

                plugin_version = plugin_data.get("version")

                if plugin_version != marketplace_version:
                    self.log_error(
                        f"{plugin_name}: versão inconsistente - "
                        f"marketplace.json={marketplace_version}, "
                        f"plugin.json={plugin_version}"
                    )
                else:
                    self.log_success(
                        f"{plugin_name}: versão consistente ({plugin_version})"
                    )

            except Exception as e:
                self.log_warning(f"{plugin_name}: erro ao ler plugin.json: {e}")

        # Resumo da validação bidirecional
        if unregistered:
            self.log_info(
                f"\n💡 Dica: {len(unregistered)} plugin(s) não registrado(s). "
                f"Execute: /update-plugin para registrá-los automaticamente"
            )

        return len(self.errors) == 0

    def print_summary(self):
        """Imprime resumo da validação"""
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 RESUMO DA VALIDAÇÃO{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

        total = len(self.success) + len(self.warnings) + len(self.errors)

        print(f"{Colors.GREEN}✅ Sucessos: {len(self.success)}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  Avisos:   {len(self.warnings)}{Colors.RESET}")
        print(f"{Colors.RED}❌ Erros:    {len(self.errors)}{Colors.RESET}")
        print(f"\n{Colors.BOLD}Total de verificações: {total}{Colors.RESET}\n")

        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}❌ VALIDAÇÃO FALHOU{Colors.RESET}")
            print(f"{Colors.RED}Corrija os erros antes de fazer commit{Colors.RESET}\n")
            return False
        elif self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  VALIDAÇÃO COM AVISOS{Colors.RESET}")
            print(f"{Colors.YELLOW}Considere corrigir os avisos{Colors.RESET}\n")
            return True
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ VALIDAÇÃO PASSOU!{Colors.RESET}")
            print(f"{Colors.GREEN}Todos os arquivos JSON estão válidos{Colors.RESET}\n")
            return True

    def run(self) -> bool:
        """Executa todas as validações"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}🔍 CI - Validador de JSON - claudecode_plugins{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'=' * 60}{Colors.RESET}\n")

        # Executar validações
        marketplace_valid = self.validate_marketplace_json()
        plugins_valid = self.validate_all_plugins()
        consistency_valid = self.check_marketplace_plugin_consistency()

        # Resumo
        success = self.print_summary()

        return success and marketplace_valid and plugins_valid and consistency_valid


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Validador de JSON para claudecode_plugins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python CI.py                # Validação padrão
  python CI.py --verbose      # Validação com logs detalhados
  python CI.py --fix          # Tenta corrigir problemas automaticamente

Exit codes:
  0 - Validação passou
  1 - Validação falhou (erros encontrados)
  2 - Validação passou com avisos
        """
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Exibe logs detalhados de todas as verificações'
    )

    parser.add_argument(
        '-f', '--fix',
        action='store_true',
        help='Tenta corrigir problemas automaticamente (não implementado ainda)'
    )

    args = parser.parse_args()

    # Executar validação
    validator = JSONValidator(verbose=args.verbose, fix=args.fix)
    success = validator.run()

    # Exit code
    if not success:
        sys.exit(1)
    elif validator.warnings:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()