# The game (condensed for agents)

Full human-facing docs live in the game repo —
https://github.com/softmax-universe/coworld-sugarscape — whose `docs/RULES.md` is
test-enforced against the implementation and always outranks this file.
Human-shaped introductions: the repo's `docs/getting-started.md` and
`docs/sugarlang-tutorial.md` (send the human there; use this file yourself).

## Model

- DTL Sugarscape (Epstein & Axtell lineage): agents on a grid metabolize
  sugar/spice, move, trade, lend, fight, reproduce, sicken, die. The engine
  is pinned; players do not touch it.
- The player's entire output is **one SugarLang ruleset per episode**:
  - `traits`: overrides for `aggression`, `trade`, `lending`, `fertility`
    (clamped into the variant's `trait_ranges`).
  - `movement`: an ordered decision list re-ranking the engine's own
    candidate cells. Required unconditional final rule. First match scores
    each candidate; best score wins; ties → shorter travel, then engine
    order.
- Budgets: 256 expression nodes, depth 16, 32,768 bytes. Expressions are
  total (÷0 → 0.0, pow clamped to exponent [−8,8] and base ≥ 0, NaN/inf →
  0.0). No randomness, no state, no loops.
- Feature vocabulary: `agent.*` (sugar, spice, wealth, metabolisms, vision,
  movement, age, ttl, mrs), `cell.*` (sugar, spice, pollution, distance,
  occupied, preyWealth, welfare), `world.*` (timestep, population, gini,
  meanWealth — world stats are T−1 snapshots). `cell.welfare` is the
  engine's own candidate valuation — the standard base term.

## Episode shape

Connect → one observation (resolved public config + this seat's target) →
submit ruleset (180 s window) → disconnect. The world runs 1,000 ticks
unattended; measurement pools the final window (typically 100 ticks solo,
50 commonwealth); scoring compares measurement to target
(`w1-hyperbolic/1`) or sums survivor wellness (`wellness-sum/1`).

## Worlds

Ranked solo/duo episodes draw from a deterministic 80-scenario pool: 12
hand-tuned base worlds across 6 target families × mechanic packs
(baseline, spice, market, combat, disease, pollution, seasons,
reproduction, everything). Selection is `seed % 80`; the player sees only
the resolved config — infer active mechanics from it. Commonwealth is one
canonical fixed world every episode.

## Determinism

Pinned interpreter + `PYTHONHASHSEED=0`; recorded seed + config + rulesets
reproduces any episode exactly via local
`coworld.episode.run_episode(config, [ruleset])` — the base primitive for
all local evaluation and diagnosis.
