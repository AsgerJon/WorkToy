"""WorkToy - Core - ModuleDescriptor
Specifying module names"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import STR


class ModuleDescriptor(STR):
  """WorkToy - Core - ModuleDescriptor
  Specifying module names"""

  def explicitGetter(self, obj: object, cls: type) -> str:
    """Explicit Getter"""
