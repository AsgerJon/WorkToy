"""WorkToy - Base
This module provides the chain of baseclasses. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._core_class import CoreClass
from ._default_class import DefaultClass

if __name__ != '__main__':
  DefaultClass.__core_instance__ = DefaultClass()
  print('core instance')
