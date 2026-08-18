---
name: sugarscape-diagnosis
binding: diagnosis
description: >
  Sugarscape binding for the core diagnose skill: the generation-shaped
  failure vocabulary and cheapest-first triage.
---

# Diagnosis binding — Sugarscape

The core `diagnose` skill carries the method: signals → 2–4 varied,
mechanistic hypotheses, each pinned to a location. This game's failures are
**generation-shaped, not gameplay-shaped** — the policy fails at producing
the right law, then the law fails at producing the right society.

## Failure vocabulary

| Failure | What happened | Detect from |
|---|---|---|
| **null-ruleset** | Missed the 180 s submission window; seat ran stock behavior | `details[i].submitted == false` |
| **validation-reject** | Ruleset broke budgets (256 nodes / depth 16 / 32,768 bytes) or shape rules; treated as no submission | container logs; locally `parse_ruleset(...).errors` |
| **extinction** | The law killed the society; score 0 | `result.extinct == true` |
| **empty-measurement** | Society lived but the measured variable had no samples (e.g. no trades for a price target) | `details[i].empty_measurement == true` |
| **wrong-bin mass** | Systematic over/undershoot vs the target histogram | measured vs target histograms in `results["histograms"]`; raw W1 direction |
| **pack-blindness** | Ruleset ignores a mechanic the drawn world activated (disease, seasons, combat…) | scores cliffed on one pack suffix in the scenario × score matrix |
| **constitution drift** | Commonwealth submission varied between episodes; qualifier DQ | qualifier round shows `rulesets_identical == false`; diff seat `ruleset_sha256` |
| **degeneracy misfire** | Commonwealth: optimized mean wellness while the score is survivors × wellness (or fumbled a documented degeneracy) | survivors × mean-wellness decomposition vs rivals'; `docs/strategy.md` |

## Triage table

Cheapest first, from results scalars before any replay:

1. `details[i].submitted` false? → null-ruleset / validation-reject; read
   container logs (`coworld episode-logs <ereq> --game`), reproduce the
   generator locally against the same observation.
2. `result.extinct` or `result.population_final` tiny? → extinction path;
   local re-run of the recorded seed, watch the population trajectory.
3. `empty_measurement`? → the variable's activity never happened; check
   which trait gate (trade for prices, fertility for population…) the
   ruleset closed.
4. Score low but society healthy? → wrong-bin mass; put measured vs target
   histograms side by side and name the direction of the miss.
5. Low scores clustered by pack? → pack-blindness; diff the ruleset's
   feature usage against the pack's active mechanics.
6. Commonwealth-specific: qualifier failed → constitution drift; score
   plateau vs rivals → run the survivors × wellness decomposition.

## Instruments

No instruments yet — build into `../../instruments/` as needs recur. The
two named first: the rule-fire trace (see the replay-inspection binding)
and the paired-sweep delta table (see the ab binding). Both build on local
re-runs of recorded seeds — this game's diagnostic superpower.
