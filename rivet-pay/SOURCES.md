# RivetPay Sources and Decisions

Maintainer inventory only. These sources informed the architecture; none is vendored or a runtime dependency. Retrieved/current review date: 2026-09-13.

| Source | Trust tier | Decision |
|---|---|---|
| [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | workflow guidance | Keep a concise orchestrator, focused references, and validation. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | workflow guidance | Prefer progressive disclosure and scoped resources. |
| [Trail of Bits workflow skill design](https://github.com/trailofbits/skills/blob/main/plugins/workflow-skill-design/skills/designing-workflow-skills/references/anti-patterns.md) | workflow guidance | Avoid monolithic prompts, hidden state, and duplicated owners. |
| [Trail of Bits audit-context-building](https://github.com/trailofbits/skills/blob/main/plugins/audit-context-building/skills/audit-context-building/SKILL.md) | audit workflow | Separate context reconstruction from findings. |
| [Trail of Bits c-review FP judge](https://github.com/trailofbits/skills/blob/main/plugins/c-review/agents/c-review-fp-judge.md) | review workflow | Reopen evidence and challenge false positives independently. |
| [Trail of Bits c-review dedup judge](https://github.com/trailofbits/skills/blob/main/plugins/c-review/agents/c-review-dedup-judge.md) | review workflow | Preserve duplicates while canonicalizing only true duplicates. |
| [Trail of Bits fp-check](https://github.com/trailofbits/skills/blob/main/plugins/fp-check/hooks/hooks.json) | tooling pattern | Use deterministic checks as gates, not as a substitute for review. |
| [Trail of Bits variant-analysis](https://github.com/trailofbits/skills/blob/main/plugins/variant-analysis/skills/variant-analysis/SKILL.md) | analysis workflow | Expand meaningful variants without Cartesian explosion. |
| [Trail of Bits spec-to-code-compliance](https://github.com/trailofbits/skills/blob/main/plugins/spec-to-code-compliance/agents/spec-compliance-checker.md) | evidence workflow | Compare explicit contract claims with implementation evidence. |
| [Consensys repo-security-review](https://github.com/Consensys/repo-security-review) | security workflow | Preserve repository-grounded, read-only review boundaries. |
| [Sentry skills conventions](https://github.com/getsentry/skills) | skill conventions | Keep skills discoverable and task-focused. |
| [Stripe AI skills](https://github.com/stripe/ai) | domain inspiration | Payment domain relevance only; no provider-specific behavior adopted. |

No external skill is required at runtime. Provider-specific facts must be established from the reviewed contract when materially necessary; these sources do not define payment semantics.
