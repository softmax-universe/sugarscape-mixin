#!/usr/bin/env python3
"""Commonwealth paired sweep runner (lab instrument).

Runs one or more constitution rulesets ("arms") across a fixed set of sim
seeds on the canonical Commonwealth world, scoring each with the real
`wellness-sum/1` scorer via in-process `run_episode`. Commonwealth is a fixed
world with a constant constitution, so the ONLY source of variance is the sim
seed — this instrument measures the per-seed mean/SD so a claimed gain can be
checked against the noise floor (see skills/ab/), and emits paired per-seed
deltas vs the first arm.

Usage (must run with the game repo's venv so `coworld` imports):

    PYTHONHASHSEED=0 ~/projects/coworld-sugarscape/.venv/bin/python \
        cw_sweep.py --arm baseline=path/to/constitution.json \
                    --arm v1=path/to/variant.json \
                    --seeds 1,2,3,4,5,6 [--timesteps 1000] \
                    --out /tmp/cw_sweep.jsonl

Each completed episode is appended to --out as one JSON line immediately, so
progress is inspectable while it runs (episodes are ~4 min each). A summary
table prints at the end.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from statistics import mean, pstdev

GAME_ROOT = Path(os.environ.get("COWORLD_SUGARSCAPE_ROOT", os.path.expanduser("~/projects/coworld-sugarscape")))
sys.path.insert(0, str(GAME_ROOT / "src"))


def _load_commonwealth_config() -> dict:
    manifest = json.loads((GAME_ROOT / "coworld_manifest.json").read_text())
    variant = next(v for v in manifest["variants"] if v["id"] == "commonwealth")
    return dict(variant["game_config"])


def _run_one(arm: str, ruleset: dict, seed: int, timesteps: int | None) -> dict:
    """Worker: run one Commonwealth episode, return the scored decomposition."""
    from coworld.episode import run_episode  # imported in-worker after sys.path insert

    config = _load_commonwealth_config()
    config["seed"] = seed
    if timesteps is not None:
        config["timesteps"] = timesteps
    t0 = time.perf_counter()
    results, _replay, _timings = run_episode(config, [ruleset], emit_timing_logs=False)
    detail = results["details"][0]
    return {
        "arm": arm,
        "seed": seed,
        "score": results["scores"][0],
        "survivors": detail.get("survivor_count"),
        "mean_wellness": detail.get("mean_wellness"),
        "score_method": results.get("score_method"),
        "secs": round(time.perf_counter() - t0, 1),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Commonwealth paired sweep")
    p.add_argument("--arm", action="append", required=True,
                   help="label=path/to/ruleset.json (repeatable; first arm is the baseline for deltas)")
    p.add_argument("--seeds", required=True, help="comma-separated integers")
    p.add_argument("--timesteps", type=int, default=None, help="override (default: variant's 1000; use small for a plumbing smoke)")
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--out", default="/tmp/cw_sweep.jsonl")
    args = p.parse_args(argv)

    arms: dict[str, dict] = {}
    order: list[str] = []
    for spec in args.arm:
        label, _, path = spec.partition("=")
        arms[label] = json.loads(Path(path).read_text())
        order.append(label)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    jobs = [(label, arms[label], seed, args.timesteps) for label in order for seed in seeds]
    out = Path(args.out)
    out.write_text("")  # truncate
    print(f"[cw_sweep] {len(jobs)} episodes ({len(order)} arms x {len(seeds)} seeds), "
          f"{args.workers} workers, timesteps={args.timesteps or 1000} -> {out}", flush=True)

    rows: list[dict] = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_run_one, *job): job for job in jobs}
        for fut in as_completed(futs):
            row = fut.result()
            rows.append(row)
            with out.open("a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(f"[done] {row['arm']} seed={row['seed']} score={row['score']:.2f} "
                  f"surv={row['survivors']} mw={row['mean_wellness']:.4f} ({row['secs']}s)", flush=True)

    # --- summary ---
    print("\n=== per-arm summary ===", flush=True)
    per_arm_scores: dict[str, dict[int, float]] = {}
    for label in order:
        arm_rows = [r for r in rows if r["arm"] == label]
        scores = [r["score"] for r in arm_rows]
        per_arm_scores[label] = {r["seed"]: r["score"] for r in arm_rows}
        survs = [r["survivors"] for r in arm_rows if r["survivors"] is not None]
        mws = [r["mean_wellness"] for r in arm_rows if r["mean_wellness"] is not None]
        if scores:
            print(f"{label:14s} score mean={mean(scores):.2f} sd={pstdev(scores):.2f} "
                  f"n={len(scores)} | survivors~{mean(survs):.0f} mean_wellness~{mean(mws):.4f}", flush=True)

    base = order[0]
    for label in order[1:]:
        deltas = [per_arm_scores[label][s] - per_arm_scores[base][s]
                  for s in seeds if s in per_arm_scores[label] and s in per_arm_scores[base]]
        if deltas:
            md = mean(deltas)
            sd = pstdev(deltas) if len(deltas) > 1 else 0.0
            wins = sum(1 for d in deltas if d > 0)
            print(f"\n[paired {label} - {base}] mean_delta={md:+.2f} sd={sd:.2f} "
                  f"n={len(deltas)} wins={wins}/{len(deltas)}  "
                  f"({'signal' if abs(md) > sd else 'within noise (|delta|<1sd)'})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
