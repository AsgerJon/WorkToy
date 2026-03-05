"""The 'tests.test_dispatch' package contains tests for the
'worktoy.dispatch' package. """
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._dispatcher_test import DispatcherTest
from ._plane_point import PlanePoint
from ._space_point import SpacePoint
from ._complex_number import ComplexNumber
from ._complex_subclass import ComplexSubclass
from ._complex_meta import ComplexMeta
from ._complex_meta_sub import ComplexMetaSub, SusComplex
from ._comflex import Comflex
from ._comflex_meta import ComflexMeta

__all__ = [
  'DispatcherTest',
  'PlanePoint',
  'SpacePoint',
  'ComplexNumber',
  'ComplexSubclass',
  'ComplexMeta',
  'ComplexMetaSub',
  'SusComplex',
  'Comflex',
  'ComflexMeta',
  ]
