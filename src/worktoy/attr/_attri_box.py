"""AttriBox provides a descriptor with lazy instantiation of the
underlying object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..static.zeroton import DELETED
from ..waitaminute import TypeException
from . import AbstractBox

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class AttriBox(AbstractBox):
  """AttriBox provides a descriptor with lazy instantiation of the
  underlying object. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def __class_getitem__(cls, wrapped: type) -> Self:
    """Get the field type."""
    self = cls.__new__(cls)
    self._setWrappedClass(wrapped)
    return self

  def __call__(self, *args, **kwargs) -> AttriBox:
    """Call the descriptor with the given arguments."""
    self.__init__(*args, **kwargs)
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, val: Any, oldVal: Any = None, **kwargs) -> None:
    """
    Strongly typed setter requiring the new value to be a strict instance
    of the wrapped class.
    """
    if oldVal is None and not kwargs.get('_recursion', False):
      try:
        oldVal = self.__instance_get__()
      except Exception as exception:
        oldVal = exception
      else:
        pass
      finally:
        return self.__instance_set__(val, oldVal, _recursion=True, **kwargs)
    cls = self.getWrappedClass()
    if not isinstance(val, cls) and val is not DELETED:
      name = self.__field_name__
      raise TypeException(name, val, cls)
    pvtName = self.getPrivateName()
    setattr(self.instance, pvtName, val)

  def __instance_delete__(self, oldVal: Any = None, **kwargs) -> None:
    """
    Strongly typed deleter requiring the value to be deleted to be an
    instance of the wrapped class.
    """
    self.__instance_set__(DELETED, )
