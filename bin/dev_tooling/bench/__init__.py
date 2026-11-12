"""The 'bench' package provides micro-benchmarks comparing worktoy
constructs against plain-Python baselines.

It is NOT part of the distribution and NOT collected by pytest (no
'test_' prefix). Run it with './bench.sh' or 'python -m bench'.

The subjects are written the way a reasonable builder writes with
worktoy: the documented spellings, used as intended. What a deprecated
feature costs, or a call that leans on the slowest fallback of a
facility, is out of scope: worse performance is to be expected there,
and a deprecation notice being slow is nearly a feature.

The goal is diagnosis, not a single headline number: the same logical
object (a 2D point) is implemented several ways in '_subjects', and
'_harness' times each operation (construct, read, write) so the cost
of the worktoy machinery can be localised per operation rather than
lumped into one ratio.

Each benchmark is a file with a 'run' function and its subjects beside
it in a private file: 'points' (the 2D point), 'dispatching' (a call of
an overloaded method), 'enumerations' (members, flags and a field over
an enumeration, beside 'enum'), 'creation' (the class statement) and
'startup' (the import).
'python -m bench --list' names them, and 'python -m bench <name>' runs
the ones named. 'attribute_ladder.py' is an older script of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
