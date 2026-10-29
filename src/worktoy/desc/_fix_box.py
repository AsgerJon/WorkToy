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

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

T = TypeVar('T')


class FixBox(AttriBox[T]):
  """
  FixBox is an 'AttriBox' whose attribute is written once. The class
  docstring of 'AttriBox' explains how a box works; this one says only
  where 'FixBox' differs: the first value an instance stores is final, a
  later assignment raises 'WriteOnceError', and 'del' raises
  'ProtectedError'. The first read stores the field object as well, so an
  attribute meant to be set at runtime is assigned before anything reads
  it.

    class Config:
      port = FixBox[int](8080)

    c = Config()
    c.port = 9090          # the one write
    c.port = 1             # WriteOnceError

    d = Config()
    d.port                 # 8080, stored by the read
    d.port = 9090          # WriteOnceError
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> Any:
    """
    The first assignment works as 'AttriBox.__instance_set__', conversion
    included; any later one raises 'WriteOnceError', and so does the first
    one after a read has stored the field object.

    Parameters
    ----------
    instance : Any
        The instance the attribute is assigned through.
    value : Any
        The assigned value.
    **kwargs : Any
        Passed on to 'AttriBox.__instance_set__'.

    Returns
    -------
    T
        The value stored, an instance of the field type.

    Raises
    ------
    WriteOnceError
        If the instance already holds a value for the attribute.
    TypeException
        If the value is not of the field type and 'typeCast' refuses it.
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
    Unlike 'AttriBox.__instance_delete__', deletion is refused: a value
    written once stays.

    Parameters
    ----------
    instance : Any
        The instance the attribute is deleted from.
    *_ : Any
        The value being deleted, which 'Object.__delete__' passes.
    **kwargs : Any
        Keyword arguments of the descriptor protocol, unused.

    Returns
    -------
    None

    Raises
    ------
    ProtectedError
        Always.
    """
    Object.__instance_delete__(self, instance, *_, **kwargs)
