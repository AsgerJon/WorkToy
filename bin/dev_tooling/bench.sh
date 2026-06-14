#!/usr/bin/env sh
#
# Apache-2.0 license
# Copyright (c) 2026 Asger Jon Vistisen
#
# Runs the worktoy micro-benchmarks in bench/ and prints a per-
# operation ratio table (construct / read / write) comparing worktoy
# descriptors against plain, slotted, and dataclass baselines. The
# bench bootstraps the src layout onto sys.path itself, so no install
# is needed. Methodology lives in bench/_harness.py.

set -eu

#  Anchor the working directory so relative paths resolve
#  no matter where the script is invoked from.
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

export PYTHONDONTWRITEBYTECODE=1

python3 -m bench "$@"
