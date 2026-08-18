# Observatory interaction (Sugarscape specifics)

The generic platform surface — auth, upload/submit semantics, API base
URL, cross-game quirks — is the seed's `docs/platform.md`. The complete
CLI/API reference is https://github.com/Metta-AI/coworld — **read its root
`COOKBOOK.md` first** for any task below; it gives both the `coworld` CLI
form and the raw REST form. This file adds only what is sugarscape-shaped.

## Task map

| Task | Command / route |
|---|---|
| Auth | `softmax login` (`--no-browser` headless), `softmax status` |
| Download the coworld | `coworld download cow_170e4f67-fc56-4307-aca9-12b0c650f4b0` |
| Upload a policy (routine, ungated) | `coworld upload-policy <image> --name <policy>` — image must be linux/amd64; multi-role images need `--run <argv>` (omitting it is the classic silent worst-case-score failure) |
| Submit to a league (THE gate) | `coworld submit <policy>[:vN] --league <id>` — league ids in `docs/leagues.md`. Commonwealth submissions then face the qualifier |
| Check membership/qualifier | `coworld submissions --mine`, `coworld memberships --mine` — commonwealth runs `qualifying → competing`; a qualifier DQ means constitution drift (see diagnosis) |
| Hosted experience (XP) request | `coworld xp-request create body.json`; body is strict (`additionalProperties: false` — a stray key 4xxs). Inspect: `xp-request list --mine`, `xp-request get xreq_… --json`, `xp-request episodes xreq_…`. Cancel: REST/UI only |
| Episode rows + scores | `coworld episodes ereq_… --json` — sugarscape rows carry `scores`, `scenario_index`, `rulesets_identical`, `result.extinct`, per-seat details |
| Game logs | `coworld episode-logs ereq_… --game [--download-dir logs/]` |
| Player (per-agent) logs | no CLI — raw route `GET /v2/episode-requests/{ereq}/{policy_version_id}/policy-logs/{agent_idx}`. Sugarscape players exit after submitting, so these logs cover generation only |
| Replays | episode row `replay_url`; `coworld replay-open ereq_…`; bulk `coworld replays --round round_… --mine --download-dir replays/` |
| Standings | `coworld results <league-id>` → division id → `coworld results <division-id>` |

## Sugarscape-shaped facts

- **Rivals' logs and artifacts 403.** Only your own policies' telemetry is
  readable; rival decode comes from replays and standings.
- Hosted episodes assign the seed — you cannot pin a scenario hosted.
  Anything scenario-pinned is local-only (see `skills/eval-design/`).
- A local-vs-hosted score divergence on the same recorded seed is version
  skew (deployed build vs your pinned checkout) — check game releases
  before touching the ruleset.
- Batches drain in minutes; poll with `xp-request get`, don't park.
- Uploading is routine and free; **league submission is the only
  irreversible act and gets the human gate** — for commonwealth, the
  decision record names the constitution's `ruleset_sha256` the human
  approved.
