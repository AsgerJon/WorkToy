"""
The 'design' folder specifies the design of 'worktoy': what the library
does for the projects built on it, and what it refuses. It is written
as tests, in three packages, and as a manual. 'design.promises' holds
what 'worktoy' owes those projects, 'design.refusals' the mistakes it
refuses, and 'design.confessions' the promises it made and could not
keep. The file 'manual.md' describes the same design in prose, in one
document: how the design is to be read, then a part for each package
of 'worktoy', what works and what is refused described together, with
every example checked. The tests in 'tests' are what 'worktoy' holds
itself to internally; the design is what it tells the projects built
on it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
