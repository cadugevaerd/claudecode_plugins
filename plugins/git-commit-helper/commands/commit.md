---
description: Realiza commit com validações completas via agente especializado
allowed-tools: Task, Bash, Read, Grep, Glob
model: ''
argument-hint: (sem argumentos necessários)
---

# Comando: /commit

Este comando delega ao agente especializado `commit-assistant` para executar o processo completo de commit seguindo as melhores práticas.

## 🎯 O que este comando faz

Invoca o agente `commit-assistant` que automaticamente:

1. ✅ **Valida segurança** - Detecta e bloqueia arquivos sensíveis
1. ✅ **Executa CI/CD** - Roda testes, linting, build e validações
1. ✅ **Analisa mudanças** - Examina git diff e categoriza alterações
1. ✅ **Verifica documentação** - Identifica docs que precisam atualização
1. ✅ **Gera mensagem** - Cria commit message seguindo Conventional Commits
1. ✅ **Executa commit** - Realiza o commit com mensagem formatada
1. ✅ **Push opcional** - Pergunta se deseja fazer push (nunca força)

## 🚀 Execução

**IMPORTANTE:** O agente executará todos os passos automaticamente. Aguarde o processo completo.

Use o **agente commit-assistant** do plugin git-commit-helper para executar o processo completo de commit no repositório atual.

O agente deve seguir o protocolo de commit completo incluindo:

- Validações de segurança (arquivos sensíveis)
- Execução de CI/CD e testes do projeto
- Análise detalhada de mudanças via git
- Verificação de documentação desatualizada
- Geração de mensagem de commit (Conventional Commits)
- Execução do commit
- Push opcional com validações

Execute o processo completo sem interrupções, a menos que encontre:

- Arquivos sensíveis (PARE e alerte)
- Testes falhando (PARE e mostre erros)
- Conflitos no push (PARE e instrua resolução)

Ao final, mostre resumo completo com estatísticas.

## 📊 Formato de Saída

Ao final da execução, você receberá:

```text
✅ Commit realizado com sucesso!

📊 Resumo:
- Arquivos modificados: X
- Linhas adicionadas: +X
- Linhas removidas: -X
- Tipo de commit: feat/fix/docs/chore/refactor/style/test
- Mensagem: "tipo(escopo): descrição"

🚀 Push disponível: [Sim/Não]
```

Em caso de erros:

```text
❌ Erro: Arquivos sensíveis detectados
📁 Arquivos: .env, credentials.json
💡 Ação: Remova do staging antes de continuar
```

```text
❌ Erro: Testes falhando
📊 Falhas: X testes
💡 Ação: Corrija os erros antes de commitar
```

```text
❌ Erro: Conflito no push
🔀 Status: Seu branch está atrás do remote
💡 Ação: Execute git pull --rebase antes de fazer push
```

## ✅ Critérios de Sucesso

- [ ] Nenhum arquivo sensível detectado (.env, \*.key, credentials)
- [ ] CI/CD executado sem erros (testes, linting, build)
- [ ] Git diff analisado e mudanças categorizadas
- [ ] Documentação verificada e atualizada (se necessário)
- [ ] Mensagem de commit gerada seguindo Conventional Commits
- [ ] Commit executado com sucesso
- [ ] Push realizado (se solicitado) ou disponível para execução
- [ ] Resumo de estatísticas apresentado ao usuário

## 📚 Documentação Completa

Para detalhes sobre como o agente funciona internamente, veja:

- `agents/commit-assistant.md` - Documentação completa do agente
- `README.md` - Guia de uso do plugin

**Desenvolvido com ❤️ por Carlos Araujo (cadu.gevaerd@gmail.com)**
