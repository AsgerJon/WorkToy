"""The 'bench' package provides micro-benchmarks comparing worktoy
constructs against plain-Python baselines.

It is NOT part of the distribution and NOT collected by pytest (no
'test_' prefix). Run it with './bench.sh' or 'python -m bench'.

The goal is diagnosis, not a single headline number: the same logical
object (a 2D point) is implemented several ways in '_subjects', and
'_harness' times each operation (construct, read, write) so the cost
of the worktoy machinery can be localised per operation rather than
lumped into one ratio.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
