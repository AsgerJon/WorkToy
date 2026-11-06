"""
The 'tests.test_ezdata' package tests 'worktoy.ezdata': the field
descriptor 'EZField', the store 'EZStore', the namespace 'EZSpace' and
its hook 'EZHook', the metaclass 'EZMeta', the base 'EZData' and the
'fields' function. Every test class is based on 'EzdataTest', the local
base of the folder, and the fixtures the tests share are small
dataclasses of their own, with one plain mixin and one descriptor.

- EzdataTest

Private, importable but not intended for public use:

- Point2D
- Circle
- Span
- Version
- Bag
- Reporter
- Labelled
- Vector
- FrozenVector
- Vector3
- Peek
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._ezdata_test import EzdataTest
from ._point2d import Point2D
from ._circle import Circle
from ._span import Span
from ._version import Version
from ._bag import Bag
from ._reporter import Reporter
from ._labelled import Labelled
from ._vector import Vector
from ._frozen_vector import FrozenVector
from ._vector3 import Vector3
from ._peek import Peek

__all__ = [
  'EzdataTest',
]
