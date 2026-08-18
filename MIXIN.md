# MIXIN — Sugarscape

The manifest for this lab: what game it binds, where it came from, and —
the load-bearing part — **every skill this mixin provides**, so core skills
resolve bindings here instead of guessing, gaps are machine-checkable, and
extra capabilities are discoverable.

## Identity

| | |
|---|---|
| **Game** | Sugarscape (v3) |
| **Coworld** | `coworld-sugarscape` v3 — `cow_049e7dc0-f4b5-49f8-81df-59ea73493b6a`; manifest at the repo root of https://github.com/Metta-AI/coworld-sugarscape (public) |
| **League(s)** | Solo (targeted generation): `league_620a74a7-eb1f-4386-b386-0e7246be4eb6` · Duos (targeted generation): `league_d5b48dfe-5e08-499f-80f1-63f14720c50c` · Commonwealth (handcrafted constitution): `league_dac00450-027a-45e6-9f6b-c9bda7ddd61d` |
| **Game source of truth** | https://github.com/Metta-AI/coworld-sugarscape — public. `docs/RULES.md` is **test-enforced against the implementation** (`tests/test_rules_documentation.py`), so it outranks memory and this lab's own docs. Also `docs/TARGETS.md`, `docs/SCENARIOS.md`, `docs/PROTOCOL.md`. Never answer mechanics questions from memory |

## Provenance

*(stamped by `tools/add_game.sh` on install; update on `--update`)*

| | |
|---|---|
| **Upstream mixin** | {{MIXIN_REPO_URL}} |
| **Commit** | {{COMMIT}} |
| **Installed** | {{DATE}} |

This lab is a vendored copy and is expected to drift from upstream. That's
fine — see SEED.md's divergence stance.

## Doctrine note: the local oracle

Sugarscape inverts the assumption behind "the live field is the only
oracle": solo and commonwealth episodes seat one policy with no opponents,
and the actual scoring function runs locally (in-process `run_episode()`,
~5 s per 1,000-tick episode, reproducible on the pinned interpreter). By
deliberate decision (James, 2026-08-18): **local paired sweeps at the
pinned ref are admissible verdict evidence for solo/commonwealth score
claims, with one hosted confirmation required before any league submit.**
Live-only remains: version skew against the deployed build, duo opponents,
league aggregation, and the commonwealth qualifier. Details in `skills/ab/`
and `skills/eval-design/`.

## Skill manifest

Core skills resolve their game bindings through this table. A required binding
that is missing or stubbed is a **gap**: the core skill announces it, proceeds
on its generic method, and warns the human that results are weaker.

### Required bindings

**What counts as "filled":** a binding is filled when its knowledge sections
are real (metrics, decompositions, taint, floors…) even if tooling doesn't
exist yet — in that case its Tooling section says so explicitly ("no tooling
yet — build as a lab instrument") and that is *not* a gap. A **gap** is a
binding that is missing entirely or still template boilerplate; core skills
announce gaps and proceed on their generic method with the human warned.

| Binding | Path | What it provides | Use when |
|---|---|---|---|
| `ab` | `skills/ab/` | Per-league metrics (`w1-hyperbolic/1`, `wellness-sum/1` decomposed), per-scenario/pack/family decompositions, taint definition, paired local comparisons, measured N floors | Any comparison between versions or policies (core: `ab-compare`) |
| `survey` | `skills/survey/` | The scenario × score matrix; which flags make an episode interesting | Reading any batch of episodes (core: `survey`) |
| `replay-inspection` | `skills/replay-inspection/` | Replay as the consequence trace of one submitted ruleset; rule attribution; the tick clock; reproducibility contract | Extracting truth from episodes (core: `replay-inspection`) |
| `eval-design` | `skills/eval-design/` | The three-tier oracle ladder (local sweep → hosted smoke → league); pool-selection mechanics; pacing | Designing any eval, local or hosted (core: `run-eval`) |
| `diagnosis` | `skills/diagnosis/` | The generation-shaped failure vocabulary and cheapest-first triage | Turning signals into hypotheses (core: `diagnose`) |

### Meta-recon support

| Provides | Path | Notes |
|---|---|---|
| Strategy and meta docs | `docs/strategy.md` | Per-league strategy surface, incl. the commonwealth degeneracy catalog |
| League structure | `docs/leagues.md` | Three leagues, scoring, the target-kind fork |

### Additional skills

*(everything else this mixin ships — game-specific capabilities beyond the
required set. List them all: an unlisted skill is an undiscoverable one.)*

| Skill | Path | What it does | Use when |
|---|---|---|---|
| `ruleset-studio` | `skills/ruleset-studio/` | Launch and drive the Ruleset Studio — the visual SugarLang editor with an agent chat bridge; the default surface for showing the human rulesets | Any session where the human is shaping or reviewing a ruleset; commonwealth hand-crafting especially |

## What else this mixin provides

| Element | Path | Notes |
|---|---|---|
| Game docs | `docs/` | `game.md`, `leagues.md`, `observatory.md`, `strategy.md`, `first-session.md` — enough that a newcomer understands the game without leaving the repo, including how it's won |
| First-session overlay | `docs/first-session.md` | Substitutions to the seed's getting-started arc for this game (local-first evaluation, the Studio, the league fork, extra interview questions) |
| Reference policy | `players/baseline/` | Buildable; the starting point `seed-a-policy` improves on. Has a real `VERSION_LOG.md`; `players/_VERSION_LOG_template.md` kept in place for future policies |
| Build tooling | `tools/build.sh` | The build entry point `build-upload` invokes. Convention: `build.sh [--ref <game-ref>] [--tag <image-tag>]` — builds the policy image for linux/amd64 and prints the image tag; pinned game refs live inside with their rationale |

No `eval_defaults.yaml` is shipped; evaluation defaults live in prose in
`skills/eval-design/SKILL.md`.
