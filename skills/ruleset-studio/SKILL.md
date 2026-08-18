---
name: sugarscape-ruleset-studio
description: >
  Launch and drive the Ruleset Studio — the visual SugarLang editor with an
  agent chat bridge. The default surface for working on rulesets with the
  human; commonwealth hand-crafting especially.
---

# Ruleset Studio — Sugarscape

The Studio is a local browser app: SugarLang movement rules as Blockly
stacks, trait sliders, live validation by the game's real Python validator,
budget meters, atomic save into the game repo's `rulesets/`, and a chat
pane bridged to you. The human edits the canvas; you both see the same
compiled ruleset.

## When to launch it

**Default surface rule** (mirrors the seed's dashboard rule): for any
session where the human is shaping or reviewing a ruleset — commonwealth
constitution work especially — launch the Studio and hand them the URL
unprompted. Gate on the recorded preference: if `user_preferences.md` §
Sugarscape records terminal-preferred, offer once, don't insist. If no
preference is recorded yet, this is one of the first-session interview
questions (lab AGENTS.md, Understand row).

## Launch runbook (handle silently — never narrate these mechanics)

Prerequisites: a checkout of https://github.com/Metta-AI/coworld-sugarscape
with its venv built (`uv sync`), Node.js, and a metta checkout at
`~/coding/metta` (or pass `--metta-root`) for the chat-bridge server.

```sh
cd <coworld-sugarscape checkout>
.venv/bin/python -m tools.ruleset_studio
```

The launcher picks free ports, starts the validation API and the link
server, opens the human's browser, and **prints a `link-bridge.mjs watch`
command**. Run that printed command to receive the next chat message from
the canvas; **it delivers exactly one message — re-run it after every
reply you send.** Replies may include `{set: {ruleset: ..., note: ...}}`
to propose a full-ruleset replacement; the Studio validates it with the
Python API and applies it as one undoable edit, toasting "Changed by
agent."

Operational rules, all silent: re-arm the watch after each reply; if chat
shows "Not connected", run the printed watch command again without
restarting; the editor works fully without the bridge (chat is the only
degraded feature). To the human, speak only about the ruleset and the
world — never about bridges, watches, ports, or re-arming.

## The consent gate

The Studio computes the canonical `ruleset_sha256` of what's on canvas —
the same hash the platform records per seat and the commonwealth qualifier
compares. **Never submit a ruleset (commonwealth constitution especially)
whose canvas state the human hasn't seen: the submit decision record names
the sha the human approved.** If the canvas changed after their last look,
show it again before submitting. This is the structural version of "the
constitution is the user's voice in a public league."

## Test runs

If the game checkout's Studio has the Play feature (`/api/run`), the human
can score the canvas ruleset in place — ranked preview (real variant
config, scenario from `seed % 80`) or exploration (pinned scenario,
shortened timesteps, labeled counterfactual) — with the episode rendered
live in the viewer. If the checkout predates the Play feature, score the
saved ruleset file with a local `run_episode` call instead (recipe in the
eval-design binding) and report the score in chat.
