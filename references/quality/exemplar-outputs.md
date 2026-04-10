# Exemplar Outputs — The Magic Rendered

> These are not templates. They are **reference outputs** the Engine uses to calibrate
> tone, density, visual rhythm, and warmth. Each exemplar shows a complete touchpoint
> as the creator should experience it. The LLM reads these, internalizes the feel, and
> REASONS about its own output — never copies verbatim.

**Load rule:** Skills load only their own exemplar section. Never load the full file.

<!-- Every exemplar follows the same anatomy. Output is a ritual, not a dump. -->
<output_anatomy>
Every Engine output follows this skeleton (omit empty layers, never reorder):

  1. GREETING / CONTEXT    — ✦ line with emotional contact (if session-start or milestone)
  2. FRAME                 — ┌─ box ─┐ with key data (if major moment)
  3. BODY                  — the substance: data, progress, analysis, question
  4. INSIGHT               — ◆ non-obvious observation (if available, max 1)
  5. NEXT ACTION           — 🎯 exactly ONE clear next step
  6. ESCAPE HATCH          — option to save/skip/pause (if interactive)

Not every output has all 6. A quiet /publish has only layers 1+5.
A /fill question has layers 3+5+6. But the ORDER is always the same.
The creator's eye learns the rhythm and knows where to look.
</output_anatomy>

---

## E1: /status — Return After 3 Days (PT-BR, expert, 14 products)

```
✦ De volta, João. 3 dias desde a última sessão.

┌─ ✦ MyClaude Studio v3.0.0 ──────────────────┐
│  Creator: João · @l0z4n0                      │
│  14 produtos live · 5 domínios                │
└───────────────────────────────────────────────┘

Desde que você saiu:
  ⚡ aegis: +31 installs (284 total)
  📊 prometheus: nova avaliação ★4

YOUR PRODUCTS
  ✦ AEGIS             Tool           Elite ★★★   🟢
  ✦ K8s Advisor       Intelligence   Premium ★★  🟢
  ✦ Semantic Amp      Tool           Elite ★★★   🟢
  ✦ NOCTIS            Setup          Elite ★★★   📦
  ... +10 more (all 🟢)

PORTFOLIO VISION
  security ████████████░░░░ 5
  prompt   ████████░░░░░░░░ 3
  design   ████░░░░░░░░░░░░ 2
  ─────────────────────────
  5 domínios · 14 produtos · 13 live

🎯 NOCTIS está pronto — /publish para ir ao ar.
```

## E2: /status — First Session Ever (EN, beginner, 0 products)

```
✦ Welcome to MyClaude Studio.

┌─ ✦ MyClaude Studio v3.0.0 ──────────────────┐
│  Creator: Sarah                               │
│  Your workshop is ready. Let's build.         │
└───────────────────────────────────────────────┘

  ○ research → ○ draft → ○ refine → ○ verify → ○ launch
  Your first product starts here.

QUICK ACTIONS
  /scout  — Research a domain first (recommended)
  /create — Start building directly

💡 Most successful products start with /scout —
   it reveals what Claude misses in your domain.
```

## E3: /create — Scaffold Celebration (PT-BR, intermediate)

```
✦ semantic-amplifier nasceu!

┌─ Novo Produto ────────────────────────────────┐
│  📦 workspace/semantic-amplifier/              │
│  Type: Tool · Target: Premium ★★              │
│  7 seções com orientação WHY                   │
└────────────────────────────────────────────────┘

  ○ research → ● draft → ○ refine → ○ verify → ○ launch
                 ▲ você está aqui

Seu portfólio prompt: 3 produtos.
Este será o 4º — a coleção está crescendo.

🎯 Próximo: /fill semantic-amplifier
   Vou te guiar seção por seção.
```

## E4: /fill — Section Question (warm elicitation, PT-BR)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊 Progresso: 3/7 seções (43%)
  ✦ Core identity travada. Estrutura sólida.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

