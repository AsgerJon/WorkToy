"""
EZStore keeps an 'EZData' field in the instance '__dict__' when a data
descriptor of the same name would otherwise take the name over.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute import MissingVariable

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional


class EZStore:
  """
  EZStore is the data descriptor an 'EZData' class places at the name of
  a field when a data descriptor of the same name sits further along its
  method resolution order. An 'EZData' instance keeps its field values
  in its own '__dict__', and Python lets a data descriptor anywhere in
  the method resolution order take precedence over that dict, so without
  the store the other descriptor would decide what the field reads and
  writes. 'Object.directory' is one such descriptor; a mixin declaring a
  property or a 'Field' under a field name is another.

  The store reads and writes the instance '__dict__' under the field
  name, which is where a field without a clash lives too, so
  construction, assignment and copying treat both alike. A field without
  a clash gets no store and is read as a plain instance attribute.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_name__: Optional[str] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, fieldName: str) -> None:
    self.__field_name__ = fieldName

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Read through the class, the store returns itself. Read through an
    instance, it returns the value the instance holds under the field
    name, and raises 'MissingVariable' on an instance that never received
    one, such as an instance made by '__new__' alone.
    """
    if instance is None:
      return self
    try:
      return instance.__dict__[self.__field_name__]
    except KeyError as keyError:
      raise MissingVariable(instance, self.__field_name__) from keyError

  def __set__(self, instance: Any, value: Any) -> None:
    instance.__dict__[self.__field_name__] = value
