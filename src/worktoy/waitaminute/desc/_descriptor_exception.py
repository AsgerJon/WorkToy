"""
DescriptorException is the base class for the descriptor-protocol
exceptions 'AccessError', 'ProtectedError', 'ReadOnlyError' and
'PhantomBoxError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class DescriptorException(WorkToyException, Exception):
  """
  Base class for the descriptor protocol exceptions 'AccessError',
  'ProtectedError', 'ReadOnlyError' and 'PhantomBoxError'; catching this
  type catches those four together. The first three are 'AttributeError's
  as well, as Python's own refusals of a read, a write and a deletion are.
  'WriteOnceError' (a 'TypeError') and
  'WithoutException' (a 'RuntimeError') are related descriptor errors
  that do NOT inherit from this class, so a bare
  'except DescriptorException' does not catch them.
  """

  @staticmethod
  def _fieldName(instance: Any, desc: Any) -> str:
    """
    The '_fieldName' method names the attribute 'desc' is placed at on
    the class of 'instance'. A descriptor that recorded its field name
    answers from that; one that recorded none, as a 'KeeNum' member
    placed in a class body does, being a shared singleton that may sit
    under several names, is looked up by identity in the classes of
    the instance. A descriptor found nowhere is named 'object'.
    """
    fieldName = getattr(desc, '__field_name__', None)
    if fieldName is not None:
      return fieldName
    for base in type(instance).__mro__:
      for name, value in vars(base).items():
        if value is desc:
          return name
    return 'object'
