# Sistema de Export e Instalação — Documentação para Branch

> Alterações feitas por Victor (CEO) em 2026-03-28/29 durante testes do primeiro bundle (LAUNCHPAD).
> Este documento descreve o padrão definitivo de export + instalação para o MyClaude Creator Engine.

---

## Resumo das Alterações

### O que mudou vs. main

1. **product-dna install_targets corrigidos** — agents, squads, workflows agora vão para `commands/` (não `skills/`)
2. **`/package` atualizado** — gera CLAUDE.md para type=system + inclui todos bundle assets dentro de `.claude/`
3. **Novo padrão de export** — sistema autônomo com .claude/skills/ + .claude/commands/ dentro do motor
4. **Bundle installer (CLAUDE.md)** — respeita mapeamento correto skills/ vs commands/
5. **Bug CSP login reportado** — `myclaude login` bloqueado por CSP (BUG-REPORT-CSP-LOGIN.md)

---

## Mapeamento de Tipos → Destinos (DEFINITIVO)

| Tipo | install_target | Destino Global | Dentro do Motor |
|------|---------------|---------------|-----------------|
| **skill** | `.claude/skills/{slug}/` | `~/.claude/skills/{slug}/` | `.claude/skills/{slug}/` |
| **prompt** | `.claude/skills/{slug}/` | `~/.claude/skills/{slug}/` | `.claude/skills/{slug}/` |
| **agent** | `.claude/commands/{slug}/` | `~/.claude/commands/{slug}/` | `.claude/commands/{slug}/` |
| **squad** | `.claude/commands/{slug}/` | `~/.claude/commands/{slug}/` | `.claude/commands/{slug}/` |
| **workflow** | `.claude/commands/{slug}/` | `~/.claude/commands/{slug}/` | `.claude/commands/{slug}/` |
| **system** | `{user_chosen_path}/` | **NÃO vai pro global** | `.claude/commands/{name}/` (registra o slash) |
| **claude-md** | `.claude/rules/{slug}.md` | `~/.claude/rules/{slug}.md` | — |
| **application** | `myclaude-products/{slug}/` | local | — |
| **design-system** | `myclaude-products/{slug}/` | local | — |

### Por que essa separação?

O Claude Code usa duas pastas para registrar slash commands:
- `~/.claude/skills/` — detecta arquivos com `SKILL.md` como entry
- `~/.claude/commands/` — detecta qualquer `.md` com frontmatter `name:` como entry

Os squads existentes do Victor (copy, hormozi, design) já estão em `commands/`. Skills (como site-alchemy, ds-library) estão em `skills/`. Misturar quebra a detecção de slash commands.

---

## Fluxo Completo: Criação → Export → Instalação

```
1. /create {type}
   → Lê product-dna/{type}.yaml (install_target, DNA patterns)
   → Scaffold em workspace/{slug}/ com WHY comments
   → .meta.yaml criado (phase: scaffold)

2. /fill [slug]
   → Preenche conteúdo seção por seção
   → .meta.yaml → phase: content

3. /validate [slug]
   → 7 stages (structural → integrity → DNA → CLI → anti-commodity)
   → Score: (DNA × 0.50) + (Structural × 0.30) + (Integrity × 0.20)
   → .meta.yaml → phase: validated

4. /package [slug]
   → Strip WHY comments
   → Gera vault.yaml + plugin.json + agentskills.yaml
   → Para type=system:
     - Inclui CLAUDE.md (gera se não existir)
     - Inclui .claude/commands/{name}/SYSTEM.md (registra slash command)
     - Inclui .claude/skills/ com skills do bundle
     - Inclui .claude/commands/ com agents/squads/workflows do bundle
   → .meta.yaml → phase: packaged

5. EXPORT (manual ou via Engine)
   → Copia .publish/ para vault-creations/{BUNDLE_NAME}/
   → Bundle: pastas por produto + CLAUDE.md installer na raiz

6. /start (usuário abre pasta do bundle no Claude Code)
   → CLAUDE.md do bundle roda automaticamente
   → Skills → ~/.claude/skills/ (global)
   → Agents, Squads, Workflows → ~/.claude/commands/ (global)
   → System → cópia pura para pasta escolhida pelo usuário
   → Motor recebe: CLAUDE.md + SYSTEM.md + .claude/ com todos assets + workspace/ + memory/

7. OPERAÇÃO (usuário abre pasta do motor no Claude Code)
   → CLAUDE.md do motor carrega
   → Lê memory/system-state.yaml + launch-history.yaml
   → Escaneia workspace/
   → TODOS os slash commands disponíveis:
     /launchpad, /launch-brief, /launch-copy,
     /launch-strategist, /launch-ops, /launch-sequence
```

---

## Diferenças: Export Manual vs CLI

