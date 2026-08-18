---
name: sugarscape-survey
binding: survey
description: >
  Sugarscape binding for the core survey skill: the scenario × score
  matrix and the flags that make an episode worth a closer look.
---

# Survey binding — Sugarscape

The core `survey` skill carries the process: aggregate, decompose, flag,
narrate — finding-first, with agent-written reasons. This binding supplies
what those words mean here.

## The overview table

A batch overview is a **scenario × score matrix**. One row per episode:

| Column | Source |
|---|---|
| scenario id + index | `results["scenario_index"]`, pool id (family.world.pack) |
| score | `results["scores"][seat]` |
| raw W1 (distribution) or survivors × mean wellness (commonwealth) | per-seat `details` |
| extinct / final population | `result.extinct`, `result.population_final` |
| submitted / empty measurement | `details[i].submitted`, `details[i].empty_measurement` |

Sort by score within mechanic pack. A competitor's first glance: which
packs does this policy survive, and where are the zeros.

## Structure worth surfacing

- **Pack cliffs**: scores clustered low on one mechanic pack — the single
  most common structure in this game.
- **Family competence**: mean score per target family shows whether the
  generator reasons about targets or memorized easy worlds.
- **Duo asymmetry**: in duo episodes both seats share one world; compare
  seat scores and final-world stats (`result.gini_final`,
  `result.population_final`) to see whether the other seat's law reshaped
  the world against you.

## What makes an episode interesting

Cheap flags, from results scalars alone:

- `result.extinct == true` — the law killed the society.
- `details[i].empty_measurement == true` without extinction — measured
  variable produced no samples (e.g. no trades for `mean_trade_price`).
- Score ≥ pack mean + 2 SD or ≤ pack mean − 2 SD — outlier worth a replay.
- `details[i].submitted == false` — generation-side failure, check logs.
- Commonwealth: a run whose survivor count or mean wellness moved sharply
  vs the standing constitution — it found (or fumbled) one of the
  documented degeneracies (`docs/strategy.md`).

## Tooling

No tooling yet — build as a lab instrument (the natural shape: a script
that ingests a directory of `results.json` files or an XP request id and
prints the matrix above).
