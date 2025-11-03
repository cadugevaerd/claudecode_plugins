---
description: Central de ajuda do plugin incremental-dev - responde perguntas sobre YAGNI, PRD, desenvolvimento incremental e uso do plugin
---

# PRD Help

Central de ajuda interativa para desenvolvimento incremental, YAGNI, PRD e uso do plugin incremental-dev.

## Como usar

### Modo pergunta direta

````bash
/prd-help "Como criar um PRD inicial?"
/prd-help "O que é YAGNI?"
/prd-help "Qual diferença entre /prd-update e /prd-fix?"
/prd-help "Quando refatorar?"

```text

### Modo interativo

```bash
/prd-help

```text

Mostra menu com categorias e permite navegação.

## Menu de categorias

1. **🚀 Começar a Usar** - Primeiros passos (novos e legacy)
2. **📋 Gestão de PRD** - Criação, atualização, estrutura
3. **⚙️ Comandos Disponíveis** - Referência rápida de todos
4. **💡 Conceitos** - YAGNI, Incremental, MVP, Evolutionary Architecture
5. **🔧 Troubleshooting** - Problemas comuns e soluções
6. **📖 Exemplos Práticos** - Casos de uso reais
7. **Fazer pergunta** - Modo direto
8. **Sair** - Fechar ajuda

## Fluxo recomendado para NOVOS projetos

```text

1. /setup-project-incremental
   └─ Configura CLAUDE.md com YAGNI

2. /start-incremental
   └─ Cria PRD.md com requisitos

3. /add-increment "funcionalidade"
   └─ Adiciona features incrementalmente

4. /review-yagni
   └─ Detecta over-engineering

5. /refactor-now
   └─ Refatora quando padrões emergem

```text

## Fluxo recomendado para PROJETOS LEGACY

```text

1. /adopt-incremental
   └─ Análise completa + PRD + roadmap

   OU (rápido):

2. /prd-retrofit
   └─ Só cria PRD retroativo

```text

## Referência de Comandos

| Comando | Quando Usar |
|---------|------------|
| `/setup-project-incremental` | Configurar novo projeto |
| `/start-incremental` | Criar PRD novo (projetos novos) |
| `/adopt-incremental` | Adotar YAGNI em projeto existente |
| `/prd-retrofit` | Criar PRD retroativo (legacy) |
| `/add-increment` | Adicionar próxima feature |
| `/prd-view` | Visualizar PRD atual |
| `/prd-update` | Atualizar PRD completo |
| `/prd-fix` | Ajuste cirúrgico no PRD |
| `/review-yagni` | Detectar over-engineering |
| `/refactor-now` | Quando refatorar |

## Conceitos-chave

### YAGNI (You Aren't Gonna Need It)

**Definição**: Não adicione funcionalidade até que seja REALMENTE necessária.

❌ **Ruim**:

```python
class User:
  name: string
  email: string
  avatar?: string      # "pode precisar no futuro"
  preferences?: JSON
  settings?: object

```text

✅ **Bom**:

```python
class User:
  name: string
  email: string
  # Só isso! Adiciona quando realmente precisar

```text

### Regra dos 3

- **1 caso**: Código inline (direto)
- **2 casos**: Deixar duplicado (duplication OK!)
- **3 casos**: AGORA abstrair padrão

NÃO refatore durante incremento!

### MVP (Minimum Viable Product)

Menor versão funcional que:
- ✅ Funciona e entrega valor
- ✅ Permite aprendizado
- ✅ Base para evoluir

**NÃO é**: Incompleto, protótipo, ou bugado

### Evolutionary Architecture

Arquitetura que evolui com o código, não definida 100% no início:
1. Começar simples
2. Identificar padrões ao codificar
3. Refatorar quando padrão emerge 3x
4. Evoluir baseado em necessidade real

## Perguntas Comuns

**P: Quando criar PRD?**
A: No início do projeto. Use `/start-incremental`

**P: Projeto já existe?**
A: Use `/prd-retrofit` ou `/adopt-incremental`

**P: Como saber se estou fazendo over-engineering?**
A: Use `/review-yagni` para detectar automaticamente

**P: Como decidir quando refatorar?**
A: Use `/refactor-now` - refatore quando padrão repetir 3x

**P: PRD é obrigatório?**
A: Não, mas ajuda MUITO a evitar over-engineering

## Próximas ações

- Começar novo projeto? → `/start-incremental`
- Projeto já existe? → `/adopt-incremental` ou `/prd-retrofit`
- Dúvida específica? → `/prd-help "sua pergunta"`
- Ver PRD atual? → `/prd-view`
- Adicionar feature? → `/add-increment`

**Bem-vindo ao desenvolvimento incremental!** 🚀
````
