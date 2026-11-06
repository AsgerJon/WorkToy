"""
The 'tests.test_desc' package tests 'worktoy.desc': the base descriptor
with its notification decorators, 'Field', 'Alias', 'AttriBox',
'FastBox', 'FixBox', 'SymbolicName' and the type alias a box subscript
gives. Every test class is based on 'DescTest', the local base of the
folder, and the fixtures the tests share are small classes of their own.

- DescTest

Private, importable but not intended for public use:

- Part
- Vessel
- Watched
- Listener
- Geometry
- Shrunk
- Circle
- Particle
- Config
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ._desc_test import DescTest
from ._part import Part
from ._vessel import Vessel
from ._watched import Watched
from ._listener import Listener
from ._geometry import Geometry
from ._shrunk import Shrunk
from ._circle import Circle
from ._particle import Particle
from ._config import Config

__all__ = [
  'DescTest',
]
