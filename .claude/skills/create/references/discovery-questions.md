# Discovery Questions

Category-specific questions asked during the `/create` flow (Stage 2: Discovery).

Ask these conversationally. Do not dump all questions at once — wait for answers
before proceeding to the next question when the creator needs to think.

**When asking each question, show the good/weak contrast to calibrate the creator's
specificity.** Generic answers produce generic products.

---

## Skills

**IMPORTANT:** Select example pairs that match `creator.profile.type`. Developer gets dev examples, non-dev gets domain examples. Show BOTH if type is hybrid. Never show only dev examples to a non-dev creator.

1. What problem does this skill solve?
   - Dev example: "Detects reentrancy vulnerabilities in Solidity smart contracts before deployment"
   - Non-dev example: "Generates a complete brand voice guide from a company's existing content — tone, vocabulary, do/don't rules"
   - Weak: "Helps with marketing" — too vague, no domain, no specificity

2. Who is the target user?
   - Dev example: "Solidity developers auditing DeFi protocols before mainnet launch"
   - Non-dev example: "Marketing consultants who need to systematize brand voice for clients"
   - Weak: "People who write" — which people? writing what? in what context?

3. When should this tool activate? (what words or situations trigger it?)
   - Dev example: "When someone says 'review my contract', 'check for reentrancy', 'audit this Solidity'"
   - Non-dev example: "When someone says 'create brand voice', 'analyze my tone', 'voice guide for [company]'"
   - Weak: "When someone needs help" — Claude can't match this to anything specific

4. What output format should it produce?
   - Dev example: "A ranked list of vulnerabilities with severity, location (file:line), and fix suggestion"
   - Non-dev example: "A structured brand voice document: personality traits, tone spectrum, vocabulary table, 5 before/after examples"
   - Weak: "A report" — what kind? how structured? what does the user do with it?

5. What domain knowledge is needed?
   - Dev example: "Solidity patterns, common DeFi attack vectors, OpenZeppelin best practices"
   - Non-dev example: "Brand archetypes (Jungian), tone-of-voice frameworks (MailChimp/Slack), copywriting principles"
   - Weak: "Marketing knowledge" — that's the whole field, not actionable expertise

6. What tools or capabilities does it need?
   - Dev example: "Needs to read code files, run linters, search for patterns in source code"
   - Non-dev example: "Needs to read existing documents, search the web for brand examples, write the output file"
   - Weak: "Standard tools" — specify which ones and why

---

## Agents

1. What role does this agent play?
   - Strong: "Senior security auditor who reviews code with a red-team mindset"
   - Weak: "A helpful assistant for security"

2. What personality/voice should it have?
   - Strong: "Direct, evidence-based, always cites the specific line of code. Never says 'looks fine' without proof."
   - Weak: "Friendly and helpful"

3. What tools does it need access to?
4. What decisions can it make autonomously vs. escalate?
   - Strong: "Can flag warnings autonomously. Must escalate to human for: deleting files, modifying production configs, approving deploys."
   - Weak: "It should be smart about what to do"

5. How does it interact with other agents (if part of a squad)?

---

## Squads

**IMPORTANT:** Squads are organism-level products. Ask archetype FIRST — it determines the coordination pattern, template structure, and routing shape. Select example pairs that match `creator.profile.type`. Show BOTH if hybrid.

1. What coordination archetype fits your squad?
   - Show options: **Sequential Pipeline** (A→B→C, assembly line), **Parallel Fan-Out** (all agents work simultaneously, synthesize), **Conditional Router** (orchestrator routes by intent), **Iterative Refinement** (loop until quality gate passes), **Hierarchical Delegation** (tiered specialists, Tier 0→1→2)
   - Dev example: "Hierarchical delegation — data agents (Tier 0) establish baseline, strategy agents (Tier 1) architect, execution agents (Tier 2) implement"
   - Non-dev example: "Sequential pipeline — research agent finds data, analysis agent interprets, writer agent produces the report"
   - Weak: "They all work together" — HOW do they work together? that's the whole point