| Aspecto | CLI (`myclaude install`) | Export Manual (/start) |
|---------|------------------------|----------------------|
| **Destino skills** | `~/.claude/skills/{slug}/` | `~/.claude/skills/{slug}/` (mesmo) |
| **Destino commands** | `~/.claude/skills/{slug}/` (CLI não separa) | `~/.claude/commands/{slug}/` (separado) |
| **System** | Instala como skill global | Copia como projeto autônomo |
| **Motor** | Não existe conceito de motor | Motor = pasta própria com .claude/ completo |
| **Bundle assets no motor** | N/A | Todos assets copiados dentro do .claude/ do motor |
| **CLAUDE.md** | N/A | Gerado para systems, é o brain do motor |
| **Pastas de trabalho** | N/A | workspace/, memory/learnings/, memory/templates/ criados |

**Nota:** O CLI do MyClaude (`myclaude install`) instala tudo em `skills/`. O export manual respeita a separação `skills/` vs `commands/`. Não mexemos no CLI — estas são alterações apenas no comportamento local do Engine.

---

## Estrutura do Motor Exportado (Padrão Definitivo)

```
{pasta_do_motor}/
├── CLAUDE.md                              ← Brain (Claude Code detecta ao abrir)
├── SYSTEM.md                              ← Referência completa do sistema
├── README.md                              ← Documentação
├── agents/                                ← Agents do sistema (orchestrator, etc.)
├── config/                                ← Configuração do sistema
├── references/                            ← Domain knowledge
├── memory/
│   ├── system-state.yaml                  ← Estado atual
│   ├── launch-history.yaml                ← Histórico (append-only)
│   ├── learnings/                         ← Padrões aprendidos
│   └── templates/                         ← Templates de lançamentos bem-sucedidos
├── workspace/                             ← Dados de trabalho (1 pasta por lançamento)
│
└── .claude/
    ├── skills/                            ← Skills do bundle (registra slash commands)
    │   ├── {skill-1}/SKILL.md
    │   └── {skill-2}/SKILL.md
    └── commands/                          ← Agents, squads, workflows, o próprio system
        ├── {system-name}/SYSTEM.md        ← Registra /system-name como comando
        ├── {agent}/AGENT.md
        ├── {squad}/SQUAD.md + agents/
        └── {workflow}/WORKFLOW.md + config/
```

---

## Estrutura do Bundle Export (o que o usuário baixa)

```
{BUNDLE_NAME}/
├── CLAUDE.md                              ← Installer (/start — roda ao abrir no CC)
├── BUNDLE-DOCS.md                         ← Documentação completa
├── .claude/skills/start/SKILL.md          ← Re-run manual do installer
├── {skill-1}/                             ← Pasta completa do skill (.publish/)
├── {skill-2}/                             ← Pasta completa do skill
├── {agent}/                               ← Pasta completa do agent
├── {squad}/                               ← Pasta completa do squad + agents/
├── {workflow}/                            ← Pasta completa do workflow
└── {system}/                              ← Pasta completa do system (COM .claude/ dentro)
    ├── CLAUDE.md                          ← Brain do motor
    ├── SYSTEM.md
    ├── .claude/skills/ + .claude/commands/ ← TODOS os assets do bundle
    ├── memory/
    └── (workspace/ e memory/learnings/ criados durante install)
```

---

## Arquivos Alterados no Engine (vs. main)

| Arquivo | Alteração |
|---------|----------|
| `product-dna/agent.yaml` | `install_target` → `.claude/commands/{slug}/` |
| `product-dna/squad.yaml` | `install_target` → `.claude/commands/{slug}/` |
| `product-dna/workflow.yaml` | `install_target` → `.claude/commands/{slug}/` |
| `product-dna/system.yaml` | `install_target` → `{user_chosen_path}/` |
| `.claude/skills/package/SKILL.md` | System type: gera CLAUDE.md + .claude/ com bundle assets |
| `creator.yaml` | Criado pelo /onboard (Victor, @darwimmusic) |
| `workspace/` | 6 produtos do LAUNCHPAD (packaged, MCS-3 100%) |
| `BUG-REPORT-CSP-LOGIN.md` | Bug report do CSP que bloqueia myclaude login |

---

## Produtos Criados (LAUNCHPAD Bundle)

| # | Slug | Tipo | DNA | Score | Preço |
|---|------|------|:---:|:-----:|-------|
| 1 | launch-brief | skill | 14/14 | 100% | Free |
| 2 | launch-copy | skill | 14/14 | 100% | Free |
| 3 | launch-strategist | agent | 15/15 | 100% | $69 |
| 4 | launch-ops | squad | 18/18 | 100% | $199 |
| 5 | launch-sequence | workflow | 12/12 | 100% | $39 |
| 6 | launchpad-os | system | 18/18 | 100% | $349 |

Bundle: $499 (24% off vs. $656 individual)

---

## Bugs Conhecidos

### CSP Login (P0)
`myclaude login` bloqueado por Content Security Policy `form-action 'self'` em myclaude.sh.
Impede `myclaude publish`. Detalhes em `BUG-REPORT-CSP-LOGIN.md`.

---

*Documentação gerada em 2026-03-29 por Victor (CEO) durante teste de criação do primeiro bundle.*
