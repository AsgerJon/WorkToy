"""
The 'tests.test_dispatch.examples' package contains example classes
implementing components from the 'worktoy.dispatch' package. These are
used in the test suite.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._plane_point import PlanePoint
from ._space_point import SpacePoint
from ._complex_number import ComplexNumber
from ._complex_subclass import ComplexSubclass
from ._comflex import Comflex
from ._complex_meta import ComplexMeta
from ._comflex_meta import ComflexMeta
from ._complex_meta_sub import ComplexMetaSub, SusComplex

__all__ = (
  'PlanePoint',
  'SpacePoint',
  'ComplexNumber',
  'ComplexSubclass',
  'Comflex',
  'ComplexMeta',
  'ComflexMeta',
  'ComplexMetaSub',
  'SusComplex',
)
