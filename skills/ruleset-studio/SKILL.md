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

## Remote / headless-agent serving (added 2026-08-18, cubi-bismarck)

The default runbook assumes the human and the agent share a machine and the
launcher opens a local browser. For a **headless agent driving the loop for a
REMOTE human** (a cubi; any cloud-hosted session), that assumption breaks. Two
things to know:

1. **No metta checkout needed for the link-server.** `link-server.mjs` is a
   single ~34 KB zero-dependency Node file. Fetch it (and `link-bridge.mjs`,
   which `discover()` still requires by path) directly instead of cloning metta
   (~1.5 GB):
   ```sh
   for f in link-server.mjs link-bridge.mjs; do
     gh api repos/Metta-AI/metta/contents/agent-plugins/ux/skills/ux.surface/app/$f \
       --jq .content | base64 -d > "$f"
   done
   ```
   Point the launcher at them: put both under a dir `M/agent-plugins/ux/skills/ux.surface/app/`
   and pass `--metta-root M` (or `COWORLD_STUDIO_LINK_SERVER=<path>/link-server.mjs`
   plus that `--metta-root` for the bridge).

2. **The Studio is localhost-only by design** — three loopback servers
   (link 4322, api 4323, run 4324), a CSP `connect-src` allowing only
   localhost/127.0.0.1, and API CORS accepting only `Origin: http://localhost:4322`.
   apps-proxy, `tailscale serve`, and cubiauth all break it (wrong served origin →
   CSP/CORS 403; apps-proxy is also single-port). **The only zero-code-change remote
   path is an SSH local-forward** from the human's machine, which preserves the
   localhost illusion:
   ```sh
   ssh -N -L 4322:127.0.0.1:4322 -L 4323:127.0.0.1:4323 -L 4324:127.0.0.1:4324 <user>@<host>
   # then open: http://localhost:4322/?api=http://127.0.0.1:4323&run=http://localhost:4324
   ```
   Launch with `--no-open` and raise the auto-shutdown graces
   (`LINK_GRACE_MS`, `LINK_FIRST_CONNECT_GRACE_MS`) so the server survives while the
   human sets up the tunnel. The human needs SSH access to the host (operator-side;
   the agent can't provision it). A hosted tailnet front (apps-proxy + cubiauth) is a
   *product change*, not a serving trick — it needs same-origin api/run, widened
   CSP, CORS accepting the served origin, a single multiplexing reverse proxy, and
   raised link-server graces.

## Test runs

If the game checkout's Studio has the Play feature (`/api/run`), the human
can score the canvas ruleset in place — ranked preview (real variant
config, scenario from `seed % 80`) or exploration (pinned scenario,
shortened timesteps, labeled counterfactual) — with the episode rendered
live in the viewer. If the checkout predates the Play feature, score the
saved ruleset file with a local `run_episode` call instead (recipe in the
eval-design binding) and report the score in chat.
