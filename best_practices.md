# Best practices — Sugarscape

Durable, graduated practice for optimizing in this game. Mixin authors: seed
this with the game community's earned lessons — it's a mixin's biggest gift.
User graduations accumulate alongside, marked with their recurrence evidence.

---

Seeded at mixin authoring (2026-08-18) from the game's documented contracts,
not from campaign recurrence:

- **Pre-score locally before every upload.** A full scored episode is ~5 s
  at the pinned ref; there is no reason to learn a score from the ladder.
- **Validate before you reason about a ruleset.** `parse_ruleset` reports
  node/depth/byte budgets exactly; an invalid ruleset is never scored.
- **Keep a survival guard.** Extinction and empty measurements score 0 in
  distribution leagues; a low-TTL guard rule is the standard floor.
- **Commonwealth submissions must be constant, not merely deterministic.**
  Any generation-time variation fails the `rulesets_identical` qualifier.
- **Read scores decomposed, never pooled.** Per-scenario and per-pack views
  are where cliffs live (see the ab binding).
