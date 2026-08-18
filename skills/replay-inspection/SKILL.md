---
name: sugarscape-replay-inspection
binding: replay-inspection
description: >
  Sugarscape binding for the core replay-inspection skill: the replay as
  the consequence trace of one submitted law, rule attribution, and the
  tick clock.
---

# Replay-inspection binding — Sugarscape

The core skill's frame is "replay = ground truth, policy artifacts = point
of view, diagnosis lives in the gap." Reframed for a game where the policy
makes exactly one decision: **the replay is the consequence trace of the
submitted ruleset; the point of view is the observation the policy
conditioned on plus the ruleset it emitted; the gap is between the
author's model of the world and the world.**

## Replays

- Format: the game's own binary replay (delta-encoded frames), rendered by
  the repo's static viewer (`replay-viewer/`, dependency-free bundle).
  Hosted episodes expose `replay_url` on the episode row; `coworld
  replay-open <ereq>` opens one, `coworld replays --round <round> --mine
  --download-dir replays/` fetches in bulk.
- The viewer measures **every catalog target every tick** regardless of the
  episode's assigned target — any target can be asked of any run. Use this
  to see what your society *would* have scored against other targets.
- Version coupling: replays reproduce under the pinned interpreter and
  `PYTHONHASHSEED=0`. A recorded seed + config + rulesets regenerates the
  episode exactly via local `run_episode` — the strongest expansion tool
  this game has: any hosted moment can be re-run locally with full
  introspection.

## Policy artifacts

There is no per-tick decision trace — the policy's entire output is one
ruleset. The artifacts that matter:

- The submitted ruleset (per-seat `details[i]`, plus `ruleset_sha256`).
- The observation it conditioned on (config + target), from the episode's
  results/replay header.
- Container logs (`coworld episode-logs <ereq> --game`) for
  generation-side failures.
- **The shared clock is the tick.** Results scalars are end-state; the
  replay carries the per-tick trajectory that explains them.

## What to look at

- **Rule attribution — the central question.** "Capability exists" ≠
  "capability fired": a movement rule that never matches is dead law.
  Watch whether behavior consistent with each `if` guard actually occurs,
  and when (early survival phase vs late equilibrium).
- Population trajectory first: most bad scores are demographic (crash,
  boom-bust, slow starvation) before they are distributional.
- The measurement window (final ticks): the score only sees the end; a
  society that matched the target at tick 500 and drifted by 1,000 scored
  the drift.
- Duo: watch the other seat's visible strategy — combat pressure, resource
  hoarding, population flooding — and how the shared world bent.

## Tooling

No tooling yet — build as a lab instrument. The first one worth building
is a **rule-fire trace**: re-run a recorded episode locally with a wrapped
evaluator counting which movement rules supplied each candidate's score
per tick. (Local re-run makes this possible without any game changes.)
