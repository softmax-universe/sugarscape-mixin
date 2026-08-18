# AGENTS — Sugarscape lab binding

Loaded whenever you work in this lab, on top of the root AGENTS.md. This file
binds the optimizer's loop to this game: how it's scored, what its structures
mean, and how each loop step specializes here.

## The game in one paragraph

Sugarscape is a one-shot lawmaking game, not real-time control. Each episode
the player connects, reads one observation (world config + its assigned
target), submits **one declarative SugarLang ruleset** (four trait overrides
+ one movement decision list, strict budgets: 256 expression nodes, depth
16, 32,768 bytes), and exits. The world then runs 1,000 ticks with no player
I/O. Score is a pure function of ruleset × world × seed. The submission
window is 180 s; missing it means the null ruleset and `submitted:false`.

## Scoring and what actually ranks

Three leagues, two scoring regimes. **The policy must branch on the target
it receives: `kind == "maximize"` → return the fixed constitution;
`kind == "distribution"` → generate a ruleset for this world + target.**

| League | Episode score | What ranks |
|---|---|---|
| Solo `league_620a74a7-eb1f-4386-b386-0e7246be4eb6` | `w1-hyperbolic/1`: 0–1 distribution match of measured variable vs assigned target histogram | Round scores → EWMA ladder |
| Duos `league_d5b48dfe-5e08-499f-80f1-63f14720c50c` | Same, but two seats share one world with different global targets; independent scores; the other seat's ruleset reshapes your measured outcome | Mean round score → 3 h EWMA |
| Commonwealth `league_dac00450-027a-45e6-9f6b-c9bda7ddd61d` | `wellness-sum/1`: sum over final-tick survivors of mean normalized happiness `(h+5)/10` over the 50-tick window. Maximize, no ceiling | Fixed canonical world; the constitution itself ranks |

Decompose the commonwealth objective: score = survivor count × mean window
wellness. Population is the dominant lever.

Extinction or an empty measurement scores 0 in distribution leagues. Solo
and commonwealth have no opponents in the episode; the field only sets what
score is *enough*.

## Structures and semantics

- Targets: `distribution` (histogram + support + bins) or `maximize`
  (commonwealth's `wellness.max`). Episodes never mix kinds.
- Solo/duo worlds come from a deterministic pool of 80 scenarios (12 base
  worlds × mechanic packs: spice, market, combat, disease, pollution,
  seasons, reproduction, everything). Selection is `scenario_pool[seed % 80]`;
  the player never sees the seed or pool index at episode time — only the
  resolved config. Duo pairs targets per scenario with alternating order.
- Habitual mistake: treating this as a game you can steer mid-episode. All
  leverage is in the one submitted ruleset; the observation (config +
  target) is everything you get to condition on.
- SugarLang can only re-rank the engine's own candidate cells and override
  four traits. It cannot add candidates, mutate the world, or use randomness.

## Platform specifics for this game

- **Commonwealth qualifier:** 3 two-seat self-play episodes; every one must
  report `rulesets_identical == true` (canonical `ruleset_sha256` per seat).
  The contract is **constancy, not mere determinism**: any generation-time
  variation — an LLM call at submission time included — passes upload and
  dies at the gate.
- `players_per_user: 1`. Images are linux/amd64 only (hard-checked).
- Episodes are seconds-to-a-minute locally, minutes hosted; batches drain
  fast. Do not import pacing habits from slow games.
- Reproducibility: pinned interpreter + `PYTHONHASHSEED=0`; a recorded seed
  + config + rulesets reproduces an episode exactly.
- `coworld` CLI reference: https://github.com/Metta-AI/coworld — read its
  root `COOKBOOK.md` first for every CLI/API task (upload, submit, XP
  requests, episodes, logs, replays). Game-specific API notes live in
  `docs/observatory.md`.

## Mechanics ground truth

The source of truth for game mechanics is
**https://github.com/Metta-AI/coworld-sugarscape** (see MIXIN.md).
`docs/RULES.md` there is test-enforced against the implementation and
outranks everything, including this lab's docs. Verify mechanics claims
against it — never from memory or guesses. Cache verified facts here with a
pointer to where they were verified:

- Submission window 180 s, closes early when all seats submit; miss ⇒ null
  ruleset, `submitted:false` (game repo `docs/PROTOCOL.md`).
- Budgets 256 nodes / depth 16 / 32,768 bytes; totals semantics (÷0 → 0.0,
  pow clamped, NaN/inf normalized) (game repo `docs/RULES.md`).
- Wellness `(h+5)/10`, final-tick-survivor filter, 50-tick window (game
  repo `docs/TARGETS.md`, `docs/designs/2026-08-18-commonwealth-league.md`).

## How the loop specializes here

| Loop step | In this game |
|---|---|
| Understand | First session: extend the calibration interview with (a) sugarscape familiarity, (b) Studio vs terminal preference, (c) commonwealth-first vs targeted-generation-first — teach the two-league split in one sentence *before* asking (c); recommend commonwealth-in-Studio for a first session. Record answers verbatim in root `user_preferences.md` under `## Sugarscape`; mirror consequences into this lab's WORKING_CONTEXT.md; never re-ask. Strategy docs: `docs/leagues.md`, `docs/strategy.md`; arc overlay: `docs/first-session.md` |
| Evaluate | The three-tier oracle ladder in the eval-design binding: local 80-scenario sweep (minutes) → hosted smoke → league. Rosters are near-moot (1–2 seats) |
| Read | Decompositions in the ab binding: per-scenario, per-mechanic-pack, per-target-family, per-league. A pooled score hides pack-shaped cliffs |
| Hypothesize | Failure vocabulary in the diagnosis binding: null-ruleset, validation-reject, extinction, empty-measurement, wrong-bin mass, pack-blindness, constitution drift, degeneracy misfire |
| Build | `tools/build.sh [--ref] [--tag]` (pinned game ref inside). The architecture question is "how does the generator produce a valid ruleset inside the 180 s window" — scripted library first; if an LLM generates at submission time, it needs a scripted fallback, and for commonwealth the answer is always the fixed constitution file. Always pre-score locally before upload — it's free |
