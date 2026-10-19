"""
Detached stands in for an argument of a pickled exception that could not
itself be pickled.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Detached:
  """
  Detached stands in for an argument of a 'WorkToyException' that could
  not be pickled, such as a lambda, a class defined inside a function or
  a namespace object. 'WorkToyException.__reduce__' replaces such an
  argument with a stand-in carrying the name of its type and its 'repr',
  so the exception rebuilt on the other side keeps its type and renders
  its message. The stand-in answers any attribute with itself, since the
  message of an exception may read through the argument, as
  'self.desc.__field_name__' does; such a message then shows the
  stand-in where the attribute was, instead of failing inside '__str__'.

  Attributes
  ----------
  typeName : str
    The name of the type of the argument that was replaced.
  text : str
    The 'repr' of that argument, taken before it was replaced.
  """

  __slots__ = ('typeName', 'text')

  def __init__(self, arg: Any) -> None:
    self.typeName = type(arg).__name__
    self.text = repr(arg)

  @classmethod
  def _fromParts(cls, typeName: str, text: str) -> Self:
    """
    The '_fromParts' constructor rebuilds a stand-in from its two parts,
    which is how a pickled stand-in comes back.
    """
    self = cls.__new__(cls)
    self.typeName = typeName
    self.text = text
    return self

  def __reduce__(self) -> tuple:
    return type(self)._fromParts, (self.typeName, self.text)

  def __getattr__(self, name: str) -> Self:
    """
    Any plain attribute answers with the stand-in itself. A dunder is
    refused, so the protocols of 'pickle' and 'copy', which look some of
    them up on the instance, do not mistake the stand-in for an object
    implementing them.
    """
    if name.startswith('__') and name.endswith('__'):
      raise AttributeError(name)
    return self

  def __str__(self) -> str:
    return '<detached %s: %s>' % (self.typeName, self.text)

  __repr__ = __str__
