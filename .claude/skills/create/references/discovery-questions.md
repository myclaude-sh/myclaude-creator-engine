# Discovery Questions

Category-specific questions asked during the `/create` flow (Stage 2: Discovery).

Ask these conversationally. Do not dump all questions at once — wait for answers
before proceeding to the next question when the creator needs to think.

**When asking each question, show the good/weak contrast to calibrate the creator's
specificity.** Generic answers produce generic products.

---

## Skills

1. What problem does this skill solve?
   - Strong: "Detects reentrancy vulnerabilities in Solidity smart contracts before deployment"
   - Weak: "Helps with security" — too vague, no domain, no specificity

2. Who is the target user? (developer, marketer, analyst, etc.)
   - Strong: "Solidity developers auditing DeFi protocols before mainnet launch"
   - Weak: "Developers" — which developers? doing what? in what context?

3. What triggers should activate this skill?
   - Strong: "When someone says 'review my contract', 'check for reentrancy', 'audit this Solidity'"
   - Weak: "When someone needs help" — Claude can't match this to anything specific

4. What output format should the skill produce?
   - Strong: "A ranked list of vulnerabilities with severity, location (file:line), and fix suggestion"
   - Weak: "A report" — what kind? how structured? what does the user do with it?

5. What domain knowledge is needed?
   - Strong: "Solidity patterns, common DeFi attack vectors, OpenZeppelin best practices"
   - Weak: "Security knowledge" — that's the whole field, not actionable expertise

6. What tools/integrations does it need?
   - Strong: "Needs Read for .sol files, Bash for running slither, Grep for pattern matching"
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

1. What is the squad's mission?
2. How many agents are needed and what roles?
3. What is the routing logic? (who handles what?)
4. What workflows does the squad execute?
5. What are the handoff protocols between agents?

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

## Prompts

1. What specific task does this prompt address?
2. Who is the target user? (what role, what context)
3. What output format is expected?
4. What variables should be customizable?
5. What tone/voice should the prompt enforce?
6. What are the edge cases the prompt must handle?

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
