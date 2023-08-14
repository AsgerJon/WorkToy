"""ProceduralError is a custom exception made specifically for use in the
WorkToy framework. When a field is accessed before it is initialized,
an instance of ProceduralError. The constructor expect the method being
called, the instance referred to in the instance, the class owning the
field and finally the name of the variable not yet initialized."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typetools import CallMeMaybe
from typing import Any


class ProceduralError(Exception):
  """ProceduralError is a custom exception made specifically for use in the
  WorkToy framework. When a field is accessed before it is initialized,
  an instance of ProceduralError. The constructor expects the method being
  called, the instance referred to in the instance, the class owning the
  field and finally the name of the variable not yet initialized."""
  #
  # def __init__(self, cls: type, ins: Any, fun: CallMeMaybe, varName: str,
  #              varType: type):
  #
