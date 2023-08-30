"""WorkToy - Symbolic - AbstractSym
This class provides the functions used by the Symbolic classes. These are
methods generally shared by classes by virtue of being Symbolic."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import DefaultClass


class SYM(DefaultClass):
  """WorkToy - Symbolic - AbstractSym
  This class provides the functions used by the Symbolic classes. These are
  methods generally shared by classes by virtue of being Symbolic."""

  __value_type__ = int

  def __init__(self, **kwargs) -> None:
    if '_root' not in [k for (k, _) in kwargs.items()]:
      DefaultClass.__init__(self, **kwargs)
      self._value = None
      self._fieldName = None
      self._ownerClass = None  # Points to the Symbolic Class

  def _setFieldName(self, fieldName: str) -> None:
    """Setter-function for field name. Subclasses must implement this
    method."""
    if self._fieldName is not None:
      raise self.createProtectedMemberError('_fieldName')

  def _setOwnerClass(self, owner: type) -> None:
    """Setter-function for owner class. Subclasses must implement this
    method."""
    self._ownerClass = owner

  def __str__(self) -> str:
    return '%s - %s' % (self.__class__.__name__, self.__name__)

  def __repr__(self) -> str:
    return '%s.%s' % (self.__class__.__name__, self.__name__)

  def __eq__(self, other: SYM) -> bool:
    if isinstance(other, SYM):
      return True if self is other else False
    if isinstance(other, str):
      return True if self._getFieldName() == other else False
    if isinstance(other, int):
      return True if self._getValue() == other else False
    return NotImplemented

  def __ne__(self, other: SYM) -> bool:
    return False if self == other else True

  def __set_name__(self, owner: type, name: str) -> None:
    self._setFieldName(name)
    self._setOwnerClass(owner)

  def _getValue(self) -> int:
    return self._value

  def _getFieldName(self) -> str:
    return self._fieldName

  def __hash__(self) -> int:
    """Implementation of the hashing function."""
    return self._getValue()
