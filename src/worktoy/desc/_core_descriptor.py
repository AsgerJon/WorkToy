"""CoreDescriptor implements the most basic functionalities of the
descriptor protocol without adding any additional features. This includes
in particular the __set_name__ method, which is invoked when the owning
class is created. Then this method informs the descriptor instance of the
class that now owns it and the name by which it appears in the namespace
of the owning class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseObject
from worktoy.text import monoSpace, typeMsg
from re import compile


class CoreDescriptor(BaseObject):
  """Implementation of basic descriptor protocol functionalities."""

  __field_name__ = None
  __field_owner__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_owner__ = owner
    self.__field_name__ = name

  def getFieldName(self) -> str:
    """Getter-function for the field name."""
    if self.__field_name__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner."""
    if self.__field_owner__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created. """
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  def _getPrivateName(self, ) -> str:
    """Returns the name of the private attribute used to store the inner
    object. """
    if self.getFieldName() is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    pattern = compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', self.__field_name__).lower()
