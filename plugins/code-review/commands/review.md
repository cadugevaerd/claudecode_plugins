---
description: Executa code review completo identificando bugs, vulnerabilidades e melhorias
---

# Code Review

Executa uma análise completa e automática do código modificado, identificando:

- 🔒 Vulnerabilidades de segurança
- 🐛 Bugs potenciais
- ✨ Melhorias de qualidade
- 🧪 Cobertura de testes
- 📚 Documentação
- 🔧 Débito técnico

## Como funciona

O comando executa automaticamente os seguintes passos:

1. **Identificação do Contexto**: Analisa `git status` e `git diff` para identificar mudanças
1. **Análise de Segurança**: Procura credenciais hardcoded, funções perigosas, inputs sem sanitização
1. **Análise de Qualidade**: Verifica estrutura, boas práticas, performance
1. **Análise de Testes**: Valida cobertura e qualidade dos testes
1. **Documentação**: Verifica se código novo está documentado
1. **Débito Técnico**: Identifica código duplicado, complexidade alta, acoplamento
1. **Relatório Final**: Gera relatório estruturado com problemas priorizados

## Como usar

````bash
/review

```text

O comando detecta automaticamente a linguagem e framework do seu projeto e adapta a análise.

## Exemplos de Uso

### Revisar mudanças antes de commit

```bash

# Após fazer modificações
git add .
/review

# O plugin analisa as mudanças staged e fornece feedback

```text

### Revisar pull request

```bash

# Checkout na branch do PR
git checkout feature-branch
/review

# Analisa todas as mudanças da branch

```text

## Saída

O comando gera um relatório estruturado em markdown com:

- ✅ **Pontos Positivos**: Aspectos bem implementados
- 🔴 **Críticos**: Problemas que devem ser corrigidos antes do commit
- 🟡 **Importantes**: Problemas que devem ser corrigidos em breve
- 🟢 **Sugestões**: Melhorias opcionais
- 📊 **Métricas**: Cobertura, arquivos modificados, linhas alteradas
- 🎯 **Ações Recomendadas**: Lista priorizada de próximos passos

Cada problema inclui:
- Localização exata (arquivo:linha)
- Explicação clara do problema
- Sugestão de correção com exemplo de código
- Nível de prioridade

## Linguagens Suportadas

O plugin é genérico e funciona com qualquer linguagem de programação. Ele detecta automaticamente:

- Python, JavaScript, TypeScript, Java, Go, Rust, C++, C#, Ruby, PHP, etc.
- Frameworks de teste (pytest, jest, junit, go test, cargo test, etc.)
- Gerenciadores de pacotes (npm, pip, cargo, maven, etc.)

## Personalização

O agente `code-reviewer` adapta a análise baseado no contexto do projeto:

- Identifica a linguagem pelos arquivos modificados
- Detecta frameworks e ferramentas em uso
- Aplica boas práticas específicas da stack
- Pula análises não aplicáveis (ex: testes se não houver framework)
````
