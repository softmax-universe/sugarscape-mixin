"""Sugarscape starter policy: dispatch a library ruleset from the assigned target.

The strategy lives entirely in library/*.json — edit those files (or add new
ones and extend TARGET_LIBRARY) without touching the connector below. The
commonwealth branch always returns library/constitution.json verbatim: the
qualifier demands byte-constancy, so never generate that file at runtime.
"""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlencode

from websockets.sync.client import connect

LIBRARY = Path(__file__).resolve().parent / "library"

# (target id, measured variable) -> library file. Matched top to bottom:
# first by exact target id, then by variable, then the fallback.
TARGET_LIBRARY: list[tuple[str | None, str | None, str]] = [
    ("wellness.max", None, "constitution.json"),  # Commonwealth: the fixed constitution
    ("wealth.egalitarian", None, "wealth-egalitarian.json"),
    ("tribe.convergence", None, "tribe-convergence.json"),
    ("disease.endemic", None, "disease-endemic.json"),
    (None, "majority_tribe_share", "tribe-diversity.json"),
    (None, "sick_fraction", "disease-sparse.json"),
    (None, "population", "survivorship.json"),
    (None, "age_at_death", "survivorship.json"),
    (None, "mean_trade_price", "trade-price.json"),
]
FALLBACK = "fallback.json"


def choose_ruleset(target: Mapping[str, object]) -> dict[str, object]:
    """Load the library ruleset for the assigned target."""

    target_id = str(target.get("id", ""))
    variable = str(target.get("variable", ""))
    for match_id, match_variable, filename in TARGET_LIBRARY:
        if match_id is not None and target_id == match_id:
            return _load(filename)
        if match_variable is not None and variable == match_variable:
            return _load(filename)
    return _load(FALLBACK)


def _load(filename: str) -> dict[str, object]:
    return json.loads((LIBRARY / filename).read_text(encoding="utf-8"))


def resolve_websocket_url(
    args: argparse.Namespace, environment: Mapping[str, str]
) -> str:
    """Prefer the platform URL and construct a local-development fallback."""

    platform_url = environment.get("COWORLD_PLAYER_WS_URL")
    if platform_url:
        return platform_url
    if args.slot is None or args.token is None:
        raise ValueError(
            "COWORLD_PLAYER_WS_URL or both --slot and --token are required"
        )
    query = urlencode({"slot": args.slot, "token": args.token})
    return f"ws://{args.host}:{args.port}/player?{query}"


def run(url: str) -> None:
    """Receive one observation, submit one valid action, and exit after ack."""

    with connect(url, max_size=64 * 1024, proxy=None) as websocket:
        observation = json.loads(websocket.recv())
        if observation.get("type") != "observation":
            raise RuntimeError("game didn't send a Sugarscape observation")
        ruleset = choose_ruleset(observation["target"])
        websocket.send(
            json.dumps({"type": "action", "ruleset": ruleset}, separators=(",", ":"))
        )
        acknowledgement = json.loads(websocket.recv())
        if (
            acknowledgement.get("type") != "ack"
            or acknowledgement.get("valid") is not True
        ):
            raise RuntimeError(f"game rejected starter ruleset: {acknowledgement}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sugarscape starter policy")
    parser.add_argument("--host", default="game")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--slot", type=int)
    parser.add_argument("--token")
    args = parser.parse_args(argv)
    run(resolve_websocket_url(args, os.environ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
