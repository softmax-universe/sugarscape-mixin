---
name: sugarscape-eval-design
binding: eval-design
description: >
  Sugarscape binding for the core run-eval skill: the three-tier oracle
  ladder (local sweep, hosted smoke, league), pool mechanics, and pacing.
---

# Eval-design binding — Sugarscape

The core `run-eval` skill carries the question→shape decision table and the
eval ladder. In this game the ladder's rungs are unusual, because the real
scoring function runs locally and solo/commonwealth episodes have no
opponents.

## The three-tier oracle ladder

1. **Local sweep** — the workhorse. In-process
   `coworld.episode.run_episode(config, [ruleset])` from a game-repo
   checkout: no docker, no seats ceremony, full scored 1,000-tick episode
   in ~6–70 s depending on world (combat/tribe worlds slowest; small
   exploration configs are ~1 s). The full 80-scenario pool sweeps in
   roughly an hour; a pack-representative subset in minutes. Scenario is
   pinned via `seed = scenario_index + 80·j`. This rung is
   admissible verdict evidence for solo/commonwealth (MIXIN.md doctrine
   note) because it runs the actual scorer at the pinned ref.
2. **Hosted smoke** — plumbing + version skew. One small XP batch answers:
   does the deployed build score my ruleset the way my pinned checkout
   does, and does my container submit inside the 180 s window? Run it
   before any submit; a local-vs-hosted score divergence is a **version
   skew finding**, not noise — check game release notes before touching
   the ruleset.
3. **League** — the only place ranking, EWMA aggregation, duo opponent
   distribution, and the commonwealth qualifier exist. Enter it to learn
   what "enough" is, not to learn your own score.

## Sensible rosters

Rosters are nearly moot: solo and commonwealth are 1-seat; duo is 2. For
duo questions, hosted XP requests seat you against the field — the
opponent's identity is the variable you cannot control locally. The local
proxy for duo: run the shared world with your ruleset in seat 0 and a
reference ruleset (e.g. the baseline's for the paired target) in seat 1;
label it a proxy — real duo evidence is hosted-only.

## Episode-count floors

From the measured per-seed SD in the ab binding: 8 seeds per scenario
gives a stable per-scenario mean; a full-pool verdict sweep is 80
scenarios × paired arms. Smoke = 1–3 episodes (it answers plumbing, not
score). Do not compute hosted floors from local variance — hosted adds
scenario draw (`seed % 80`, unpinnable) on top of sim seed, so hosted
per-episode scores mix scenario difficulty with everything else; that is
what the local paired rung removes.

## Role/seat pinning

Nothing is pinnable hosted: the platform assigns the seed (hence scenario)
and duo pairing. Locally everything is pinnable — scenario, seed,
opponent-seat ruleset, timesteps, window. Pin freely for mechanism
questions; report pinned exploration runs as exploration, never as ranked
previews.

## Pacing

Episodes are seconds-to-minutes; hosted batches drain in minutes. The
seed's slow-game pacing guidance (don't overlap multi-hour arms, park
long-running batches) **does not apply** and following it here just
manufactures ceremony. The discipline that replaces it: cheap evaluation
is a reason to show the human more intermediate results and more forks —
not to take more unsupervised steps.

## eval_defaults.yaml

Not shipped. The defaults above are the defaults; they live in prose
because the numbers depend on the question (see floors).
