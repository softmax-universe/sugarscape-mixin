# Strategy surface (authoring-day analysis, 2026-08-18)

Everything here is doc-derived or standings-derived analysis, not campaign
experience. Verify with replays and sweeps before betting on it; META.md
carries the dated field picture.

## Targeted generation (solo/duo)

- **The generator's real job is breadth.** 80 scenarios = 6 target families
  × mechanic packs. The scoring cliff to attack first is pack coverage: a
  ruleset that ignores disease/seasons/combat when active gives those
  scenarios away. Infer active mechanics from the resolved config in the
  observation.
- **Survival before shape.** Extinction and empty measurements are 0. The
  standard floor: a low-`agent.ttl` guard rule, plus traits that keep the
  measured variable *active* (trade > 0 for price targets, fertility > 0
  for population/survivorship targets).
- **Match direction, not vibes.** The score is a W1 distance: compare the
  measured histogram to the target and name which bins hold too much mass.
  Concentrating forces (lending, welfare-greed) push right-skew;
  protective/equalizing forces (low aggression, trade) spread mass.
- **Duo:** both targets are global on one world. Expect adversarial
  pressure on shared aggregates (e.g. convergence vs diversity pairs);
  robustness to a hostile co-lawgiver is worth more than a point of solo
  fit. Solo standings (0.47–0.63 spread) suggest nobody owns the hard
  packs yet.

## Commonwealth

Score = survivors × mean window wellness, no ceiling. The three
**documented, deliberately accepted degeneracies** (game repo
`docs/designs/2026-08-18-commonwealth-league.md`) are the day-one meta:

1. **Sacrificial pauper** — the wealth-happiness term saturates on
   sign(wealth − mean): a few destitute agents dragging the mean below the
   median raises everyone else's wealth happiness.
2. **Population dominance** — non-negative per-agent wellness means adding
   an agent never hurts: fertility is the dominant lever, score ≈
   population × mean wellness.
3. **Conflict asymmetry** — under the canonical config, fighting only
   subtracts happiness (unless disease pushes aggression above 1): zero
   aggression is close to strictly correct.

**Caveat (measured 2026-08-18, cubi-bismarck):** for the Commonwealth *world*,
fertility is NOT an available lever — the variant ships `trait_ranges: null`
→ default clamp `[0,1]`, and the shipped baseline already submits `fertility:
1` (the max), so #2's "dominant lever" is already pinned by default. The
baseline also pins the other degenerate optima (aggression 0; trade, lending
maxed). Measured consequence: the shipped baseline is already strong — local
seed-mean **~722** (hosted ~681), i.e. at/above the field leader. Treat this
league as "beat an already-tuned baseline" (a real, noise-limited optimization
problem), NOT "grab the obvious fertility win" — that win is already banked.
Refuted first-session guesses so far: additive resource-tilt on movement, and
`lending→0` (both refuted by local paired sweeps).

Current field (2026-08-18): 3 entrants, ~2× score spread (708 / 648 /
373) — young frontier, likely the highest-ROI league for a new player.
First question for any rival constitution: is its score population-driven
or wellness-driven?

## Where local compute wins

Every strategic hypothesis above is testable in minutes at the pinned ref
(recipes in `skills/eval-design/`). The discipline: one change per sweep,
paired seeds, decomposed reads — and show the human the interesting
intermediate results, not just the final ruleset.
