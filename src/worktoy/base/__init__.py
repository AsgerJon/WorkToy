"""WorkToy - Core
The core module provides the chain of default classes:
  'CoreClass'
  'GuardClass'
  'DefaultClass'
The final class should be called DefaultClass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._core_class import CoreClass
from ._guard_class import GuardClass
from ._default_class import DefaultClass

if __name__ != '__main__':
  DefaultClass.__core_instance__ = DefaultClass()
