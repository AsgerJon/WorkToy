"""WorkToy - Symbolics - Symbolic
This class represents the category to which a series of symbolics belong.
The Symbolic class cannot be instantiated. Instead, the members of the
category represented by the Symbolic class, are in fact members of the
common SYM class. These instances are set as descriptors on the Symbolic
class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.symbolics import MetaSym, SYM


class AbstractSym(metaclass=MetaSym):
  """WorkToy - Symbolics - Symbolic
  This class represents the category to which a series of symbolics belong.
  The Symbolic class cannot be instantiated. Instead, the members of the
  category represented by the Symbolic class, are in fact members of the
  common SYM class. These instances are set as descriptors on the Symbolic
  class."""

  __current_index__ = 0
  __symbolic_instances__ = []
  __names_values__ = {}
  __symbolic_class__ = None

  @classmethod
  def _getSymbolicInstances(cls) -> list:
    return cls.__symbolic_instances__

  @classmethod
  def _createSymbolicClass(cls) -> None:
    """Abstract method responsible for creating the instance class."""

  @classmethod
  def _getSymbolicClass(cls, **kwargs) -> type:
    if cls.__symbolic_class__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createSymbolicClass()
      return cls._getSymbolicClass(_recursion=True)
    return cls.__symbolic_class__

  def __new__(cls, name: str = None, value: int = None) -> SYM:
    pass
