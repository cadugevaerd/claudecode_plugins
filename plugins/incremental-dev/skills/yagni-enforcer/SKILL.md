---
name: yagni-enforcer
description: Detecta automaticamente quando código está sendo criado "para o futuro" ou tem complexidade desnecessária. Use quando implementar funcionalidades, criar classes/abstrações, ou adicionar configurações. Detecta over-engineering, abstrações prematuras, e antecipação de requisitos futuros.
allowed-tools: Read, Grep, Glob
---

# YAGNI Enforcer

Skill que detecta automaticamente quando código está prestes a violar YAGNI (You Aren't Gonna Need It), identificando over-engineering, abstrações prematuras, e funcionalidades antecipadas.

## 🎯 Gatilhos de Invocação

Invoque automaticamente quando:

1. **Criar classes abstratas/interfaces** - "Vou criar AbstractX..."
2. **Implementar design patterns** - "Usando Factory/Strategy..."
3. **Adicionar configuração complexa** - "ConfigManager para..."
4. **Antecipar funcionalidades** - "Para facilitar no futuro..."
5. **Criar múltiplos níveis de abstração** - Hierarquias complexas
6. **Implementar features não pedidas** - "Vou adicionar também..."

### Termos Suspeitos
- "para o futuro", "caso precise", "para facilitar expansão"
- "preparar para", "deixar flexível", "para reutilização"
- "será útil depois", "pode ser necessário"

## ⚠️ Padrões YAGNI

### Padrão 1: Abstração Prematura
- Classe abstrata com 1 implementação
- Interface para 1-2 implementações
- Hierarquia sem 3+ casos de uso

**Alternativa**: Função/classe direta, refatore quando tiver 3+ tipos

### Padrão 2: Antecipação de Futuro
- Parâmetros não usados "para depois"
- Comentários "TODO: adicionar X"
- Código preparando expansão hipotética

**Alternativa**: Implementar apenas o necessário AGORA

### Padrão 3: Over-Configuration
- ConfigurationManager para < 10 configs
- Sistema elaborado para valores simples
- Validação complexa de config

**Alternativa**: Dict simples para < 10 configs

### Padrão 4: Factory Desnecessário
- Factory criando apenas 1 tipo
- Factory sem variação runtime

**Alternativa**: Criação direta (não precisa factory com 1 tipo)

### Padrão 5: Patterns Forçados
- Singleton para objeto stateless
- Observer sem necessidade de notificação
- Strategy com apenas 1-2 implementações

**Alternativa**: Função simples; use patterns com 3+ casos

## 📊 Níveis de Alerta

| Nível | Severidade | Ação |
|-------|------------|------|
| 🔴 CRÍTICO | Grave | Não implementar, sugerir simples |
| 🟡 MODERADO | Provável | Alertar fortemente |
| 🟢 LEVE | Possível | Sugerir alternativa |

## 📋 Checklist Mental

Ao implementar código, verificar:

```
[ ] Criando abstração? → Tenho 3+ casos? NÃO → ⚠️
[ ] Usando pattern? → Tenho 3+ casos? NÃO → ⚠️
[ ] Adicionando config? → 10+ valores? NÃO → ⚠️
[ ] Criando factory? → 3+ tipos? NÃO → ⚠️
[ ] Adicionando parâmetro? → Usa AGORA? NÃO → ⚠️
[ ] "Para o futuro"? → Requisito concreto? NÃO → ⚠️
[ ] Hierarquia de classes? → Realmente necessária? NÃO → ⚠️
```

## 💡 Princípios de Ouro

1. **Regra dos 3**: Abstraia apenas com 3+ implementações
2. **Não antecipe**: Se não usa AGORA, não adicione
3. **Simples > Complexo**: Sempre preferir simplicidade
4. **MVP funcional**: Funcionando > código elegante
5. **Delete > Refactor**: Não adicione = não precisa refatorar

## 📚 Referência Detalhada

Para aprofundar em YAGNI:

- **PATTERNS.md** - Padrões YAGNI com exemplos de código
- **PRINCIPLES.md** - Princípios core e regra dos 3
- **EXAMPLES.md** - Exemplos práticos de bom vs ruim
- **CHECKLIST.md** - Checklists para detectar over-engineering

## ⚡ Objetivo

✅ Prevenir over-engineering ANTES de implementar
✅ Manter código simples e focado
✅ Sugerir alternativas mais simples
❌ Não implementar código (apenas alertar)

**Valor**: Desenvolvimento INCREMENTAL e SIMPLES, sem complexidade prematura.
