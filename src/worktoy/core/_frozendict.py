"""FrozenDict is a custom subclass of the builtin 'dict' that is
immutable, meaning that it cannot be altered after creation. As a note,
this code was written entirely by chat-GPT August 3 Version, except for
formatting changes. It also provided the docstrings upon request. For
type hinting, I explained the introduction of 'typing.Never' introduced in
Python 3.11 which serves the same function as NoReturn. Chat-GPT then
added this import:
  from typing import NoReturn as Never
This was changed to just importing 'Never'.
The addition of the metaclass bedrock meta was to augment the __str__ and
__repr__ defined on the class itself.

Since the class inherits from dict, it retains the same instance creation
methods, for example:
  frozenDict = FrozenDict(a=1, b=2)"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from typing import Never


class FrozenDict(dict, ):
  """
  An immutable version of a dictionary.
  This class is hashable and can be used as a key in another dictionary
  or as an element in a set.
  """

  def __hash__(self) -> int:
    """Return the hash value of the object."""
    return hash(frozenset(self.items()))

  def __setitem__(self, key: object, value: object) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")

  def __delitem__(self, key: object) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")

  def pop(self, *args, **kwargs) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")

  def popItem(self, *args, **kwargs) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")

  def setDefault(self, *args, **kwargs) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")

  def update(self, *args, **kwargs) -> Never:
    """Raise TypeError since frozenDict is immutable."""
    raise TypeError("frozenDicts are immutable")
