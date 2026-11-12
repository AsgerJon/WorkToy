"""
EZStore shadows a data descriptor that would otherwise take over the
name of an 'EZData' field, so the field stays in the instance '__dict__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute import MissingVariable

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional


class EZStore:
  """
  EZStore is the descriptor an 'EZData' class places at the name of a
  field when a data descriptor of the same name sits further along its
  method resolution order. An 'EZData' instance keeps its field values
  in its own '__dict__', and Python lets a data descriptor anywhere in
  the method resolution order take precedence over that dict, so without
  the store the other descriptor would decide what the field reads and
  writes. 'Object.directory' is one such descriptor; a mixin declaring a
  property or a 'Field' under a field name is another.

  Implementation
  --------------

  The store defines '__get__' alone. Python finds it first along the
  resolution order and, since it is no data descriptor, lets the
  instance '__dict__' answer a populated read and take every write
  through 'object.__setattr__', so construction, assignment and copying
  treat a stored field as any other. The data descriptor behind it is
  never reached. '__get__' runs only for an instance that holds no value
  under the name, as one made by '__new__' alone, and raises
  'MissingVariable'. An 'Alias' of the field reads through the store and
  is refused a write or a deletion by the alias, since the store takes
  neither; the field itself is assigned through the generated
  '__setattr__' of its class. A field without a clash gets no store and
  is read as a plain instance attribute.
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
    A field whose name a data descriptor further along the resolution order
    would take over must still be read from the instance, and an instance
    holding no value under the name must fail as a missing attribute does,
    not answer with what that descriptor gives.

    Implementation
    --------------

    Through the class, the store returns itself. Python reads the store
    through an instance only when the instance holds no value under the
    field name, and that read raises 'MissingVariable': the instance never
    received one, as an instance made by '__new__' alone. An 'Alias' of the
    field calls this method itself, for an instance that does hold a value,
    and receives that value.

    Parameters
    ----------

    instance : Any
      The instance read through, or 'None'.

    owner : type
      The class read through.

    Returns
    -------

    Any
      The store through the class, the value of the instance otherwise.

    Raises
    ------

    MissingVariable
      The instance holds no value under the field name.
    """
    if instance is None:
      return self
    try:
      return instance.__dict__[self.__field_name__]
    except KeyError as keyError:
      raise MissingVariable(instance, self.__field_name__) from keyError
