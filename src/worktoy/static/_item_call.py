"""
ItemCall encapsulates a call to a namespace.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never


class ItemCall:
  """
  ItemCall encapsulates calls to the __setitem__, __getitem__,
  and __delitem__ methods of the AbstractNamespace class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  __slots__ = ('space', 'key', 'value', 'call')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args) -> None:
    """
    Initializes the ItemCall instance with the provided arguments.

    Args:
      key: str
        The key for the item call.
      value: Any
        The value for the item call or the error or 'None' for deletion.
      call: FunctionType
        One of: 'dict.__setitem__', 'dict.__getitem__',
        or 'dict.__delitem__'.
    """
    if len(args) == 4:
      self.space, self.key, self.value, self.call = args
    elif len(args) == 3:
      self.space, self.key, self.call = args
      self.value = None
    else:
      infoSpec = """%s constructor expected 2 or 3 arguments, but received 
      %d!"""
      info = monoSpace(infoSpec % (type(self).__name__, len(args)))
      raise ValueError(info)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __hash__(self, ) -> int:
    """
    Returns the hash of the ItemCall instance.
    """
    try:
      if self.value is None:
        valueHash = 0
      else:
        valueHash = hash(self.value)
    except TypeError:
      valueHash = hash(object.__str__(self.value))
    callHashes = {
        dict.__setitem__: 1,
        dict.__getitem__: 2,
        dict.__delitem__: 3
    }
    for call, hash_ in callHashes.items():
      if self.call is call:
        break
    else:
      infoSpec = """Unable to resolve the call type for ItemCall: '%s'!"""
      info = monoSpace(infoSpec % (str(self.call),))
      raise ValueError(info)
    return hash((self.key, valueHash, hash_))

  def __eq__(self, other: Any) -> bool:
    """
    Compares the ItemCall instance with another object for equality.

    Args:
      other: Any
        The object to compare with.

    Returns:
      bool: True if the other object is an ItemCall and has the same key,
      value, and call, otherwise False.
    """
    if not isinstance(other, ItemCall):
      return False
    if self.space != other.space:
      return False
    if self.key != other.key:
      return False
    if self.value != other.value:
      return False
    if self.call is not other.call:
      return False
    return True

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def apply(self, space: dict) -> Any:
    """
    Applies the ItemCall to the provided namespace.

    Args:
      space: dict
        The namespace to apply the ItemCall to.

    Returns:
      dict: The updated namespace after applying the ItemCall.
    """
    if self.call is dict.__getitem__:
      return dict.__getitem__(space, self.key)
    if self.call is dict.__delitem__:
      try:
        dict.__delitem__(space, self.key)
      except Exception as exception:
        raise exception
      else:
        return space
      finally:
        pass  # NOQA
    if self.call is dict.__setitem__:
      dict.__setitem__(space, self.key, self.value)
      return space
    infoSpec = """%s expected 'call' to be one of: 'dict.__getitem__', 
    '__dict.__setitem__' or 'dict.__delitem__', but received '%s'!"""
    info = monoSpace(infoSpec % (type(self).__name__, str(self.call)))
    raise ValueError(info)
