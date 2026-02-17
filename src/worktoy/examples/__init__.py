"""
The 'worktoy.examples' module provides example usages of the 'worktoy'
library.

Usage:
In a terminal:
python -m worktoy.examples <name_of_example>

For example,
python -m worktoy.examples complex_number

The available examples are:

"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._complex_number import ComplexNumber

__all__ = [
  'ComplexNumber',
  ]