2. What is the squad's mission? (what does the TEAM achieve that no single agent can?)
   - Strong: "Transform raw business data into growth decisions — requires data analysis, strategic framing, execution planning, and measurement in coordinated sequence"
   - Weak: "Help with marketing" — a single agent could do that; what needs COORDINATION?

3. What specialists compose the squad? (name each role and its exclusive domain)
   - Dev example: "security-scanner (finds vulns), threat-modeler (classifies risk), fix-generator (writes patches), reviewer (validates fixes) — 4 agents, zero overlap"
   - Non-dev example: "researcher (gathers data), strategist (interprets patterns), writer (produces deliverables), editor (quality gate) — each owns one phase"
   - Weak: "A few agents that help" — which agents? doing what? if roles overlap, it's not a squad

4. What is the routing logic? (how does the orchestrator decide who handles what?)
   - Strong: "IF input is raw data → data-compass. IF input is strategic question → brian-balfour. IF input is execution brief → paid-executor. Ambiguous → traffic-chief classifies first."
   - Weak: "The system figures it out" — no, YOU define it; the orchestrator follows YOUR routing table

5. What are the entity lifecycles? (what objects flow through the squad and how?)
   - Strong: "A CAMPAIGN flows: hypothesis→architect→creative→build→launch→monitor→optimize→scale/kill→post-mortem — each phase mapped to a specialist"
   - Non-dev: "A PROPOSAL flows: research→outline→draft→review→revise→finalize — each step owned by a different agent"
   - Weak: "They pass stuff around" — what stuff? in what format? through what sequence?

6. What handoff format do agents use to pass work?
   - Strong: "XML envelope: <handoff><from>{agent}</from><task>{description}</task><state>{current data}</state><constraints>{rules}</constraints></handoff>"
   - Weak: "They communicate" — communication without format specification produces drift and silent failures

7. What does the kernel (orchestration intelligence) do beyond simple routing?
   - Strong: "Scores which agents are most relevant per request, adapts the plan mid-flight, persists context between sessions, and learns from past decisions"
   - Non-dev: "The coordinator remembers past sessions, scores which agents are most relevant, and adapts the plan mid-flight"
   - Weak: "It coordinates" — that's the definition of orchestrator, not a design decision. What INTELLIGENCE does it add?

8. What are the escalation rules? (when does the squad give up and ask the human?)
   - Strong: "Escalate when: agent confidence < 60%, two agents disagree on strategy, any irreversible action (budget >$1K, public launch, data deletion)"
   - Weak: "When it can't figure it out" — define the threshold

---

## Design Systems

1. What brand identity? (colors, typography, personality)
2. What platforms? (web, mobile, both)
3. What export formats? (Tailwind, CSS variables, DTCG)
4. What component library depth? (tokens only vs. full components)
5. What theming support? (single theme vs. multi-theme)

---

## Workflows

1. What process does this workflow automate?
2. What triggers it? (manual, event, schedule)
3. What are the inputs and expected outputs?
4. How many steps? What are the dependencies between steps?
5. What happens when a step fails? (retry, fallback, abort)
6. What tools or external services does it need?

---

## Bundles

1. What products does this bundle include? (list each by slug or name)
   - Strong: "Includes security-audit-skill, code-review-agent, and pre-commit-hooks — a complete security pipeline"
   - Weak: "Some security tools" — buyers need to know exactly what they're getting

2. Why are these products bundled together? (curation rationale)
   - Strong: "These 3 products form a complete CI security pipeline — the skill audits, the agent reviews, and the hooks automate"
   - Weak: "They're related" — related how? what's the compound value?

3. Is there a specific order to install/use them?
4. Do the products depend on each other or work independently?
5. What discount or value does the bundle offer over individual purchases?

---

## Statuslines

1. What information does this status line display?
   - Strong: "Current model, session cost, git branch, and context window usage with color-coded thresholds"
   - Weak: "Useful info" — which info? how displayed?

2. What data sources does it read from? (the JSON stdin fields: model, cost, cwd, context_window, etc.)
   - Strong: "Uses model, cost, and context_window from stdin JSON. Also runs `git rev-parse` for branch name."
   - Weak: "System data" — be specific about which fields

3. How should it look? (describe the visual format: colors, separators, layout)
4. What should it show when data is unavailable? (fallback display)
5. Does it need external tools? (jq for JSON parsing, git, etc.)

---

## Hooks

1. What Claude Code event triggers this hook? (from 25 available events)
   - Strong: "PostToolUse with matcher Write|Edit — fires after Claude modifies any file"
   - Weak: "When Claude does something" — which event? which matcher?

2. What does the handler do when triggered?
   - Strong: "Runs eslint --fix on the modified file, then prettier --write"
   - Weak: "Cleans up the code" — what specifically? which commands?

3. Is the handler idempotent? (safe to run multiple times on the same event)
4. What happens if the handler fails? Should it block Claude (exit 2) or continue silently (exit 0)?
5. Are there security implications? (shell commands, file access, network calls)
   - Strong: "Runs npm commands locally. No network calls. Only modifies the file Claude just wrote."
   - Weak: "It's safe" — document exactly what commands run

---

## Minds

**NOTE:** Minds are the most accessible product type for non-developers. Always include non-dev examples.

1. What domain expertise does this mind embody?
   - Dev example: "Kubernetes RBAC design — role scoping, service accounts, pod security standards"
   - Non-dev example: "B2B SaaS pricing strategy — value-based pricing, willingness-to-pay research, tier construction"
   - Weak: "Business strategy" — that's an entire MBA, not a mind

2. How does this mind think? What mental models does it use?
   - Dev example: "Threat modeling with STRIDE, attack tree analysis, defense-in-depth layering"
   - Non-dev example: "Van Westendorp pricing model, Good-Better-Best tier framework, value metric mapping"
   - Weak: "It thinks carefully" — which frameworks? what's the thinking process?

3. What questions does this mind always ask before answering?
   - Strong: "Always asks: What's your current pricing? Who's your ideal customer? What's your cost structure? What are competitors charging?"
   - Weak: "Asks some questions first" — which questions? this defines the mind's diagnostic process

4. What does this mind refuse to do or claim knowledge about?
   - Strong: "Won't advise on B2C pricing, won't predict revenue numbers, won't replace a CFO on financial modeling"
   - Weak: "Stays in its lane" — where exactly IS its lane?

5. How does this mind communicate? (formal, casual, Socratic, direct)
   - Strong: "Direct and practical. Uses tables for comparisons. Always gives a recommendation, not just options. Challenges assumptions with 'have you considered...'"
   - Weak: "Professional tone" — every AI is professional, what makes THIS mind's voice distinct?
6. Who is this mind for? What problem does the buyer have?
   - Dev example: "For platform engineers drowning in RBAC misconfigs — every cluster audit finds the same 5 mistakes"
   - Non-dev example: "For SaaS founders who know their product works but are leaving money on the table with bad pricing"
   - Weak: "For people who need help with pricing"

---

## CLAUDE.md

1. What type of project? (Next.js, Python, monorepo, etc.)
2. What are the key architectural decisions?
3. What security rules apply?
4. What conventions or standards should be enforced?
5. What is the team composition? (solo, small team, enterprise)

---

## Applications

1. What does this application do? (utility, tool, template)
2. What is the tech stack? (language, framework, dependencies)
3. Who is the target user? (developer, end-user, both)
4. Does it require external services? (APIs, databases, auth)
5. What is the deployment model? (local, hosted, CLI)

---

## Systems

1. What is the system's overarching purpose?
2. What product types does it combine? (skills + agents + workflows?)
3. How do the components interact? (routing, handoffs, shared state)
4. What is the entry point for the user?
5. Can components be used independently or only as a system?
