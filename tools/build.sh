#!/usr/bin/env bash
# Build the baseline policy image for linux/amd64 and print the image tag.
#
#   tools/build.sh [--ref <game-ref>] [--tag <image-tag>]
#
# The player is self-contained (player.py + library/), so no game checkout
# is needed to build. --ref exists to keep the contract convention and to
# label the image with the game revision the library was last verified
# against; it defaults to the pin below and does not change what is built.
#
# PINNED_GAME_REF rationale: coworld-sugarscape d314c5f is the revision the
# library rulesets were exported from and verified behaviorally identical
# to the bundled baseline (see players/baseline/VERSION_LOG.md v0). Bump it
# when re-verifying the library against a newer game release.
#
# linux/amd64 is mandatory: the platform hard-checks it, and an arm64 image
# will upload but fail to start in hosted episodes.
set -euo pipefail

PINNED_GAME_REF="d314c5f6a64cdc122219e9591ea7982df5ffdbb8"
GAME_REF="$PINNED_GAME_REF"
# Distinct from the game repo's compose-built "sugarscape-baseline" image.
TAG="sugarscape-mixin-baseline:latest"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref) GAME_REF="$2"; shift 2 ;;
    --tag) TAG="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker build \
  --platform linux/amd64 \
  --label "sugarscape.game_ref=$GAME_REF" \
  -t "$TAG" \
  "$LAB_ROOT/players/baseline"

echo "$TAG"
