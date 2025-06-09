"""
The 'Some' class considers all objects as instances of itself, except for
'None'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import TypeAlias, Any

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class _MetaSome(type):
  """
  Implementation of custom 'isinstance' logic requires metaclass level
  implementation. This metaclass implements the logic that considers all
  objects as instances of 'Some', except for 'None'. It also prevents
  'Some' from being subclassed and from being instantiated.
  """

  def __instancecheck__(*args) -> bool:  # NOQA
    """
    Custom 'isinstance' logic that considers all objects as instances of
    'Some', except for 'None'.
    """
    for arg in args:
      if arg is None:
        return False
    else:
      return True

  def __subclasscheck__(cls, other: type) -> bool:  # NOQA
    """
    Any class except 'NoneType' is considered a subclass of 'Some'.
    """
    try:
      _ = issubclass(other, object)  # even NoneType is an object
    except Exception as exception:
      raise exception
    else:
      if other is type(None):
        return False
      return True

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Space:
    """
    Prepares the namespace for the 'Some' class, ensuring it is not
    instantiated or subclassed.
    """
    if kwargs.get('_root', False):
      return dict()
    from worktoy.waitaminute import IllegalInstantiation
    raise IllegalInstantiation(mcls)


class Some(metaclass=_MetaSome, _root=True):
  """
  The 'Some' class considers all objects as instances of itself, except for
  'None'. It is not meant to be instantiated or subclassed.
  """
  pass
