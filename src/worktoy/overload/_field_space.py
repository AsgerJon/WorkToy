"""WorkToy - MetaClass - FieldSpace
Namespace class for use in implementation of function over loading."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function
from worktoy.metaclass import AbstractNameSpace


class FieldSpace(AbstractNameSpace):
  """WorkToy - MetaClass - FieldSpace
  Namespace class for use in implementation of function over loading."""

  def __init__(self, *args, **kwargs, ) -> None:
    AbstractNameSpace.__init__(self, *args, **kwargs)
    self._overloadedNameSpace = None

  def getOverloadedNameSpace(self) -> dict[str, list[Function]]:
    """Getter-function for the overloaded namespace."""
    self._overloadedNameSpace = {}
    for item in self.getLog():
      key = item[1]
      types = getattr(item[2], '__overload_signature__', None)
      if types is not None:
        existing = self._overloadedNameSpace.get(key, [])
        self._overloadedNameSpace[key] = [*existing, item[2]]
    return self._overloadedNameSpace
