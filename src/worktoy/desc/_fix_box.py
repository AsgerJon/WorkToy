"""
FixBox is a write-once 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from worktoy.core import Object
from worktoy.desc import AttriBox
from worktoy.waitaminute.desc import WriteOnceError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

T = TypeVar('T')


class FixBox(AttriBox[T]):
  """
  FixBox subclasses 'AttriBox' and provides a descriptor for write-once
  attributes. Two methods change: a second assignment raises
  'WriteOnceError', and deletion is disabled (it raises 'ProtectedError').

  The single write counts whatever stores the value, not only an
  explicit assignment. Reading an unset field lazily builds and stores
  the deferred default, and that store consumes the single write, so an
  explicit assignment after any read raises 'WriteOnceError' with the
  lazily built default as the old value. A field meant to receive its
  value at runtime must therefore be written before it is first read.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    The '__instance_set__' method stores the value once; a subsequent
    assignment raises 'WriteOnceError'. The unset state is detected via
    'AttributeError' rather than 'is None', so an explicit assignment of
    'None' still counts as the one write.
    """
    pvtName = self.getPrivateName()
    try:
      oldValue = object.__getattribute__(instance, pvtName)
    except AttributeError:
      pass
    else:
      raise WriteOnceError(self, oldValue, value)
    AttriBox.__instance_set__(self, instance, value, **kwargs)

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    Deletion is disabled on 'FixBox'. The '__instance_delete__' method
    falls through to 'Object.__instance_delete__', which raises
    'ProtectedError'.
    """
    Object.__instance_delete__(self, instance, *_, **kwargs)
