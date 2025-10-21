---
description: Realiza commit com validações completas via agente especializado
---

# Comando: /commit

Este comando delega ao agente especializado `commit-assistant` para executar o processo completo de commit seguindo as melhores práticas.

---

## 🎯 O que este comando faz

Invoca o agente `commit-assistant` que automaticamente:

1. ✅ **Valida segurança** - Detecta e bloqueia arquivos sensíveis
2. ✅ **Executa CI/CD** - Roda testes, linting, build e validações
3. ✅ **Analisa mudanças** - Examina git diff e categoriza alterações
4. ✅ **Verifica documentação** - Identifica docs que precisam atualização
5. ✅ **Gera mensagem** - Cria commit message seguindo Conventional Commits
6. ✅ **Executa commit** - Realiza o commit com mensagem formatada
7. ✅ **Push opcional** - Pergunta se deseja fazer push (nunca força)

---

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

---

## 📚 Documentação Completa

Para detalhes sobre como o agente funciona internamente, veja:
- `agents/commit-assistant.md` - Documentação completa do agente
- `README.md` - Guia de uso do plugin

---

**Desenvolvido com ❤️ por Carlos Araujo (cadu.gevaerd@gmail.com)**
