"""EZBox subclasses AttriBox and uses overloading for the constructor. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Any, Never, TYPE_CHECKING
except ImportError:
  Any = object
  Never = object
  TYPE_CHECKING = False

from worktoy.desc import AttriBox
from worktoy.base import overload


class EZBox(AttriBox):
  """EZBox subclasses AttriBox and uses overloading for the constructor. """

  @classmethod
  def __class_getitem__(cls, item) -> Never:
    """EZBox disables the '__class_getitem__' method. """
    e = """EZBox does not use the AttriBox[] syntax!"""
    raise SyntaxError(e)

  @overload(type, object)
  def __init__(self, fieldClass: type, defVal: object) -> None:
    """EZBox constructor with fieldClass and optional arguments. """
    AttriBox.__init__(self, fieldClass)
    self(defVal)

  @overload(object, type)
  def __init__(self, defVal: object, fieldClass: type) -> None:
    """EZBox constructor with optional arguments and fieldClass. """
    AttriBox.__init__(self, fieldClass)
    self(defVal)

  @overload(tuple)
  def __init__(self, args) -> None:
    """EZBox constructor with tuple arguments. """
    self.__init__(*args)

  @overload(type)
  def __init__(self, fieldClass: type) -> None:
    """EZBox constructor with fieldClass. """
    AttriBox.__init__(self, fieldClass)
    self()
