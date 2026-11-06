"""
ARGS uses a Sentinel metaclass and provides a placeholder for a starred
argument in an overload signature.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SentinelMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self, Iterator, Optional


class _MetaARGS(SentinelMeta):
  """
  An overload signature needs a marker for a variadic tail: any number of
  further positional arguments, each of one type. The marker is written
  last in the signature, must carry its inner type, and must be a
  sentinel name held for the whole process like every other. The starred
  form '@overload(int, *ARGS)' must read naturally as well.

  Implementation
  --------------

  '_MetaARGS' is based on 'SentinelMeta', so 'ARGS' is registered like
  any sentinel, but its '__call__' builds an instance carrying an inner
  type, which 'SentinelMeta' refuses for other sentinels. Iterating over
  the class 'ARGS' yields 'ARGS[object]', which is what the star unpacks.

  Attributes
  ----------

  __inner_type__ : type or None
    'None' when read off the class 'ARGS'; each instance has its own.
  """

  __inner_type__: Optional[type] = None

  def __call__(cls, type_: type) -> _MetaARGS:
    """
    'ARGS[int]' must give a marker carrying 'int'.

    Implementation
    --------------

    An instance is built with 'type.__call__' and given the inner type.

    Parameters
    ----------

    type_ : type
      The type every argument of the tail must have.

    Returns
    -------

    ARGS
      A new instance.
    """
    self = type.__call__(cls, )
    self.__inner_type__ = type_
    return self

  def __iter__(cls, ) -> Iterator:
    """
    '*ARGS' in a signature must mean any number of arguments of any type.

    Implementation
    --------------

    The class yields 'ARGS[object]'.
    """
    yield from (cls[object],)

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    def __getitem__(cls, type_: type) -> Self:  ...


class ARGS(metaclass=_MetaARGS):
  """
  A signature such as '@overload(str, ARGS[int])' must match a 'str'
  followed by zero or more integers, and '@overload(int, ARGS)' an 'int'
  followed by anything. A subclass redeclaring a variadic signature must
  be recognized as overriding the one it inherits, although each
  subscript builds a new object.

  Implementation
  --------------

  'ARGS[int]' builds an instance whose inner type is 'int'. Instances
  compare and hash by their inner type, and iterate to themselves, so
  '*ARGS[int]' means 'ARGS[int]'. A bare 'ARGS' is read as 'ARGS[object]'
  by 'TypeSig.starARGS'. The text of an instance is its subscript, as
  'ARGS[int]'.

  Attributes
  ----------

  __inner_type__ : type
    The type every argument of the tail must have.
  """

  def __iter__(self) -> Iterator[Self]:
    """
    '*ARGS[int]' must unpack to 'ARGS[int]' itself.

    Implementation
    --------------

    The instance yields itself.
    """
    yield from (self,)

  def __eq__(self, other: Any) -> bool:
    """
    Two signatures declaring 'ARGS[int]' hold two distinct instances, and
    must still compare equal.

    Implementation
    --------------

    Inner types are compared by identity. Anything that is not an 'ARGS'
    instance, the class 'ARGS' included, is left to the other operand.

    Parameters
    ----------

    other : Any
      The object compared with.

    Returns
    -------

    bool
      Whether both are instances of one inner type, or 'NotImplemented'.
    """
    if not isinstance(other, ARGS):
      return NotImplemented
    return True if self.__inner_type__ is other.__inner_type__ else False

  def __hash__(self) -> int:
    """
    Equal objects must hash alike, or a set or a signature holding one of
    them does not find the other. '__eq__' takes an instance of any
    subclass of 'ARGS' as equal to the 'ARGS' instance of the same inner
    type, so the hash must not depend on the class of the instance.

    Implementation
    --------------

    The inner type is hashed beside the fixed tag 'ARGS', so an instance
    does not hash as its bare inner type does.

    Returns
    -------

    int
      The hash.
    """
    return hash(('ARGS', self.__inner_type__))

  def __str__(self) -> str:
    innerType = self.__inner_type__
    innerName = getattr(innerType, '__name__', None) or str(innerType)
    return '%s[%s]' % (type(self).__name__, innerName)

  __repr__ = __str__

  @classmethod
  def __class_getitem__(cls, type_: type) -> Self:
    """
    'ARGS[int]' must give a marker of the variadic tail of 'int'.

    Parameters
    ----------

    type_ : type
      The type every argument of the tail must have.

    Returns
    -------

    ARGS
      A new instance.
    """
    return cls(type_)
