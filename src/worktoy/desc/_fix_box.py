"""
FixBox is a write-once 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from ..core import Object
from ..waitaminute.desc import WriteOnceError
from . import AttriBox

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

T = TypeVar('T')


class FixBox(AttriBox[T]):
  """
  Some attributes must be set once per instance and never change after,
  as a port fixed at startup, while keeping everything an 'AttriBox'
  gives: a declared type and default, lazy building, conversion of the
  value assigned, and the notification decorators.

    class Config(BaseObject):
      port = FixBox[int](8080)

  Implementation
  --------------

  The first value an instance stores is final: a later assignment raises
  'WriteOnceError' and a deletion raises 'ProtectedError'. A read stores
  the default it builds, so an attribute meant to be set at runtime is
  assigned before anything reads it. The value is kept under
  '__<name>__fixbox_field_object__', apart from an 'AttriBox' at the same
  name. A 'preSet' callback runs before a refused write is refused.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> Any:
    """
    The first write of an instance must be stored as for 'AttriBox', and
    any later one refused.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned.

    Returns
    -------

    T
      The value stored.

    Raises
    ------

    WriteOnceError
      The instance holds a value already, written or built by a read.

    TypeException
      The value is not of the field type and does not convert.
    """
    pvtName = self._getStorageName()
    try:
      oldValue = object.__getattribute__(instance, pvtName)
    except AttributeError:
      pass
    else:
      raise WriteOnceError(self, oldValue, value)
    return AttriBox.__instance_set__(self, instance, value, **kwargs)

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    A value written once must stay.

    Raises
    ------

    ProtectedError
      Always.
    """
    Object.__instance_delete__(self, instance, *_, **kwargs)
