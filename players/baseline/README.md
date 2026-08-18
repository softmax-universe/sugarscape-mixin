# baseline — the starter policy

A clean, editable scaffold at the strength of the game's bundled
certification baseline. The connector (`player.py`) reads one observation,
picks a ruleset from `library/` by the assigned target, submits it, and
exits. **All strategy lives in the library JSON files** — improving this
policy means editing rulesets, not code.

- `library/constitution.json` — the Commonwealth constitution
  (`wellness.max`). Served verbatim, never generated: the qualifier
  demands byte-constancy across episodes.
- The other files cover each target family; `fallback.json` catches
  anything unmapped. Dispatch order and mapping: `TARGET_LIBRARY` in
  `player.py`.

Provenance: dispatch and rulesets vendored from the game repo's
target-aware baseline (`players/baseline/player.py` at coworld-sugarscape
`d314c5f`), verified behaviorally identical across the full target
catalog at vendoring time. It is intentionally simple — beating it is the
first improvement loop.

Build: `tools/build.sh [--tag <image-tag>]` from the lab root (linux/amd64).
Local smoke: run the game repo's `docker compose up` and point this image
at it, or score any library file directly with `run_episode` (see the
eval-design skill).

**Version log rule (repeated at point of use):** every change to this
policy — a library edit counts — gets a `VERSION_LOG.md` row *before*
upload, including the `ruleset_sha256` of what changed. No row, no upload.
