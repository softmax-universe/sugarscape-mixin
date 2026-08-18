# First session — sugarscape overlay

The seed's `docs/getting-started.md` runs the first session (its seven
beats stand). This file is the sugarscape **substitution list**: where this
game's shape changes what the arc should do. It never replaces the seed's
document — read both.

## Beat 0 (Calibrate) — three extra questions

After the seed's standard calibration, additionally establish, and record
verbatim in root `user_preferences.md` under `## Sugarscape`:

1. **Sugarscape familiarity** — heard of Epstein & Axtell / agent-based
   models, or brand new? (Sets how much of `docs/game.md` to teach.)
2. **Studio vs terminal** — "There's a visual editor where we can build
   rulesets together in your browser, or we can work purely in
   chat/terminal. Which do you prefer?" (Gates the default-surface rule in
   `skills/ruleset-studio/`.)
3. **Which league first** — teach before asking, one sentence first:
   *"Two ways to play: the ladders draw a random world and target each
   episode and your policy must generate a law to match; the Commonwealth
   is one fixed world where you hand-craft a single constitution scored by
   total citizen wellbeing."* Then: **recommend Commonwealth-in-Studio for
   a first session** (one fixed world, visual editing, instant local
   scoring, 3-entrant field) and let them choose.

Mirror the operational consequences (league focus, default surface) into
this lab's `WORKING_CONTEXT.md`. Never re-ask a recorded answer.

## Beat 2 addendum — stand up the local oracle (do this on install)

`add_game.sh` installs the *knowledge pack* only; the local sweep rung and the
Studio both need a **checkout of the game repo with its venv built**, which no
beat currently does. Do it once, right after install, silently:

```sh
git clone https://github.com/Metta-AI/coworld-sugarscape ~/projects/coworld-sugarscape
cd ~/projects/coworld-sugarscape && uv sync    # repo is unpackaged: run via PYTHONPATH=src
```
Then verify with a single scored Commonwealth episode (the base primitive
everything downstream uses) — `coworld.episode.run_episode(config, [ruleset])`
where `config` is the `commonwealth` variant's `game_config` from
`coworld_manifest.json` with `seed` pinned (it ships `seed: -1`). Read
`score_method`/`scores[0]` and `details[0]` (`survivor_count`, `mean_wellness`).
Set `PYTHONHASHSEED=0`.

**Reality check to set expectations:** a full 1,000-tick Commonwealth episode is
**~4 min** (worse under CPU contention), NOT the "seconds to a minute" the
eval-design binding advertises — the high-fertility population explosion is
expensive. And the local checkout must match the DEPLOYED build or scores are
biased (see MIXIN.md version-match note).
`instruments/cw_sweep.py` in this lab wraps this into a paired multi-seed sweep.

## Beat 5 (First improvement) — the speed-stance question is reshaped

The seed asks whether the user prefers a quick static check or shipping
straight to evaluation. Here the check **is** an evaluation: a full scored
episode costs seconds to a minute locally and runs the real scorer. So don't pose that
fork; record the stance as **"always pre-score locally before upload"**
and say why in one line ("scoring is free here, so nothing ships
unscored").

## Beat 6 (First evaluation) — the ladder is local-first

Replace roster design with the three-tier ladder (`skills/eval-design/`):
local sweep → hosted smoke → league. A good first session closes the loop
with a local score in minutes, then one hosted smoke batch, then — with
the human's explicit go — a league submission. The seed's slow-batch
guidance (parking long evals, streaming harvests) does not apply; batches
drain in minutes.

## The Studio is a first-session beat, not an extra

If the user chose Commonwealth or Studio-preferred: launch the Studio
during beats 4–5 and build the first ruleset together on canvas
(`skills/ruleset-studio/`). The worked examples to open with live in the
game repo: `rulesets/worked-example.json` and the human tutorial
`docs/sugarlang-tutorial.md`.

## The anti-runaway rule

Cheap evaluation cuts both ways. It makes the loop closable in one
session — and it makes it tempting to run twenty sweeps and return with a
finished policy the user never touched. **Cheap evaluation is a reason to
show the user more intermediate results and more forks, not to take more
unsupervised steps.** The user's idea should still be the first upload.

## Commonwealth-specific first-session note

The constitution is the user's voice in a public league. Build it with
them on canvas, and the submit decision record names the constitution's
`ruleset_sha256` they approved (`skills/ruleset-studio/`, consent gate).
The qualifier demands byte-constancy: the policy ships the constitution as
a literal file, never regenerates it.
