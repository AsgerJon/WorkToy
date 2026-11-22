"""
The 'design.promises' package holds the Promise API of 'worktoy', an
invention of Asger Jon Vistisen: what 'worktoy' promises the projects
built on it, written as tests. The tests in 'tests' are what 'worktoy'
promises internally, its discipline and the record a reader checks
before trusting it; the promises here are what it promises externally.
A behaviour no promise covers may change in any release. Each package
of 'worktoy' has a subfolder of its own, and 'deprecations' holds the
promises that end at the next major update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations
