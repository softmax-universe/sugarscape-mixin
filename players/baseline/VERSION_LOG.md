# Version log — baseline

Maps every uploaded version of this policy to the one change it carries.
**The row is mandatory before anything else happens after an upload** —
an unlogged version is a hole in the campaign's memory. Honest caveats
("NOT proven better — the A/B was contaminated") are valuable entries.

Validation states: `unvalidated` → `validated` / `refuted` (by a recorded
experiment) → `submitted` (with the decision record appended below the row).

For this game, "the one change" is usually a ruleset diff: record the
canonical `ruleset_sha256` of the changed library file in the row.

| Version | Policy version id | Uploaded (UTC) | The one change (and its mechanism) | Runtime config | Validation | Notes |
|---|---|---|---|---|---|---|
| v0 | — (no uploads yet) | 2026-08-18 | Vendored upstream reference: dispatch + library exported from coworld-sugarscape `d314c5f` `players/baseline/player.py`, verified behaviorally identical across the full target catalog; re-verified unchanged at `a307912` (2026-08-18, post studio-play/onboarding merges). Constitution `ruleset_sha256` `f13b0a218f455a9d06fe379d635043c1a5194d905e1dec1ea32f4a2efc671a37` | Dockerfile in this dir (linux/amd64, `PYTHONHASHSEED=0`) | unvalidated | Certification-baseline strength by design; the starting point, not a contender |

## Submission decision records

Appended by `submit` when a version enters a league — the evidence that
justified it, the human's recorded go-ahead, and the rollback plan. For a
Commonwealth submission the record must name the constitution
`ruleset_sha256` the human approved on canvas.
