---
name: sugarscape-ab
binding: ab
description: >
  Sugarscape binding for the core ab-compare skill: per-league metrics,
  per-scenario/pack decompositions, taint definition, paired local
  comparisons, and measured N floors.
---

# A/B binding — Sugarscape

The core `ab-compare` skill carries the comparison standard (fresh + matched,
taint before means, decompose before judging, noise is a verdict, regression
sweep). This binding supplies everything game-shaped.

**The inversion to internalize first:** solo and commonwealth episodes have
no opponents, and the actual scoring function runs locally at the pinned
ref. By recorded decision (MIXIN.md "Doctrine note"), **local paired sweeps
are admissible verdict evidence for solo/commonwealth score claims**, with
one hosted confirmation required before any league submit. What stays
live-only: version skew vs the deployed build, duo opponents, league
aggregation, the commonwealth qualifier.

## Metrics that matter

| Metric | Type | Direction | Why |
|---|---|---|---|
| `scores[seat]` / `score.seat_N` (`w1-hyperbolic/1`) | mean over episodes, 0–1 | higher | The ranked metric in solo/duo |
| raw Wasserstein-1 distance (per-seat `details`) | mean | lower | Mechanism evidence: same score can hide different miss shapes |
| `wellness-sum/1` score | mean | higher | The commonwealth metric. **Always decompose**: survivors × mean window wellness — population is the dominant lever |
| `result.extinct`, `result.population_final` | rate / mean | — | Extinction ⇒ 0 in distribution leagues; the first thing to check on any bad score |
| per-seat `details[i].empty_measurement` | rate | lower | An empty measurement scores 0 without extinction |

## Decompositions

Never verdict on a pooled mean. The splits, in order:

1. **Per-scenario** (`results["scenario_index"]`, 0–79): the pool is 12 base
   worlds × mechanic packs; a policy can be excellent on baseline worlds and
   score 0.2 wherever combat or disease is active.
2. **Per-mechanic-pack** (scenario id suffix: baseline/spice/market/combat/
   disease/pollution/seasons/reproduction/everything): the canonical
   "aggregate hides the gap" split here.
3. **Per-target-family** (scenario id prefix): reveals whether the generator
   understands a target or got lucky on easy worlds.
4. **Per-league**: never mix `w1-hyperbolic/1` and `wellness-sum/1` numbers.

## Taint — what an invalid episode is

- `details[i].submitted == false` — missed the 180 s window; the seat ran
  the null ruleset. Our-policy failure, not platform failure, unless the
  episode-request row shows an infra error.
- Episode-request level failures (image pull, crash, timeout) — platform or
  container failure; check `coworld episodes <ereq> --json` state before
  blaming the ruleset.
- **Not taint:** a low score on a hard scenario, an extinction the ruleset
  caused, an empty measurement the ruleset caused. Those are findings.
  Never filter low scores.

## Tests and floors

Local comparisons can be **truly paired**: same scenario, same seeds, both
arms — `seed = scenario_index + 80·j` holds the scenario fixed while
varying the sim seed. Compare per-seed score deltas (sign test / mean delta
with SD), which cancels scenario difficulty entirely.

Measured 2026-08-18 at game repo main (`d314c5f`), target-aware baseline,
full 1,000-tick episodes, n=8 seeds per scenario — per-seed score SD within
a fixed scenario:

| Scenario (pack: baseline) | mean | SD | range |
|---|---|---|---|
| `wealth-skewed.twin-peaks` | 0.8584 | **0.0088** | 0.8460–0.8698 |
| `capacity.compact-regrow-1` | 0.3333 | **0.0000** | exactly 0.3333 ×8 |
| `tribe-convergence.three-way-mixed` | 0.5696 | **0.0999** | 0.4143–0.6859 |

The spread is the finding: **variance is scenario- and target-dependent by
two orders of magnitude.** Population-capacity scoring was seed-invariant
for the baseline (one observation, not 8 — the agricogla warning applies:
deterministic dynamics + pinned scenario can collapse N to 1); wealth
targets are tight (SD ≈ 0.01); tribe/combat worlds are noisy (SD ≈ 0.10).
Re-measure the SD for the specific scenarios your claim covers before
choosing n — never reuse these numbers as universal constants.

Recipe to re-measure (run from a game-repo checkout):
vary `seed = scenario_index + 80*j`, run `coworld.episode.run_episode` with
your ruleset, collect `results["scores"][0]`, compute SD. Wall time is
~6–70 s per 1,000-tick pool episode (combat/tribe worlds slowest).

Floors that follow: treat |mean paired delta| < 1 SD at n=8 as noise;
for verdicts sweep every scenario the claim covers (all 80 for a "better
overall" claim — roughly an hour of local compute per arm). Commonwealth: the
world is fixed and the constitution is constant, so variance comes only
from the sim seed; 8 seeds gives a stable mean, and any claimed gain
smaller than the seed SD is noise.

Hosted arms remain independent samples (you cannot pin hosted seeds):
paired analysis does not apply there — that is another reason the local
rung is the workhorse.

## Tooling

No tooling yet — build as a lab instrument. The primitive is the game
repo's `coworld.episode.run_episode(config, [ruleset])` (in-process, no
docker; see the eval-design binding for the sweep recipe). First instrument
worth building: a sweep runner that takes two ruleset files and emits the
paired per-scenario delta table.
