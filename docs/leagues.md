# The three leagues

Two competition styles share one game. **The policy must branch on the
target kind it receives** — this is the single most important structural
fact in the lab:

- `kind == "distribution"` → generate a ruleset conditioned on this world
  and target (targeted-generation leagues).
- `kind == "maximize"` → return the fixed constitution, byte-identical
  every time (Commonwealth).

## Targeted generation

| | Solo | Duos |
|---|---|---|
| League id | `league_620a74a7-eb1f-4386-b386-0e7246be4eb6` | `league_d5b48dfe-5e08-499f-80f1-63f14720c50c` |
| Seats | 1 | 2, shared world, distinct global targets, independent scores |
| World | 1 of 80 pool scenarios (`seed % 80`) | same pool; target pairs per scenario, order alternating |
| Score | `w1-hyperbolic/1` ∈ [0,1] distribution match | same |
| Ranking | round scores → EWMA ladder | mean round score → 3 h EWMA |

What ranks is breadth: the pool spans 6 target families × mechanic packs,
so a generator that only handles easy worlds caps out fast. Extinction and
empty measurements score 0.

Duos is the one place another policy exists inside your episode: both
targets are global, so the other seat's law bends the same measured
outcome you're scored on. Local duo runs (your ruleset vs a reference in
seat 1) are proxies only.

## Commonwealth (handcrafted)

- League id: `league_dac00450-027a-45e6-9f6b-c9bda7ddd61d`.
- Same canonical world every episode; target `wellness.max`
  (`kind: maximize`); no scenario pool, no target histogram.
- Score `wellness-sum/1`: over agents alive at the final tick, sum of each
  survivor's mean normalized happiness `(h+5)/10` across the 50-tick
  window. **Decomposes as survivors × mean window wellness; population is
  the dominant lever.** Maximize, no ceiling.
- **Qualifier:** 3 two-seat self-play episodes; each must report
  `rulesets_identical == true` (canonical `ruleset_sha256` per seat,
  every seat submitted). The contract is **constancy, not mere
  determinism** — an LLM generating "the same" constitution at submission
  time will drift and die at the gate. Ship a literal file.
- The constitution is an artifact the human should co-own: craft it in the
  Ruleset Studio (see `skills/ruleset-studio/`), and never submit a
  constitution hash the human hasn't seen.

## Practical consequences

- One policy container serves all three leagues via the target-kind
  branch; `players/baseline/` implements it.
- Local paired sweeps are verdict evidence for solo/commonwealth score
  claims at the pinned ref, with one hosted confirmation before any
  submit (MIXIN.md doctrine note; details in `skills/ab/` and
  `skills/eval-design/`).
- `players_per_user: 1` — one policy slot per league; submission is the
  gate, upload is routine.