── Seção 4/7: Anti-Patterns ──────────────

Pense nos erros que você vê repetidamente
no seu domínio. Os padrões que fazem você
pensar "de novo isso?"

Preciso de pelo menos 5 — cada um com:
  • O que acontece (o erro)
  • Por que acontece (a causa raiz)
  • Como evitar (a prevenção)

💡 Se travar: me conte um caso real que
   você já encontrou. Eu ajudo a estruturar.
```

## E5: /fill — Section Complete + Sparring (EN, expert)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊 Progress: 5/7 sections (71%)
  ✦ Anti-patterns locked. Strong domain signal.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Section quality: SOLID — 7 anti-patterns with
clear prevention. One pushback:

  ◆ Anti-pattern #3 ("ignoring context window")
    describes the symptom but not the root cause.
    What makes developers ignore it — ignorance
    or tooling gaps?

  1. Deepen this one
  2. Move on — good enough
  3. Save progress, continue later
```

## E6: /validate — Pass (PT-BR, first validation ever)

```
┌─ ✦ Validação Completa ───────────────────────┐
│                                               │
│  ✦ READY — 88% (target: 85%)                 │
│                                               │
│  ┌──────────┐                                 │
│  │ ★★ PREMIUM │  — Expertise profunda          │
│  └──────────┘    verificada                   │
│                                               │
│  Sua primeira validação. 88% é acima da       │
│  média do marketplace (82%).                  │
│                                               │
└───────────────────────────────────────────────┘

  15/15 padrões de qualidade passando.
  Substância: 72/100 — conhecimento real detectado.

  ○ research → ○ draft → ○ refine → ● verify → ○ launch
                                      ▲

🎯 Próximo: /test para validação comportamental.
```

## E7: /validate — Failure (EN, direct)

```
─── NEEDS WORK ─── 68% (target: 85%) ──────────
│
│ Top 3 fixes (highest impact first):
│   1. Anti-patterns: 2 found, need 5
│      → Add 3 domain-specific failure modes
│   2. Quality gate: criteria aspirational
│      → Change "output must be clear" to
│        "output contains exactly 3 sections"
│   3. Activation: no reference files loaded
│      → Add references/ with domain knowledge
│
│ Fix these, then: /validate
──────────────────────────────────────────────────

Estimated score after fixes: ~82%
Still 3% short of Premium. The gap is substance
depth — your anti-patterns need real examples.
```

## E8: /publish — First Product (PT-BR, celebration)

```
┌─ ✦ MyClaude Studio ──────────────────────────┐
│                                               │
│  ✦ Seu primeiro produto está no ar.           │
│                                               │
│  semantic-amplifier · Tool · Premium ★★       │
│                                               │
│  Cobre 8 gaps que o Claude não alcança        │
│  sozinho. Cada sessão que descobrir isso       │
│  vira um vetor de distribuição.               │
│                                               │
│  myclaude install semantic-amplifier           │
│                                               │
└───────────────────────────────────────────────┘

🎯 Use você mesmo primeiro — a melhor validação
   é o uso diário. Em alguns dias:
   myclaude stats semantic-amplifier
```

## E9: /publish — Nth Product (EN, expert, compact)

```
✦ Published. myclaude install k8s-hardening
  Portfolio: 5 in security domain.
  ◆ Bundle opportunity — /create bundle to compose.
```

---

## Loading Matrix

| Skill | Load exemplar(s) |
|-------|------------------|
| /status | E1, E2 |
| /create | E3 |
| /fill | E4, E5 |
| /validate | E6, E7 |
| /publish | E8, E9 |
| /package | — (uses /publish exemplars for preview) |
| /onboard | E2 (adapted) |

**Rule:** Exemplars inform, never constrain. The Engine REASONS about
its own creator's context and produces output that may differ in every
detail — but carries the same warmth, rhythm, and visual intention.
