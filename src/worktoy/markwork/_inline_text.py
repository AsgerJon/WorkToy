"""
InlineText subclasses 'InlineBase' and encapsulates a text string. This
class provides nothing besides non-specific text. The owning 'Block'
class is responsible for deciding how to render it.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import InlineBase
from ..core.sentinels import THIS
from ..mcls import BaseObject
from ..utilities import textFmt
from ..desc import Field, AttriBox
from ..dispatch import overload

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Any, Self, Iterator

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]
  StrBox: TypeAlias = Union[str, AttriBox]


class InlineText(InlineBase):
  """
  InlineText subclasses 'InlineBase' and encapsulates a text string. This
  class provides nothing besides non-specific text. The owning 'Block'
  class is responsible for deciding how to render it.

  Attributes
  ----------
  text: str
    The text contained by the instance.

  Signatures
  ----------
  __init__(text: str) -> None
    Construct an instance of 'InlineText' with the given text.

  __init__(other: Self) -> None
    Construct an instance of 'InlineText' by copying the text from another
    instance.

  __init__() -> None
    Construct an instance of 'InlineText' without any text.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def __init__(self, text: str) -> None:
    self.text = text

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.text = other.text

  @overload()
  def __init__(self, ) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _resolveOther(cls, other: Any) -> Self:
    """
    This method attempts to instantiate a class representation of other
    which may then be used in binary operations defined below.

    Parameters
    ----------
    other: Any
      The object to resolve.

    Returns
    -------
    Self
      An instance of the class representing 'other'.
    NotImplemented
      If 'other' cannot be resolved to an instance of the class.
    """
    if isinstance(other, cls):
      return other
    if isinstance(other, str):
      return cls(other)
    return NotImplemented

  def __add__(self, other: Any) -> Self:
    """
    The addition operator is understood to mean the instance of the class
    containing the text in self followed by the text in 'other'.

    Parameters
    ----------
    other: Any
      The object to add to self. This is resolved to an instance of the
      class using '_resolveOther'.

    Returns
    -------
    Self
      An instance of the class containing the text in 'self' followed by the
      text in 'other'.
    NotImplemented
      If '_resolveOther' returns 'NotImplemented', this method does as well.

    Examples
    --------
    Concatenating two 'InlineText' instances
    >>> a = InlineText("Hello")
    >>> b = InlineText("World")
    >>> c = a + b
    >>> print(c)
    <InlineText: Hello World>

    Concatenating an 'InlineText' instance with a string
    >>> a = InlineText("Hello")
    >>> b = a + "World"
    >>> print(b)
    <InlineText: Hello World>
    """
    resolved: Self = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(textFmt("""%s %s""" % (self.text, resolved.text)))

  def __iadd__(self, other: Any) -> Self:
    """
    In-place addition extends the text in self with the text in 'other'.

    Parameters and return values as for '__add__'.

    Examples
    --------
    In-place extension of existing 'InlineText' instance.
    >>> a = InlineText("Hello")
    >>> a += InlineText("World")
    >>> print(a)
    <InlineText: Hello World>

    In-place extension of existing 'InlineText' instance with a string.
    >>> a = InlineText("Hello")
    >>> a += "World"
    >>> print(a)
    <InlineText: Hello World>
    """
    resolved: Self = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    self.text = textFmt("""%s %s""" % (self.text, resolved.text))
    return self

  def __radd__(self, other: Any) -> Self:
    """
    The reflected addition operator allows for extension of 'other' str
    object with 'self' into a new 'InlineText' instance.

    Parameters and return values as for '__add__'.

    Examples
    --------
    Extension of string with 'InlineText' instance using reflected addition.
    >>> a = InlineText("World")
    >>> b = "Hello " + a
    >>> print(b)
    <InlineText: Hello World>
    """
    resolved: Self = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(textFmt("""%s %s""" % (resolved.text, self.text)))

  def __contains__(self, item: Any) -> bool:
    """
    The containment operator checks if 'self.text' contains the given item.

    Parameters
    ----------
    item: Any
      The object of containment check. The item is resolved to another
      'InlineText' instance using '_resolveOther'. If resolution results
      in 'NotImplemented', the item is rejected.

    Returns
    -------
    bool
      Specifies membership of the given item.

    Examples
    --------
    Checking if an 'InlineText' instance contains a string.
    >>> foo = InlineText('Never gonna give you up')
    >>> print('Together forever' in foo)
    False
    >>> print('Never gonna' in foo)
    True
    """
    if isinstance(item, str):
      return item in self.text
    resolved: Self = self._resolveOther(item)
    if resolved is NotImplemented:
      return False
    return resolved.text in self

  def __eq__(self, other: Any) -> bool:
    """
    Two instances of 'InlineText' or an instance and a 'str' object are
    equal when 'self.text' is.

    Parameters
    ----------
    other: Any
      The object to compare with self. This is resolved to an instance of
      the class using '_resolveOther'.

    Returns
    -------
    bool
      Specifies whether 'self.text' is equal to the text in 'other'.
    NotImplemented
      If '_resolveOther' returns 'NotImplemented', this method does as well.
    """
    resolved: Self = self._resolveOther(other)
    if resolved is NotImplemented:
      return NotImplemented
    return True if self.text == resolved.text else False

  def __len__(self, ) -> int:
    """
    Returns the number of words in 'self.text'. Here 'word' is understood
    to mean character sequences separated by whitespace.

    Returns
    -------
    int
      The number of words in 'self.text'.

    Examples
    --------
    Counting the number of words in an 'InlineText' instance.
    >>> foo = InlineText('Never gonna give you up')
    >>> print(len(foo))
    5
    """
    return len(str.split(self.text, ))

  def __iter__(self, ) -> Iterator[str]:
    """
    Yields from 'self.text' one word at a time. Here 'word' is understood
    to mean character sequences separated by whitespace.

    Returns
    -------
    Iterator[str]
      An iterator yielding the words in 'self.text' one at a time.

    Examples
    --------
    Iterating over the words in an 'InlineText' instance.
    >>> foo = InlineText('Never gonna give you up')
    >>> for word in foo:
    ...   print(word)
    Never
    gonna
    give
    you
    up
    """
    yield from str.split(self.text, )
